---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/kernel-methods-svm
  - theory/paradigms/supervised/linear-models
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/trees-and-ensembles
---

# 支援向量機

支援向量機（SVM）是一種分類器：在所有能分開各類別的邊界中，選出間隔最寬的那一條。它不必明確計算特徵，而是透過核函數運作，因此能畫出非線性的邊界。核方法的家族全貌見[支援向量機與核方法](index.md)頁。

## 概述

SVM 結合了兩個想法。第一是最大間隔原則：在能分開訓練資料的邊界中，選出離最近的點最遠的那一條。Cortes 與 Vapnik（1995）指出，所得決策曲面的特殊性質使其具有高度泛化能力。第二是核技巧。訓練問題只透過內積依賴資料，以核函數取代內積，就等於在高維特徵空間中做線性判別，而不需要真的建構該空間。

Boser、Guyon 與 Vapnik（1992）提出一個最大化間隔的訓練演算法，其解是支撐樣本的線性組合，而且其形式可以使用核。Cortes 與 Vapnik（1995）則把此方法推廣到非可分的訓練資料。今天一般所說的「SVM」指的就是這個版本。

## 核心概念

- **間隔**：決策邊界與最近訓練點之間的距離。對超平面 \(w^\top x + b = 0\)，兩個支撐超平面之間的寬度為 \(2/\lVert w\rVert\)。
- **支援向量**：位於間隔上或間隔內的訓練點。只有它們在解中具有非零權重。
- **鬆弛與軟間隔**：鬆弛變數 \(\xi_i \ge 0\) 允許部分點違反間隔，常數 \(C\) 則決定這些違反的代價。
- **合頁損失**：軟間隔目標對每個點施加的懲罰 \(\max(0, 1 - y f(x))\)。
- **核函數**：函數 \(k(x, x') = \langle \phi(x), \phi(x') \rangle\)，等於某個特徵空間 \(\phi\) 中的內積，而該特徵從不被直接計算。有效的核必須對稱且半正定（Mercer 條件）。

## 運作方式

原始形式的軟間隔問題為

\[
\min_{w, b, \xi}\ \tfrac12\lVert w\rVert^2 + C\sum_{i=1}^{n}\xi_i \quad \text{subject to}\quad y_i\big(w^\top\phi(x_i) + b\big) \ge 1 - \xi_i,\ \ \xi_i \ge 0
\]

其對偶形式只透過核值依賴資料：

\[
\max_{\alpha}\ \sum_{i}\alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j\,y_i y_j\,k(x_i,x_j) \quad \text{subject to}\quad 0 \le \alpha_i \le C,\ \ \sum_i \alpha_i y_i = 0
\]

預測時只用支援向量，也就是 \(\alpha_i > 0\) 的點：

\[
f(x) = \operatorname{sign}\Big(\sum_{i} \alpha_i\, y_i\, k(x_i, x) + b\Big)
\]

常見的核有線性、多項式與高斯（RBF）：

- 線性：\(k(x, x') = x^\top x'\)。
- 多項式：\(k(x, x') = (x^\top x' + c)^p\)。
- 高斯（RBF）：\(k(x, x') = \exp(-\gamma\lVert x - x'\rVert^2)\)。

## 關鍵方法

### A training algorithm for optimal margin classifiers（Boser, Guyon & Vapnik, 1992）

- **問題：** 最大間隔分類器的泛化能力良好，但需要非線性的邊界。顯式計算高維特徵映射的成本很高，因此方法必須在不計算它的情況下運作。
- **核心想法：** 透過對偶形式訓練最大間隔分類器，資料只以內積的形式出現。把每個內積換成核，就能在特徵空間中評估分類器，而不必建構它。解是支撐樣本的線性組合。
- **公式或演算法：** 硬間隔對偶問題。它就是上節的軟間隔對偶，去掉上界 \(C\)，並要求 \(\alpha_i \ge 0\)：

\[
\max_{\alpha}\ \sum_{i}\alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j\,y_i y_j\,k(x_i,x_j) \quad \text{subject to}\quad \alpha_i \ge 0,\ \ \sum_i \alpha_i y_i = 0
\]

- **結果：** 論文報告了手寫數字資料庫上的實驗。摘要未給出錯誤率，本次也未核對論文中的表格，因此此處不列出數值。
- **限制：** 硬間隔形式需要資料可分。訓練需要對所有訓練點求解一個二次規劃，成本隨範例數快速增加。

### Support-vector networks（Cortes & Vapnik, 1995）

- **問題：** 真實的訓練資料很少是可分的，因此硬間隔問題可能無解。方法需要在允許部分錯誤的同時，保留間隔的概念。
- **核心想法：** 把間隔方法推廣到非可分的資料。輸入被映射到極高維的特徵空間，並在其中建立線性的決策曲面；每一次違反都以鬆弛變數與常數 \(C\) 計入代價。
- **公式或演算法：** 軟間隔的原始形式與對偶形式，以及核決策函數，見運作方式一節。
- **結果：** 摘要提到光學字元辨識的基準測試，但未給出錯誤率，因此此處不列出數值。
- **限制：** 常數 \(C\) 與核參數（例如 RBF 核的 \(\gamma\)）必須調校，通常以交叉驗證進行。在有雜訊的資料上，支援向量的數量會增加，預測成本也隨之上升。訓練成本仍隨範例數快速增長。

## 關聯

- 核方法的家族全貌與各核的比較見[支援向量機與核方法](index.md)。
- 決策函數在特徵空間中是線性的，因此本方法與[線性模型](../linear-models/index.md)相鄰。
- 合頁損失把 SVM 的訓練與分類的[損失函數](../loss-functions-and-optimization/index.md)觀點連結起來。
- 間隔是[泛化理論](../generalization-theory/index.md)中基於間隔的界限的核心量。
- 在表格資料上，常見的替代方法是[隨機森林](../trees-and-ensembles/random-forests.md)與[梯度提升](../trees-and-ensembles/gradient-boosting.md)。
- 高斯過程等以核為基礎的貝氏模型，見[實例基礎與機率方法](../instance-based-and-probabilistic/index.md)。

## 開放問題

- 學得的深度特徵可以取代人工選定的核。在資料很少的情況下，固定的核何時仍是較好的選擇？
- 當資料大到無法重複進行交叉驗證時，應如何設定 \(C\) 與核的寬度？

## 參考文獻

### 開創性論文

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers. COLT 1992, 頁 144–152. https://doi.org/10.1145/130385.130401 — 提出對偶形式的最大間隔訓練演算法，使核能取代內積。
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297. https://doi.org/10.1007/BF00994018 — 把間隔分類器推廣到非可分的訓練資料，允許違反但須付出代價。

### 綜述與教科書

- Vapnik, V. N. (1995). *The Nature of Statistical Learning Theory*. Springer. https://doi.org/10.1007/978-1-4757-2440-0 — 支撐基於間隔之泛化的統計學習理論。
- Schölkopf, B. & Smola, A. J. (2002). *Learning with Kernels*. MIT Press. https://dblp.uni-trier.de/rec/books/lib/ScholkopfS02.html — 關於核方法、支援向量機及其理論與演算法的標準參考書。

### 文章與文件

- Chang, C.-C. & Lin, C.-J. (2011). LIBSVM: A library for support vector machines. *ACM Transactions on Intelligent Systems and Technology*, 2(3), Article 27. https://www.csie.ntu.edu.tw/~cjlin/papers/libsvm.pdf — 廣泛使用的 SVM 函式庫及其求解器。
