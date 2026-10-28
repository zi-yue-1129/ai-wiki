---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - ranking
---

# Ranking Metrics

Ranking metrics score an ordered list. They are used in search, recommendation and retrieval, where the question is whether the most relevant items appear first. Metrics such as accuracy ignore order, so they cannot tell a good ranking from a poor one that contains the same items.

## Problem

A system returns a list of items for a query, and each item has a relevance judgement, binary or graded. A useful ranking metric rewards placing relevant items near the top, gives less credit to relevance that appears lower down, and can be averaged across queries. Set-based measures such as precision and recall ignore position, so they must be extended before they can judge a ranking.

## Key concepts

- **Relevance label:** a binary judgement (relevant or not) or a graded score for each item.
- **Cutoff \(k\):** the number of top positions that are scored. Metrics are often reported at a fixed cutoff, such as \(k = 10\).
- **Position discount:** a weight that falls with rank, so a relevant item at rank 1 counts for more than the same item at rank 10.
- **Normalisation:** dividing by the value of the ideal ordering, so a perfect list scores 1 and scores are comparable across queries.

## Key methods

### Normalised discounted cumulative gain (NDCG)

NDCG uses graded relevance and a logarithmic position discount. The discounted cumulative gain at cutoff \(k\) is

\[
\mathrm{DCG}_k = \sum_{i=1}^{k} \frac{g(\mathrm{rel}_i)}{\log_2(i+1)},
\]

where \(\mathrm{rel}_i\) is the grade of the item at rank \(i\) and \(g\) is a gain that increases with the grade. Implementations commonly use \(g(r) = 2^r - 1\). NDCG divides by the DCG of the ideal ordering, \(\mathrm{IDCG}_k\), so \(\mathrm{NDCG}_k = \mathrm{DCG}_k / \mathrm{IDCG}_k\) lies between 0 and 1. Järvelin and Kekäläinen (2002) introduced cumulated-gain measures with this kind of discount. The details are on the [NDCG](ndcg.md) page.

- **Results:** Wang et al. (2013) analyse the theoretical properties of NDCG-type measures, including the position discounts they use.
- **Limitations:** NDCG depends on the choice of gain, discount and cutoff, and on the ideal ordering, which needs judgements for every relevant item.

### Mean average precision (MAP)

For binary relevance, the average precision of one query is

\[
\mathrm{AP} = \frac{1}{R} \sum_{k} P(k)\, \mathrm{rel}(k),
\]

where \(P(k)\) is precision at rank \(k\), \(\mathrm{rel}(k)\) is 1 if the item at rank \(k\) is relevant and 0 otherwise, and \(R\) is the number of relevant items. MAP is the mean of AP over queries. Manning, Raghavan and Schütze (2008) define these measures for ranked retrieval. The details are on the [MAP](map.md) page.

- **Results:** MAP is a standard summary in information retrieval benchmarks, where relevance is usually judged as yes or no.
- **Limitations:** MAP ignores graded relevance. Averaging over queries gives every query equal weight, whatever its number of relevant items.

## Connections

Average precision, the per-query quantity behind MAP, is closely related to the precision-recall metrics in [classification metrics](../classification/index.md). Ranking metrics are the list-level counterparts of the classification scores, and one list can be scored with either family.

## Open questions

- Which gain and discount best match what users read, and how sensitive are model comparisons to that choice?
- How should metrics treat items that were never judged, which is common in large retrieval collections?

## References

### Seminal papers

- Järvelin, K. & Kekäläinen, J. (2002). Cumulated gain-based evaluation of IR techniques. *ACM Transactions on Information Systems* 20(4), 422–446. https://doi.org/10.1145/582415.582418 — Introduces cumulated gain-based measures with a position discount, the basis of NDCG.
- Wang, Y., Wang, L., Li, Y., He, D., Chen, W. & Liu, T.-Y. (2013). A theoretical analysis of NDCG type ranking measures. COLT 2013, PMLR 30. https://proceedings.mlr.press/v30/Wang13.html — Theoretical analysis of NDCG-type ranking measures and the position discounts they use.

### Surveys and textbooks

- Manning, C. D., Raghavan, P. & Schütze, H. (2008). *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines average precision for a ranked list and the retrieval measures used to compare rankings.

### Articles and documentation

- scikit-learn contributors. *ndcg_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html — API reference for normalised discounted cumulative gain, with a worked example.
- scikit-learn contributors. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — API reference for average precision computed from prediction scores.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking.
