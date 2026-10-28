---
translation_reviewed: 2026-10-28
---

# 拉格朗日乘數法

拉格朗日乘數法用來解有等式或不等式約束的最佳化問題。它以額外的變數（即乘數，每個約束一個）把有約束問題改寫為無約束問題。支持向量機與有約束的強化學習目標都以此方式建構。本頁是[微積分與最佳化基礎](index.md)的一部分。

## 概述

許多學習問題都有約束。間隔分類器必須分開各類別，策略必須接近參考策略，機率向量的元素總和必須為一。直接解 \(\min_x f(x)\) 且 \(g(x)=0\) 很困難，因為可行集是彎曲的。拉格朗日方法把 \(\lambda g(x)\) 加入目標，並尋找合併後函數的駐點。

## 關鍵概念

- **拉格朗日函數**：\(\mathcal{L}(x,\lambda) = f(x) + \lambda\, g(x)\)。其駐點給出候選解。
- **乘數**：\(\lambda\) 衡量若放寬該約束，最佳值會改變多少。
- **不等式約束**：\(h(x)\le 0\) 會加入非負乘數 \(\mu\ge 0\)，以及互補鬆弛條件 \(\mu\,h(x)=0\)。
- **KKT 條件**：含不等式約束的有約束最佳化的一階必要條件，以 Karush、Kuhn 與 Tucker 命名。
- **對偶性**：對偶問題是在原變數上最大化拉格朗日函數。它有時更容易求解，核方法進入支持向量機正是透過此途徑。

## 運作方式

對於單一等式約束，\(\mathcal{L}\) 的駐點滿足

\[
\nabla f(x) + \lambda \nabla g(x) = 0, \qquad g(x)=0.
\]

幾何上，在最佳點目標函數的梯度與約束的梯度平行。對不等式約束，KKT 條件另外加入 \(\mu\ge 0\) 與 \(\mu\,h(x)=0\)。支持向量機是經典例子：其對偶問題只涉及位於間隔邊界上的訓練點，這些點的乘數非零（Cortes & Vapnik, 1995）。

拉格朗日乘數也會以懲罰項的形式出現在深度學習中：當一個不等式約束以懲罰而非精確求解來實施時，就會用到權重固定或自適應的乘數。

## 主要方法

- [牛頓法](newtons-method.md)：可用於拉格朗日函數的駐點條件的二階方法，是一階 KKT 方法的替代。
- 內點法：以障礙項處理不等式約束，與此相關但不同的方法，見 Boyd 與 Vandenberghe（2004）。

## 與其他頁面的連結

- [微積分與最佳化基礎](index.md)提供駐點條件所用的梯度微積分。
- [線性代數](../linear-algebra/index.md)說明權重範數的約束如何與投影相關。
- 支持向量機出現在[監督式學習](../../paradigms/supervised/index.md)中。

## 應用

- **支持向量機**：透過對偶問題求解的最大間隔分類器（Cortes & Vapnik, 1995）。
- **有約束的策略更新**：信賴域方法以 KL 散度的約束限制每次更新中策略的移動幅度（見[強化學習](../../paradigms/reinforcement-learning/index.md)）。
- **公平性與安全約束**：有約束的訓練問題以乘數執行可量測的要求（Boyd & Vandenberghe, 2004）。

## 開放問題

- 以隨機梯度訓練大型模型的有約束訓練可能不穩定。乘數的更新與參數的更新以目前尚未完全理解的方式相互作用。
- 非凸約束沒有一般的對偶性保證，因此 KKT 條件是必要的，但未必能得到全域解。

## 參考文獻

### 奠基性論文

- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning* 20(3), 273–297. https://doi.org/10.1007/BF00994018 — 以帶乘數的約束最佳化推導支持向量機。
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 介紹拉格朗日對偶、KKT 條件及其在凸問題中的應用。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 在支持向量機的討論中涵蓋有約束最佳化與拉格朗日函數。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋核方法所用的有約束形式。

### 文章與文件

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — 綜述學習用的最佳化方法，包括有約束的形式及其實務成本。
