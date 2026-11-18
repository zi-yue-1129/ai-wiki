---
translation_reviewed: 2026-11-14
---

# MLP-Mixer

MLP-Mixer 交替使用兩種多層感知器（MLP）進行影像分類。一種在影像小塊之間交換資訊，另一種混合特徵通道。架構還包含小塊投影、正規化、殘差連線及分類器。[多層感知器](index.zh-TW.md)。[^mixer]

## 概述

假設影像高度 $H$ 和寬度 $W$ 都可被小塊邊長 $P$ 整除，先將影像切成不重疊的正方形小塊。每塊攤平後，透過共用的線性投影得到 $C$ 個特徵。所得矩陣 $X\in\mathbb{R}^{S\times C}$ 有 $S=HW/P^2$ 列，每列對應一個小塊 token。視覺 Transformer 也使用這種表示法。[視覺 Transformer](../transformer/vision-transformer/index.zh-TW.md)。[^mixer][^vit]

## 問題

將影像表示成小塊後，模型需要讓相距較遠的位置交換資訊。Mixer 論文檢驗以全連接運算跨小塊混合，再逐塊轉換特徵，是否能支援大規模影像分類。[^mixer]

## 核心想法

**跨小塊混合**把同一個 MLP 套用到 $X$ 的每一欄。權重在通道間共用，並依小塊位置索引。推論時學得的位置權重固定，激活值則隨影像而變。架構因此直接利用小塊的排列順序。[^mixer]

**通道混合**把同一個 MLP 套用到每一列，在單一小塊內混合特徵，權重在各小塊位置間共用。經過最後一層 Mixer 與正規化後，分類頭將小塊表示取平均，再套用線性分類器。[^mixer]

## 演算法

設 $D_S$ 和 $D_C$ 分別為跨小塊與通道 MLP 的隱藏寬度。每個 MLP 之前的層正規化 $\mathrm{LN}$ 都在每塊的 $C$ 個通道上運算。省略偏置，以 $\sigma$ 表示 GELU，並將通道向量寫成直行，更新式如下。[GELU](gelu/index.zh-TW.md)、[層正規化](layer-normalisation/index.zh-TW.md)。[^mixer][^gelu][^ln]

$$
\begin{aligned}
U_{:,i} &= X_{:,i}+W_2\,\sigma\!\left(W_1\,\mathrm{LN}(X)_{:,i}\right),\\
Y_{j,:}^{\top} &= U_{j,:}^{\top}+W_4\,\sigma\!\left(W_3\,\mathrm{LN}(U)_{j,:}^{\top}\right).
\end{aligned}
$$

第一式對 $i=1,\ldots,C$ 成立，第二式對 $j=1,\ldots,S$ 成立。兩次殘差更新的輸出形狀皆為 $S\times C$。四個權重矩陣的維度如下。[^mixer]

$$
W_1\in\mathbb{R}^{D_S\times S},\quad
W_2\in\mathbb{R}^{S\times D_S},\quad
W_3\in\mathbb{R}^{D_C\times C},\quad
W_4\in\mathbb{R}^{C\times D_C}.
$$

以 $S=4$、$C=3$、$D_S=2$ 和 $D_C=5$ 為例。跨小塊 MLP 執行三次 $4\to2\to4$ 的映射，每個通道一次。通道 MLP 執行四次 $3\to5\to3$ 的映射，每個小塊一次。各 MLP 在重複運算時使用同一對矩陣。

每張影像在每一層的全連接矩陣乘法，分別需要 $2CSD_S$ 和 $2SCD_C$ 次乘加運算，偏置、正規化與激活運算另計。固定 $C$、$D_S$ 和 $D_C$ 時，成本與 $S$ 成線性關係。若 $P=16$，將正方形輸入從 $224\times224$ 增為 $448\times448$，小塊數會從 $196$ 增至 $784$。兩個跨小塊混合矩陣都需配合新尺寸。論文的高解析度做法也按 $S$ 的比例增加 $D_S$，將預訓練矩陣複製到擴大後矩陣的對角區塊，再進行微調。[^mixer]

## 主要結果

論文以 ImageNet 原始驗證標籤計算 top-1 準確率。下表列出各組結果的預訓練資料與微調時的輸入尺寸。[^mixer]

| 模型 | 預訓練資料 | 輸入尺寸 | Top-1 | 來源 |
| --- | --- | --- | --- | --- |
| Mixer-B/16 | ImageNet，加上額外正則化 | 224 | 76.44% | 表 3 |
| Mixer-B/16 | ImageNet-21k，加上額外正則化 | 224 | 80.64% | 表 3 |
| Mixer-L/16 | ImageNet-21k，加上額外正則化 | 224 | 82.89% | 表 3 |
| Mixer-L/16 | ImageNet-21k，加上額外正則化 | 448 | 83.91% | 表 3 |
| Mixer-L/16 | ImageNet-21k | 448 | 84.15% | 表 2 |
| Mixer-H/14 | JFT-300M | 448 | 87.94% | 表 2 |

表 3 將三次微調的結果取平均。第 3.1 節另將 224 像素的 Mixer-L/16 結果寫為 82.84%。上表該列採用表 3 的數值，84.15% 則來自表 2 的另一組比較。[^mixer]

## 限制

- 跨小塊混合取決於小塊數目與排列。固定小塊大小而改變解析度時，需調整該子層的矩陣維度。[^mixer]
- 準確率與吞吐量取決於訓練資料、正則化、模型大小和輸入解析度。原論文指出，Mixer 直接在 ImageNet 從頭訓練時有過擬合現象，使用較大的預訓練資料集則得到較高的準確率。[^mixer]

## 關聯

ResMLP 使用線性層跨小塊混合，並搭配通道 MLP。gMLP 則透過空間閘控單元混合位置。兩者都探索如何結合空間互動與逐 token 的特徵轉換。[ResMLP 論文](https://arxiv.org/abs/2105.03404)、[gMLP 論文](https://arxiv.org/abs/2105.08050)。[^resmlp][^gmlp]

## 應用

論文評估影像分類及向其他分類資料集遷移的表現，涵蓋 CIFAR 與 VTAB-1k 任務。[電腦視覺](../computer-vision/index.zh-TW.md)。[^mixer]

[^mixer]: Tolstikhin et al.，[*MLP-Mixer*](https://arxiv.org/html/2105.01601)，第 2 至 3 節及附錄 C。
[^vit]: Dosovitskiy et al.，[*An Image is Worth 16x16 Words*](https://arxiv.org/abs/2010.11929)，第 3.1 節。
[^gelu]: Hendrycks and Gimpel，[*Gaussian Error Linear Units*](https://arxiv.org/abs/1606.08415)，第 2 節。
[^ln]: Ba et al.，[*Layer Normalization*](https://arxiv.org/abs/1607.06450)，第 3 節。
[^resmlp]: Touvron et al.，[*ResMLP*](https://arxiv.org/abs/2105.03404)，第 2 節。
[^gmlp]: Liu et al.，[*Pay Attention to MLPs*](https://arxiv.org/abs/2105.08050)，第 2 節。

## 參考文獻

### 開創性論文

- Tolstikhin 等人（2021）。*MLP-Mixer: An all-MLP Architecture for Vision*。NeurIPS。 https://arxiv.org/abs/2105.01601 — 定義兩種混合運算，並報告 ImageNet 實驗。
- Dosovitskiy 等人（2021）。*An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*。ICLR。 https://arxiv.org/abs/2010.11929 — 提出以影像小塊嵌入為輸入的視覺 Transformer。
- Hendrycks 與 Gimpel（2016）。*Gaussian Error Linear Units (GELUs)*。 https://arxiv.org/abs/1606.08415 — 定義 Mixer 內部 MLP 使用的逐元素激活函數。
- Ba、Kiros 與 Hinton（2016）。*Layer Normalization*。 https://arxiv.org/abs/1607.06450 — 推導使用單一樣本特徵計算的正規化。
- Touvron 等人（2021）。*ResMLP: Feedforward Networks for Image Classification with Data-Efficient Training*。 https://arxiv.org/abs/2105.03404 — 以線性層混合小塊，並搭配通道 MLP。
- Liu、Dai、So 與 Le（2021）。*Pay Attention to MLPs*。 https://arxiv.org/abs/2105.08050 — 提出 gMLP，透過空間閘控單元讓 token 互動。
