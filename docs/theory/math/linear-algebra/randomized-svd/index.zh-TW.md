---
translation_reviewed: 2026-10-28
---

# 隨機化 SVD

隨機化 SVD 透過把矩陣投影到一個小的隨機子空間，再對小得多的矩陣做精確 SVD，來計算近似的截斷奇異值分解。這使得對於古典演算法而言太大的矩陣，也能進行低秩近似。它是[AI 的線性代數](../index.md)三個關鍵方法之一，並建立在[截斷 SVD](../truncated-svd/index.md)之上。

## 概述

截斷 SVD 是最佳的低秩近似，但對一個稠密的 $m\times n$ 矩陣做精確 SVD 需要約 $mn\min(m,n)$ 次運算，而且要把整個矩陣同時放進記憶體。許多 AI 問題只需要非常大的矩陣（例如嵌入表或大型權重矩陣）的前幾個奇異向量。對這些問題而言，計算所有方向的精確分解是浪費。

Halko、Martinsson 與 Tropp（2011）指出，對矩陣作用做隨機取樣，就能捕捉到大部分重要的方向。此程序很簡單，需要的資料遍歷次數少，並且很適合在平行硬體上執行。其準確度取決於矩陣奇異值衰減的速度。

## 核心概念

- **矩陣的值域**：所有向量 $Ax$ 的集合，即 $A$ 各行張成的空間。最大的奇異向量張成了值域中最重要的部分。
- **草圖（sketch）**：乘積 $Y = A\Omega$，其中 $\Omega$ 是隨機矩陣。它是 $A$ 各行的一小組隨機組合。
- **正交基底**：張成草圖的、行向量為正交單位向量的矩陣 $Q$。投影 $QQ^\top A$ 逼近 $A$。
- **過取樣**：取比目標秩多幾個隨機向量，以少量成本換取更高的準確度。
- **冪迭代**：把草圖乘上 $AA^\top$ 數次，使譜變得更尖銳，讓隨機子空間偏向較大的奇異值。

## 運作方式

給定矩陣 $A \in \mathbb{R}^{m\times n}$、目標秩 $k$、少量的過取樣量 $p$，以及冪迭代次數 $q$，演算法分六步進行：

1. 抽取高斯隨機矩陣 $\Omega \in \mathbb{R}^{n\times(k+p)}$。
2. 形成草圖 $Y = (AA^\top)^q A\,\Omega$。以冪迭代取代單純的 $A\Omega$。
3. 計算張成 $Y$ 各行的正交基底 $Q$，例如以 QR 分解。當奇異值快速衰減時，$QQ^\top A$ 是 $A$ 的良好近似。
4. 形成小矩陣 $B = Q^\top A \in \mathbb{R}^{(k+p)\times n}$。
5. 對 $B$ 做精確 SVD：$B = \tilde U \Sigma V^\top$。由於 $B$ 的列數很少，這一步很便宜。
6. 令 $U = Q\tilde U$，並保留前 $k$ 個奇異值與向量。

輸出的形式與截斷 SVD 相同，$A \approx U_k\Sigma_k V_k^\top$。關鍵在於，昂貴的工作只透過與瘦矩陣的乘積來接觸 $A$。在稠密矩陣的情形下，依其摘要，作者指出隨機化方法需要 $O(mn\log k)$ 次浮點運算，而古典方法需要 $O(mnk)$。

## 結果

論文以大量數值實驗與詳細的誤差分析支持其主張。依摘要，在許多情況下，隨機化方法在準確度、穩健性與速度上都優於古典方法，而其優點取決於計算環境。

Rokhlin、Szlam 與 Tygert（2009）把一種隨機化低秩演算法應用於 PCA。依其摘要，對任意大小的矩陣，其準確度非常接近可能的最佳值；而在先前的快速演算法中，除非矩陣的一個或兩個維度很小，否則沒有準確度保證。他們的證據來自數值例子。

沒有單一的基準能概括這些結果，因此比較是定性的：當目標秩相對於矩陣大小很小，且譜會衰減時，此方法最具吸引力。

## 限制

- **是近似，不是精確解。** 輸出的誤差取決於譜的形狀。當奇異值衰減緩慢時，草圖會遺漏重要的方向，誤差可能遠大於最佳的秩 $k$ 誤差。
- **隨機性。** 不同的隨機抽樣會給出略有不同的結果。在條件良好時，這種變動很小，但它仍是輸出的一部分。
- **資料遍歷次數。** 每次冪迭代都需要對矩陣額外遍歷一次，因此準確度與成本直接互換。
- **小矩陣。** 對於能輕鬆放進記憶體的矩陣，古典 SVD 較簡單，通常也夠快。

## 未解問題

- 單次遍歷的串流版本，能否在資料只出現一次的情況下，達到多次遍歷方法的準確度？
- 當譜近乎平坦（學得的權重常是如此）時，能給出什麼樣的保證？
- 低精度運算與分散式硬體，如何改變草圖的取捨？

## 參考文獻

### 開創性論文

- Halko, N., Martinsson, P. G. & Tropp, J. A.（2011）. Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions. *SIAM Review*. https://doi.org/10.1137/090771806 — 提出一套模組化的隨機化演算法框架，透過取樣子空間來計算部分矩陣分解。
- Rokhlin, V., Szlam, A. & Tygert, M.（2009）. A Randomized Algorithm for Principal Component Analysis. *SIAM Journal on Matrix Analysis and Applications*. https://doi.org/10.1137/080736417 — 把隨機化低秩近似應用於 PCA，準確度接近可能的最佳值。
- Eckart, C. & Young, G.（1936）. The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — 給出隨機化方法所近似的精確截斷 SVD。

### 綜述與教科書

- Martinsson, P.-G. & Tropp, J. A.（2020）. Randomized numerical linear algebra: Foundations and algorithms. *Acta Numerica*. https://doi.org/10.1017/S0962492920000021 — 綜述機率演算法，涵蓋低秩近似、子空間迭代與誤差估計。
- Woodruff, D. P.（2014）. Sketching as a Tool for Numerical Linear Algebra. https://arxiv.org/abs/1411.4357 — 綜述線性草圖技術，包括其在低秩近似與迴歸中的應用。
