---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/knowledge-graphs
tags:
  - knowledge graphs
  - embeddings
  - link prediction
aliases:
  - TransE
  - Translating embeddings
  - 翻譯嵌入
---

# TransE

TransE is a knowledge graph embedding model that represents each relation as a translation vector. A triple (h, r, t) is plausible when the head embedding plus the relation embedding lands near the tail embedding. Part of [Knowledge graphs and knowledge representation](index.md).

## Overview

Knowledge graphs are incomplete, and the missing facts are predicted from the rest of the graph. TransE treats this as learning vectors. Every entity and relation gets a point in a vector space, and a triple is scored by how well the relation acts as a shift from the head to the tail. The model is simple, has few parameters, and scales to large graphs (Bordes et al., 2013).

## Key concepts

- **Embedding**: a learned vector for each entity and each relation.
- **Translation**: the idea that a relation moves the head vector to the tail vector, \(\mathbf{h}+\mathbf{r}\approx\mathbf{t}\).
- **Corrupted triple**: a negative example made by replacing the head or tail of a true triple with a random entity.
- **Link prediction**: ranking candidate tails for a given head and relation, or the reverse, and measuring the rank of the true entity.

## How it works

For a triple \((h,r,t)\), the score is the distance \(d(\mathbf{h}+\mathbf{r},\mathbf{t})\), usually the L1 or L2 norm. Training minimises a margin-based ranking loss,

\[
\mathcal{L}=\sum_{(h,r,t)\in S}\sum_{(h',r,t')\in S'}\big[\gamma+d(\mathbf{h}+\mathbf{r},\mathbf{t})-d(\mathbf{h}'+\mathbf{r},\mathbf{t}')\big]_+,
\]

where \(S\) contains true triples, \(S'\) contains corrupted triples, \(\gamma\) is a margin and \([x]_+=\max(0,x)\). Embeddings are normalised during training, and the loss pushes true triples to score closer than corrupted ones by at least \(\gamma\).

## Variants

- **Relation-specific projections** give each relation its own space, so that one entity can have different representations under different relations.
- **Complex-valued and rotational relations** address TransE's weakness on asymmetric relations (Trouillon et al., 2016).

## Results and limits

- TransE is competitive on standard link-prediction benchmarks, and it is fast to train (Bordes et al., 2013).
- It cannot represent symmetric relations well, because \(\mathbf{h}+\mathbf{r}\approx\mathbf{t}\) and \(\mathbf{t}+\mathbf{r}\approx\mathbf{h}\) together force \(\mathbf{r}\approx\mathbf{0}\).
- For one-to-many and many-to-many relations, distinct tails for the same head and relation are pushed toward the same point, which hurts ranking. The 2013 paper analyses these relation types.
- The model is a single translation, so it cannot capture composition or hierarchy without extension.

## Applications

- **Completing knowledge graphs**: predicting missing facts for large public and enterprise graphs.
- **Question answering**: retrieving entities that match a query by vector arithmetic.
- **Recommendation**: scoring user–item links in graphs that include relation types.

## Open questions

- Whether translation is the right inductive bias for many relation types is unsettled, and richer models have not uniformly beaten it.
- Evaluation depends on benchmark splits that leak inverse relations, so reported gains need careful checking.

## References

### Seminal papers

- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — Introduces TransE, its margin-based training and the analysis of relation types.
- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — Models asymmetric relations, which TransE handles poorly.

### Surveys and textbooks

- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — Reviews translation and other relational embedding models.
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — Surveys TransE and its extensions across knowledge graph tasks.
- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — Places embedding models within knowledge graph research.
