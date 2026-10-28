---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
tags:
  - batch normalisation
  - normalisation
  - convolutional networks
aliases:
  - 批次正規化
  - 批次歸一化
  - Batch normalization
---

# 批次正規化

批次正規化使用當前小批次的平均值與變異數，對每一層的各個通道做正規化，然後套用可學習的縮放與平移。它的提出是為了加速深層影像分類器的訓練，並成為卷積網路的預設元件。

## 概觀

[本章](index.zh-TW.md)涵蓋正規化層這一家族。本頁說明開創此家族的方法。批次正規化在批次中的樣本與空間位置上計算各通道的統計量，因此統計量依賴於批次。

## 問題

深層網路訓練緩慢，對學習率與初始化很敏感，部分原因是每一層的輸入會隨前面各層的變化而持續偏移。論文的目標是在不改變模型容量的前提下，使訓練更快也更穩定。

## 核心想法

對每個通道，在批次與空間軸上計算平均值與變異數，用它們正規化每個激活值，並套用可學習的縮放 $\gamma$ 與平移 $\beta$。測試時，該層使用訓練期間累積的移動平均統計量，因此單一樣本也能獨立處理。

## 方程式

對於一個通道，其在小批次中的激活值為 $x_1, \ldots, x_m$：

$$\mu_B = \frac{1}{m}\sum_{i=1}^{m} x_i, \qquad \sigma_B^2 = \frac{1}{m}\sum_{i=1}^{m}(x_i - \mu_B)^2, \qquad y_i = \gamma\,\frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}} + \beta$$

原論文報告，在一個影像分類模型上，此方法以少 14 倍的訓練步數達到與基準相同的準確度 [(Ioffe and Szegedy, 2015)](https://arxiv.org/abs/1502.03167)。

## 結果

論文的主要成果是大型影像分類模型的訓練加速。確切的準確度與步數見其結果章節。

## 限制

- 統計量依賴於批次。小批次會得到有雜訊的估計，進而損害效能。
- 訓練與推論的行為不同，因為推論使用的是移動平均。
- 具有可變長度輸入的序列模型，難以適用批次統計量，這也是 Transformer 使用層正規化的原因之一。

[群組正規化](group-normalisation.zh-TW.md)處理了小批次的問題，[RMSNorm](rms-normalisation.zh-TW.md)則處理語言模型中平均值與變異數計算的成本問題。

## 關聯

批次正規化的解釋爭論見[本章](index.zh-TW.md)，其中 Santurkar 等人主張它會使最佳化地形更平滑 [(Santurkar et al., 2018)](https://arxiv.org/abs/1805.11604)。流經此層的梯度，依[自動微分](../../math/automatic-differentiation/index.zh-TW.md)中所述計算。

## 應用

使用大批次訓練的影像分類器、物件偵測器與分割網路，以及許多視覺骨幹網路中的卷積堆疊。

## 開放問題

- 批次正規化的好處主要來自批次統計量，還是來自正規化後的尺度？
- 當批次被切分到多個裝置上做大規模訓練時，批次統計量應如何共享？

## 參考文獻

### 奠基性論文

- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 原始方法與報告的訓練加速。
- Santurkar、Tsipras、Ilyas 與 Madry，*How Does Batch Normalization Help Optimization?*（2018）。https://arxiv.org/abs/1805.11604 — 主張其主要效果是使最佳化地形更平滑。
- Ba、Kiros 與 Hinton，*Layer Normalization*（2016）。https://arxiv.org/abs/1607.06450 — 不依賴批次的樣本內替代方案。
- Wu 與 He，*Group Normalization*，European Conference on Computer Vision（2018）。https://arxiv.org/abs/1803.08494 — 小批次的替代方案，並與批次大小為 2 的批次正規化做數值比較。
- Xiong、Yang、He、Zheng、Zheng、Xing、Zhang、Lan、Wang 與 Liu，*On Layer Normalization in the Transformer Architecture*（2020）。https://arxiv.org/abs/2002.04745 — 在初始化時分析 Transformer 區塊中的前置與後置正規化，與正規化在殘差區塊中的位置相關。
