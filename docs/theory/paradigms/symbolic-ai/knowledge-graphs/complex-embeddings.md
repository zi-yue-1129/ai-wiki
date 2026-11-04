---
last_reviewed: 2026-11-04
related:
  - theory/paradigms/symbolic-ai/knowledge-graphs
tags:
  - knowledge graphs
  - embeddings
  - link prediction
aliases:
  - ComplEx
  - Complex embeddings
  - 複數嵌入
  - 複數值嵌入
---

# ComplEx (Complex Embeddings)

ComplEx is a knowledge graph embedding model that represents entities and relations as complex-valued vectors and scores a triple with a Hermitian product. Its main purpose is to model asymmetric relations, which the translation-based [TransE](transe.md) handles poorly. Part of [Knowledge graphs and knowledge representation](index.md).

## Overview

Link prediction ranks candidate entities for the missing slot of a triple, as in the TransE setting (Bordes et al., 2013). Many early embedding models score a triple with a real-valued bilinear product. For such models the score of (h, r, t) and of (t, r, h) are often the same, so they cannot represent an asymmetric relation such as "is parent of" without extra machinery. Trouillon et al. (2016) observed that complex numbers solve this at little extra cost: a relation whose embedding has a non-zero imaginary part gives different scores in the two directions.

## Key concepts

- **Complex embedding**: each entity and relation is a vector of complex numbers, with real and imaginary parts learned from the data.
- **Hermitian product**: the sum of the products of one head entry, one relation entry and the conjugate of one tail entry. Its real part is the score.
- **Asymmetry**: a relation is asymmetric when (h, r, t) can hold while (t, r, h) does not. The model needs a non-real relation vector to express this.
- **Regularised logistic loss**: training pushes true triples above corrupted ones, with an L2 penalty on the embeddings.

## How it works

For a triple (h, r, t), with complex vectors in $\mathbb{C}^k$, ComplEx uses the score

\[
\phi(h,r,t)=\operatorname{Re}\Big(\sum_{i=1}^{k} h_i\, r_i\, \overline{t_i}\Big),
\]

where $\overline{t_i}$ is the complex conjugate of $t_i$. Writing $r = r_R + i\,r_I$, the score is a sum of real terms in which $r_I$ multiplies cross-products of the head and tail parts. When $r$ is real, the score is symmetric in $h$ and $t$. When $r$ has a non-zero imaginary part, swapping head and tail changes the score, so the model can represent asymmetry.

Training follows the usual pattern for embedding models. True triples are paired with corrupted ones, obtained by replacing the head or the tail. The model is fitted with a logistic loss and an L2 regulariser, using gradient-based optimisation (Trouillon et al., 2016). Because the score is bilinear in the embeddings, its gradients are simple to compute.

## Key methods

- [TransE](transe.md): a translation model that is simple and fast, but whose score for a symmetric relation forces the relation vector toward zero. ComplEx keeps the same goal and changes the score to a complex product.
- Other embedding models with different score functions are surveyed in Wang et al. (2017) and Nickel et al. (2016).

## Results and limits

- The paper reports strong link-prediction results on standard benchmarks, compared with the models available at the time (Trouillon et al., 2016). Exact numbers should be taken from the paper's tables, not from this page.
- Representing asymmetry doubles the number of real parameters per dimension, which costs memory and training time.
- The bilinear score does not directly represent composition of relations, so multi-hop reasoning needs other tools.
- Results depend on the benchmark and the evaluation protocol. Some benchmarks contain inverse relations that make the task easier than it looks (Dettmers et al., 2018).

## Applications

- **Completing large knowledge graphs**: predicting missing facts for search and question answering.
- **Graphs with directed relations**: recommendation or biomedical graphs in which relations such as "treats" or "causes" depend on direction.

## Connections

- [TransE](transe.md) shares the link-prediction goal and gives a useful contrast on symmetric relations.
- [Neuro-symbolic AI](../neuro-symbolic/index.md) explores combining embedding-based completion with logical constraints.
- [Knowledge graphs overview](index.md) places ComplEx among the embedding methods.

## Open questions

- How the embedding dimension trades off against the relation types it can capture is not fully understood.
- Embedding models are transductive: they cannot place entities that were not seen during training without retraining.
- Benchmark design still affects which model appears best (Dettmers et al., 2018).

## References

### Seminal papers

- Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G. (2016). Complex embeddings for simple link prediction. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/trouillon16.html — Introduces ComplEx and the complex Hermitian score for asymmetric relations.
- Bordes, A., Usunier, N., Garcia-Duran, A., Weston, J. & Yakhnenko, O. (2013). Translating embeddings for modeling multi-relational data. In *Advances in Neural Information Processing Systems* 26. https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html — The TransE benchmark setting that ComplEx builds on.
- Dettmers, T., Minervini, P., Stenetorp, P. & Riedel, S. (2018). Convolutional 2D knowledge graph embeddings. In *Proceedings of the AAAI Conference on Artificial Intelligence* 32. https://arxiv.org/abs/1707.01476 — Shows that widely used benchmarks contain inverse-relation leakage.

### Surveys and textbooks

- Nickel, M., Murphy, K., Tresp, V. & Gabrilovich, E. (2016). A review of relational machine learning for knowledge graphs. *Proceedings of the IEEE* 104(1), 11–33. https://doi.org/10.1109/JPROC.2015.2483592 — Reviews relational embedding models, including the bilinear family.
- Wang, Q., Mao, Z., Wang, B. & Guo, L. (2017). Knowledge graph embedding: a survey of approaches and applications. *IEEE Transactions on Knowledge and Data Engineering* 29(12), 2724–2743. https://doi.org/10.1109/TKDE.2017.2754499 — Surveys embedding methods and their score functions.
- Hogan, A. et al. (2021). Knowledge graphs. *ACM Computing Surveys* 54(4), 1–37. https://doi.org/10.1145/3447772 — Places embedding models within knowledge graph research.
