---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# Probabilistic Metrics

Probabilistic metrics score the probabilities a model reports, not just its chosen labels. They matter when the probability itself is used: as a risk score, in a decision that weighs costs, or as input to another system. A model that ranks cases well can still give probabilities that are too high or too low, so these metrics check a different property from [classification metrics](../classification/index.md).

## Key metrics

| Metric | What it measures | Lower or higher is better |
|---|---|---|
| [Log-loss](log-loss.md) | Negative log-likelihood of the true labels under the predicted probabilities | Lower |
| [Brier score](brier-score.md) | Mean squared difference between predicted probability and outcome | Lower |
| [Calibration error](calibration-error.md) | Gap between predicted confidence and observed frequency, averaged over bins | Lower |

Log-loss and the Brier score reward both good ranking and honest probabilities. Calibration error isolates the second property. A model can have a good log-loss and still be miscalibrated in one range of probabilities, so reading the calibration error alongside them is useful.

## Connections

Discrimination, the ability to separate classes, is measured by [ROC-AUC](../classification/roc-auc.md) and [PR-AUC](../classification/pr-auc.md). Guo et al. (2017) show that modern neural networks are often overconfident, which is why calibration is reported separately. The procedures for splitting data before fitting a calibration step are covered in [Protocols](../../protocols/index.md).

## References

### Seminal papers

- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — Shows that modern networks are overconfident and that temperature scaling corrects it.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — Compares probability calibration across common classifiers and the effect of calibration methods.

### Articles and documentation

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of scorers that take predicted probabilities.
