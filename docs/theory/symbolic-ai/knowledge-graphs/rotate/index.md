---
status: draft
last_reviewed: 2026-10-28
tags:
  - representation learning
  - knowledge representation
aliases:
  - RotatE
  - 知識圖譜嵌入
  - 關係旋轉
  - Knowledge graph embedding
  - Relational rotation
---

# RotatE

RotatE is a knowledge-graph embedding model. It represents each entity as a complex vector and each relation as an element-wise rotation, so that a true triple $(h, r, t)$ is one in which the head, rotated by the relation, lands on the tail. Sun and colleagues introduced it at ICLR 2019. It is one of the landmark methods in the [knowledge graphs overview](../index.md).

## Overview

Knowledge graphs are incomplete, so a central task is link prediction: which tail entities are plausible for a given head and relation? Embedding methods give each entity and relation a vector and score each triple. The score must respect how relations behave. The paper names three patterns: **symmetry** (if A is married to B, then B is married to A), **inversion** (if A is the parent of B, then B is the child of A) and **composition** (a chain of two relations implies a third).

Earlier models capture only some of these. TransE handles inversion and composition but forces a symmetric relation to a zero translation vector. ComplEx handles asymmetry but cannot infer composition. RotatE is designed to handle all three.[^1] A symbolic system would write these as rules; RotatE encodes them as geometry.

## Key concepts

- **Complex embedding**: each entity is a vector of $k$ complex numbers.
- **Unit-modulus relation**: each element of a relation vector has absolute value 1, so it is a pure phase $e^{i\theta}$. Multiplying by it rotates a complex number without stretching it.
- **Self-adversarial sampling**: negative (false) triples are weighted by how plausible the current model finds them, so training effort goes to hard cases.

## How it works

Here $h, r, t \in \mathbb{C}^k$ and RotatE expects

$$
t_i = h_i\, r_i, \qquad |r_i| = 1.
$$

Each $r_i = e^{i\theta_{r,i}}$ is a counterclockwise rotation by $\theta_{r,i}$ radians. The scoring distance, with $\circ$ the element-wise (Hadamard) product, is

$$
d_r(h, t) = \lVert h \circ r - t \rVert.
$$

The modulus constraint gives the patterns. A relation is symmetric when each element of its vector is $\pm 1$. Two relations are inverses when one vector is the complex conjugate of the other. A relation is the composition of two others when its phases are the sums of theirs. The paper proves these in its appendix.[^1]

Training uses a margin loss over sampled negatives $(h'_i, r, t'_i)$:

$$
L = -\log \sigma\big(\gamma - d_r(h, t)\big) - \sum_{i=1}^{n} p(h'_i, r, t'_i)\,\log \sigma\big(d_r(h'_i, t'_i) - \gamma\big),
$$

where $\gamma$ is a fixed margin and $\sigma$ is the sigmoid. Each negative's weight is a softmax over the current model's scores $f_r = -d_r$, with temperature $\alpha$:

$$
p(h'_j, r, t'_j) = \frac{\exp\big(\alpha\, f_r(h'_j, t'_j)\big)}{\sum_i \exp\big(\alpha\, f_r(h'_i, t'_i)\big)}.
$$

Closer, more plausible negatives receive larger weights. The paper states that the cost of the model stays linear in time and memory.[^1]

## Results

The paper evaluates on four benchmarks: FB15k, WN18, FB15k-237 and WN18RR. Metrics are mean reciprocal rank (MRR) and Hits@N, in the filtered setting.[^2]

On FB15k, RotatE reports an MRR of 0.797 and Hits@10 of 0.884, against 0.692 and 0.840 for ComplEx. On WN18 it reports an MRR of 0.949 and Hits@10 of 0.959.[^2]

The gains are larger on FB15k-237 and WN18RR. There RotatE reports an MRR of 0.338 and Hits@10 of 0.533 on FB15k-237, against 0.325 and 0.501 for ConvE, and an MRR of 0.476 and Hits@10 of 0.571 on WN18RR, against 0.43 and 0.52 for ConvE.[^2] The gap to its phase-only variant, which also constrains entity moduli, is largest on these sets, which the paper reads as evidence that modulus matters for composition.[^2]

## Limitations

- **Triples only.** The model uses no entity types, text or ontology axioms, so it cannot apply schema constraints directly.
- **Uncertainty.** The authors list modelling uncertainty in the graph as future work, so the model does not represent how confident a fact is.[^1]
- **Comparisons.** Some baseline numbers come from other papers, so the comparison mixes training runs.[^2]
- **Tuning.** The margin and sampling temperature were chosen from a grid, and the results depend on that search.[^1]

## Open questions

- Can rotation-based models represent facts with more than two entities, or facts that change over time? Ji and colleagues survey temporal graphs.[^3]
- Does the pattern structure found in learned relations hold for noisy, automatically built graphs?

## References

### Seminal papers

- Sun, Z. et al. (2019). RotatE: Knowledge Graph Embedding by Relational Rotation in Complex Space. *ICLR*. https://arxiv.org/abs/1902.10197 — Models each relation as a rotation in complex space and reports link-prediction results on four benchmarks.
- Yang, B. et al. (2014). Embedding Entities and Relations for Learning and Inference in Knowledge Bases. arXiv. https://arxiv.org/abs/1412.6575 — A simple bilinear model for link prediction, one of the baselines RotatE compares with.
- Trouillon, T. et al. (2016). Complex Embeddings for Simple Link Prediction. arXiv. https://arxiv.org/abs/1606.06357 — Uses complex-valued embeddings to handle symmetric and antisymmetric relations.

### Surveys and textbooks

- Nickel, M. et al. (2015). A Review of Relational Machine Learning for Knowledge Graphs. arXiv. https://arxiv.org/abs/1503.00759 — Reviews latent-feature models for predicting facts in knowledge graphs.
- Ji, S. et al. (2020). A Survey on Knowledge Graphs: Representation, Acquisition and Applications. arXiv. https://arxiv.org/abs/2002.00388 — Surveys knowledge-graph representation learning, completion, temporal graphs and applications.

[^1]: Sun et al. (2019), listed above.
[^2]: Sun et al. (2019), listed above, Tables 4 and 5. Numbers are copied from the tables, whose baseline rows come from other papers.
[^3]: Ji et al. (2020), listed above.
