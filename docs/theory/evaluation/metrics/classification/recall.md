---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# Recall

Recall is the share of true positives that the model finds. It answers: of all the real cases, how many did the model catch? It is also called sensitivity or the true positive rate.

## Definition

$$\text{Recall} = \frac{TP}{TP + FN}$$

Recall is undefined when there are no true positives in the data, because the denominator is zero.

## Interpretation

Recall measures the cost of misses. A screening test with high recall rarely lets a real case pass unflagged. Like precision, recall depends on the threshold: lowering the threshold catches more true positives and raises recall, at the price of more false alarms.

## When to use it

Use recall when a missed positive is costly, for example in disease screening or safety monitoring. The usual practice is to fix a minimum recall the application requires and then report the precision that goes with it.

## Pitfalls

- **Trivial recall.** A model that predicts everything positive has recall 1.0 and is useless. Always read recall with precision.
- **Threshold dependence.** Report the threshold, or use a threshold-free metric such as [ROC-AUC](roc-auc.md) or [PR-AUC](pr-auc.md) for model comparison.

## Related metrics

Recall is paired with [precision](precision.md) in the [F1](f1.md) score. The family overview is [Classification Metrics](index.md).

## References

### Articles and documentation

- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines recall as a set-based measure and notes that sensitivity is another name for it.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of classification scorers, including recall, and how they are computed.

### Additional sources

- scikit-learn contributors. *recall_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html — API reference giving the definition tp / (tp + fn) for recall.
- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
