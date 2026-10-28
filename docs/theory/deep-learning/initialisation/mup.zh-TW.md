---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
tags:
  - muP
  - hyperparameter transfer
  - scaling
aliases:
  - 最大更新參數化
  - muP
  - Maximal update parametrisation
---

# 最大更新參數化（muP）

最大更新參數化，通常寫作 muP，是一種依照網路寬度來縮放初始化與學習率的方式，使最佳超參數在模型變大時大致保持不變。在窄模型上調好的超參數，因此可以重用於寬模型，省下調整超大模型的大部分成本。

## 概觀

[本章](index.zh-TW.md)把初始化描述為訊號尺度的問題。muP 提出一個相關的問題：權重、更新量與學習率的尺度應如何隨寬度變化，才能使不同大小之間的訓練動態保持可比較？

## 問題

在標準參數化下把網路加寬時，最佳學習率通常會隨寬度而改變。以搜尋來調整大型模型成本高昂，而在小模型上找到的學習率可能無法轉移。問題在於，是否存在一種參數化方式，使最佳點保持穩定。

## 核心想法

Yang 等人研究無限寬的極限，並找出一種參數化方式，在此方式下隱藏層激活的更新量大小，會隨寬度增加保持為階數一的量。在此參數化下，學習率與初始化尺度依據該層的寬度設定，論文報告小網路的最佳超參數對大網路仍接近最佳。他們稱之為零樣本超參數轉移 [(Yang et al., 2022)](https://arxiv.org/abs/2203.03466)。

## 方程式

標準的縮放會把每個隱藏層的權重乘以 $1/\sqrt{n}$，其中 $n$ 是寬度。在 muP 中，輸出層與學習率會隨寬度縮放，使特徵的更新量大小不依賴寬度。各層類型與最佳化器的規則不同。論文在其表格中給出 SGD 與 Adam 的初始化、乘數與學習率規則；本頁不重述，使用前請查閱論文。

## 結果

摘要報告，在小模型上調好的超參數，可以不直接調整大模型就用到大得多的模型上；論文在 Transformer 與 ResNet 上驗證此結果。具體數值見論文結果。

## 限制

- 理論是在無限寬的極限下發展的，其保證在有限寬度時只是近似。
- 確切規則取決於架構與最佳化器，因此每種設定都需要各自的推導。
- 跨深度的轉移是另一個與跨寬度轉移不同的問題。

## 關聯

muP 是與 [Glorot 初始化](glorot-initialisation.zh-TW.md)和 [He 初始化](he-initialisation.zh-TW.md)相同的初始變異數論證的縮放規則。正規化層會改變寬度的相依性，而論文的設定並未完全涵蓋這一點；見[正規化](../normalisation/index.zh-TW.md)。

## 應用

調整大型語言模型與其他超寬網路，其中完整的超參數搜尋成本過高。

## 開放問題

- 轉移能跨越深度、批次大小與架構到多遠？
- muP 與正規化以及 Adam 以外的最佳化器會如何互動？

## 參考文獻

### 奠基性論文

- Yang 等人，*Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*（2022）。https://arxiv.org/abs/2203.03466 — 提出 muP 與零樣本超參數轉移。
- Glorot 與 Bengio，*Understanding the difficulty of training deep feedforward neural networks*，Proceedings of the 13th International Conference on Artificial Intelligence and Statistics（2010）。https://proceedings.mlr.press/v9/glorot10a.html — muP 所推廣、基於扇入與扇出的變異數規則，並延伸到訓練動態。
- He、Zhang、Ren 與 Sun，*Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*（2015）。https://arxiv.org/abs/1502.01852 — 縮放規則必須遵守的整流初始化。
- Schoenholz、Gilmer、Ganguli 與 Sohl-Dickstein，*Deep Information Propagation*（2016）。https://arxiv.org/abs/1611.01232 — 隨深度變化的訊號傳播平均場分析。
- Vaswani 等人，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — muP 最常應用的 Transformer 架構。
