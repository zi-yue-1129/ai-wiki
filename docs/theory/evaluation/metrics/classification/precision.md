---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# Precision

Precision is the share of predicted positives that are truly positive. It answers: when the model raises an alarm, how often is it right?

## Definition

$$\text{Precision} = \frac{TP}{TP + FP}$$

Precision is undefined when the model predicts no positives, because the denominator is zero.

## Interpretation

Precision measures the cost of false alarms. A spam filter with high precision rarely sends real mail to the spam folder. Precision depends on the decision threshold: raising the threshold usually removes some false positives and raises precision, at the price of [recall](recall.md).

## When to use it

Use precision when acting on a positive prediction is expensive or harmful, for example when a flagged transaction is blocked or a patient is called back for further tests. Report it at the threshold you will actually deploy, not at a default value.

## Pitfalls

- **Threshold dependence.** Precision at one threshold says little about the model as a whole. Pair it with a threshold-free metric such as [PR-AUC](pr-auc.md).
- **Rare positives.** A high precision on a small number of predicted positives can be noisy. Report the counts.

## Related metrics

Precision is one half of the [F1](f1.md) score. Its counterpart is [recall](recall.md). The family overview is [Classification Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html — API reference giving the definition $tp / (tp + fp)$ and the options for averaging over classes.
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Describes precision as a set-based retrieval measure.
