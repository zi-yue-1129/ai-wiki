---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/paradigms/unsupervised/clustering
  - theory/paradigms/unsupervised/autoencoders-and-representations
tags:
  - dimensionality reduction
  - visualisation
  - manifold learning
aliases:
  - t 分布隨機鄰域嵌入
  - t-SNE
  - t-distributed stochastic neighbor embedding
---

# t-SNE

t-SNE maps high-dimensional points to two or three dimensions so that nearby points stay nearby, which makes it a widely used tool for drawing structure in datasets. It is a nonlinear method, and its output is for looking at, not for measuring distances. The family-level picture is on the [Dimensionality Reduction](index.md) page.

## Overview

Van der Maaten and Hinton (2008) describe t-SNE as a refinement of stochastic neighbour embedding (SNE, [Hinton & Roweis 2002](#references)). Their abstract says the new method is much easier to optimise and reduces the tendency of points to crowd together in the centre of the map.

## Key concepts

- **Affinity** \(p_{j\mid i}\): the probability that point \(i\) would pick point \(j\) as its neighbour, under a Gaussian centred on \(x_i\) in the original space.
- **Perplexity**: a user-set value that controls the effective number of neighbours. Each point's bandwidth \(\sigma_i\) is found so that its neighbour distribution has this perplexity.
- **Low-dimensional similarity** \(q_{ij}\): the same kind of quantity for the map points, but using a heavy-tailed Student-t kernel with one degree of freedom.
- **Crowding**: in a low-dimensional map, many moderately distant points have nowhere to go. The heavy tail gives them more room, which is the reason for the choice of kernel.

## How it works

The high-dimensional affinities are Gaussian and are symmetrised:

\[
p_{j\mid i} = \frac{\exp(-\|x_i-x_j\|^2/2\sigma_i^2)}{\sum_{k\ne i}\exp(-\|x_i-x_k\|^2/2\sigma_i^2)}, \qquad
p_{ij} = \frac{p_{j\mid i}+p_{i\mid j}}{2n}.
\]

The bandwidth \(\sigma_i\) is set by binary search so that \(\mathrm{Perp}(P_i)=2^{H(P_i)}\) equals the chosen perplexity, where \(H\) is the Shannon entropy in bits.

The map affinities use the Student-t kernel:

\[
q_{ij} = \frac{(1+\|y_i-y_j\|^2)^{-1}}{\sum_{k\ne l}(1+\|y_k-y_l\|^2)^{-1}}.
\]

Training minimises the Kullback–Leibler divergence between the two distributions,

\[
C = \mathrm{KL}(P\,\|\,Q) = \sum_i\sum_{j} p_{ij}\log\frac{p_{ij}}{q_{ij}},
\]

by gradient descent with gradient

\[
\frac{\partial C}{\partial y_i} = 4\sum_j (p_{ij}-q_{ij})(y_i-y_j)\,(1+\|y_i-y_j\|^2)^{-1}.
\]

The paper's optimisation settings for its visualisations are: the \(p_{ij}\) are multiplied by 4 (early exaggeration) for the first 50 iterations; there are 1000 iterations in total; momentum is 0.5 before iteration 250 and 0.8 after; and the data are reduced to 30 dimensions with PCA first.

## Key methods

### Visualizing Data using t-SNE (van der Maaten & Hinton, 2008)

- **Problem:** existing embedding methods, including SNE, had trouble with optimisation and with crowding, so the map often showed overlapping clusters.
- **Core idea:** keep Gaussian affinities in the original space, use a Student-t kernel with one degree of freedom in the map, and minimise the KL divergence between the two.
- **Equation or algorithm:** the affinity, perplexity, KL and gradient equations above, and the optimisation schedule.
- **Results:** on MNIST, under 10-fold cross-validation, the 1-nearest-neighbour error is 5.75% on the original 784-dimensional data. The two-dimensional map from the paper's random-walk variant, built from 6,000 digits with affinities computed over all 60,000, reaches 5.13%.
- **Limitations:** the paper states that the cost function is not convex, so runs can end in different local minima. The paper describes t-SNE as non-parametric and lists a parametric version as future work, which would allow generalisation to held-out data.

## Connections

- Its linear counterpart is [PCA](pca.md), which is often run first to reduce the dimension before t-SNE.
- [UMAP](umap.md) is the most common alternative. It is built on a neighbour graph, and its authors report that it runs faster than t-SNE on large datasets.
- Clusters seen in a t-SNE map should be checked with a method from the [Clustering](../clustering/index.md) page, not read off the map alone.
- Nonlinear encoders that also produce low-dimensional features are covered in [autoencoders and representations](../autoencoders-and-representations/index.md).

## Open questions

- How well does a t-SNE map keep the global geometry of the data, and can that be measured?
- Which choice of perplexity and iteration schedule is robust across datasets?

## References

### Seminal papers

- van der Maaten, L. & Hinton, G. (2008). Visualizing Data using t-SNE. *Journal of Machine Learning Research*, 9, 2579–2605. https://jmlr.org/papers/v9/vandermaaten08a.html — Introduces t-SNE, with the Student-t map kernel and the KL objective. The MNIST figures and optimisation settings above were checked against the PDF.
- Hinton, G. & Roweis, S. (2002). Stochastic Neighbor Embedding. *Advances in Neural Information Processing Systems 15 (NIPS 2002)*. https://papers.nips.cc/paper/2276-stochastic-neighbor-embedding — The SNE method that t-SNE refines.

### Theory

- Linderman, G. C. & Steinerberger, S. (2019). Clustering with t-SNE, provably. arXiv preprint: https://arxiv.org/pdf/1706.02582 — A theoretical analysis of clustering with t-SNE, as the title indicates. The arXiv record was confirmed by search; the journal version (SIAM Journal on Mathematics of Data Science) was not confirmed and is not cited.

### Applications

- Kobak, D. & Berens, P. (2019). The art of using t-SNE for single-cell transcriptomics. *Nature Communications*, 10, 5416. https://doi.org/10.1038/s41467-019-13056-x — Practical guidance on using t-SNE for single-cell transcriptomic data.
- Becht, E. et al. (2019). Dimensionality reduction for visualizing single-cell data using UMAP. *Nature Biotechnology*, 37, 38–44. https://doi.org/10.1038/nbt.4314 — Applies UMAP to visualising single-cell data.
