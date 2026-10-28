---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/gnn
tags:
  - graph neural networks
  - anomaly detection
aliases:
  - CARE-GNN
  - 圖神經網路詐欺偵測
  - 抗偽裝圖神經網路
  - Camouflage-resistant GNN
---

# CARE-GNN (Dou et al. 2020)

CARE-GNN is a graph neural network for fraud detection that learns which neighbours to trust before it aggregates them. It was built for fraudsters who disguise themselves in a network, and it is one of the methods described on the parent page [Insurance and Actuarial Science](../index.md), where claims and claimant networks have a similar structure.

## Overview

Graph neural networks (GNNs) classify a node by combining its own features with those of its neighbours. That helps when fraud is organised, but it hurts when fraudsters link mostly to benign users. Dou and colleagues (2020) describe two kinds of camouflage. In *feature camouflage*, a fraudster's own features look like those of ordinary users. In *relation camouflage*, a fraudster connects to many benign nodes through some relation, so an unfiltered aggregation mostly averages in benign signal.

The paper's experiments use two review-fraud datasets, one from Yelp and one from Amazon, not insurance data. The method is included here because claims and provider networks, in which claimants share addresses, repairers or intermediaries, can be camouflaged in the same way. Using it on claims is an extrapolation, not a result from the paper. For the graph method itself, see [Graph Neural Networks](../../../theory/models/gnn/index.md).

## Key concepts

- **Relation**: a type of edge in a multi-relation graph. In the Yelp graph, two reviews are linked if they are by the same user, for the same product with the same star rating, or for the same product in the same month.
- **Label-aware similarity**: a score that is high when two nodes are predicted to share a label, computed from a learned prediction for each node.
- **Top-$p$ sampling**: keeping only the most similar fraction $p_r$ of a node's neighbours under relation $r$.
- **Adaptive threshold**: $p_r$ is learned during training with reinforcement learning, rather than set by hand.
- **Relation-level aggregation**: neighbourhood information from each relation is combined with weights taken from the learned thresholds.

## How it works

For a node $v$ and a neighbour $v'$ at layer $l$, a one-layer network predicts a label score for each node. The similarity is one minus the $\ell_1$ distance between the two scores:

$$
S^{(l)}(v,v') = 1 - \big\| \sigma\big(\mathrm{MLP}^{(l)}(h_v)\big) - \sigma\big(\mathrm{MLP}^{(l)}(h_{v'})\big) \big\|_1,
$$

where $h_v$ is the node embedding and $\sigma$ is the tanh activation. The method then proceeds in steps.

1. Compute similarity scores between each node and its neighbours under each relation.
2. For each relation $r$, keep the top $p_r$ fraction of neighbours by similarity, and discard the rest.
3. Aggregate the kept neighbours within each relation, then combine the relations, using $p_r$ as the weight of each relation.
4. Update $p_r$ with a reinforcement learning step. The agent is a Bernoulli bandit whose actions raise or lower $p_r$ by a fixed step of 0.02, and whose reward is positive when the newly selected neighbours are more similar than in the previous epoch.
5. Train the classifier with a cross-entropy loss, together with a loss on the similarity measure and an $\ell_2$ penalty.

## Results

The paper evaluates on Yelp and Amazon, with 5% to 40% of nodes used for training. For Yelp at 40% training data, CARE-GNN reaches an AUC of 75.70%, against 52.47% for a GCN baseline and 62.07% for GraphConsis, the strongest non-CARE baseline in that table. On Amazon at the same proportion, CARE-GNN reaches an AUC of 89.73%, against 74.34% for GCN. The authors report that CARE-GNN outperforms the other baselines under most training proportions and metrics. The figures are from Table 3 of the paper.

The paper also compares variants that change only the aggregator across relations, such as attention, learned weights or a plain mean. Their results are similar in most settings. The authors take this as evidence that once the neighbours are filtered, the choice of aggregator matters less. The attention variant is the clear exception on Yelp at 5% training data.

## Limitations

- **Not tested on insurance data.** The datasets are review-fraud graphs. Performance on claims networks, with different relations and label rates, is unknown.
- **Relation design drives results.** The method filters neighbours within relations that the analyst defines. A poor choice of relations limits what the filter can recover.
- **Dependence on labels.** In the paper's table, CARE-GNN's AUC rises as the training share grows from 5% to 40%, and fraud labels are scarce in practice.
- **Adaptive fraudsters.** The camouflages studied are those known when the paper was written. Fraudsters who change tactics may evade the learned filter.
- **Complexity.** Reinforcement learning and similarity learning add tuning and training steps compared with a standard GNN.

## Open questions

- How well do the learned thresholds transfer to claims networks, where the relations are address sharing or common repairers?
- Can the filtering decisions be explained to a claims investigator, so that a flagged claim comes with reasons?
- How should such a detector be audited for disparate impact, given that protected attributes may sit behind graph structure?

## References

### Seminal papers

- Dou, Y. et al. (2020). Enhancing Graph Neural Network-based Fraud Detectors against Camouflaged Fraudsters. *CIKM*. https://arxiv.org/abs/2008.08692 — Introduces CARE-GNN, with label-aware similarity, adaptive top-p filtering and reinforcement-learned thresholds, tested on Yelp and Amazon fraud graphs.
- Kipf, T. N. & Welling, M. (2017). Semi-Supervised Classification with Graph Convolutional Networks. *ICLR*. https://arxiv.org/abs/1609.02907 — Introduces the graph convolutional network, the GCN baseline used in the paper.
- Hamilton, W. L., Ying, R. & Leskovec, J. (2017). Inductive Representation Learning on Large Graphs. *NeurIPS*. https://arxiv.org/abs/1706.02216 — Introduces GraphSAGE, a neighbourhood-sampling GNN that is one of the baselines in the paper's comparison.

### Surveys and textbooks

- Bolton, R. J. & Hand, D. J. (2002). Statistical Fraud Detection: A Review. *Statistical Science*. https://doi.org/10.1214/ss/1042727940 — Review of statistical tools for detecting fraud, including the network and relational ideas that graph methods extend.
