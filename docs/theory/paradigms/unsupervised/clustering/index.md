---
tags:
  - unsupervised learning
  - clustering
---

# Clustering

Clustering partitions unlabelled data into groups whose members are more similar to each other than to other groups. It is one of the oldest and most used unsupervised tools, and it is also one of the easiest to misuse.

## Overview

Given points $x_1,\dots,x_n$, a clustering assigns each point to a group. Nothing in the data says how many groups there are or what "similar" means, so every method embeds an assumption about cluster shape, density or connectivity. Choosing that assumption matters more than the choice of algorithm.

## Main methods

| Method | Assumed cluster shape | Needs $k$? | Cost |
|---|---|---|---|
| k-means | Roughly spherical, similar size | Yes | $O(nkd)$ per iteration |
| Gaussian mixtures (EM) | Ellipsoidal, soft assignment | Yes | Similar, with covariance terms |
| Hierarchical (agglomerative) | Any, depends on linkage | No (cut the tree) | $O(n^2)$ or more |
| DBSCAN / HDBSCAN | Arbitrary, separated by low-density gaps | No | Near $O(n\log n)$ with indexes |
| Spectral clustering | Any, found through a graph | Yes | Eigendecomposition of an $n\times n$ matrix |

## How they work

**k-means** alternates two steps: assign each point to its nearest centre, then move each centre to the mean of its points. It minimises the within-cluster sum of squares and always converges, but only to a local optimum. The usual remedy is many random restarts or k-means++ seeding.

**Gaussian mixtures** model the data as a weighted sum of Gaussians and fit them with expectation–maximisation. Each point gets a probability of belonging to each cluster, which gives soft assignments and a full density model (see [density estimation](../density-and-generative-models/index.md)).

**DBSCAN** defines clusters as regions of high density that are connected through "core" points. It finds clusters of any shape and labels sparse points as noise, which is useful when the number of clusters is unknown. HDBSCAN removes the need to pick a distance threshold.

**Spectral clustering** builds a similarity graph, takes the eigenvectors of its Laplacian, and clusters the rows of that embedding with k-means. It can separate intertwined shapes that k-means cannot.

## Evaluating clusters

Without labels, quality is judged indirectly: internal scores such as the silhouette coefficient measure compactness against separation, while external scores such as the adjusted Rand index compare against known labels when they exist. Stability under resampling and the usefulness of the clusters for a downstream task are often more informative.

## Connections

Clusters can be seen as discrete latent variables in a mixture model, linking clustering to [probabilistic methods](../../probabilistic/index.md). Dimensionality reduction is often applied first to make distances meaningful, see [dimensionality reduction](../dimensionality-reduction/index.md). Topic models such as latent Dirichlet allocation cluster words and documents jointly.

## Applications

Customer segmentation, grouping single cells by gene expression, community detection in social and citation networks, and organising image or document collections. Biology is a major user: single-cell clustering is a standard step in atlas projects.

## Open questions

How many clusters are there? Is a "true" clustering even defined? Clustering in high dimensions suffers from distance concentration, and results can change with small preprocessing choices. Evaluation without ground truth remains the central difficulty.

## References

### Seminal papers

- Lloyd (1982), "Least squares quantization in PCM", *IEEE Transactions on Information Theory* 28(2). https://www.stat.cmu.edu/~rnugent/PCMI2016/papers/LloydKMeans.pdf — The original least-squares quantisation paper behind the k-means algorithm.
- Fraley & Raftery (2002), "Model-based clustering, discriminant analysis, and density estimation", *JASA* 97(458). https://sites.stat.washington.edu/raftery/Research/PDF/fraley2002.pdf — Defines Gaussian mixture clustering and the model-selection criterion used in the mclust software.
- Ester, Kriegel, Sander & Xu (1996), "A density-based algorithm for discovering clusters in large spatial databases with noise", KDD. https://webdocs.cs.ualberta.ca/~zaiane/courses/cmput695-00/papers/00153.pdf — Introduces DBSCAN, which finds arbitrarily shaped clusters and marks noise.
- Ng, Jordan & Weiss (2001), "On spectral clustering: analysis and an algorithm", NeurIPS. https://papers.nips.cc/paper/2092-on-spectral-clustering-analysis-and-an-algorithm — Gives the standard spectral clustering algorithm and its analysis.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

- Lloyd, S. P. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory*, 28(2), 129–137. https://www.stat.cmu.edu/~rnugent/PCMI2016/papers/LloydKMeans.pdf — Presents the iterative least-squares quantisation method that underlies the k-means algorithm.

### Articles and documentation

(none beyond the entries above)

## Further learning

- StatQuest with Josh Starmer, episodes on k-means clustering and hierarchical clustering, YouTube. https://www.youtube.com/@statquest — Visual, step-by-step walkthroughs of how k-means and hierarchical methods build clusters.

## Further reading

- Jain (2010), "Data clustering: 50 years beyond k-means", *Pattern Recognition Letters* 31. https://doi.org/10.1016/j.patrec.2009.09.011 — A survey of clustering methods from k-means onward.
- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, chapter 14. https://doi.org/10.1007/978-0-387-84858-7
