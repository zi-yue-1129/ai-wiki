---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
---

# Metrics

A metric turns a model's outputs and the true answers into one number. The right metric depends on the decision the number will inform, so choosing it is part of the design. This page maps the common metrics by task. The classic supervised setting is covered in depth in [Evaluation and Validation](../../paradigms/supervised/evaluation-and-validation/index.md).

## Metric families by task

| Task | Metric | What it rewards | Caution |
|---|---|---|---|
| Classification | Accuracy | Overall correctness | Misleading when classes are imbalanced |
| Classification | Precision, recall, F1 | Correct positives at one chosen threshold | Depend on the threshold, so report it |
| Classification | ROC-AUC | Positives ranked above negatives, over all thresholds | Can look optimistic for rare positives |
| Classification | PR-AUC | Precision across recall levels | Its baseline equals the positive rate, so it varies between datasets |
| Probabilistic | Log-loss, Brier score | Honest probabilities | Log-loss punishes confident mistakes hard |
| Calibration | Calibration error | Predicted confidence matching observed frequency | Depends on how predictions are binned |
| Regression | RMSE, MAE, $R^2$ | Size of errors | RMSE penalises large errors more than MAE |
| Ranking | NDCG, MAP | Ordering, weighted by position | Needs graded or binary relevance labels |
| Segmentation | IoU, Dice | Overlap between predicted and true regions | Small regions amplify boundary errors |

The scikit-learn guide lists the standard scorers for each family (see References).

## Matching the metric to the decision

- **Choosing a short list of candidates** calls for a ranking metric. Accuracy at a fixed threshold can hide a good ordering.
- **Rare events**, such as fraud or disease, call for PR-AUC and precision at the threshold you will actually use. ROC-AUC can stay high while precision is poor.
- **Using probabilities directly**, for example as risk scores, requires checking calibration as well as discrimination. Guo et al. (2017) show that modern neural networks are often overconfident.

## Calibration

A model is calibrated when, among cases it assigns probability $p$, about a fraction $p$ turn out positive. Calibration is separate from accuracy: a model can rank cases well and still give badly scaled probabilities. Temperature scaling corrects overconfidence in deep networks (Guo et al., 2017). Niculescu-Mizil and Caruana (2005) compare calibration across common classifiers.

## Metrics for language models

Language models are often scored by log-likelihood on held-out text, or by accuracy on multiple-choice questions. Free-form answers are usually checked by a program or a judge model. Those choices, and the protocols around them, are covered in [Evaluation & Benchmarks](../../../engineering/evaluation/index.md) and in [Protocols](../protocols/index.md). Metrics for generative image models are not yet covered on this page.

## Open issues

A metric is a proxy. Whether it matches what users value is a question for the application, and no formula settles it. Because no single metric captures every trade-off, the sensible practice is to report several, with their definitions and thresholds.

## Connections

Metric values depend on how the data was split, so the same metric can give different numbers under different protocols. See [Protocols](../protocols/index.md).

## References

### Seminal papers

- Saito, T. & Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. *PLoS ONE* 10(3). https://doi.org/10.1371/journal.pone.0118432 — Shows why precision-recall curves are more informative than ROC curves for rare positives.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — Compares probability calibration across common classifiers and the effect of calibration methods.
- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — Shows that modern networks are overconfident and that temperature scaling corrects it.

### Surveys and textbooks

- Fawcett, T. (2006). An introduction to ROC analysis. *Pattern Recognition Letters* 27(8), 861–874. https://doi.org/10.1016/j.patrec.2005.10.010 — Explains how ROC curves and the AUC are built, read and commonly misused.

### Articles and documentation

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Reference for standard classification, regression and ranking scorers, with their definitions.
