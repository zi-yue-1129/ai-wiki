---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/models/mlp/layer-normalisation
  - theory/models/transformer
tags:
  - normalisation
  - optimisation
  - training stability
aliases:
  - 正規化層
  - 歸一化
  - 批次正規化
  - Normalisation layers
---

# 正規化層

正規化層會重新縮放網路內部的激活值，通常先減去平均值、再除以標準差，然後套用可學習的縮放與平移。它們使深層網路更容易訓練，允許使用更大的學習率，如今幾乎出現在每個現代架構中。選擇在哪些維度上正規化，是主要的設計決定。

## 概觀

訓練網路時，每一層輸入的分布會隨著前面各層的改變而變化。正規化使這些分布保持在穩定的範圍內。批次正規化的提出是為了處理這個問題的某一種解釋，後來的研究質疑這種解釋是否為它有效的真正原因。其他變體則在不同的軸上正規化，這在批次很小或序列長度可變時特別重要。

## 關鍵概念

- **正規化軸（normalisation axis）**：計算平均與變異數所用的維度集合。批次、通道與詞元軸各自對應不同的方法。
- **可學習的仿射參數（learned affine parameters）**：正規化後套用的縮放與平移，使層在必要時能還原原本的尺度。
- **內部共變量偏移（internal covariate shift）**：批次正規化有效的原因，原先提出的說法，指的是訓練期間層輸入分布的變化。
- **前置正規化與後置正規化（pre-norm and post-norm）**：在 Transformer 區塊中，正規化是放在殘差分支之前還是之後。

## 運作方式

對於某個軸集合 $S$ 上的激活值 $x$，此層計算 $\hat{x} = (x - \mu_S)/\sqrt{\sigma^2_S + \epsilon}$，然後回傳 $\gamma \hat{x} + \beta$。各種方法的差別在於 $S$。批次正規化使用批次與空間軸，群組正規化使用單一樣本內的通道群組，層正規化使用單一詞元的所有特徵。Ioffe 與 Szegedy 提出了批次正規化，並報告在一個影像分類模型上，它能以少 14 倍的訓練步數達到相同的準確度 [(Ioffe and Szegedy, 2015)](https://arxiv.org/abs/1502.03167)。

## 關鍵方法

各個里程碑方法的差別在於它們正規化的對象。

- [批次正規化](batch-normalisation.zh-TW.md)：沿批次正規化，是批次較大的卷積網路的標準選擇。
- [群組正規化](group-normalisation.zh-TW.md)：在每個樣本內沿通道群組正規化，與批次大小無關。
- [RMSNorm](rms-normalisation.zh-TW.md)：去掉減平均值的步驟，改以均方根正規化，計算成本較低。
- [層正規化](../../models/mlp/layer-normalisation/index.zh-TW.md)：沿單一詞元的特徵正規化，在 MLP 頁面中說明。

## 為何有效，以及爭論

內部共變量偏移的說法存在爭議。Santurkar 等人主張，批次正規化主要是使最佳化的損失地形明顯更平滑，而不是減少輸入分布的偏移 [(Santurkar et al., 2018)](https://arxiv.org/abs/1805.11604)。對任何單一解釋都應視為部分正確。這項效果在實務上已被充分確認，而其機制仍是開放問題。

## Transformer 中的前置與後置正規化

原始 Transformer 把層正規化放在殘差相加之後，稱為後置正規化。Xiong 等人分析了初始化時的梯度，並指出把正規化放在殘差分支內部，即前置正規化，能讓輸出層附近的梯度表現良好，使學習率預熱較不關鍵 [(Xiong et al., 2020)](https://arxiv.org/abs/2002.04745)。目前大多數大型模型使用前置正規化或其變體。

## 關聯

這些層中梯度流動的機制依賴[自動微分](../../math/automatic-differentiation/index.zh-TW.md)。初始化與正規化相互配合，見[權重初始化](../initialisation/index.zh-TW.md)。Transformer 的背景見[Transformer](../../models/transformer/index.zh-TW.md)。

## 應用

影像分類器與偵測器中的批次正規化，小批次與影片模型中的群組正規化，語言模型中的 RMSNorm 與層正規化，以及擴散模型中的正規化。

## 開放問題

- 為什麼正規化有效？在提出的各種解釋中，哪一個承擔了最主要的效果？
- 對於極大規模訓練的模型，當批次統計量無法跨裝置取得時，最好的正規化是什麼？

## 參考文獻

### 奠基性論文

- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 提出批次正規化，並報告訓練步數減少 14 倍。
- Ba、Kiros 與 Hinton，*Layer Normalization*（2016）。https://arxiv.org/abs/1607.06450 — 在每個樣本內沿特徵正規化，避免依賴批次大小。
- Wu 與 He，*Group Normalization*，European Conference on Computer Vision（2018）。https://arxiv.org/abs/1803.08494 — 沿通道群組正規化，在小批次時表現穩定。
- Zhang 與 Sennrich，*Root Mean Square Layer Normalization*（2019）。https://arxiv.org/abs/1910.07467 — 去掉減平均值步驟、較便宜的層正規化替代方案。
- Xiong、Yang、He、Zheng、Zheng、Xing、Zhang、Lan、Wang 與 Liu，*On Layer Normalization in the Transformer Architecture*（2020）。https://arxiv.org/abs/2002.04745 — 在初始化時分析 Transformer 的前置與後置正規化。
- Santurkar、Tsipras、Ilyas 與 Madry，*How Does Batch Normalization Help Optimization?*（2018）。https://arxiv.org/abs/1805.11604 — 主張批次正規化的主要效果是使最佳化地形更平滑。
