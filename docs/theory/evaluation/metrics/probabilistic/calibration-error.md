---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# Calibration Error

Calibration error measures whether predicted confidence matches observed frequency. A calibrated model that predicts 0.8 is right about 80% of the time. Calibration is a property of the probabilities alone, separate from how well the model ranks cases.

## Definition

Predictions are grouped into $M$ bins by confidence. For each bin $B_m$, compare the mean predicted confidence with the observed fraction of positives. The expected calibration error (ECE) is their weighted average:

$$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{n} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$

where $\text{acc}(B_m)$ is the observed fraction of positives in bin $m$ and $\text{conf}(B_m)$ is the mean predicted probability in that bin. Naeini et al. (2015) develop binning-based estimates of this kind. The result depends on how many bins are used, so the bin count must be reported.

## Interpretation

An ECE near zero means the confidence is close to the observed frequency on average. ECE does not show which confidence range is at fault; a reliability diagram, which plots observed frequency against confidence per bin, does. Modern deep networks are often overconfident, which raises the ECE (Guo et al., 2017).

## When to use it

Use calibration error when probabilities are used for decisions, reported to users, or passed to another system, and when the question is whether the numbers mean what they say.

## Pitfalls

- **Bin choice.** Equal-width bins are sensitive to the number of bins and to sparse ranges. Report the bin count and the binning scheme.
- **Small samples.** Bins with few samples give noisy estimates. Show the counts per bin.
- **Calibration is not accuracy.** A calibrated model can still be a poor classifier. Read it with [ROC-AUC](../classification/roc-auc.md) or [PR-AUC](../classification/pr-auc.md).

## Connections

Temperature scaling, a single-parameter fix for overconfident networks, is described in Guo et al. (2017). It is usually fitted on a held-out validation set, and then the calibration error is measured on the test set. The family overview is [Probabilistic Metrics](index.md).

## References

### Seminal papers

- Naeini, M. P., Cooper, G. & Hauskrecht, M. (2015). Obtaining well calibrated probabilities using Bayesian binning. *Proceedings of the AAAI Conference on Artificial Intelligence* 29(1). https://ojs.aaai.org/index.php/AAAI/article/view/9602 — Develops binning-based estimates of how well a model's probabilities are calibrated.
- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — Shows that modern networks are overconfident, and that temperature scaling corrects it.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — Compares probability calibration across common classifiers and the effect of calibration methods.

### Articles and documentation

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the probabilistic scorers used alongside calibration checks.
