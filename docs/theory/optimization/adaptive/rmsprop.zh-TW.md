---
translation_reviewed: 2026-10-28
---

# RMSProp

RMSProp 依每個參數最近平方梯度的移動平均來縮放其步長，而不是依整個訓練過程的總和。這個平均會遺忘舊梯度，因此步長不會縮小到零。Tieleman 與 Hinton 在 2012 年的講義中提出它，它從未以論文形式發表。上層概述見[自適應方法](index.md)。

## 概述

RMSProp 是對 AdaGrad 的小幅修改：以指數移動平均取代累積總和。它就是 Adam 所用的自適應縮放，但不含動量項。

## 問題

AdaGrad 的累加和會無止境地增長，因此其有效學習率持續衰減。在非凸的深度網路中，這種衰減可能在找到好解之前就讓學習停止。

## 核心想法

對每個座標保存平方梯度的指數平均，並把梯度除以其平方根。這個平均只記住最近幾十步，因此縮放反映的是目前的梯度大小，而非整個歷史。

## 演算法

令衰減率為 \(\beta\)，移動平均更新為

\[
v_t = \beta\, v_{t-1} + (1 - \beta)\, g_t \odot g_t,
\]

參數移動為

\[
\theta_{t+1} = \theta_t - \eta\, \frac{g_t}{\sqrt{v_t} + \epsilon}.
\]

常用值是 \(\beta\) 接近 0.9，並加上維持數值穩定的小 \(\epsilon\)。除法逐元素進行。

## 主要結果

RMSProp 沒有論文，因此本頁不引用基準測試數字。它的效果記錄在講義中，並在後來的比較中被提及，特別是 Kingma 與 Ba（2015）在 Adam 內使用了同樣的平方梯度指數平均。

## 限制

- 與 Adam 不同，它在訓練初期沒有對平均做偏差校正，因此最初幾步可能異常大。
- 它沒有動量項，因此不會平滑更新的方向。
- 衰減率與學習率都需要調校。

## 關聯

- [AdaGrad](adagrad.md)是 RMSProp 所修改的方法，以平均取代總和。
- [Adam](adam.md)在同樣的縮放上加入動量與偏差校正。
- [自適應方法](index.md)是上層概述，RMSProp 與其他逐座標變體並列於其中。

## 應用

- 在 Adam 成為預設之前，廣泛用於訓練循環網路與早期深度模型。

## 開放問題

- 對於非平穩的梯度，衰減率的選擇是否與學習率同樣重要？
- 當 RMSProp 與 Adam 的偏差校正結合時，行為會如何改變？

## 參考文獻

### 開創性論文

- Tieleman, T. & Hinton, G.（2012）。*Lecture 6.5 — RMSProp: Divide the gradient by a running average of its recent magnitude*。Coursera 講義，*Neural Networks for Machine Learning*。— RMSProp 最初、未發表的介紹。
- Duchi, J., Hazan, E. & Singer, Y.（2011）。Adaptive Subgradient Methods for Online Learning and Stochastic Optimization。*Journal of Machine Learning Research*，12，2121–2159。https://jmlr.org/papers/v12/duchi11a.html — RMSProp 以平均取代的累積總和方法。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — 在 Adam 中使用同樣的平方梯度指數平均，並加入動量與偏差校正。
- Loshchilov, I. & Hutter, F.（2017）。*Decoupled Weight Decay Regularization*。ICLR。https://arxiv.org/abs/1711.05101 — 這一族自適應方法所用的解耦權重衰減。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 自適應隨機方法及其取捨的綜述。
