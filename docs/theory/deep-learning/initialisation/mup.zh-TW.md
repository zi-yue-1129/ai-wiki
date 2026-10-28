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

最大更新參數化，通常寫作 muP，是一種隨網路寬度增加而縮放初始化與學習率的規則。Yang 等人指出，在此規則下，在窄模型上找到的最佳超參數，對較寬的模型仍然接近最佳。他們稱之為零樣本超參數轉移。

## 概觀

[本章](index.zh-TW.md)把初始化視為訊號尺度的問題。muP 則問：權重、更新量與學習率的尺度應如何隨寬度變化，才能使不同模型大小之間的訓練動態保持可比較？

## 問題

在標準參數化下，最佳學習率通常會隨寬度而改變。以搜尋來調整大型模型成本高昂，而在小模型上找到的學習率可能無法轉移。問題在於，是否存在一種參數化方式，使最佳超參數隨寬度增加而保持不變。

## 核心想法

Yang 等人找到了這樣的參數化，並在 Transformer 與 ResNet 模型上驗證了轉移。在論文的乘數形式中，每一層的學習率與輸出乘數依該層寬度設定，見下方的表格。

## 方程式

論文的表 8 給出 Adam 的乘數形式，其中 $\text{fan\_in}$ 為該層的輸入寬度：

- 隱藏權重：Adam 學習率與 $1/\text{fan\_in}$ 成正比；
- 輸出層：輸出乘數為 $1/\text{fan\_in}$，Adam 學習率為 1；
- 輸入層：Adam 學習率為 1。

## 結果

摘要報告，在小模型上調好的超參數，可以不直接調整大模型就用到大得多的模型上，並且此結果對 Transformer 與 ResNet 模型成立。具體數值見論文的結果。

## 限制

- 表格中的數值是針對 Adam 而定的。其他最佳化器需要各自的推導，本頁不涵蓋。
- 論文的驗證涵蓋 Transformer 與 ResNet 模型，其他架構需要各自檢驗。

## 關聯

關於以扇入為基礎的初始化規則，見 [Glorot 初始化](glorot-initialisation.zh-TW.md)與 [He 初始化](he-initialisation.zh-TW.md)。

## 應用

調整非常大的網路，此時完整的超參數搜尋成本高昂。

## 開放問題

- 轉移能跨越深度、批次大小與架構到多遠？
- muP 與正規化層，以及 Adam 以外的最佳化器，會如何互動？

## 參考文獻

### 奠基性論文

- Yang 等人，*Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer*（2022）。https://arxiv.org/abs/2203.03466 — 提出 muP 與零樣本超參數轉移。
- Glorot 與 Bengio，*Understanding the difficulty of training deep feedforward neural networks*，Proceedings of the 13th International Conference on Artificial Intelligence and Statistics（2010）。https://proceedings.mlr.press/v9/glorot10a.html — 分析深度前饋網路的訓練困難，並提出以扇入與扇出為基礎的初始化。
- He、Zhang、Ren 與 Sun，*Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*（2015）。https://arxiv.org/abs/1502.01852 — 提出為整流網路設計的初始化。
- Schoenholz、Gilmer、Ganguli 與 Sohl-Dickstein，*Deep Information Propagation*（2016）。https://arxiv.org/abs/1611.01232 — 對深層網路中訊號傳播做平均場分析。
- Vaswani 等人，*Attention Is All You Need*（2017）。https://arxiv.org/abs/1706.03762 — 提出 Transformer 架構。
