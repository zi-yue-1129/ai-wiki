---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - theory/paradigms/symbolic-ai/neuro-symbolic
tags:
  - knowledge graphs
  - knowledge representation
  - symbolic AI
aliases:
  - 知識圖譜
  - 知識表示
  - Knowledge graphs
  - Knowledge representation
  - Link prediction
---

# Knowledge Graphs and Knowledge Representation

A knowledge graph stores facts as a graph of entities connected by labelled relations, usually as triples of the form (subject, relation, object). Knowledge representation studies how such facts and their meanings are written down so that machines can use them. Part of [Symbolic AI, search and planning](../index.md).

## Overview

Symbolic AI represented knowledge as rules and logic, which are precise but hard to build and maintain at scale. Knowledge graphs take a more data-oriented route. They store many simple facts, often extracted from text and databases, and attach an ontology that says what kinds of entities and relations are allowed. Large public graphs, such as those behind search engine answer panels, are built this way.

## Key concepts

- **Triple**: a fact such as (Paris, capital of, France). A graph is the set of triples over a shared vocabulary.
- **Ontology or schema**: the classes of entities and the relations between them, with constraints such as domains and ranges.
- **Description logics**: decidable fragments of first-order logic that underlie web ontology languages. They balance expressiveness and reasoning cost (Hogan et al., 2021).
- **Knowledge graph completion**: predicting missing triples from the existing graph, usually called link prediction.

## How it works

A knowledge graph can be used in two ways. Symbolic use queries and reasons over the explicit facts and the ontology, for instance by inferring that a subclass inherits the properties of its parent. Statistical use turns entities and relations into vectors and scores candidate triples. The second approach is the basis of [knowledge graph embeddings](transe.md), a family of methods that predict missing links from learned representations (Nickel et al., 2016).

## Key methods

- [TransE](transe.md): represents relations as translations between entity embeddings, so that a true triple satisfies head plus relation is close to tail (Bordes et al., 2013).

Other embedding models use different score functions, for example complex-valued scores (Trouillon et al., 2016), and are summarised in the surveys (Wang et al., 2017; Nickel et al., 2016).

## Connections

- [Symbolic AI, search and planning](../index.md) places knowledge representation next to search, planning and theorem proving.
- [Neuro-symbolic AI](../neuro-symbolic/index.md) combines knowledge graphs or logical rules with neural learning.
- [Probability and statistics](../../../math/probability-statistics/index.md) gives the probabilistic view of uncertain facts that some knowledge graphs use.

## Applications

- **Search and question answering**: answer panels that give facts about an entity directly from a graph.
- **Recommendation**: graphs that link users, items and attributes to explain and rank suggestions.
- **Biomedicine**: graphs of genes, drugs and diseases used to propose new hypotheses for study.

## Open questions

- Knowledge graphs are incomplete, and the closed-world and open-world assumptions give different answers to missing facts.
- Embedding methods are evaluated mainly by link prediction on a few benchmarks, and better evaluation of the facts they predict is needed.
- Combining learned representations with logical constraints so that predictions respect the ontology remains difficult.

## References

### Seminal papers

- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — Introduces TransE for knowledge graph embedding.
- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — Uses complex-valued embeddings to model asymmetric relations.

### Surveys and textbooks

- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — Broad survey of knowledge graph models, ontologies and reasoning.
- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — Reviews statistical methods for predicting links in knowledge graphs.
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — Surveys embedding methods and their applications.
