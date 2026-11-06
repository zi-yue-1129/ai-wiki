---
status: complete
last_reviewed: 2026-11-06
translation_reviewed: 2026-11-06
related:
  - theory/deep-learning/normalisation
tags:
  - group normalisation
  - normalisation
  - small batches
aliases:
  - 群組正規化
  - 分組歸一化
  - Group normalization
---

# 群組正規化

群組正規化（GN）將每個樣本的通道分成數組。每組共用一個平均值與變異數，統計範圍涵蓋組內通道及其空間位置。當參數固定時，單一樣本的正規化結果與同批次的其他樣本無關。[^gn]

## 動機

訓練時，[批次正規化](batch-normalisation.md)會跨樣本彙總統計量，對影像而言通常也會在每個通道內跨空間位置彙總。使用高解析度影像訓練偵測模型時，每個裝置可能只能容納少數幾張影像。若統計量在裝置本地計算，換掉其中幾張影像就會改變該裝置所有影像採用的估計值。群組正規化分別計算每張影像的統計量，因此每個裝置的影像數量改變時，仍可使用相同運算。[^bn][^gn]

## 計算方式與統計軸

對形狀為 $[N,C,H,W]$ 的激活張量 $x$，選擇能整除 $C$ 的正整數群組數 $G$。每組包含 $C/G$ 個通道。索引從零開始時，通道 $c$ 屬於群組 $g(c)=\lfloor c/(C/G)\rfloor$。令 $\mathcal{S}_g$ 包含第 $g$ 組的通道與空間索引，共有 $M=(C/G)HW$ 個元素。對樣本 $n$，統計量為

$$
\mu_{n,g}=\frac{1}{M}\sum_{(c,h,w)\in\mathcal{S}_g} x_{n,c,h,w},
\qquad
v_{n,g}=\frac{1}{M}\sum_{(c,h,w)\in\mathcal{S}_g}(x_{n,c,h,w}-\mu_{n,g})^2.
$$

此層用這些統計量將各激活值中心化並重新縮放，再套用逐通道的仿射轉換。[^gn]

$$
y_{n,c,h,w}=\gamma_c
\frac{x_{n,c,h,w}-\mu_{n,g(c)}}{\sqrt{v_{n,g(c)}+\epsilon}}
+\beta_c.
$$

當群組的變異數很小或為零時，$\epsilon>0$ 可穩定除法。變異數以 $M$ 為除數，對應修正值為零的估計式。同一通道的各空間位置共用可學習的縮放 $\gamma_c$ 與偏移 $\beta_c$。PyTorch 允許停用仿射轉換，並在訓練與評估時都使用當前輸入的統計量。[^torch-gn]

將張量由 $[N,C,H,W]$ 重塑為 $[N,G,C/G,H,W]$，即可看出要彙總的軸。沿最後三個維度彙總，每組 $(n,g)$ 各保留一個平均值與變異數，再恢復原本的形狀並套用逐通道縮放與偏移。[^gn]

### 計算範例

取一個有四個通道、一列及兩個空間位置的樣本。令 $G=2$，縮放為一且偏移為零。兩組變異數皆為正，因此可用 $\epsilon\to0^+$ 的極限計算。

| 群組 | 各通道的值 | 平均值 | 變異數 | 各通道的正規化結果 |
|---|---|---|---|---|
| 0 | $(1,3)$ 和 $(5,7)$ | 4 | 5 | $(-3,-1)/\sqrt{5}$ 和 $(1,3)/\sqrt{5}$ |
| 1 | $(10,14)$ 和 $(18,22)$ | 16 | 20 | $(-3,-1)/\sqrt{5}$ 和 $(1,3)/\sqrt{5}$ |

第一個激活值變為 $(1-4)/\sqrt{5}\approx-1.3416$。每個通道的兩個位置皆使用同一組統計量。第二組可由第一組經正倍率縮放與平移得到，所以在此極限下兩組正規化結果相同。正的 epsilon 會略微改變縮放結果。

## 與其他正規化方法的關係

| 設定 | 每個樣本的統計範圍 | 與其他方法相同的條件 |
|---|---|---|
| $G=1$ | 所有通道與空間位置 | 沿 $(C,H,W)$ 計算的 LayerNorm，在 epsilon 與變異數計算方式相同時，會得到相同的標準化數值。 |
| $1<G<C$ | 每組通道及其空間位置 | 各組各自使用一套統計量。 |
| $G=C$ | 各通道的空間位置 | InstanceNorm 使用當前樣本統計量，且 epsilon 與變異數計算方式相同時，會得到相同的標準化數值。 |

若要讓整層輸出相同，還需比對仿射轉換。啟用仿射參數時，PyTorch 沿 $(C,H,W)$ 計算的 LayerNorm 為每個元素配置縮放與偏置。GroupNorm 則為每個通道配置一組參數，供該通道所有空間位置共用。[^gn][^ln][^in][^torch-ln]

## 論文結果

Wu 與 He 在八張 GPU 上以 ImageNet 訓練 ResNet-50。BatchNorm 的統計量在每張 GPU 上分別計算。表 2 在兩種單張 GPU 訓練批次大小下回報以下驗證錯誤率。[^results]

| 每張 GPU 的訓練影像數 | BatchNorm 錯誤率 | GroupNorm 錯誤率 |
|---|---|---|
| 2 | 34.7% | 24.1% |
| 32 | 23.6% | 24.1% |

每張 GPU 使用兩張影像時，差距為 **10.6 個百分點**，以 34.7% 為基準則相對減少約 30.5%。每張 GPU 使用 32 張影像時，BatchNorm 的錯誤率低 0.5 個百分點。這些結果適用於論文的訓練設定及其使用本地統計量的 BatchNorm 基準。論文也評估了 COCO 的偵測與實例分割，以及 Kinetics 的影片分類。[^results]

## 實務考量

- **群組大小。** 若固定群組數，層的通道數改變時，每組通道數也會改變。論文探討了固定群組數和固定每組通道數兩種做法。請確認各層的整除條件，並在目標任務上比較有效設定。[^results][^torch-gn]
- **空間大小。** 群組統計量涵蓋 $(C/G)HW$ 個數值。若只有一個值，中心化會使標準化數值變為零。若啟用了仿射參數，輸出即為該通道的偏移。
- **訓練行為。** 樣本前向運算的獨立性指的是正規化層。改變訓練批次大小，仍可能改變每次最佳化步驟彙總的梯度。
- **檢查點相容性。** 訓練完成的 BatchNorm 層可以在評估時使用儲存的統計量，GroupNorm 則會從各樣本重新計算。替換層會改變模型函數，因此需要重新評估。[^bn][^torch-gn]

## 關聯

[正規化概覽](index.md)比較主要方法使用的統計軸。[層正規化](../../models/mlp/layer-normalisation/index.md)也在單一樣本內計算統計量。[RMSNorm](rms-normalisation.md)使用未中心化的二階動差，提供另一種統計量選擇。

[^gn]: Wu 與 He（2018），第 3.1–3.2 節、方程式 1–7 與圖 3 定義群組統計軸、仿射轉換，以及與 LayerNorm 和 InstanceNorm 的關係。
[^bn]: Ioffe 與 Szegedy（2015），第 3 節說明小批次統計量與推論程序。
[^ln]: Ba、Kiros 與 Hinton（2016），《Layer Normalization》定義逐樣本統計量與可學習的仿射參數。
[^in]: Ulyanov、Vedaldi 與 Lempitsky（2016），《Instance Normalization》說明訓練與測試均使用逐樣本、逐通道的空間統計量。
[^torch-gn]: PyTorch 2.15 的《GroupNorm》說明通道整除條件、變異數計算方式、可選的逐通道仿射參數，以及兩種模式使用的統計量。
[^torch-ln]: PyTorch 2.15 的《LayerNorm》說明最後幾個統計軸與逐元素仿射參數。
[^results]: Wu 與 He（2018），第 4.1 節及表 2–3 說明 ImageNet 的批次與群組比較。第 4.2–4.3 節涵蓋 COCO 與 Kinetics。

## 參考文獻

### 奠基性論文

- Wu, Y. & He, K. (2018). *Group Normalization*. ECCV 2018. https://arxiv.org/abs/1803.08494 — 定義群組統計量，並評估批次大小與群組劃分。
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. https://arxiv.org/abs/1502.03167 — 說明訓練時的小批次統計量與推論時的固定統計量。
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. https://arxiv.org/abs/1607.06450 — 提出逐樣本特徵統計量及可學習的縮放與偏置。
- Ulyanov, D., Vedaldi, A. & Lempitsky, V. (2016). *Instance Normalization: The Missing Ingredient for Fast Stylization*. https://arxiv.org/abs/1607.08022 — 為風格轉換提出逐樣本、逐通道的空間正規化。

### 文章與文件

- PyTorch contributors. *GroupNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.GroupNorm.html — 指定有效群組數、輸入統計量與逐通道仿射參數。
- PyTorch contributors. *LayerNorm*, PyTorch 2.15 documentation. https://docs.pytorch.org/docs/2.15/generated/torch.nn.LayerNorm.html — 指定最後幾個正規化軸與仿射參數形狀。
