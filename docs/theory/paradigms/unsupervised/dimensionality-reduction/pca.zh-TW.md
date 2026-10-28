---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
  - theory/paradigms/unsupervised/autoencoders-and-representations
---

# PCA：主成分分析

PCA 把資料旋轉到一組互相正交的方向上，這些方向依所捕捉的變異量排序，然後保留前幾個。它是標準的線性降維方法，也是更複雜方法之前常用的第一步。家族層級的全貌見[降維](index.md)頁。

## 概述

給定資料點 \(x_1,\dots,x_n\in\mathbb R^d\)，PCA 找出一組標準正交方向 \(w_1,\dots,w_k\)，使投影到這些方向時保留最多的變異量。同一組方向也給出以平方誤差衡量、每個點只用 \(k\) 個數字的最佳線性重建。兩種觀點等價，並導向同一個計算：對共變異數矩陣做特徵分解，或對中心化的資料做奇異值分解。

## 核心概念

- **中心化資料**：減去樣本平均值後的資料。PCA 是在中心化資料上定義的。
- **主成分**：標準正交方向 \(w_j\)，依其捕捉的變異量排序。
- **載荷與分數**：成分 \(w_j\) 稱為載荷，投影後的座標 \(z_{ij}=w_j^\top x_i\) 稱為分數。
- **解釋變異比例**：前 \(k\) 個成分所捕捉的總變異比例，即 \(\sum_{j\le k}\lambda_j / \sum_j \lambda_j\)，其中 \(\lambda_j\) 為由大到小排列的共變異數特徵值。

## 運作方式

令 \(X\) 為 \(n\times d\) 的中心化資料矩陣，樣本共變異數為 \(S = \frac{1}{n-1}X^\top X\)。第一個主方向使投影的變異數最大，

\[
w_1 = \arg\max_{\|w\|=1}\ w^\top S\, w,
\]

它是 \(S\) 中最大特徵值對應的特徵向量。後續方向依序為次大的特徵向量，且與前面的方向正交。

等價地，對 \(X = U\Sigma V^\top\) 做奇異值分解。\(V\) 的各欄即為主方向，秩為 \(k\) 的重建為 \(X_k = U_k\Sigma_k V_k^\top\)。它是在平方 Frobenius 範數下，\(X\) 的最佳秩 \(k\) 近似，即 Eckart–Young 定理（[Eckart 與 Young，1936](#參考文獻)）。降到 \(k\) 維的投影為 \(Z = XV_k\)。

## 關鍵方法

### On lines and planes of closest fit to systems of points in space（Pearson，1901）

- **問題：** 對空間中的一組點，擬合最接近這些點的直線與平面。論文標題即點出這個設定。
- **核心想法：** 「最佳擬合子空間」這一觀點的歷史起源。本頁不重述論文本身的表述。

### Analysis of a complex of statistical variables into principal components（Hotelling，1933）

- **問題：** 把一組統計變數改寫為主成分來分析。論文標題即點出這個設定。
- **核心想法：** 上文各節所用的主成分表述。

### Probabilistic principal component analysis（Tipping 與 Bishop，1999）

- **問題：** 摘要指出 PCA 並非建立在機率模型之上。
- **核心想法：** 觀測資料向量的主軸，可以在與因子分析密切相關的潛在變數模型中，以最大概似估計求得。論文也提出以 EM 演算法估計主子空間。
- **結果：** 本頁沒有引用論文中的數值結果。
- **限制：** 本頁不重現論文中的概似函數分析。

## 關聯

- [自動編碼器](../autoencoders-and-representations/index.md)頁涵蓋非線性編碼器，而 PCA 是其線性基準。
- 在 PCA 降維後的資料上執行 [k-means](../clustering/k-means.md) 是常見做法，因為低維子空間中的距離通常較有資訊量。
- 同樣保留鄰域結構的非線性替代方法是 [t-SNE](t-sne.md) 與 [UMAP](umap.md)。它們主要用於視覺化，且常先用 PCA 降維。t-SNE 論文便是在最佳化前先以 PCA 把資料降到 30 維。

## 開放問題

- 變異量大不等於重要。在什麼情況下，變異量最大的方向才是任務真正需要的？
- PCA 對特徵尺度與離群值敏感，實務上應如何處理？

## 參考文獻

### 開創性論文

- Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*。https://zenodo.org/records/1430636/files/article.pdf — 「最佳擬合子空間」這一 PCA 觀點的歷史起源。連結為該文的數位化副本；期刊出處依文章標題與數位化紀錄判定。
- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*, 24。https://www.bohrium.com/paper-details/analysis-of-a-complex-of-statistical-variables-into-principal-components/812082556450111489-11152 — 以主成分之名提出此方法的論文。期刊與年份已由搜尋確認；連結為索引頁，而非出版社紀錄。
- Tipping, M. E. & Bishop, C. M. (1999). Probabilistic principal component analysis. *Journal of the Royal Statistical Society: Series B*, 61(3), 611–622. https://doi.org/10.1111/1467-9868.00196 — 將 PCA 表述為潛在變數模型上的最大概似，並提出估計主子空間的 EM 演算法。
- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika*, 1(3), 211–218. https://doi.org/10.1007/BF02288367 — 上述奇異值分解表述所用的最佳低秩近似定理。

### 綜述與教科書

- Jolliffe, I. T. & Cadima, J. (2016). Principal component analysis: a review and recent developments. *Philosophical Transactions of the Royal Society A*, 374, 20150202. https://doi.org/10.1098/rsta.2015.0202 — PCA 及其近期發展的綜述。
- Jolliffe, I. T. (2002). *Principal Component Analysis*（第 2 版）。Springer Series in Statistics。https://doi.org/10.1007/b98835 — PCA 的標準教科書。
