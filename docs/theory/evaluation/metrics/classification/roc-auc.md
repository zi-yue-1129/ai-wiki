---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - classification
---

# ROC-AUC

ROC-AUC is the area under the receiver operating characteristic curve. The curve plots the true positive rate against the false positive rate as the decision threshold sweeps from high to low. The area summarises how well the scores separate positives from negatives, with no single threshold chosen.

## Definition

At each threshold $t$, the true positive rate is $TP/(TP+FN)$ and the false positive rate is $FP/(FP+TN)$. The ROC curve collects these points, and ROC-AUC is the area under it.

A useful reading is the ranking interpretation: ROC-AUC equals the probability that a randomly chosen positive receives a higher score than a randomly chosen negative. A perfect ranking gives 1.0 and random scores give 0.5 (Fawcett, 2006).

## Interpretation

ROC-AUC needs only the scores, not labels at a threshold, so it compares models without fixing an operating point. It depends on the ordering of scores, not their calibration: a model can have a high ROC-AUC while its probabilities are badly scaled. See [Calibration Error](../probabilistic/calibration-error.md).

## When to use it

Use ROC-AUC for model comparison when the operating threshold is not yet known, and when positives and negatives are of comparable size.

## Pitfalls

- **Rare positives.** When negatives vastly outnumber positives, the false positive rate stays small even for many false alarms, so ROC-AUC can look better than the model is for the positive class. Saito and Rehmsmeier (2015) show that the precision-recall view is more informative in this case. Use [PR-AUC](pr-auc.md) for rare events.
- **Multiclass use.** In scikit-learn, multiclass ROC-AUC requires the `multi_class` argument set to `'ovr'` or `'ovo'`; the default raises an error.

## Related metrics

[PR-AUC](pr-auc.md) is the precision-recall counterpart. The family overview is [Classification Metrics](index.md).

## References

### Seminal papers

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — Explains how ROC curves and the AUC are built, read and commonly misused.
- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Compares ROC and precision-recall curves on imbalanced data.

### Articles and documentation

- scikit-learn contributors. *roc_auc_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html — API reference for computing ROC AUC from prediction scores, with binary and multiclass usage.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
