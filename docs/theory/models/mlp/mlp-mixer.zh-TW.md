---
translation_reviewed: 2026-10-28
---

# MLP-Mixer

MLP-Mixer 是只由多層感知器（MLP）構成的影像分類器，不使用卷積，也不使用注意力。Tolstikhin 等人（2021）顯示，當在大量資料上訓練或採用現代正規化時，這樣的網路能在影像基準上達到有競爭力的準確率。上層概述見[多層感知器](index.md)。

## 概述

與[視覺 Transformer](../transformer/vision-transformer/index.md)相同，MLP-Mixer 把影像切成不重疊的小塊，並把每一塊投影成一個向量。接著它交替使用兩種 MLP 處理這組小塊向量。與 Transformer 的差別在於，跨小塊的混合是由固定的 MLP 完成，而非注意力。

## 問題

卷積與注意力在電腦視覺中都很常見，而兩者各自都對輸入有某種假設。論文提問：兩者是否必要？只用 MLP 構成的網路，能否以相當的成本把影像分類得很好？

## 核心想法

把視覺模型所需的兩種混合分開。跨小塊混合 MLP 在小塊之間混合資訊，因此承載空間資訊。通道混合 MLP 則在每一小塊的特徵之間混合資訊。堆疊這兩種層，便構成整個網路。

## 演算法

影像被切成 \(S\) 個小塊，每塊投影到 \(C\) 個通道，得到大小為 \(S \times C\) 的表 \(X\)。每個 Mixer 層套用兩個帶有殘差連線的 MLP 區塊，非線性為 GELU \(\sigma\)：

\[
U_{*,i} = X_{*,i} + W_2\, \sigma\!\big(W_1\, \mathrm{LayerNorm}(X)_{*,i}\big), \qquad i = 1, \ldots, C,
\]

\[
Y_{j,*} = U_{j,*} + W_4\, \sigma\!\big(W_3\, \mathrm{LayerNorm}(U)_{j,*}\big), \qquad j = 1, \ldots, S.
\]

第一式是跨小塊混合區塊：MLP 在每個通道的 \(S\) 個小塊上運作。第二式是通道混合區塊：MLP 在每個小塊的 \(C\) 個通道上運作。論文在第 2 節以逐元素 GELU（\(\sigma\)）寫出這些式子。

## 主要結果

論文在兩張表中回報 ImageNet top-1 準確率：

- **ImageNet-21k 預訓練，加上額外正規化**（表 3）：Mixer-B/16 達 80.64%，Mixer-L/16 達 82.89%，兩者都是 224 解析度。
- **ImageNet-21k 預訓練，公開檢查點**（表 2）：Mixer-L/16 在 448 解析度微調後達 84.15%。

正文給出 Mixer-L/16 在 224 解析度的 82.84%，表 3 則為 82.89%。本頁採用表中的數值。論文將這些分數描述為有競爭力，且預訓練與推論成本與最先進模型相當。

## 限制

- 摘要指出，模型在大型資料集上訓練或採用現代正規化方案時，才能達到有競爭力的分數。沒有這兩者時，論文不宣稱有競爭力的準確率。
- 跨小塊混合的權重依小塊數量決定大小，因此改變輸入解析度會改變層的形狀。論文中較高解析度的結果來自在新解析度下的微調。
- 論文描述的成本與最先進模型相當，而非更低。此架構並未消除大規模預訓練的運算成本。

## 關聯

- [視覺 Transformer](../transformer/vision-transformer/index.md)是具有相同小塊前端、以注意力為核心的模型。兩者的比較可以分離出「以固定 MLP 取代注意力」的效果。
- [多層感知器](index.md)是上層概述，MLP-Mixer 與它所用的兩個元件 [GELU](gelu/index.md) 與[層正規化](layer-normalisation/index.md)並列其中。
- [電腦視覺](../computer-vision/index.md)涵蓋基於小塊的分類器所應用的任務。

## 應用

- 在 ImageNet 上的影像分類，即論文所用的基準。
- 將大規模預訓練的視覺模型遷移到下游影像任務。

## 開放問題

- 增益來自兩種混合運算本身，還是來自論文所用的大規模預訓練資料？
- 固定的跨小塊混合 MLP 如何處理大小會變化的輸入，例如偵測與分割？

## 參考文獻

### 開創性論文

- Tolstikhin, I., Houlsby, N., Kolesnikov, A., 等人（2021）。*MLP-Mixer: An all-MLP Architecture for Vision*。NeurIPS 2021。https://proceedings.neurips.cc/paper/2021/hash/cba0a4ee5ccd02fda0fe3f9a3e7b89fe-Abstract.html — 提出 MLP-Mixer 及其跨小塊混合與通道混合區塊。查核：NeurIPS 論文條目；arXiv 2105.01601 的作者列表相符。
- Dosovitskiy, A., Beyer, L., Kolesnikov, A., 等人（2021）。*An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*。arXiv。https://arxiv.org/abs/2010.11929 — 視覺 Transformer，與 MLP-Mixer 使用相同的小塊前端，但以注意力取代混合 MLP。查核：arXiv metadata。
- Vaswani, A., 等人（2017）。*Attention Is All You Need*。NeurIPS 2017。https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need — MLP-Mixer 在混合步驟中所取代的注意力架構。查核：NeurIPS 論文條目。
- Hendrycks, D. & Gimpel, K.（2016）。*Gaussian Error Linear Units (GELUs)*。arXiv。https://arxiv.org/abs/1606.08415 — Mixer 所用的 GELU 激活函數。查核：arXiv metadata。
- Ba, J. L., Kiros, J. R. & Hinton, G. E.（2016）。*Layer Normalization*。arXiv。https://arxiv.org/abs/1607.06450 — 每個 MLP 區塊之前所套用的正規化。查核：arXiv metadata。

### 綜述與教科書

- Liu, H., Dai, Z., So, D. R. & Le, Q. V.（2021）。*Pay Attention to MLPs*。arXiv。https://arxiv.org/abs/2105.08050 — 同期的純 MLP 視覺模型，帶有空間閘控單元，供比較之用。查核：arXiv metadata。
