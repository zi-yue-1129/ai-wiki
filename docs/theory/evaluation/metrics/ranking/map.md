---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# Mean Average Precision

Mean average precision (MAP) is the average, over queries, of the average precision of each ranked list. Average precision for one query is the mean of the precision values at each position where a relevant item appears. MAP summarises ranking quality with binary relevance labels.

## Definition

For one query with ranked list $1..N$, let $P(k)$ be the precision in the top $k$ results and $\text{rel}(k) = 1$ if item $k$ is relevant. Then

$$\text{AP} = \frac{1}{R} \sum_{k=1}^{N} P(k)\, \text{rel}(k)$$

where $R$ is the number of relevant items. MAP is the mean of AP over all queries. The Manning et al. chapter in References defines average precision in this way.

Note that scikit-learn's `average_precision_score` computes AP for one set of scores, the step-wise area under the precision-recall curve, which is the same idea for a single ranking (see References).

## Interpretation

MAP is high when relevant items are placed early and consistently. It rewards finding all relevant items, because a relevant item that is never retrieved contributes nothing to the sum.

## When to use it

Use MAP for information retrieval benchmarks where relevance is yes or no and every relevant item matters. Use [NDCG](ndcg.md) when relevance has several levels or only the top results count.

## Pitfalls

- **Query weighting.** MAP gives every query equal weight, so a few queries with many relevant items do not dominate. Report the number of queries.
- **Incomplete judgments.** If some relevant items are not labelled, MAP is underestimated. This is a property of the test collection, not of the ranking.

## Related metrics

[NDCG](ndcg.md) uses graded relevance and discounts by position. The family overview is [Ranking Metrics](index.md).

## References

### Articles and documentation

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines average precision for a single ranked list, which MAP averages over queries.
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference for average precision from scores, and its step-wise formula.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
