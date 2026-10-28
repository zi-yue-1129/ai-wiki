---
status: draft
last_reviewed: 2026-10-28
tags:
  - retrieval
  - supervised learning
aliases:
  - RankNet
  - 成對式學習排序
---

# RankNet (Burges et al. 2005)

RankNet is a neural network that learns to order search results from pairs of documents, where one of the two should rank higher. Burges and colleagues introduced it at ICML in 2005, and it started the pairwise family of [learning-to-rank](../index.md) methods. The method is one of the landmark approaches listed on the parent page [Search Engines and Information Retrieval](../index.md).

## Overview

Before RankNet, ranking functions for search were usually tuned by hand, or fitted with simple linear models. Burges et al. asked whether a neural network trained by gradient descent could learn a ranking function directly from human judgements of which document is better. Their key choice was to learn from pairs rather than from absolute scores. Asking "is document A better than document B for this query?" is often easier for a labeller than assigning each document an exact grade, and it matches the way a ranked list is judged.

## Key concepts

- **Scoring function**: a network $f$ that maps the features of one document to a single real-valued score. The ranking for a query is obtained by sorting documents by score.
- **Pairwise preference**: for two documents $i$ and $j$ in the same query, a target probability that $i$ should rank above $j$. The target is 1 when $i$ is more relevant, 0 when $j$ is, and 0.5 when they are tied.
- **Probabilistic cost**: the model turns the score difference into a probability, and the cost is the cross-entropy between that probability and the target.

## How it works

For documents $i$ and $j$ with feature vectors $x_i$ and $x_j$, the score difference and the modelled probability are

$$
o_{ij} = f(x_i) - f(x_j), \qquad P_{ij} = \frac{e^{o_{ij}}}{1 + e^{o_{ij}}}
$$

The cost for the pair is the cross-entropy between the target $\bar{P}_{ij}$ and $P_{ij}$:

$$
C_{ij} = -\bar{P}_{ij}\log P_{ij} - (1-\bar{P}_{ij})\log(1-P_{ij})
$$

Because the cost depends only on the difference of two scores, adding a constant to every score changes nothing, and the network learns relative order rather than absolute grades. The training procedure is:

1. For each query, collect the candidate documents and their relevance labels.
2. Form pairs $(i, j)$ in which the labels say $i$ should rank above $j$, with ties given target 0.5.
3. Score both documents with the same network.
4. Compute the pair's probability and cross-entropy cost.
5. Backpropagate the cost and update the weights by gradient descent.
6. At serving time, score each candidate and sort by score.

## Results

The paper presents test results on toy data and on data from a commercial internet search engine. The abstract gives no figures, so this page does not quote numbers.

## Limitations

- **Every pair counts equally.** A mistake near the top of a list costs the same as a mistake near the bottom, but ranking quality metrics concentrate on the top positions. Burges (2010) describes LambdaRank, which scales each pair's gradient by the change in nDCG that swapping the two documents would cause, and LambdaMART, which applies the same idea to boosted trees.
- **Labelled pairs are expensive.** Pairs grow quadratically with the length of a candidate list, and they need preference labels that are costly to collect.
- **Fixed features.** The network works on features that engineers supply. It does not learn text representations, which later neural rankers such as [DSSM](../dssm/index.md) and BERT rerankers did.
- **Clicks are biased.** Users click the top positions more often, so pairs derived from logged clicks inherit that bias, even when clicks are read as preferences as Joachims (2002) proposed.

## Open questions

- Pairwise costs do not directly optimise ranking metrics. How much of the gap is closed by listwise or metric-weighted variants is still studied.
- Whether pairwise training survives in large neural rerankers, which use cross-encoders over text rather than hand-made features.

## Connections

- The cost is a pairwise loss of the kind covered in [Loss functions and optimisation](../../../theory/paradigms/supervised/loss-functions-and-optimization/index.md).
- LambdaMART, the tree-based successor, is a boosted-tree model, see [Trees and ensembles](../../../theory/paradigms/supervised/trees-and-ensembles/index.md).
- Neural text matching, which replaces hand-made features, is the subject of [DSSM](../dssm/index.md).

## Applications

RankNet and its successors order the result lists of search engines, where the candidates have already been retrieved and need to be sorted by relevance.

## References

### Seminal papers

- Burges, C. et al. (2005). Learning to rank using gradient descent. ICML. https://doi.org/10.1145/1102351.1102363 — Introduces RankNet, a neural ranker trained with a probabilistic cost on pairs of documents, tested on a commercial search engine's data.
- Joachims, T. (2002). Optimizing search engines using clickthrough data. KDD. https://doi.org/10.1145/775047.775067 — Shows how user clicks can be turned into pairwise preference data for training a ranking function.
- Dehghani, M. et al. (2017). Neural ranking models with weak supervision. https://arxiv.org/abs/1704.08803 — Trains neural rankers on labels generated automatically rather than from human judgements, reducing the need for annotation.

### Surveys and textbooks

- Liu, T.-Y. (2009). Learning to rank for information retrieval. Foundations and Trends in Information Retrieval. https://doi.org/10.1561/1500000016 — Survey that organises learning-to-rank methods into pointwise, pairwise and listwise approaches.
- Burges, C. J. C. (2010). From RankNet to LambdaRank to LambdaMART: An overview. Microsoft Research Technical Report MSR-TR-2010-82. https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/ — Self-contained account of how the pairwise RankNet cost developed into the listwise LambdaRank and the tree-based LambdaMART.
- Lin, J., Nogueira, R. & Yates, A. (2020). Pretrained transformers for text ranking: BERT and beyond. https://arxiv.org/abs/2010.06467 — Survey of neural text ranking, placing pairwise and pointwise losses in the context of transformer rerankers.
