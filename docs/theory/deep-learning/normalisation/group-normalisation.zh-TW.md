---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
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

群組正規化把每個樣本的通道分成若干群組，並使用各群組自己的統計量進行正規化。由於它不依賴批次，因此在小批次時也能運作，而批次正規化在小批次時會變得不可靠。

## 概觀

[本章](index.zh-TW.md)比較了各種正規化的軸。本頁說明群組正規化，它介於批次正規化與實例正規化之間。它在空間位置與一組通道上正規化，而且只在單一樣本之內進行。

## 問題

批次正規化從批次中估計統計量。當批次很小時，例如在高解析度影像上訓練的偵測與分割模型，估計值會很有雜訊，錯誤率隨之上升。此方法的設計目標是消除這種依賴。

## 核心想法

把樣本的 $C$ 個通道分成 $G$ 個群組，每組 $C/G$ 個通道。對每一群組，在群組內的通道與空間位置上計算平均值與變異數，進行正規化，然後套用逐通道可學習的縮放與平移。它不跨批次計算任何東西，因此單一樣本的結果與其他樣本無關。

## 方程式

對於激活張量 $x$，其空間位置為 $(h, w)$、通道索引為 $c$，統計量在包含通道 $c$ 的群組 $\mathcal{S}_i$ 上計算：

$$\mu_i = \frac{1}{|\mathcal{S}_i|}\sum_{k \in \mathcal{S}_i} x_k, \qquad \sigma_i^2 = \frac{1}{|\mathcal{S}_i|}\sum_{k \in \mathcal{S}_i}(x_k - \mu_i)^2$$

集合 $\mathcal{S}_i$ 包含單一樣本內第 $i$ 群組的位置與通道。令 $G = 1$ 得到通道與位置上的層正規化，令 $G = C$ 則得到實例正規化。

## 結果

論文報告，群組正規化在常見的批次大小下與批次正規化表現相當，而在小批次時則優於批次正規化。其摘要指出，在批次大小為 2 時，群組正規化的錯誤率比對應的批次正規化低 10.6% [(Wu and He, 2018)](https://arxiv.org/abs/1803.08494)。

## 限制

- 群組數是一個超參數，最佳選擇可能因任務而異。
- 當批次很大時，批次正規化仍可能更好，因此此方法並非普遍適用的替代品。
- 它並未消除對可學習縮放與平移項的需求，這些項仍需謹慎初始化。

## 關聯

Ulyanov 等人為風格轉換而提出的實例正規化，是每個通道各成一群組的極端情況 [(Ulyanov et al., 2016)](https://arxiv.org/abs/1607.08022)。用於序列的樣本內替代方案是[層正規化](../../models/mlp/layer-normalisation/index.zh-TW.md)。以批次為基礎的基準則是[批次正規化](batch-normalisation.zh-TW.md)。

## 應用

物件偵測與分割模型、影片模型，以及任何因輸入很大而導致批次很小的場景。

## 開放問題

- 如何為新架構自動選擇群組數？
- 群組正規化是否具有批次分析所描述的同樣平滑效果？

## 參考文獻

### 奠基性論文

- Wu 與 He，*Group Normalization*，European Conference on Computer Vision（2018）。https://arxiv.org/abs/1803.08494 — 此方法，附有跨批次大小的比較。
- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 群組正規化在小批次時所取代的以批次為基礎的方法。
- Ba、Kiros 與 Hinton，*Layer Normalization*（2016）。https://arxiv.org/abs/1607.06450 — 群組正規化所推廣的樣本內正規化。
- Ulyanov、Vedaldi 與 Lempitsky，*Instance Normalization: The Missing Ingredient for Fast Stylization*（2016）。https://arxiv.org/abs/1607.08022 — 對每個樣本的每個通道做正規化，即每通道一群組的情況。
- Santurkar、Tsipras、Ilyas 與 Madry，*How Does Batch Normalization Help Optimization?*（2018）。https://arxiv.org/abs/1805.11604 — 關於正規化為何有助於最佳化的背景，與替代方案相關。
