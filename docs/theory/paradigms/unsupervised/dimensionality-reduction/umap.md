---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
tags:
  - dimensionality reduction
  - visualisation
  - manifold learning
aliases:
  - UMAP
  - 均勻流形近似與投影
  - Uniform Manifold Approximation and Projection
---

# UMAP

UMAP is a nonlinear dimensionality reduction method that builds a weighted neighbour graph on the data and then lays out a low-dimensional copy of that graph. Its authors compare it with t-SNE on run time and on how well global structure is kept, while giving similar visualisations. The family-level picture is on the [Dimensionality Reduction](index.md) page.

## Overview

McInnes, Healy and Melville (2018) motivate UMAP with a theory from Riemannian geometry and algebraic topology. In practice the method reduces to three steps: estimate local distances from the \(k\) nearest neighbours of each point, turn them into fuzzy edge weights, and then optimise a low-dimensional layout whose edge weights match the high-dimensional ones. The abstract describes the result as visualisation quality competitive with t-SNE, which the authors say arguably preserves more of the global structure, with superior run time performance.

## Key concepts

- **Local connectivity** \(\rho_i\): the distance from point \(i\) to its nearest neighbour. Each point is connected to at least one neighbour with weight 1.
- **Fuzzy weight**: an edge weight between 0 and 1, which decays with distance beyond \(\rho_i\). It is the membership strength of an edge in a fuzzy simplicial set.
- **Minimum distance** (`min_dist`): a parameter that sets how tightly points may pack in the map.
- **Nearest-neighbour descent**: the approximate \(k\)-nearest-neighbour method UMAP uses to build its graph, which the paper reports as roughly \(O(N^{1.14})\) empirically.

## How it works

For each point \(x_i\), let \(x_{i1},\dots,x_{ik}\) be its \(k\) nearest neighbours. Its directed weights are

\[
w_{j\mid i} = \exp\!\Big(-\frac{\max(0,\ d(x_i,x_{ij})-\rho_i)}{\sigma_i}\Big),
\]

where \(\sigma_i\) is found by binary search so that the weights sum to a fixed target. The directed weights are merged into a symmetric weight with the fuzzy union

\[
v_{ij} = v_{j\mid i} + v_{i\mid j} - v_{j\mid i}\,v_{i\mid j}.
\]

In the low-dimensional map the weights take the form

\[
w_{ij} = \big(1+a\,\|y_i-y_j\|^{2b}\big)^{-1},
\]

where \(a\) and \(b\) are fitted by nonlinear least squares to a target curve set by `min_dist`. The paper reports \(a \approx 1.929\) and \(b \approx 0.7915\) for the default values in the UMAP implementation. Setting \(a=b=1\) gives the Student-t kernel that t-SNE uses. The layout is found by minimising the cross-entropy between the two weighted graphs,

\[
C = \sum_{i\ne j}\Big[v_{ij}\log\frac{v_{ij}}{w_{ij}} + (1-v_{ij})\log\frac{1-v_{ij}}{1-w_{ij}}\Big].
\]

The attractive terms pull connected points together, and the repulsive terms push unconnected points apart.

## Key methods

### UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction (McInnes, Healy & Melville, 2018)

- **Problem:** the authors compare UMAP with t-SNE and look for a method that is practical on large real datasets, with visualisation quality comparable to t-SNE and better preservation of global structure.
- **Core idea:** build a fuzzy neighbour graph in the original space, then find a low-dimensional layout whose graph is as close to it as possible, measured by cross-entropy.
- **Equation or algorithm:** the fuzzy weights, the symmetrisation, the low-dimensional curve \(w_{ij}\), and the cross-entropy loss given above.
- **Results:** in the paper's runtime table (Table 3 of the arXiv v3 version), UMAP takes 87 seconds on MNIST (70,000 × 784), against 1450 seconds for t-SNE (MulticoreTSNE) and 292 seconds for FIt-SNE. On Pen Digits (1,797 × 64), UMAP takes 9 seconds, against 17 seconds for t-SNE, 2 seconds for Laplacian Eigenmaps and 2 seconds for Isomap. The paper says that its UMAP timings are for a single-core version, while FIt-SNE uses multiple cores, so the timings are not on equal footing.
- **Limitations:** Table 3 shows that some classical methods are faster on small data, as the Pen Digits result shows. The complexity figure is empirical, and the paper notes that no theoretical complexity bounds have been established for nearest-neighbour descent. Results depend on the number of neighbours and on `min_dist`.

## Connections

- Its main comparison method is [t-SNE](t-sne.md), which uses the same Student-t kernel with \(a=b=1\).
- Its graph-based idea links to the spectral view of [clustering](../clustering/index.md), where similarity graphs are also central.
- The linear baseline [PCA](pca.md) can be run before UMAP to reduce high-dimensional inputs first.

## Open questions

- How much of the claimed preservation of global structure holds up across datasets, and how should it be measured? Kobak & Linderman (2021) argue that initialisation is critical for global structure in both t-SNE and UMAP.
- How sensitive is the layout to the choice of neighbour count and `min_dist`?

## References

### Seminal papers

- McInnes, L., Healy, J. & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv preprint. https://arxiv.org/abs/1802.03426 — Introduces UMAP, with its fuzzy-graph construction and cross-entropy layout objective. The runtime table and the fitted a and b values above were checked against the arXiv v3 PDF.
- McInnes, L., Healy, J. & Melville, J. (2018). UMAP: Uniform Manifold Approximation and Projection. *Journal of Open Source Software*. https://joss.theoj.org/papers/10.21105/joss.00861 — The software paper for the UMAP implementation.

### Applications and comparisons

- Becht, E. et al. (2019). Dimensionality reduction for visualizing single-cell data using UMAP. *Nature Biotechnology*, 37, 38–44. https://doi.org/10.1038/nbt.4314 — Applies UMAP to visualising single-cell data.
- Kobak, D. & Linderman, G. C. (2021). Initialization is critical for preserving global data structure in both t-SNE and UMAP. *Nature Biotechnology*. https://doi.org/10.1038/s41587-020-00809-z — Argues, per its title, that initialisation is critical for preserving global data structure in t-SNE and UMAP.
- Sainburg, T., McInnes, L. & Gentner, T. Q. (2021). Parametric UMAP embeddings for representation and semisupervised learning. *Neural Computation*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8516496 — A parametric version of UMAP for representation and semi-supervised learning, per its title.
