---
translation_reviewed: 2026-10-28
---

# SGD 雜訊尺度

SGD 雜訊尺度是一個量 \(g = \epsilon\,(N/B - 1) \approx \epsilon N/B\)，其中 \(\epsilon\) 為學習率、\(N\) 為訓練集大小、\(B\) 為批次大小。Smith 與 Le（2018）主張，最佳批次大小隨學習率與訓練集大小而成長，並且雜訊尺度決定了最佳化器的路徑有多少是由梯度雜訊驅動的。上層概述見[最佳化中的正則化與權重衰減](regularisation-and-weight-decay.md)。

## 概述

隨機梯度下降以小批次的平均值取代全資料的梯度。兩者之間的差異就是雜訊。它的大小取決於批次大小，而這些雜訊對軌跡的影響又取決於學習率。Smith 與 Le 把兩者合併為單一個量，它決定了最佳化器在收斂區域附近遊走的幅度。適度的遊走有助於泛化，因此最佳的批次大小，是讓雜訊尺度落在特定數值的那一個。

## 問題

實務上，學習率與批次大小會互相影響，而人們通常分別調校它們。Smith 與 Le 想知道，兩者之間是否存在某種關係，能在給定訓練集的情況下得到最佳的泛化，而不必各自調校。

## 核心想法

把更新寫成一個隨機步，並以高斯雜訊近似隨機項，其尺度由 \(\epsilon N/B\) 決定。以此論證最佳批次大小與學習率、訓練集大小皆成正比。論文指出，改變學習率或訓練集大小時，應保持雜訊尺度固定。

## 演算法

論文並未提出新的最佳化器。此方法是選擇批次大小的一條規則：

1. 固定學習率 \(\epsilon\) 與訓練集大小 \(N\)。
2. 對候選批次大小 \(B\) 計算雜訊尺度 \(g = \epsilon (N/B - 1)\)。
3. 偏好使 \(g\) 落在實驗所認定之最佳範圍內的批次大小。
4. 學習率改變時，批次大小也依比例改變，使 \(g\) 保持不變。

## 結果

- 摘要指出，最佳批次大小同時隨學習率與訓練集大小而成長，作者以實驗驗證了這一點。
- 摘要未給出數值結果，因此定量效應應參考論文中的實驗。

## 限制

- 雜訊尺度的論證使用了小批次雜訊的高斯近似，對於重尾的梯度可能不成立。
- 此規則是以普通 SGD 表述的，並非直接適用於 Adam 等自適應最佳化器，因為它們的有效步長取決於二階矩。
- 最佳批次大小取決於所處的機制，此規則只是對所研究設定成立的近似。

## 關聯

- [尖銳極小值與大批次泛化](sharp-minima.md)提供同一批次大小效應的經驗面向。
- [漸進式預熱與線性縮放](gradual-warm-up.md)是依批次大小縮放學習率的實用規則，雜訊尺度為其提供動機。
- [SGD 與動量](sgd-and-momentum/index.md)是此論證最清楚的設定。
- [學習率排程](learning-rate-schedules.md)很重要，因為排程會在訓練過程中改變雜訊尺度。

## 開放問題

- 雜訊尺度規則能否推廣到自適應最佳化器與動量方法？
- 是否存在一個雜訊尺度，使泛化在各種架構下都最佳？

## 參考文獻

### 開創性論文

- Smith, S. L. & Le, Q. V. (2018). *A Bayesian Perspective on Generalization and Stochastic Gradient Descent*. ICLR. https://arxiv.org/abs/1710.06451 — 提出 SGD 雜訊尺度 \(\epsilon N/B\)，並主張最佳批次大小隨學習率與訓練集大小而變。
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — 雜訊尺度論述所要解釋的經驗性批次大小效應。
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — 學習率依批次大小線性縮放，使雜訊尺度大致不變。
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — 顯示自適應最佳化器會改變有效學習率，而雜訊尺度規則並未考慮這一點。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 隨機梯度方法的綜述，討論梯度雜訊與步長。
