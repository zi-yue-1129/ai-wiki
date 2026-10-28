---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# Ranking Metrics

Ranking metrics score an ordered list. They are used in search, recommendation and retrieval, where the question is whether the most relevant items appear first. Metrics such as accuracy ignore order, so they cannot tell a good ranking from a poor one with the same items.

## Key metrics

| Metric | What it measures | Relevance labels |
|---|---|---|
| [NDCG](ndcg.md) | Gain from relevant items, discounted by position and normalised to the ideal ordering | Graded or binary |
| [MAP](map.md) | Average of precision values at each relevant item, averaged over queries | Binary |

NDCG rewards placing highly relevant items near the top and works with graded relevance. MAP treats relevance as yes or no and is common in information retrieval benchmarks.

## Connections

Average precision, the per-query quantity behind MAP, is closely related to the precision-recall metrics in [Classification Metrics](../classification/index.md). The Manning et al. chapter in References defines these measures for retrieval.

## References

### Articles and documentation

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines average precision for a ranked list and the retrieval measures used to compare rankings.
- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — API reference for normalised discounted cumulative gain, with a worked example.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference for average precision computed from prediction scores, with its step-wise formula.
- Wang, Y., Wang, L., Li, Y., He, D., Chen, W. & Liu, T.-Y. (2013). A theoretical analysis of NDCG type ranking measures. COLT 2013, PMLR 30. https://proceedings.mlr.press/v30/Wang13.html — Theoretical analysis of NDCG-type ranking measures and the position discounts they use.
