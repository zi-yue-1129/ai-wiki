---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
  - theory/paradigms/unsupervised/autoencoders-and-representations
tags:
  - dimensionality reduction
  - linear methods
  - unsupervised learning
aliases:
  - PCA
  - 主成分分析
  - Principal component analysis
---

# PCA: Principal Component Analysis

PCA rotates the data onto orthogonal directions, ordered by how much variance they capture, and keeps the first few. It is the standard linear dimensionality reduction method, and it is the usual first step before more complicated methods. The family-level picture is on the [Dimensionality Reduction](index.md) page.

## Overview

Given data points \(x_1,\dots,x_n\in\mathbb R^d\), PCA finds a set of orthonormal directions \(w_1,\dots,w_k\) such that projecting onto them keeps as much variance as possible. The same directions also give the best linear reconstruction of the data from \(k\) numbers per point, in squared error. These two views are equivalent, and they lead to the same computation: an eigendecomposition of the covariance matrix or a singular value decomposition of the centred data.

## Key concepts

- **Centred data**: the data with the sample mean subtracted. PCA is defined on centred data.
- **Principal components**: the orthonormal directions \(w_j\), ordered by the variance they capture.
- **Loadings and scores**: the components \(w_j\) are the loadings, and the projected coordinates \(z_{ij}=w_j^\top x_i\) are the scores.
- **Explained variance ratio**: the share of total variance captured by the first \(k\) components, \(\sum_{j\le k}\lambda_j / \sum_j \lambda_j\), where \(\lambda_j\) are the covariance eigenvalues in decreasing order.

## How it works

Let \(X\) be the \(n\times d\) matrix of centred data, with sample covariance \(S = \frac{1}{n-1}X^\top X\). The first principal direction maximises the variance of the projection,

\[
w_1 = \arg\max_{\|w\|=1}\ w^\top S\, w,
\]

which is the eigenvector of \(S\) with the largest eigenvalue. The next directions are the eigenvectors with the next largest eigenvalues, each orthogonal to those before it.

Equivalently, take the singular value decomposition \(X = U\Sigma V^\top\). The columns of \(V\) are the principal directions, and the rank-\(k\) reconstruction is \(X_k = U_k\Sigma_k V_k^\top\). This is the best rank-\(k\) approximation of \(X\) in squared Frobenius norm, which is the Eckart–Young theorem ([Eckart & Young, 1936](#references)). Projection to \(k\) dimensions is \(Z = XV_k\).

## Key methods

### On lines and planes of closest fit to systems of points in space (Pearson, 1901)

- **Problem:** fit lines and planes to a system of points in space so that they are closest to the points. The title states this setting.
- **Core idea:** the historical origin of the best-fitting subspace view of PCA. The paper's own formulation is not restated here.

### Analysis of a complex of statistical variables into principal components (Hotelling, 1933)

- **Problem:** analyse a set of statistical variables by recasting them as principal components. The title states this setting.
- **Core idea:** the principal-components formulation used in the sections above.

### Probabilistic principal component analysis (Tipping & Bishop, 1999)

- **Problem:** the abstract notes that PCA is not based on a probability model.
- **Core idea:** the principal axes of a set of observed data vectors can be found by maximum likelihood estimation in a latent-variable model closely related to factor analysis. The paper also gives an EM algorithm for estimating the principal subspace.
- **Results:** this page does not quote numeric results from the paper.
- **Limitations:** this page does not reproduce the paper's likelihood analysis.

## Connections

- The [autoencoder](../autoencoders-and-representations/index.md) page covers nonlinear encoders, for which PCA is the linear baseline.
- Running [k-means](../clustering/k-means.md) on PCA-reduced data is a common practice, because distances in a low-dimensional subspace are often more informative.
- Nonlinear alternatives that also preserve neighbourhoods are [t-SNE](t-sne.md) and [UMAP](umap.md). They are for visualisation, and PCA is often run first. The t-SNE paper, for example, reduces the data to 30 dimensions with PCA before optimisation.

## Open questions

- Variance is not the same as relevance. When is the top-variance direction the one that matters for a task?
- PCA is sensitive to feature scaling and to outliers. How should these be handled in practice?

## References

### Seminal papers

- Pearson, K. (1901). On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://zenodo.org/records/1430636/files/article.pdf — The historical origin of the best-fitting subspace view of PCA. Link is a digitised copy of the article; venue from the article's title and the digitisation record.
- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*, 24. https://www.bohrium.com/paper-details/analysis-of-a-complex-of-statistical-variables-into-principal-components/812082556450111489-11152 — The paper that introduces principal components under that name. Venue and year confirmed by search; the link is an index page, not the publisher's record.
- Tipping, M. E. & Bishop, C. M. (1999). Probabilistic principal component analysis. *Journal of the Royal Statistical Society: Series B*, 61(3), 611–622. https://doi.org/10.1111/1467-9868.00196 — Presents PCA as maximum likelihood in a latent-variable model, with an EM algorithm for the principal subspace.
- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika*, 1(3), 211–218. https://doi.org/10.1007/BF02288367 — The best low-rank approximation theorem used in the SVD formulation above.

### Surveys and textbooks

- Jolliffe, I. T. & Cadima, J. (2016). Principal component analysis: a review and recent developments. *Philosophical Transactions of the Royal Society A*, 374, 20150202. https://doi.org/10.1098/rsta.2015.0202 — A review of PCA and its recent developments.
- Jolliffe, I. T. (2002). *Principal Component Analysis* (2nd ed.). Springer Series in Statistics. https://doi.org/10.1007/b98835 — The standard textbook on PCA.
