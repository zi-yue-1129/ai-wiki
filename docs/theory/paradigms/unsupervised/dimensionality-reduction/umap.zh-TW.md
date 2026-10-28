---
translation_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
---

# UMAP

UMAP 是非線性降維方法，它先在資料上建立加權的鄰域圖，再排出該圖的低維版本。作者在執行時間與保留全域排列的程度上，把它與 t-SNE 相比，同時得到相近的視覺化結果。家族層級的全貌見[降維](index.md)頁。

## 概述

McInnes、Healy 與 Melville（2018）以黎曼幾何與代數拓撲的理論來說明 UMAP。實際上，此方法可歸結為三個步驟：用每個點的 \(k\) 個最近鄰估計局部距離，把距離轉為模糊的邊權重，然後最佳化一個低維排列，使其邊權重與高維的權重相符。摘要描述其結果為：視覺化品質與 t-SNE 相當，作者認為它可能保留較多的全域結構，並有較佳的執行時間表現。

## 核心概念

- **局部連通性** \(\rho_i\)：點 \(i\) 到其最近鄰的距離。每個點至少與一個鄰居以權重 1 相連。
- **模糊權重**：介於 0 與 1 之間的邊權重，超過 \(\rho_i\) 的距離後會衰減。它是邊在模糊單純集中的隸屬強度。
- **最小距離**（`min_dist`）：控制圖上點可以多緊密地聚在一起的參數。
- **最近鄰下降法**（nearest-neighbour descent）：UMAP 用來建立圖的近似 \(k\) 最近鄰方法。論文報告其經驗複雜度約為 \(O(N^{1.14})\)。

## 運作方式

對每個點 \(x_i\)，令 \(x_{i1},\dots,x_{ik}\) 為其 \(k\) 個最近鄰。其有向權重為

\[
w_{j\mid i} = \exp\!\Big(-\frac{\max(0,\ d(x_i,x_{ij})-\rho_i)}{\sigma_i}\Big),
\]

其中 \(\sigma_i\) 以二分搜尋決定，使權重總和等於一個固定目標。有向權重以模糊聯集合併為對稱權重：

\[
v_{ij} = v_{j\mid i} + v_{i\mid j} - v_{j\mid i}\,v_{i\mid j}.
\]

在低維圖上，權重的形式為

\[
w_{ij} = \big(1+a\,\|y_i-y_j\|^{2b}\big)^{-1},
\]

其中 \(a\) 與 \(b\) 以非線性最小平方法擬合到由 `min_dist` 決定的目標曲線。論文報告，使用 UMAP 實作的預設值時 \(a \approx 1.929\)、\(b \approx 0.7915\)。若設 \(a=b=1\)，就得到 t-SNE 所用的 Student-t 核。排列的求解方式是最小化兩個加權圖之間的交叉熵，

\[
C = \sum_{i\ne j}\Big[v_{ij}\log\frac{v_{ij}}{w_{ij}} + (1-v_{ij})\log\frac{1-v_{ij}}{1-w_{ij}}\Big].
\]

吸引項把相連的點拉近，排斥項則把不相連的點推開。

## 關鍵方法

### UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction（McInnes、Healy 與 Melville，2018）

- **問題：** 作者把 UMAP 與 t-SNE 相比，並希望找到在大型真實資料集上實用的方法，視覺化品質與 t-SNE 相當，且更能保留全域結構。
- **核心想法：** 在原始空間建立模糊的鄰域圖，接著找出一個低維排列，使其圖以交叉熵衡量時盡可能接近原圖。
- **公式或演算法：** 上節的模糊權重、對稱化、低維曲線 \(w_{ij}\)，以及交叉熵損失。
- **結果：** 論文的執行時間表（arXiv v3 版的表 3）顯示，在 MNIST（70,000 × 784）上 UMAP 花 87 秒，而 MulticoreTSNE 的 t-SNE 花 1450 秒，FIt-SNE 花 292 秒。在 Pen Digits（1,797 × 64）上，UMAP 花 9 秒，t-SNE 花 17 秒，Laplacian Eigenmaps 與 Isomap 各花 2 秒。論文說明 UMAP 的時間是單核版本，而 FIt-SNE 使用多核，因此各方的時間並非在相同條件下比較。
- **限制：** 表 3 顯示，在小資料上某些經典方法較快，Pen Digits 的結果即為一例。複雜度數字是經驗性的，論文也指出 nearest-neighbour descent 尚無理論上的複雜度界。結果取決於鄰居數量與 `min_dist`。

## 關聯

- 其主要比較對象是 [t-SNE](t-sne.md)，兩者使用相同的 Student-t 核（\(a=b=1\)）。
- 其圖結構的想法與[分群](../clustering/index.md)的譜觀點相通，後者也以相似度圖為核心。
- 線性基準方法 [PCA](pca.md) 可在 UMAP 之前先用來降低高維輸入的維度。

## 開放問題

- 論文所稱保留全域結構的主張，在不同資料集上有多少成立？應如何量化？Kobak 與 Linderman（2021）主張，初始化對 t-SNE 與 UMAP 的全域結構保留至關重要。
- 排列結果對鄰居數量與 `min_dist` 的選擇有多敏感？

## 參考文獻

### 開創性論文

- McInnes, L., Healy, J. & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv 預印本。https://arxiv.org/abs/1802.03426 — 提出 UMAP，包括模糊圖的建構與交叉熵的排列目標。上述執行時間表與 a、b 數值已對照 arXiv v3 PDF 核對。
- McInnes, L., Healy, J. & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection. *Journal of Open Source Software*。https://joss.theoj.org/papers/10.21105/joss.00861 — UMAP 實作的軟體論文。

### 應用與比較

- Becht, E. 等人 (2019). Dimensionality reduction for visualizing single-cell data using UMAP. *Nature Biotechnology*, 37, 38–44。https://doi.org/10.1038/nbt.4314 — 將 UMAP 應用於單細胞資料的視覺化。
- Kobak, D. & Linderman, G. C. (2021). Initialization is critical for preserving global data structure in both t-SNE and UMAP. *Nature Biotechnology*。https://doi.org/10.1038/s41587-020-00809-z — 依其標題主張，初始化對 t-SNE 與 UMAP 的全域資料結構保留至關重要。
- Sainburg, T., McInnes, L. & Gentner, T. Q. (2021). Parametric UMAP embeddings for representation and semisupervised learning. *Neural Computation*。https://pmc.ncbi.nlm.nih.gov/articles/PMC8516496 — 依其標題，為表示學習與半監督學習而設計的參數化 UMAP 版本。
