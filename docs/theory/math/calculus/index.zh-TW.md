---
translation_reviewed: 2026-10-28
---

# 微積分與最佳化基礎

訓練模型就是調整參數以降低損失，而微積分告訴我們損失如何隨每個參數的變化而改變。本頁涵蓋最佳化與深度學習各頁所假設的微積分：梯度、雅可比與海森矩陣、連鎖律、泰勒展開、凸性與有約束的最佳化。它是[數學基礎概述](../index.md)的一部分。

## 概述

損失 \(L(\theta)\) 是參數向量 \(\theta\) 的函數。其梯度 \(\nabla_\theta L\) 指向增加最快的方向，因此沿其反方向移動即可降低損失。步伐多大、以及損失在哪些方向上彎曲得最厲害，則由海森矩陣收集的二階導數回答。兩者都是局部的，只描述當前參數附近的小範圍。

AI 使用的微積分大多是一階的（梯度、連鎖律），少數是二階的（曲率、牛頓法）。約束透過拉格朗日乘數進入，這在支持向量機與有約束的強化學習目標中都會出現。

## 關鍵概念

- **偏導數與梯度**：\(\partial L/\partial\theta_j\) 衡量損失隨參數 \(j\) 的變化，梯度則把它們收集成一個向量。
- **雅可比矩陣**：向量值函數所有一階導數構成的矩陣，例如某層輸出對輸入的導數。
- **海森矩陣**：二階導數矩陣 \(H_{jk} = \partial^2 L / \partial\theta_j\partial\theta_k\)，描述曲率。
- **連鎖律**：複合函數的導數是沿路徑上各導數之積。反向傳播就是系統性地套用此規則於整個網路。
- **泰勒展開**：局部的多項式近似，\(L(\theta+\delta) \approx L(\theta) + \nabla L^\top\delta + \tfrac12\delta^\top H\delta\)。
- **凸性**：凸函數沒有虛假的局部極小值，因此局部極小即全域極小。

## 運作方式

連鎖律是訓練的引擎。對於一個參數為 \(w\)、先產生隱藏值 \(z\)、再產生輸出 \(y\) 的網路，

\[
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial w}.
\]

反向傳播（Rumelhart et al., 1986）從輸出端往回計算這些乘積，並重複利用中間結果，因此計算一次梯度的成本與一次前向傳播相近。

梯度下降只使用梯度：\(\theta \leftarrow \theta - \eta\nabla L\)。牛頓法同時使用海森矩陣，以 \(H^{-1}\) 調整步長；在海森矩陣性質良好時，它在極小值附近收斂得更快，但每步成本高得多。二階泰勒展開解釋了兩者的差異。詳見[牛頓法](newtons-method.md)與[拉格朗日乘數法](lagrange-multipliers.md)兩頁。

## 主要方法

三個代表性工具組織了訓練的微積分。每個都有獨立頁面或連結到相應頁面。

- [牛頓法](newtons-method.md)：利用海森矩陣取得依曲率調整的步長；接近極小值時很快，但在高維時代價高。
- [拉格朗日乘數法](lagrange-multipliers.md)：以額外的乘數把有約束問題轉為無約束問題；是支持向量機與 KKT 條件的基礎。
- 隨機梯度下降：以小批次產生的雜訊估計取代完整梯度。其收斂理論源於 Robbins 與 Monro（1951）；建立在此之上的方法見[最佳化章節](../../optimization/index.md)。

## 與其他頁面的連結

- [線性代數](../linear-algebra/index.md)提供海森矩陣的特徵值，它們決定各方向的曲率與問題的條件數。
- [機率與統計](../probability-statistics/index.md)說明為何負對數概似是常用的、可微分的損失。
- [最佳化](../../optimization/index.md)在本頁基礎上介紹一階與適應性方法。
- 腦與認知：在人工網路中，基於梯度的學習是突觸可塑性的標準模型。大腦是否實現類似反向傳播的機制，仍是開放問題；爭論見[神經科學與 AI 的連結](../../../brain-mind/neuroai/index.md)。

## 應用

- **訓練神經網路**：每次參數更新都使用反向傳播計算的梯度（Rumelhart et al., 1986）。
- **支持向量機**：對偶問題以拉格朗日乘數推導（Cortes & Vapnik, 1995）。
- **病態問題**：二階資訊解釋了為何某些問題對梯度下降特別困難（Boyd & Vandenberghe, 2004）。
- **大規模機器學習**：隨機方法與二階方法的比較見 Bottou et al.（2018）的綜述。

## 開放問題

- 深度網路的損失地形是非凸的，但梯度方法常能找到好的解。其原因只被部分理解。
- 二階方法可以加快訓練，但在極大模型中成本很高。實用的近似在精確度與速度之間取捨，其方式仍在研究中。

## 參考文獻

### 奠基性論文

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature* 323, 533–536. https://doi.org/10.1038/323533a0 — 說明連鎖律可以有效地用來計算多層網路的梯度。
- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics* 22(3), 400–407. https://doi.org/10.1214/aoms/1177729586 — 提出隨機逼近，是隨機梯度下降的理論基礎。
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning* 20(3), 273–297. https://doi.org/10.1007/BF00994018 — 以帶乘數的約束最佳化定義支持向量機。

### 綜述與教科書

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 免費線上教材；涵蓋凸集、牛頓法、對偶與 KKT 條件。
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 說明邏輯斯回歸的牛頓–拉弗森更新，並提供導數的數學背景。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋以梯度為基礎的最佳化及其在訓練模型中的應用。

### 文章與文件

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — 綜述機器學習的最佳化方法，包括隨機、二階與有約束的形式，以及其實務成本。
