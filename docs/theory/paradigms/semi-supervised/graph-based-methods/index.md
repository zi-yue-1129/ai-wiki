---
tags:
  - semi-supervised learning
  - graphs
  - label propagation
---

# Graph-Based Semi-Supervised Learning

Graph-based methods connect similar examples with weighted edges and spread labels from the labelled nodes across the graph. They are natural when the data have a relational structure, and they make the manifold assumption explicit.

## Overview

Build a graph whose nodes are examples and whose edge weights measure similarity, often from a k-nearest-neighbour graph. Labels are then propagated so that connected nodes receive similar labels. The solution is found by solving a linear system involving the graph Laplacian.

## Main methods

- **Label propagation and harmonic functions** (Zhu, Ghahramani & Lafferty, 2003) fix the labelled nodes and compute, for each unlabelled node, the harmonic function that averages its neighbours. The solution is unique and can be found in closed form.
- **Local and global consistency** (Zhou et al., 2004) balances fitting the known labels with smoothness over the graph, using a normalised Laplacian.
- **Manifold regularisation** (Belkin, Niyogi & Sindhwani, 2006) adds a penalty on a function's variation along the data manifold to a standard kernel learner, so the method works for new points as well.
- **Graph neural networks** such as the graph convolutional network (Kipf & Welling, 2017) learn node features with neighbour aggregation and train on few labels, now a standard setting for citation and molecule graphs. See [graph neural networks](../../../models/gnn/index.md).

## Assumptions

Graph methods assume that nodes connected by strong edges share labels, and that the graph captures the true structure. Both can fail. Noisy or badly chosen similarity measures create misleading edges, and high-dimensional data often produce graphs whose neighbours are not semantically close.

## Connections

Manifold regularisation is a kernel method, see [kernel methods](../../supervised/kernel-methods-svm/index.md). The smoothness assumption matches the one behind [consistency regularisation](../consistency-regularisation/index.md). Graphs built from learned embeddings tie this to [self-supervised representations](../../self-supervised/index.md).

## Applications

Classifying documents in citation networks, predicting protein function from interaction graphs, semi-supervised image labelling on nearest-neighbour graphs, and node classification in social networks.

## Open questions

Scaling graph construction and propagation to millions of points, learning the similarity measure rather than fixing it, and handling graphs whose structure changes over time remain active problems.

## References

### Seminal papers

- Zhu, Ghahramani & Lafferty (2003), "Semi-supervised learning using Gaussian fields and harmonic functions", ICML. https://www.cs.cmu.edu/~zhuxj/pub/zgl.pdf — Label propagation through harmonic functions on a graph, with a closed-form solution.
- Zhou, Bousquet, Lal, Weston & Schölkopf (2004), "Learning with local and global consistency", NeurIPS. https://papers.nips.cc/paper/2506-learning-with-local-and-global-consistency — Balances fitting known labels with graph smoothness.
- Belkin, Niyogi & Sindhwani (2006), "Manifold regularization: a geometric framework for learning from labeled and unlabeled examples", *JMLR* 7. https://www.jmlr.org/papers/v7/belkin06a.html — Adds manifold smoothness to kernel learners, so they generalise to new points.
- Singh, Nowak & Zhu (2008), "Unlabeled data: now it helps, now it doesn't", NeurIPS. https://proceedings.neurips.cc/paper/2008/hash/07871915a8107172b3b5dc15a6574ad3-Abstract.html — Shows when smoothing over a graph with unlabelled data helps and when it hurts.
- Kipf & Welling (2017), "Semi-supervised classification with graph convolutional networks", ICLR, [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — Graph convolutions that train on few labels, the standard graph semi-supervised model.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

- Chapelle, Schölkopf & Zien (eds.), *Semi-Supervised Learning*, MIT Press (2006), chapter on graph methods. https://doi.org/10.7551/mitpress/9780262033589.001.0001 — The standard volume; this link is to the whole book, not to the chapter.
