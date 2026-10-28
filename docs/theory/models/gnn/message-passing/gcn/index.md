---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Convolutional Networks
  - GCN
  - 圖卷積網路
tags:
  - graph neural networks
  - spectral convolution
  - semi-supervised learning
  - message passing
last_reviewed: 2026-10-28
---

# Graph Convolutional Networks

Graph convolutional networks (GCN) classify the nodes of a graph when only a few of them have labels. The model was introduced by Kipf and Welling (2016). Each layer propagates node features over the adjacency matrix of the graph, so the network is conditioned on the graph's structure. The propagation step adds self-loops and normalises by node degree on both sides.

## Problem

Node classification is hard when labels exist for only a few nodes. Earlier graph methods handled this by adding a Laplacian regulariser, which assumes that connected nodes tend to share labels.

## Core idea

Instead of adding a penalty based on that assumption, the GCN conditions the network on the adjacency matrix. Each layer propagates features over that matrix with self-loops and symmetric degree normalisation. The authors describe the result as a first-order approximation of a localised spectral convolution.

## Equation or algorithm

With Ã = A + I, where I is the identity matrix (so Ã adds self-loops to the adjacency matrix A), and D̃ the diagonal degree matrix of Ã, one layer computes

\[
H^{(l+1)} = \sigma\!\left(\tilde{D}^{-1/2}\,\tilde{A}\,\tilde{D}^{-1/2}\,H^{(l)}\,W^{(l)}\right)
\]

Here H^(l) stacks the node features at layer l, W^(l) is the layer's weight matrix, and σ is a nonlinearity. Each row of the output mixes a node's features with those of its neighbours, weighted by the degrees of both endpoints.

## Results

On Citeseer, Cora, Pubmed and NELL, the paper reports test accuracies of 70.3%, 81.5%, 79.0% and 66.0%, in that order. These were the best results among the methods the paper compares against.

## Limitations

Full-batch training needs memory that grows linearly with the dataset. The model does not support edge features. The best results came from two or three layers, and training deeper models without residual connections becomes difficult beyond about seven layers.

## Connections

GCN is the first-order, spectrally motivated case of the message-passing scheme, with a fixed, degree-weighted sum over neighbours. The general framework is on the [message-passing](../index.md) page, and the wider family is on the [graph neural networks](../../index.md) page. The learned-attention and sum-based alternatives are on the [GAT](../gat/index.md) and [GIN](../gin/index.md) pages.

## Open issues and further variants

- **Edge features.** The layer as defined takes no edge features, while the general message function on the [graph neural networks](../../index.md) page includes an edge term. How to add edge information to the GCN layer is not covered here.
- **Depth.** Results were best at two or three layers, and training deeper stacks without residual connections is hard. This page does not cover how to make deep graph convolutions trainable.
- **Large graphs.** Full-batch training is limited by memory. Neighbour sampling, as in GraphSAGE, is the approach the family page lists for scaling to large graphs.

## References

### Seminal papers

- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". arXiv:1609.02907 — The GCN layer with symmetric degree normalisation.
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". arXiv:1704.01212 — Gives the message-passing framework and shows that several graph models fit it.
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". arXiv:1706.02216 — GraphSAGE, sampled neighbourhood aggregation for unseen nodes.
- Veličković, P., et al. (2017). "Graph Attention Networks". arXiv:1710.10903 — Learned attention weights over neighbours, computed from the features of the two endpoints.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". arXiv:1810.00826 — Shows the expressivity limits of aggregation functions and proposes sum-based GIN.
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". arXiv:1801.07606 — Analyses how repeated graph convolution makes node features converge.
