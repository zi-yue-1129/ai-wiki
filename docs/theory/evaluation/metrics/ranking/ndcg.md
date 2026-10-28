---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# NDCG

Normalised discounted cumulative gain (NDCG) scores a ranked list by summing the relevance of each item, discounted by how far down the list it appears, and dividing by the best possible score for the same items. It is between 0 and 1.

## Definition

For a list of predicted scores, the items are sorted by those scores. Each item contributes its true relevance divided by a logarithm of its position, so items lower down count for less. The discounted cumulative gain (DCG) is the sum of these contributions. NDCG divides DCG by the ideal DCG, which is the value obtained by sorting the items by their true relevance.

In scikit-learn, `ndcg_score` takes the true relevance and the predicted scores, and an optional cut-off $k$ that counts only the top $k$ items (see References).

## Interpretation

An NDCG of 1.0 means the ordering is ideal. Because each position is discounted, moving a highly relevant item from rank 1 to rank 5 costs more than moving it from rank 50 to rank 54. The score can use graded relevance, such as 0 to 10, which MAP cannot.

## When to use it

Use NDCG to compare rankings in search and recommendation, especially when relevance has several levels or when only the top results matter, in which case set a cut-off $k$ and report it.

## Worked example

Take six items whose graded relevance, in the order the model ranks them, is $(3, 2, 3, 0, 1, 2)$. The discounted cumulative gain is $\mathrm{DCG} = \sum_{i=1}^{6} \mathrm{rel}_i / \log_2(i + 1) \approx 6.86$. The ideal order $(3, 3, 2, 2, 1, 0)$ gives $\mathrm{IDCG} \approx 7.14$, so NDCG is $6.86 / 7.14 \approx 0.96$.

## Properties and variants

- **Gain and discount.** The gain is the relevance, and the discount $1 / \log_2(i + 1)$ falls with rank $i$. Järvelin and Kekäläinen (2002) introduced this family of discounted cumulated gains. Scikit-learn uses linear gain. Web search often uses exponential gain, $2^{\mathrm{rel}} - 1$, which weights high grades more heavily.
- **Normalisation.** Dividing by the ideal DCG gives 1 for the best possible order of the same items, so scores are comparable across queries with different numbers of relevant items.
- **Cut-off variant.** NDCG@$k$ computes both DCG and the ideal DCG over the top $k$ positions, so it measures only the top of the list.
- **Limit.** The discount base and the gain function are conventions. Two papers reporting "NDCG" may use different ones, so the formula must be stated.

## Pitfalls

- **Normalisation per query.** NDCG is computed for each query and then averaged. A query with no relevant items needs a stated convention.
- **Cut-off.** Results at $k = 10$ and at $k = $ all items answer different questions. Report the cut-off with the score.

## Related metrics

[MAP](map.md) uses binary relevance and averages precision over relevant items. The family overview is [Ranking Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — API reference giving the definition, the top-$k$ option and a worked example.
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Describes ranked retrieval evaluation, the setting in which discounted gain measures were developed.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference for average precision computed from prediction scores, with its step-wise formula.
- Wang, Y., Wang, L., Li, Y., He, D., Chen, W. & Liu, T.-Y. (2013). A theoretical analysis of NDCG type ranking measures. arXiv:1304.6480. https://arxiv.org/abs/1304.6480 — Theoretical analysis of NDCG-type ranking measures and the position discounts they use.
