---
translation_reviewed: 2026-10-28
---

# AdaGrad

AdaGrad 把每個參數的步長，依其過去所有平方梯度之和的平方根來縮放。收到較大或較頻繁梯度的參數會走較小的步，很少被更新的參數則保有較大的步長。Duchi、Hazan 與 Singer（2011）為線上學習與隨機最佳化提出此方法。上層概述見[自適應方法](index.md)。

## 概述

AdaGrad 是最早被廣泛使用的逐座標自適應方法。後來的變體 RMSProp 與 Adam 把累加的總和換成指數移動平均，從而修正了它的主要弱點。

## 問題

若只用一個全域學習率，很少出現的特徵會得到極小的更新，而頻繁出現的特徵則得到很大的更新。在稀疏問題中，例如使用詞袋特徵的文字，學習率必須同時適合兩種座標。

## 核心想法

為每個座標 \(i\) 保存其平方梯度的累加和。該座標的步長除以此總和的平方根。梯度歷史大的座標步長較小，歷史少的座標則保持接近基礎學習率的步長。

## 演算法

令 \(g_t\) 為第 \(t\) 步的梯度，\(G_{t} = \sum_{s \le t} g_s \odot g_s\) 為累積的平方梯度，其中 \(\odot\) 為逐元素乘積。更新式為

\[
\theta_{t+1} = \theta_t - \eta\, \frac{g_t}{\sqrt{G_t} + \epsilon},
\]

其中除法逐元素進行，\(\eta\) 為基礎學習率，\(\epsilon\) 為維持數值穩定的小常數。

## 主要結果

Duchi 等人（2011）摘要提出一族次梯度方法，這些方法會動態納入先前迭代中所觀察到之資料幾何的資訊。摘要用「大海撈針」來形容其效果，意即很少出現但有資訊量的特徵不再被頻繁特徵淹沒。摘要未給出數值結果，因此本頁不引用數字。

## 限制

- 累加和從不遞減，因此有效步長會持續縮小。訓練可能在收斂前就停滯，在深度網路中尤其如此，這也是 RMSProp 與 Adam 出現的動機。
- 基礎學習率仍需調校，且最佳值取決於問題。
- 每個參數都需要一個累加器，記憶體成本與其他逐座標方法相同。

## 關聯

- [自適應方法](index.md)是上層概述，AdaGrad 與 RMSProp、Adam 及後續變體並列於其中。
- [RMSProp](rmsprop.md)把總和換成指數平均，使步長不會縮小到零。
- [Adam](adam.md)把逐座標縮放與動量項及偏差校正結合。
- [Shampoo](../shampoo.md)把逐座標的想法延伸到完整的矩陣預條件子。

## 應用

- 在稀疏特徵上訓練線性模型與嵌入，這正是此方法設計來幫助的場景。
- 早期的深度學習實驗，在指數平均的變體成為標準之前。

## 開放問題

- 累加器能否在不損失稀疏特徵效益的前提下，以有原則的方式重設或衰減？
- AdaGrad 的幾何感知縮放，在深度網路上與 Shampoo 及 SOAP 的矩陣預條件子相比如何？

## 參考文獻

### 開創性論文

- Duchi, J., Hazan, E. & Singer, Y.（2011）。Adaptive Subgradient Methods for Online Learning and Stochastic Optimization。*Journal of Machine Learning Research*，12，2121–2159。https://jmlr.org/papers/v12/duchi11a.html — 提出 AdaGrad，依每個座標累積的平方梯度縮放步長。
- Tieleman, T. & Hinton, G.（2012）。*Lecture 6.5 — RMSProp: Divide the gradient by a running average of its recent magnitude*。Coursera 講義，*Neural Networks for Machine Learning*。https://cir.nii.ac.jp/crid/1370017282431050757 — 以指數平均修正 AdaGrad 步長縮小問題的 RMSProp 來源。
- Gupta, V., Koren, T. & Singer, Y.（2018）。*Shampoo: Preconditioned Stochastic Tensor Optimization*。ICML。https://arxiv.org/abs/1802.09568 — 把逐座標的 AdaGrad 想法延伸到完整的矩陣預條件子。
- Kingma, D. P. & Ba, J.（2015）。*Adam: A Method for Stochastic Optimization*。ICLR。https://arxiv.org/abs/1412.6980 — 把逐座標縮放與動量及偏差校正結合。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J.（2018）。*Optimization Methods for Large-Scale Machine Learning*。SIAM Review。https://arxiv.org/abs/1606.04838 — 自適應隨機方法綜述，以及大規模訓練中的取捨。
