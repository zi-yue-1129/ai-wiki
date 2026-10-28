---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# Classification Metrics

Classification metrics score a model whose output is a class label or a score for each class. Some metrics read the labels at one decision threshold: accuracy, precision, recall and F1. Others read the scores across all thresholds and ask how well positives are ranked above negatives: ROC-AUC and PR-AUC. The two groups answer different questions, so a model can look strong on one and weak on the other.

## Key metrics

| Metric | What it measures | Threshold needed | Use when |
|---|---|---|---|
| [Accuracy](accuracy.md) | Fraction of correct labels | Yes | Classes are balanced and every error costs the same |
| [Precision](precision.md) | Share of predicted positives that are correct | Yes | False alarms are costly |
| [Recall](recall.md) | Share of true positives that are found | Yes | Missed cases are costly |
| [F1](f1.md) | Harmonic mean of precision and recall | Yes | One number for the positive class |
| [ROC-AUC](roc-auc.md) | Ranking of positives above negatives | No | Comparing models without fixing a threshold |
| [PR-AUC](pr-auc.md) | Precision across recall levels | No | Positives are rare |

The label-based metrics change with the threshold, so report the threshold together with the number. The ranking metrics do not depend on one threshold, but they can look optimistic when positives are rare.

## Connections

Whether the scores behave like probabilities is a separate question, covered in [Probabilistic Metrics](../probabilistic/index.md). The procedure for splitting data and validating a classifier is in [Evaluation and Validation](../../../paradigms/supervised/evaluation-and-validation/index.md).

## References

### Surveys and documentation

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Reference for the standard classification scorers and their definitions.
- Manning, C. D., Raghavan, P. & Schütze, H. *Evaluation of ranked retrieval results*, online edition of *Introduction to Information Retrieval*. https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html — Defines precision, recall, the F measure and average precision for retrieval, which carry over to classification.

### Additional sources

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — Explains how ROC curves and the AUC are built, read and commonly misused.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
