---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - RMSNorm
  - normalisation
  - language models
aliases:
  - 均方根正規化
  - RMSNorm
  - Root mean square layer normalization
---

# RMSNorm

RMSNorm 以特徵向量的均方根來正規化，不減去平均值。它是層正規化較簡單、較便宜的形式，現今在大型語言模型中相當常見。

## 概觀

[本章](index.zh-TW.md)涵蓋正規化家族。本頁說明 RMSNorm，它保留了層正規化的重新縮放步驟，並去掉重新中心化的步驟。其想法是檢驗：層正規化所提供的好處，是否真的需要減去平均值。

## 問題

層正規化會為每個詞元計算平均值與變異數。在大型模型中，這會耗費時間，而減去平均值的運算也必須在訓練與推論中一併處理。問題在於，較便宜的正規化能否保持相同的效能。

## 核心想法

對於向量 $\mathbf{x} \in \mathbb{R}^d$，計算其各項的均方根，再除以它。然後套用可學習的逐特徵增益。它不減去平均值，也沒有可學習的偏置。Zhang 與 Sennrich 報告，此方法的效能與層正規化相當，同時降低運行時間 [(Zhang and Sennrich, 2019)](https://arxiv.org/abs/1910.07467)。

## 方程式

$$\mathrm{RMS}(\mathbf{x}) = \sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2 + \epsilon}, \qquad \mathrm{RMSNorm}(\mathbf{x}) = \frac{\mathbf{x}}{\mathrm{RMS}(\mathbf{x})} \odot \mathbf{g}$$

這裡 $\mathbf{g}$ 是可學習的增益向量，$\epsilon$ 是為了數值穩定而加的小常數。層正規化則會先減去 $\mathbf{x}$ 的平均值，再除以其標準差。

## 結果

摘要指出，RMSNorm 達到與層正規化相當的效能，並依模型不同，將運行時間減少 7% 至 64%。詳細比較見論文。

## 限制

- 其好處主要在速度上。若層正規化相對於模型其他部分本來就便宜，改善就很小。
- 效能相當的主張，建立在論文所測試的任務上。其他任務的表現可能不同。
- 與層正規化一樣，它位於殘差區塊之內，因此其位置仍然重要。前置與後置正規化的討論見[本章](index.zh-TW.md)。

## 關聯

RMSNorm 是[層正規化](../../models/mlp/layer-normalisation/index.zh-TW.md)的直接簡化。它在 Transformer 區塊中的用法見 [Transformer](../../models/transformer/index.zh-TW.md) 頁面，而正規化位置的問題由 Xiong 等人分析 [(Xiong et al., 2020)](https://arxiv.org/abs/2002.04745)。

## 應用

大型語言模型內部的正規化，其較低的成本在規模化時特別重要。

## 開放問題

- 減去平均值在某些架構或資料上是否曾經重要？
- 在非常大的規模下，RMSNorm 是否會改變原始實驗未測試過的訓練動態？

## 參考文獻

### 奠基性論文

- Zhang 與 Sennrich，*Root Mean Square Layer Normalization*（2019）。https://arxiv.org/abs/1910.07467 — 提出 RMSNorm，並報告其速度與效能。
- Ba、Kiros 與 Hinton，*Layer Normalization*（2016）。https://arxiv.org/abs/1607.06450 — RMSNorm 所簡化的正規化方法。
- Ioffe 與 Szegedy，*Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*（2015）。https://arxiv.org/abs/1502.03167 — 推動此家族發展的以批次為基礎的方法。
- Xiong、Yang、He、Zheng、Zheng、Xing、Zhang、Lan、Wang 與 Liu，*On Layer Normalization in the Transformer Architecture*（2020）。https://arxiv.org/abs/2002.04745 — 分析正規化在 Transformer 區塊中的位置。
- Vaswani 等人，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — 使用這些正規化的 Transformer 架構。
