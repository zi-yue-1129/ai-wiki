---
related:
- theory/models/transformer
aliases:
  - Message Passing
  - Graph Convolution
  - Graph Attention
  - 訊息傳遞
  - 圖卷積
tags:
  - graph neural networks
  - message passing
  - architecture
last_reviewed: 2026-10-28
---

# Message Passing

Most graph neural networks follow one template. Each node holds a feature vector, and in each layer it collects messages from its neighbours, aggregates them, and updates its own vector. Gilmer et al. (2017) gave this template a common name, the message-passing framework, and showed that many earlier graph models were special cases. The variants differ in how messages are formed, how they are aggregated, and how the update treats the node's own state. These choices decide what the network can distinguish, and how deep it can go before its node features blur together.

## Core idea

For node \(v\) at layer \(k\), the update has the form \(h_v^{(k+1)} = \mathrm{UPDATE}\big(h_v^{(k)}, \mathrm{AGGREGATE}\{\mathrm{MESSAGE}(h_v^{(k)}, h_u^{(k)}, e_{uv}) : u \in \mathcal{N}(v)\}\big)\). The message can depend on the edge features \(e_{uv}\), and the aggregation must not depend on the order of the neighbours.

## Approaches

| Variant | Message and aggregation | Key property |
|---|---|---|
| Graph convolution (GCN) | Normalised sum of neighbour features, fixed by degree | Simple, a spectral approximation |
| GraphSAGE | Sampled neighbours, with learned aggregators | Works on large and unseen graphs |
| Graph attention (GAT) | Weights from learned attention over neighbours | Adaptive weighting of neighbours |
| Graph isomorphism network (GIN) | Sum aggregation with an MLP update | Maximally expressive among message-passing models with the same neighbourhood information |

### Normalised convolution

Kipf and Welling (2016) derived a layer that averages neighbour features with symmetric degree normalisation, and motivated it as a first-order approximation of a spectral filter. The layer is cheap and works well on citation graphs, but its fixed weights cannot emphasise particular neighbours.

### Sampling and attention

GraphSAGE samples a fixed number of neighbours and aggregates them with a learned function, which makes training possible on graphs too large for full neighbourhoods, and gives an embedding for nodes not seen in training. Veličković et al. (2017) replaced fixed weights with attention coefficients computed from the features of the two endpoints, so that each node weighs its neighbours by relevance.

### Expressivity

Xu et al. (2018) asked which aggregation functions can distinguish graphs as well as the Weisfeiler–Leman test does. They showed that sum aggregation with an MLP update is as powerful as that test, while mean and max aggregation are not. This result explains why sum-based designs are often preferred for graph classification.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Graph convolutional networks (GCN) | 2016 | Degree-normalised neighbour averaging, a first-order spectral filter | [GCN](gcn/index.md) |
| Graph attention networks (GAT) | 2017 | Learned attention weights over neighbours | [GAT](gat/index.md) |
| Graph isomorphism networks (GIN) | 2018 | Sum aggregation with an MLP update, as expressive as the WL test | [GIN](gin/index.md) |
| GraphSAGE | 2017 | Samples a fixed number of neighbours and aggregates them, so it works on unseen nodes | [GraphSAGE](graphsage/index.md) |

## Trade-offs

- **Expressivity versus cost.** Richer messages and attention cost more memory per edge, while simple normalised sums are cheap but less expressive.
- **Depth.** Stacking many layers lets information spread farther, but repeated averaging makes node features converge, which is the oversmoothing problem.
- **Scale.** Full-neighbourhood aggregation is expensive on dense graphs, so sampling is used on large ones.

## Connections

The message-passing view is the core of the [graph neural network](../index.md) family. Attention over neighbours is the graph counterpart of the [attention variants](../../transformer/attention-variants/index.md) in Transformers, with the graph structure replacing the full token set. The expressivity questions also connect to the theory of [symbolic and relational reasoning](../../../symbolic-ai/index.md).

## Open issues and further variants

- **Oversmoothing.** Li et al. (2018) showed that a few layers of graph convolution already make node features similar on many graphs. Residual connections, normalisation and jumping-knowledge designs reduce the effect, but a complete solution is not known.
- **Long-range interactions.** Message passing needs many layers to connect distant nodes, and that depth causes oversmoothing and congestion, so graph transformers and global attention are used as alternatives.
- **Benchmarks.** Many reported gains are small and depend on dataset splits, which makes fair comparison difficult.

## References

### Seminal papers

- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". arXiv:1704.01212 — Gives the message-passing framework and shows that several graph models fit it.
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". arXiv:1609.02907 — The GCN layer with symmetric degree normalisation.
- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". arXiv:1706.02216 — GraphSAGE, sampled neighbourhood aggregation for unseen nodes.
- Veličković, P., et al. (2017). "Graph Attention Networks". arXiv:1710.10903 — Learned attention weights over neighbours, computed from the features of the two endpoints.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". arXiv:1810.00826 — Shows the expressivity limits of aggregation functions and proposes sum-based GIN.
- Li, Q., Han, Z. & Wu, X.-M. (2018). "Deeper Insights into Graph Convolutional Networks for Semi-Supervised Learning". arXiv:1801.07606 — Analyses how repeated graph convolution makes node features converge.
