---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
  - theory/paradigms/unsupervised/autoencoders-and-representations
---

# t-SNE

t-SNE 把高維點映射到二或三維，使相近的點在圖上仍然相近，因此它是描繪資料集結構的常用工具之一。它是非線性方法，輸出用來觀察，而不是用來量測距離。家族層級的全貌見[降維](index.md)頁。

## 概述

Van der Maaten 與 Hinton（2008）把 t-SNE 描述為隨機鄰域嵌入（SNE，[Hinton 與 Roweis，2002](#參考文獻)）的改良版。摘要指出，新方法的最佳化明顯更容易，並減少點擠在圖中央的傾向。

## 核心概念

- **親和度** \(p_{j\mid i}\)：在原始空間中，以 \(x_i\) 為中心的高斯分布下，點 \(i\) 會選擇點 \(j\) 作為鄰居的機率。
- **困惑度**（perplexity）：使用者設定的值，控制有效鄰居數量。每個點的頻寬 \(\sigma_i\) 都經過調整，使其鄰居分布的困惑度等於此值。
- **低維相似度** \(q_{ij}\)：對圖上的點使用相同形式的量，但改用重尾的 Student-t 核，自由度為一。
- **擁擠問題**（crowding）：在低維圖中，許多中等距離的點沒有足夠空間可放。重尾的核讓它們有更多空間，這就是選擇此核的理由。

## 運作方式

原始空間的親和度為高斯型，並經過對稱化：

\[
p_{j\mid i} = \frac{\exp(-\|x_i-x_j\|^2/2\sigma_i^2)}{\sum_{k\ne i}\exp(-\|x_i-x_k\|^2/2\sigma_i^2)}, \qquad
p_{ij} = \frac{p_{j\mid i}+p_{i\mid j}}{2n}.
\]

頻寬 \(\sigma_i\) 以二分搜尋決定，使 \(\mathrm{Perp}(P_i)=2^{H(P_i)}\) 等於所選的困惑度，其中 \(H\) 為以位元為單位的 Shannon 熵。

圖上的親和度使用 Student-t 核：

\[
q_{ij} = \frac{(1+\|y_i-y_j\|^2)^{-1}}{\sum_{k\ne l}(1+\|y_k-y_l\|^2)^{-1}}.
\]

訓練以梯度下降最小化兩個分布之間的 Kullback–Leibler 散度，

\[
C = \mathrm{KL}(P\,\|\,Q) = \sum_i\sum_{j} p_{ij}\log\frac{p_{ij}}{q_{ij}},
\]

其梯度為

\[
\frac{\partial C}{\partial y_i} = 4\sum_j (p_{ij}-q_{ij})(y_i-y_j)\,(1+\|y_i-y_j\|^2)^{-1}.
\]

論文的視覺化最佳化設定如下：前 50 次迭代時將 \(p_{ij}\) 乘以 4（早期誇大），總共迭代 1000 次；動量在第 250 次迭代前為 0.5，之後為 0.8；並先以 PCA 把資料降到 30 維。

## 關鍵方法

### Visualizing Data using t-SNE（Van der Maaten 與 Hinton，2008）

- **問題：** 包括 SNE 在內的既有嵌入方法在最佳化與擁擠問題上有困難，圖上的群集常常重疊。
- **核心想法：** 在原始空間保留高斯親和度，在圖上使用自由度為一的 Student-t 核，並最小化兩者之間的 KL 散度。
- **公式或演算法：** 上節的親和度、困惑度、KL 與梯度公式，以及最佳化排程。
- **結果：** 以 10 折交叉驗證計，MNIST 的 1-最近鄰錯誤率在原始 784 維資料上為 5.75%。論文隨機漫步變體所建的二維圖（以 6,000 個數字建構，親和度由全部 60,000 個計算）達到 5.13%。
- **限制：** 論文指出成本函數非凸，因此不同執行可能停在不同的局部極小值。論文把 t-SNE 描述為非參數方法，並把參數化版本列為未來工作，以便推廣到留出的資料。

## 關聯

- 其線性對應方法是 [PCA](pca.md)，常在 t-SNE 之前先用它降維。
- [UMAP](umap.md) 是最常見的替代方法。它建立在鄰域圖上，作者報告其在大型資料集上比 t-SNE 快。
- 在 t-SNE 圖上看到的群集，應該用[分群](../clustering/index.md)頁的方法再檢驗，而不是只看圖。
- 同時產生低維特徵的非線性編碼器，見[自動編碼器與表示](../autoencoders-and-representations/index.md)。

## 開放問題

- t-SNE 圖能保留多少資料的全域幾何？能否量化？
- 困惑度與迭代排程的哪種選擇，能在不同資料集上都穩健？

## 參考文獻

### 開創性論文

- Van der Maaten, L. & Hinton, G. (2008). Visualizing Data using t-SNE. *Journal of Machine Learning Research*, 9, 2579–2605. https://jmlr.org/papers/v9/vandermaaten08a.html — 提出 t-SNE，包括 Student-t 圖上核與 KL 目標函數。上述 MNIST 數值與最佳化設定已對照 PDF 核對。
- Hinton, G. & Roweis, S. (2002). Stochastic Neighbor Embedding. *Advances in Neural Information Processing Systems 15 (NIPS 2002)*. https://papers.nips.cc/paper/2276-stochastic-neighbor-embedding — t-SNE 所改良的 SNE 方法。

### 理論

- Linderman, G. C. & Steinerberger, S. (2019). Clustering with t-SNE, provably. arXiv 預印本：https://arxiv.org/pdf/1706.02582 — 對以 t-SNE 進行分群的理論分析，如標題所示。arXiv 紀錄已由搜尋確認；期刊版本（SIAM Journal on Mathematics of Data Science）未經確認，故不引用。

### 應用

- Kobak, D. & Berens, P. (2019). The art of using t-SNE for single-cell transcriptomics. *Nature Communications*, 10, 5416. https://doi.org/10.1038/s41467-019-13056-x — 在單細胞轉錄體資料上使用 t-SNE 的實務指引。
- Becht, E. 等人 (2019). Dimensionality reduction for visualizing single-cell data using UMAP. *Nature Biotechnology*, 37, 38–44. https://doi.org/10.1038/nbt.4314 — 將 UMAP 應用於單細胞資料的視覺化。
