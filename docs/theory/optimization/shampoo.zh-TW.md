---
translation_reviewed: 2026-10-28
---

# Shampoo

Shampoo 是針對張量參數的預條件隨機最佳化器。它為每個張量維度保存一個預條件矩陣，並以這些矩陣的乘積重新縮放梯度，因此能捕捉對角方法（如 Adam）所忽略的結構。Gupta、Koren 與 Singer（2018）提出了此方法。上層概述見[二階與擬牛頓方法](second-order.md)，對角式的相對方法則是 [Adam](adaptive/adam.md)。

## 概述

自適應方法分別縮放每個座標，因此忽略了參數之間的相關性。全矩陣的 AdaGrad 使用能捕捉相關性的矩陣預條件子，但對一個有 $d$ 個元素的參數，它需要 $d \times d$ 的矩陣，對神經網路來說太大。Shampoo 把矩陣或張量參數視為每個維度各有一個索引的張量，並為每個維度保存一個小的預條件子。對矩陣參數 $W \in \mathbb{R}^{m \times n}$，它保存一個 $m \times m$ 與一個 $n \times n$ 的矩陣，遠小於完整的預條件子。

## 問題

全矩陣的自適應方法能適應梯度中的相關性，但其成本使它們不適用於深度網路。Gupta 等人想知道，張量參數的結構能否讓預條件子保有大部分好處，同時成本接近對角方法。

## 核心想法

對參數張量的每個維度，累積一個由沿該維度展開的梯度所建構的統計量。以這些統計量的反四次方根作為每一邊的預條件子。更新量即是梯度乘上各維度的預條件子。

## 演算法

對於梯度為 $G_t$ 的矩陣參數 $W$，保存兩個累加器：

$$
L_t = L_{t-1} + G_t G_t^\top, \qquad R_t = R_{t-1} + G_t^\top G_t
$$

然後以下式更新參數：

$$
W_{t+1} = W_t - \eta\, L_t^{-1/4}\, G_t\, R_t^{-1/4}
$$

論文採用延遲更新：每 20 到 100 步才重新計算一次逆根，並報告這對精度幾乎沒有影響，同時降低了每步的平均成本。此規則可推廣到張量，做法是對每個維度套用一個這樣的矩陣。

## 結果

摘要指出，Shampoo 每步的執行時間「與 SGD、AdaGrad、Adam 等簡單的梯度方法相當」，儘管其更新規則較為複雜。在最先進的深度學習模型實驗中，論文報告 Shampoo「收斂速度明顯快於常用的最佳化器」。摘要未給出具體數字，因此比較結果應參考論文的實驗。

## 限制

- 計算逆根很昂貴，因此論文採用延遲的重算排程。更新間隔是額外的超參數，而論文「對精度幾乎沒有影響」的發現，來自其自身的實驗。
- 此方法對矩陣與張量參數最為自然。對於偏置等向量，它會退化為對角方法。
- 收斂比較是經驗性的主張。它相對於 Adam 的優勢取決於預條件子調校得好不好。

## 關鍵方法

- [自適應方法](adaptive/index.md)是 Shampoo 所推廣的對角預條件子家族，其中 [Adam](adaptive/adam.md) 是主要代表。
- [K-FAC](kfac.md)是相關的結構化預條件子，它由費雪矩陣而非梯度統計量建構。
- [L-BFGS](lbfgs.md)是擬牛頓法，它由短歷史中的梯度差建構曲率。

## 關聯

- [二階與擬牛頓方法](second-order.md)是上層概述，Shampoo 與 L-BFGS、K-FAC 並列於其中。
- [數學](../math/index.md)涵蓋更新式中使用的矩陣平方根與克羅內克結構。

## 應用

- 訓練大型神經網路，其中注意力與前饋層的矩陣參數是自然的目標。
- 針對大型語言模型的較快最佳化器研究，通常與 Adam 比較。

## 開放問題

- 應如何更新逆根，才能在不損失收斂優勢的情況下限制成本？
- 哪些張量形狀最受益於結構化預條件子？在什麼情況下對角方法就已足夠？

## 參考文獻

### 開創性論文

- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — 提出 Shampoo，為張量參數的每維度矩陣預條件子，每步執行時間與一階方法相當。
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — 針對神經網路的另一種結構化預條件子，由費雪矩陣建構。
- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — 針對大型問題的擬牛頓法，在不儲存矩陣的情況下利用曲率。
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — 自然梯度，結構化預條件子的目標即在於近似它。

### 綜述與教科書

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — 自適應與預條件隨機方法的綜述及其取捨。
