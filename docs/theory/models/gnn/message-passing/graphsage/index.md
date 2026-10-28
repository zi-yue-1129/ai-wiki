---
related:
- theory/models/gnn/message-passing
- theory/models/gnn
aliases:
  - Graph Sample and Aggregate
  - GraphSAGE
  - 圖採樣與聚合
tags:
  - graph neural networks
  - inductive learning
  - neighbourhood sampling
last_reviewed: 2026-10-28
---

# GraphSAGE

GraphSAGE is an inductive method for learning node embeddings, introduced by Hamilton, Ying and Leskovec in their 2017 paper "Inductive Representation Learning on Large Graphs" ([arXiv:1706.02216](https://arxiv.org/abs/1706.02216)). Rather than learning one embedding vector per node, it learns functions that build a node's representation by sampling and aggregating features from its local neighbourhood, so the same functions can embed nodes that were absent during training.

## Problem

Earlier node-embedding methods are transductive. They learn an embedding for every node seen in training and need all nodes to be present during training, so they do not readily produce embeddings for nodes that arrive later. Aggregating over every neighbour of every node is also expensive on large graphs. The paper addresses both problems: it asks for embeddings of unseen nodes, and for a method that works on graphs too large for full neighbourhoods.

## Core idea

Each node's representation is built layer by layer. At each depth, the node combines its own representation from the previous depth with an aggregate of its sampled neighbours' representations, using learned weights that are shared across all nodes. Because the parameters are functions rather than per-node tables, an unseen node can be embedded by applying the same functions to its features and neighbourhood. Neighbours are drawn as a fixed-size uniform sample, which keeps the cost of each batch fixed whatever the node's degree. The paper notes that the mean aggregator is close to a convolutional layer, and that concatenating the node's own representation acts as a simple skip connection.

## Equation or algorithm

For each depth \(k = 1, \dots, K\), each node \(v\) first aggregates its sampled neighbours, then combines the result with its own previous representation:

\[
h_{\mathcal{N}(v)}^{k} = \mathrm{AGGREGATE}_k\big(\{h_u^{k-1}, \forall u \in \mathcal{S}_{\mathcal{N}(v)}\}\big), \qquad
h_v^{k} = \sigma\big(W^{k} \cdot \mathrm{CONCAT}(h_v^{k-1},\, h_{\mathcal{N}(v)}^{k})\big),
\]

where \(\mathcal{S}_{\mathcal{N}(v)}\) is the fixed-size random sample of neighbours drawn at each iteration. Each \(h_v^{k}\) is then L2-normalised, and the output embedding is \(z_v = h_v^{K}\).

The paper gives these aggregators:

- **Mean:** \(h_v^{k} = \sigma\big(W \cdot \mathrm{MEAN}(\{h_v^{k-1}\} \cup \{h_u^{k-1}, \forall u \in \mathcal{N}(v)\})\big)\), which skips the concatenation step.
- **Pool:** \(\mathrm{AGGREGATE}^{\mathrm{pool}}_k = \max\big(\{\sigma(W_{\mathrm{pool}}\, h_{u_i}^{k-1} + b), \forall u_i \in \mathcal{N}(v)\}\big)\), an element-wise max after a shared fully connected layer.
- **LSTM:** an LSTM applied to a random permutation of the neighbours. The paper gives no equation for it.

For unsupervised training, the paper uses a graph-based loss. A node \(u\) is pulled towards a node \(v\) that co-occurs with it on a short random walk, and pushed away from negative samples:

\[
J_G(z_u) = -\log\big(\sigma(z_u^{\top} z_v)\big) - Q\, \mathbb{E}_{v_n \sim P_n(v)}\big[\log\big(\sigma(-z_u^{\top} z_{v_n})\big)\big],
\]

where \(\sigma\) is the sigmoid, \(P_n\) is a negative-sampling distribution and \(Q\) is the number of negative samples. The supervised variants use cross-entropy loss instead. In the experiments, \(K = 2\), with \(S_1 = 25\) and \(S_2 = 10\) sampled neighbours at the two depths. The sampled cost per batch is \(\prod_i S_i\), and a node's neighbours are sampled with replacement when its degree is below the sample size.

## Results

The paper reports micro-averaged F1 scores. In its Table 1, unsupervised GraphSAGE-pool reaches 0.798 on the citation data, against 0.701 for DeepWalk with features and 0.575 for raw features. On Reddit, the supervised GraphSAGE-LSTM reaches 0.954 and GraphSAGE-mean 0.950, against 0.585 for raw features. On the multi-graph PPI dataset, which tests generalisation to completely unseen graphs, the supervised GraphSAGE-LSTM reaches 0.612 and GraphSAGE-pool 0.600, against 0.422 for raw features. The paper states that unsupervised GraphSAGE-pool beats DeepWalk with features by 13.8% on the citation data and 29.1% on Reddit. No single aggregator wins on every column of the table.

## Limitations

Uniform neighbourhood sampling adds variance, and non-uniform samplers are left for future work. The LSTM aggregator needs a random permutation of neighbours, and the paper reports it as about twice as slow as pooling. Increasing the depth beyond \(K = 2\) gave marginal returns for a large runtime cost. The authors note that their significance tests are weak, since they rest on only six settings. The theoretical results are identifiability arguments, not proofs that the required functions can be learned efficiently, and the dimension they require could be \(O(|V|)\) in the worst case. DeepWalk cannot be applied to the multi-graph PPI setting, which the paper cites as a reason for the comparison's scope.

## Connections

GraphSAGE is a sampled, learned-aggregator member of the [message-passing](../index.md) framework. Its mean aggregator is the inductive counterpart of the full-neighbourhood averaging in [GCN](../gcn/index.md), which is transductive. Its pooling and LSTM aggregators learn their behaviour from data, but they do not weight neighbours by attention as in [GAT](../gat/index.md). The sum-based alternative and its expressivity results are on the [GIN](../gin/index.md) page. The wider family is on the [graph neural networks](../../index.md) page.

## Open issues and further variants

- **Sampling strategy.** Uniform sampling adds variance, and the paper leaves non-uniform samplers for future work. How the sampler should be chosen for a given graph is not settled.
- **Choice of aggregator.** Table 1 shows that no single aggregator wins on every dataset, and this page gives no rule for choosing one. The LSTM is the slowest of the options the paper compares.
- **Depth and sample size.** The paper finds little gain beyond two layers and uses fixed sample sizes of 25 and 10. How these settings transfer to graphs with different degree distributions is not checked here.

## References

### Seminal papers

- Hamilton, W., Ying, Z. & Leskovec, J. (2017). "Inductive Representation Learning on Large Graphs". [arXiv:1706.02216](https://arxiv.org/abs/1706.02216) — GraphSAGE, sampled neighbourhood aggregation for unseen nodes.
- Kipf, T. N. & Welling, M. (2016). "Semi-Supervised Classification with Graph Convolutional Networks". [arXiv:1609.02907](https://arxiv.org/abs/1609.02907) — The GCN layer with symmetric degree normalisation.
- Veličković, P., et al. (2017). "Graph Attention Networks". [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) — Learned attention weights over neighbours, computed from the features of the two endpoints.
- Gilmer, J., et al. (2017). "Neural Message Passing for Quantum Chemistry". [arXiv:1704.01212](https://arxiv.org/abs/1704.01212) — Gives the message-passing framework and shows that several graph models fit it.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Xu, K., et al. (2018). "How Powerful are Graph Neural Networks?". [arXiv:1810.00826](https://arxiv.org/abs/1810.00826) — Shows the expressivity limits of aggregation functions and proposes sum-based GIN.
