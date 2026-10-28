---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic/uncertainty-calibration
tags:
  - calibration
  - evaluation metric
  - uncertainty quantification
aliases:
  - 期望校準誤差
  - ECE
  - Expected calibration error
  - Calibration metric
---

# Expected Calibration Error

Expected calibration error (ECE) is a summary of miscalibration. It groups predictions into bins by confidence and averages the gap between each bin's confidence and its accuracy, weighted by the number of predictions in each bin. Part of [Uncertainty quantification and calibration](index.md).

## Overview

To check calibration, one needs a number. A reliability diagram shows the confidence and accuracy per bin, and ECE condenses that diagram into a single value. It is widely used in calibration studies of classifiers, and it was used by Guo et al. (2017) to compare calibration methods. The metric is simple, but its value depends on how the bins are chosen.

## Key concepts

- **Confidence**: the highest predicted probability for a prediction, which is the model's stated confidence in its predicted label.
- **Accuracy**: the fraction of predictions in a bin whose predicted label is correct.
- **Bin**: a range of confidence values, usually of equal width, into which predictions are grouped.
- **Reliability diagram**: a plot of accuracy against confidence per bin. A calibrated model lies on the diagonal.

## How it works

Let there be \(n\) predictions, split into \(B\) bins \(B_b\), each containing \(n_b\) predictions. Then

\[
\mathrm{ECE}=\sum_{b=1}^{B}\frac{n_b}{n}\,\big|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)\big|,
\]

where \(\mathrm{acc}(B_b)\) is the accuracy in the bin and \(\mathrm{conf}(B_b)\) the average confidence. A value of zero means every bin's accuracy equals its average confidence. Guo et al. (2017) use 15 equal-width bins in their experiments.

## Variants

- **Maximum calibration error** takes the largest bin gap instead of the weighted average, which emphasises the worst bin.
- **Adaptive binning** chooses bins with equal numbers of predictions, which reduces the variance in sparse bins.
- **Class-wise ECE** computes the gap for each class separately, which catches miscalibration on rare classes.

## Results and limits

- ECE is easy to compute and to explain, and it directly measures the gap that calibration aims to remove.
- Its value depends on the number and placement of bins, so comparisons across papers need the same binning.
- It is biased in small samples, and bins with few predictions are noisy.
- It does not measure sharpness or discrimination. A model that always predicts the base rate can have low ECE and be useless. The Brier score, which combines calibration and refinement, avoids this (Brier, 1950; DeGroot & Fienberg, 1983).

## Applications

- **Comparing calibration methods**: ECE before and after [temperature scaling](temperature-scaling.md) on image classifiers (Guo et al., 2017).
- **Monitoring deployed models**: tracking calibration over time, as the input distribution changes.
- **Reporting**: a single number for model cards and papers, to be read with the reliability diagram.

## Open questions

- A binning-free measure of calibration that is stable and unbiased in small samples remains a research question.
- ECE is defined for classification. Extending a comparable measure to structured prediction and generative models is unsettled.

## References

### Seminal papers

- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — Uses ECE with reliability diagrams to show miscalibration of modern networks.
- DeGroot, M. H. & Fienberg, S. E. (1983). The comparison and evaluation of forecasters. *The Statistician* 32(1/2), 12–22. https://doi.org/10.2307/2987588 — Defines calibration and the decomposition of forecast scores into calibration and refinement.
- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — Introduces the Brier score, an alternative measure that does not rely on binning.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning*, 625–632. https://doi.org/10.1145/1102351.1102430 — Evaluates classifiers' probabilities using calibration measures.

### Surveys and textbooks

- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers calibration and proper scoring rules.
- Angelopoulos, A. N. & Bates, S. (2023). Conformal prediction: a gentle introduction. *Foundations and Trends in Machine Learning* 16(4), 494–591. https://doi.org/10.1561/2200000101 — Places calibration measures alongside coverage-based uncertainty methods.
