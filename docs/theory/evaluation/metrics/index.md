---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
---

# Metrics

A metric turns a model's outputs and the true answers into one number. The right metric depends on the decision the number will inform, so choosing it is part of the design. This section groups metrics by task. Each family has its own overview, and each metric has its own page.

## Families

| Family | Task | Metrics |
|---|---|---|
| [Classification](classification/index.md) | Predicting a class | [Accuracy](classification/accuracy.md), [Precision](classification/precision.md), [Recall](classification/recall.md), [F1](classification/f1.md), [ROC-AUC](classification/roc-auc.md), [PR-AUC](classification/pr-auc.md) |
| [Probabilistic](probabilistic/index.md) | Judging predicted probabilities | [Log-loss](probabilistic/log-loss.md), [Brier score](probabilistic/brier-score.md), [Calibration error](probabilistic/calibration-error.md) |
| [Regression](regression/index.md) | Predicting a number | [MAE](regression/mae.md), [RMSE](regression/rmse.md), [R²](regression/r-squared.md) |
| [Ranking](ranking/index.md) | Ordering a list | [NDCG](ranking/ndcg.md), [MAP](ranking/map.md) |
| [Segmentation](segmentation/index.md) | Overlap of predicted and true regions | [IoU](segmentation/iou.md), [Dice](segmentation/dice.md) |

The classic supervised setting, including splitting data and validating a model, is covered in [Evaluation and Validation](../../paradigms/supervised/evaluation-and-validation/index.md).

## Choosing a metric

- **Start from the decision.** Ask what a false alarm, a miss, a large error or a misordered list would cost, and choose the family that measures that cost.
- **Report a threshold-free metric and a threshold metric.** Ranking metrics such as ROC-AUC or PR-AUC do not depend on one cut-off; precision, recall and F1 do. Show both when a cut-off will be used.
- **Check calibration** whenever probabilities are used directly, not only their ranking.
- **State the baseline.** A metric value means little without the score of a trivial model, such as the majority-class rate or the mean prediction.

## Open issues

A metric is a proxy. Whether it matches what users value is a question for the application, and no formula settles it. Because no single metric captures every trade-off, report several with their definitions and thresholds. The protocols that use these metrics are in [Protocols](../protocols/index.md).
