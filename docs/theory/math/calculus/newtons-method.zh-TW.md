---
translation_reviewed: 2026-10-28
---

# 牛頓法

牛頓法透過反覆最小化損失的局部二次近似來求極小值。它以海森矩陣調整每一步，因此在平坦方向上走得遠，在陡峭方向上則走得謹慎。它在極小值附近收斂很快，但每一步都需要海森矩陣。本頁是[微積分與最佳化基礎](index.md)的一部分。

## 概述

梯度下降沿負梯度方向走固定大小的步。這個大小在各方向上都相同，因此在一個方向陡峭、另一個方向平坦的損失上會來回擺動，前進緩慢。牛頓法透過曲率修正這點。它在當前點擬合一個二次模型，並直接跳到該二次函數的極小值。

## 關鍵概念

- **二階模型**：\(L(\theta+\delta)\approx L(\theta)+\nabla L^\top\delta+\tfrac12\delta^\top H\delta\)，其中 \(H\) 為海森矩陣。
- **牛頓步**：使模型最小的 \(\delta\)，即 \(\delta = -H^{-1}\nabla L\)。
- **正定性**：當 \(H\) 為正定矩陣時，此步是下降步；否則可能走向鞍點或極大值。
- **二次收斂**：在海森矩陣為正定的極小值附近，誤差大致在每步平方。

## 運作方式

更新式為

\[
\theta_{k+1} = \theta_k - H_k^{-1}\nabla L(\theta_k).
\]

實務上不會直接求 \(H_k\) 的逆矩陣，而是解線性系統 \(H_k\delta = -\nabla L\)。因此每次迭代需要梯度、海森矩陣與一次線性求解。若模型有 \(n\) 個參數，海森矩陣有 \(n^2\) 個元素，對大型網路並不實際。

海森矩陣的特徵值決定其行為。特徵值大的方向較陡，牛頓步在該方向縮小移動；特徵值小的方向較平，步長則放大。因此純牛頓步可能衝過頭，或走向鞍點，這就是實務版本加入阻尼或線搜尋的原因。

邏輯斯回歸是牛頓法實用的典型例子，因為參數數量少。Bishop（2006）展示了由此得到的迭代加權最小平方更新。

## 主要方法

- [梯度下降](../../optimization/index.md)：一階替代方法，每步成本較低，但接近極小值時較慢。
- 擬牛頓法（如 L-BFGS）由梯度差分近似海森矩陣，避免直接形成它。見[最佳化章節](../../optimization/index.md)。

## 與其他頁面的連結

- [微積分與最佳化基礎](index.md)提供此方法所需的泰勒展開與海森矩陣。
- [線性代數](../linear-algebra/index.md)說明海森矩陣的特徵值如何控制各方向的步長。
- 腦與認知：此方法在這裡是計算工具，而非神經處理的模型。

## 應用

- **邏輯斯回歸**：牛頓更新，常稱為迭代加權最小平方（Bishop, 2006）。
- **凸最佳化**：內點法在經障礙項修改的問題上使用牛頓步（Boyd & Vandenberghe, 2004）。
- **大規模學習**：二階方法被視為隨機梯度下降的替代方案，兩者在成本上有取捨（Bottou et al., 2018）。

## 開放問題

- 深度網路可擴展的二階方法仍是活躍的研究領域，因為在大規模下形成與求逆海森矩陣的成本過高。
- 鞍點在高維損失地形中很常見，除非經過修改，牛頓型步驟可能被吸引至其中。

## 參考文獻

### 奠基性論文

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — 比較大規模學習中的二階與一階方法，包括海森資訊的成本。
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 介紹牛頓法及其收斂分析，以及實務中使用的阻尼版本。

### 綜述與教科書

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 展示邏輯斯回歸的牛頓–拉弗森更新。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；在廣義線性模型的擬合中討論牛頓法。
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — 涵蓋每一步牛頓法所需的線性求解。
