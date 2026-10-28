---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Isomorphism Networks
  - GIN
  - 圖同構網路
tags:
  - graph neural networks
  - expressivity
  - message passing
  - graph isomorphism
last_reviewed: 2026-10-28
---

# Graph Isomorphism Networks

Graph isomorphism networks (GIN) are a message-passing design built to match the discriminative power of the Weisfeiler–Lehman (WL) graph isomorphism test. The model was introduced by Xu et al. (2018), who also showed the limits of aggregation-based GNNs.

## Problem

Which aggregation schemes give a GNN the discriminative power of the Weisfeiler–Lehman (WL) isomorphism test? The paper's first result is that any aggregation-based GNN is at most as powerful as that test.

## Core idea

A maximally powerful GNN must map different neighbourhoods to different representations, which requires an injective aggregation. Sum aggregation can represent injective functions over multisets, while mean and max cannot in general.

## Equation or algorithm

Each layer updates a node by summing its own feature, scaled by (1 + ε), with its neighbours' features, and passing the result through an MLP:

\[
h_v^{(k)} = \text{MLP}^{(k)}\!\Big((1+\epsilon^{(k)})\cdot h_v^{(k-1)} + \sum_{u\in\mathcal{N}(v)} h_u^{(k-1)}\Big)
\]

GIN-0 is the variant that fixes ε = 0.

## Results

On the benchmarks REDDIT-BINARY, COLLAB, MUTAG and NCI1, GIN-0 reached 92.4 ± 2.5, 80.2 ± 1.9, 89.4 ± 5.6 and 82.7 ± 1.7, respectively. The mean-aggregation variant scored 50.0 on REDDIT-BINARY, which the paper ties to mean aggregators failing to capture structure.

## Limitations

The theory assumes countable input features, and it does not address generalisation. Aggregation-based GNNs remain bounded by the WL test, and the authors name going beyond neighbourhood aggregation as future work.

## Connections

GIN is the sum-aggregation case of the message-passing scheme. The [message-passing](../index.md) page covers the expressivity of sum-based aggregation, and the [graph neural networks](../../index.md) page lists expressivity limits among its known issues. The normalised and attention-weighted aggregators are on the [GCN](../gcn/index.md) and [GAT](../gat/index.md) pages.

## Open issues and further variants

- **Beyond the WL bound.** The paper names going beyond neighbourhood aggregation as future work. This page does not describe such methods.
- **Generalisation.** The theory does not address generalisation, so the proof here does not explain the benchmark results.
- **Continuous features.** The theory assumes countable input features. How the analysis carries over to continuous inputs is not covered here.

## References

### Seminal papers

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". [arXiv:1810.00826](https://arxiv.org/abs/1810.00826) — Shows the expressivity limits of aggregation functions and proposes sum-based GIN.
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — The GCN layer with symmetric degree normalisation.
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — Gives the message-passing framework and shows that several graph models fit it.
- Veličković, P., et al. (2017). "Graph Attention Networks". [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) — Learned attention weights over neighbours, computed from the features of the two endpoints.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) — GraphSAGE, sampled neighbourhood aggregation for unseen nodes.
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". [arXiv:1801.07606](https://arxiv.org/abs/1801.07606) — Analyses how repeated graph convolution makes node features converge.
