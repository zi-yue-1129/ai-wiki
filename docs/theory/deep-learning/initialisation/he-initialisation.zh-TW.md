---
status: draft
last_reviewed: 2026-10-28
translation_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
  - theory/models/cnn
tags:
  - He initialisation
  - ReLU
  - initialisation
aliases:
  - He 初始化
  - Kaiming 初始化
  - He initialization
---

# He（Kaiming）初始化

He 初始化把權重的變異數設為 Glorot 規則（僅考慮扇入）所給出值的兩倍，使訊號在經過整流線性激活時能保持穩定。它使非常深的整流網路能從頭開始訓練。

## 概觀

[本章](index.zh-TW.md)說明了整體圖像。本頁說明 He 初始化，即適用於使用 ReLU 及其相關變體的網路的規則。提出此方法的論文同時提出了 PReLU，這是一種可學習斜率的整流變體。

## 問題

整流函數會把所有負的輸入設為零，因此每一層大約會丟掉一半的訊號。使用 Glorot 尺度時，訊號的變異數每層大約會減半，深層網路在訓練開始前就會失去訊號。

## 核心想法

調整權重的尺度，把整流所損失的變異數補回來。對於扇入為 $n_{\text{in}}$、使用 ReLU 激活的層，當權重變異數為 $2/n_{\text{in}}$ 時，前向變異數能被保持。He 等人推導出此規則，也推導出反向傳播的對應版本 [(He et al., 2015)](https://arxiv.org/abs/1502.01852)。

## 方程式

對於整流層的常態初始化，

$$W \sim \mathcal{N}\left(0,\; \frac{2}{n_{\text{in}}}\right)$$

對於斜率為 $a$ 的參數化整流函數 $\mathrm{PReLU}$，變異數以 $2/(1+a^2)$ 縮放，當 $a = 0$ 時還原為 ReLU 的情況。

## 結果

論文報告，一個 PReLU 網路在 ImageNet 2012 分類上超越了所報告的人類水準，摘要中的數字為 top-5 測試錯誤率 4.94%。論文也指出，此初始化使非常深的網路可以訓練，而先前的尺度做不到。

## 限制

- 此規則假設激活函數為整流函數，且輸入彼此獨立；這只在訓練後的網路中近似成立。
- 殘差連接會改變各區塊之間的變異數，因此此規則必須搭配謹慎安排的正規化或縮放後的殘差分支使用。

## 關聯

He 初始化是把 [Glorot 規則](glorot-initialisation.zh-TW.md)針對整流函數修正而得。最常使用它的架構，即殘差網路，見[卷積神經網路](../../models/cnn/index.zh-TW.md)。與激活尺度互動的正則化器見[丟棄法](../dropout/index.zh-TW.md)。

## 應用

卷積層與全連接層在使用 ReLU 或其變體時的預設值，也是大多數影像分類骨幹網路的標準做法。

## 開放問題

- 對於平均值非零的激活函數（如 GELU 或 SwiGLU），此規則應如何修改？
- 殘差縮放規則能否在極大深度下捕捉到最佳行為？

## 參考文獻

### 奠基性論文

- He、Zhang、Ren 與 Sun，*Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification*（2015）。https://arxiv.org/abs/1502.01852 — 提出 He 初始化與 PReLU，並報告 top-5 錯誤率。
- Glorot 與 Bengio，*Understanding the difficulty of training deep feedforward neural networks*，Proceedings of the 13th International Conference on Artificial Intelligence and Statistics（2010）。https://proceedings.mlr.press/v9/glorot10a.html — He 初始化對整流函數所修正的規則。
- He、Zhang、Ren 與 Sun，*Deep Residual Learning for Image Recognition*，IEEE Conference on Computer Vision and Pattern Recognition（2016）。https://doi.org/10.1109/CVPR.2016.90 — 以最深形式使用此初始化的殘差網路。
- Krizhevsky、Sutskever 與 Hinton，*ImageNet Classification with Deep Convolutional Neural Networks*，NeurIPS（2012）。https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html — 在 ImageNet 上訓練的深層整流網路，是促成此規則的背景。
- Schoenholz、Gilmer、Ganguli 與 Sohl-Dickstein，*Deep Information Propagation*（2016）。https://arxiv.org/abs/1611.01232 — 整流網路及其他深層網路中訊號傳播的平均場分析。
