---
translation_reviewed: 2026-10-28
---

# 特徵值分解

特徵值分解把方陣寫成其特徵向量與特徵值的形式。對稱矩陣的特徵向量彼此正交，特徵值為實數，因此此分解常用於共變異數矩陣與損失函數的海森矩陣。本頁是[線性代數](index.md)的一部分。

## 概述

方陣 \(A\) 的特徵向量是非零向量 \(\mathbf{v}\)，\(A\) 作用後方向不變：\(A\mathbf{v} = \lambda \mathbf{v}\)。純量 \(\lambda\) 為特徵值，即 \(A\) 沿該方向拉伸的倍數。沿特徵向量方向，矩陣只做簡單的縮放，因此重複作用很容易分析：\(A^k\mathbf{v} = \lambda^k\mathbf{v}\)。

## 關鍵概念

- **特徵對**：特徵值與其對應的特徵向量。
- **譜定理**：實對稱矩陣的特徵值皆為實數，且有一組標準正交的特徵向量。
- **半正定矩陣**：所有特徵值皆非負的對稱矩陣。共變異數矩陣即屬此類。
- **譜半徑**：特徵值絕對值的最大值。矩陣重複相乘時，增長或衰減取決於譜半徑大於或小於一。

## 運作方式

對實對稱 \(n\times n\) 矩陣，譜定理給出

\[
A = Q\Lambda Q^\top, \qquad \Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n),
\]

其中正交矩陣 \(Q\) 的各欄為特徵向量。二次型因此沿特徵方向分解：

\[
\mathbf{x}^\top A \mathbf{x} = \sum_{i} \lambda_i \, (\mathbf{q}_i^\top \mathbf{x})^2 .
\]

因此每個特徵值就是該二次函數在其自身方向上的曲率。這是海森矩陣的特徵值對最佳化很重要的原因：大的特徵值標示陡峭方向，小的則標示平坦方向（見[微積分與最佳化](../calculus/index.md)）。

求主特徵向量的一個標準方法是冪迭代，即反覆套用 \(A\) 並正規化結果。當主特徵值與其他特徵值有明顯間隔時，它會收斂到絕對值最大特徵值所對應的特徵向量（見 [Golub 與 Van Loan](index.md)）。

## 主要方法

特徵值分解是線性代數中兩個代表性的矩陣分解之一，另一個是奇異值分解。

- [奇異值分解](svd.md)：適用於任意矩陣。對半正定對稱矩陣，其奇異值等於特徵值，兩種分解在此一致。

方陣且對稱時（如共變異數矩陣或海森矩陣）使用特徵值分解；資料或權重矩陣為非方陣時使用奇異值分解。

## 與其他頁面的連結

- [主成分分析](../../paradigms/unsupervised/dimensionality-reduction/pca.md)以共變異數矩陣的特徵向量作為主方向，各方向上的變異數即對應的特徵值。
- [機率與統計](../probability-statistics/index.md)中多元高斯分布的共變異數矩陣，即以此方式對角化。
- [微積分與最佳化](../calculus/index.md)以海森矩陣及其特徵值描述損失函數的局部形狀。

## 應用

- **主成分分析**：資料集的主成分即其共變異數矩陣的特徵向量（Bishop, 2006 涵蓋 PCA）。
- **曲率與條件數**：海森矩陣最大與最小特徵值之比，說明一個二次目標用梯度下降解有多困難（Boyd & Vandenberghe, 2004）。
- **穩定性分析**：線性動力系統會衰減或增長，取決於其矩陣的特徵值。

## 開放問題

- 對非常大的矩陣（例如大型網路的海森矩陣）計算特徵值分解成本高昂，實用方法依賴近似，而其精確度難以保證。
- 非對稱矩陣的特徵值可能為複數或病態，因此其特徵值分解比對稱矩陣可靠度低。

## 參考文獻

### 奠基性論文

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — 以共變異數矩陣的特徵向量定義 PCA 的教科書說明。

### 綜述與教科書

- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — 涵蓋對稱特徵值問題與冪迭代。
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — 研究所教材，涵蓋特徵值問題及其數值行為。
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — 免費教科書；涵蓋 PCA 及其所對角化的共變異數矩陣。

### 講義

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — 課程講次包含特徵值與特徵向量，之後是對角化。

### 文章與文件

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — 免費線上教材；涵蓋海森矩陣特徵值所參與的二階條件，以及二次問題的條件數。
