---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Attention Networks
  - GAT
  - 圖注意力網路
tags:
  - graph neural networks
  - attention
  - message passing
last_reviewed: 2026-10-28
---

# Graph Attention Networks

Graph attention networks (GAT) let each node weigh its neighbours by learned attention. The model was introduced by Veličković et al. (2017). Unlike the fixed, degree-based normalisation of GCN, the attention coefficients are computed from the features of the two endpoints of each edge.

## Problem

Spectral filters depend on the graph's Laplacian. A model trained on one graph structure therefore cannot be applied directly to another structure, and the filters are not spatially localised.

## Core idea

Each node attends over its neighbours. The attention coefficients come from a shared linear transform of the node features, normalised with a softmax over the neighbourhood. Several attention heads run in parallel, and their outputs are concatenated in hidden layers.

### Animated walkthrough

![Four-stage GAT animation showing edge scores, neighborhood softmax, weighted messages, and the updated target node.](../../../../../assets/concept-animations/gat-aggregation-motion.svg)

*Original CC BY-SA 4.0 teaching animation based on Veličković et al. (2017; see References). It visualizes a **single attention head**, not multi-head concatenation. On MkDocs, the **Play/Pause** control is keyboard accessible; reduced-motion preferences initially select the [GitHub-readable static overview](../../../../../assets/concept-animations/gat-aggregation-still.svg). [Open the animated SVG](../../../../../assets/concept-animations/gat-aggregation-motion.svg).*

The diagram uses the **same four-node star and scalar features as the GCN walkthrough**: $h_i=0.5,\ h_A=1,\ h_B=1.5,\ h_C=2$, including the self-loop in the target's neighborhood. To make the arithmetic reproducible, take $W=1$ and one illustrative shared additive scorer $e_{ij}=\operatorname{LeakyReLU}(h_j-h_i)$. All four scores are nonnegative, so the logits are $(0,0.5,1,1.5)$. Neighborhood softmax gives coefficients approximately $(0.1015,0.1674,0.2760,0.4551)$ for $(i,A,B,C)$; their weighted feature sum is $1.5423$ with an identity output activation. These coefficients sum to one, unlike the degree-normalized GCN weights. The scorer, scalar features, and output are **constructed teaching values**, not parameters or activations measured from a trained GAT.

## Equation or algorithm

For a node i and its neighbours j, the layer computes

\[
e_{ij} = a(\mathbf{W}\vec{h}_i,\; \mathbf{W}\vec{h}_j), \qquad
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k\in\mathcal{N}_i}\exp(e_{ik})}, \qquad
\vec{h}'_i = \sigma\!\Big(\sum_{j\in\mathcal{N}_i}\alpha_{ij}\,\mathbf{W}\vec{h}_j\Big)
\]

Here e_ij is the attention score between nodes i and j, a is a shared attention function, W is a shared linear transform, N_i is the neighbourhood of node i, and σ is a nonlinearity.

## Results

On Cora in the transductive setting, the paper reports test accuracy of 83.0% ± 0.7% (GCN 81.5%). On Citeseer it reports 72.5% ± 0.7% (GCN 70.3%). On Pubmed it matched GCN at 79.0%. On the inductive PPI dataset the micro-F1 was 0.973, against 0.768 for GraphSAGE in the comparison table that the paper reports.

## Limitations

The sparse implementation supports only rank-2 tensors, which limits batching across graphs. The receptive field is bounded by depth. Multi-head attention multiplies the parameter count by the number of heads.

## Connections

GAT is the learned-attention case of the message-passing scheme: its aggregation weights are computed from the features rather than fixed by the graph. The general framework is on the [message-passing](../index.md) page, and the wider family is on the [graph neural networks](../../index.md) page. The fixed-weight and sum-based alternatives are on the [GCN](../gcn/index.md) and [GIN](../gin/index.md) pages.

## Open issues and further variants

- **Batching across graphs.** The rank-2 limit of the sparse implementation restricts batching across graphs. This page does not describe a remedy.
- **Attention versus sum aggregation.** The softmax makes each layer a weighted average of neighbour messages. Its expressive power relative to sum aggregation is not established on this page. For reference, the [GIN](../gin/index.md) page gives the paper's mean-aggregation result of 50.0 on REDDIT-BINARY.
- **Head count.** Multi-head attention multiplies the parameter count, and this page gives no rule for choosing the number of heads.

## References

### Seminal papers

- Veličković, P., et al. (2017). "Graph Attention Networks". [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) — Learned attention weights over neighbours, computed from the features of the two endpoints.
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — The GCN layer with symmetric degree normalisation.
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — Gives the message-passing framework and shows that several graph models fit it.
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) — GraphSAGE, sampled neighbourhood aggregation for unseen nodes.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". [arXiv:1810.00826](https://arxiv.org/abs/1810.00826) — Shows the expressivity limits of aggregation functions and proposes sum-based GIN.
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". [arXiv:1801.07606](https://arxiv.org/abs/1801.07606) — Analyses how repeated graph convolution makes node features converge.
