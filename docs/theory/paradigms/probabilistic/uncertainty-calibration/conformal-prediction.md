---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic/uncertainty-calibration
tags:
  - uncertainty quantification
  - conformal prediction
  - coverage guarantee
aliases:
  - 共形預測
  - Conformal prediction
  - Conformal inference
  - Prediction sets
---

# Conformal Prediction

Conformal prediction turns any predictor into one that outputs prediction sets or intervals with a guaranteed probability of containing the true outcome. The guarantee holds for any model, under the assumption that the data are exchangeable. Part of [Uncertainty quantification and calibration](index.md).

## Overview

A classifier that outputs a single label gives no sense of its uncertainty, and a probability score may be badly calibrated. Conformal prediction takes a different route. It asks for a set of plausible labels that contains the true one with probability at least \(1-\alpha\), for a level \(\alpha\) chosen by the user. The method uses a held-out calibration set to decide how large the set must be.

## Key concepts

- **Nonconformity score**: a measure \(s(x,y)\) of how unusual the label \(y\) is for input \(x\). A common choice is one minus the predicted probability of \(y\).
- **Exchangeability**: the calibration and test data can be permuted without changing their joint distribution. It is weaker than independence and is the assumption behind the guarantee.
- **Coverage**: the probability that the true label lies in the prediction set. The guarantee is on coverage, not on accuracy of the point prediction.

## How it works

In split conformal prediction, the data are split into a training set and a calibration set. The model is trained on the first part. On the calibration set, compute the scores \(s_i=s(x_i,y_i)\) and let \(\hat q\) be the \((1-\alpha)(1+1/n)\)-quantile of these scores. The prediction set for a new input is

\[
C(x)=\{\,y : s(x,y)\le \hat q\,\},
\]

and under exchangeability \(P(Y\in C(X))\ge 1-\alpha\) (Angelopoulos & Bates, 2023). For regression, the same idea gives prediction intervals, and the score can be the absolute residual or a quantity from a quantile model. Lei et al. (2018) develop distribution-free predictive inference for regression in this framework.


<div style="max-width:100%;overflow-x:auto" role="group" aria-label="Conformal prediction animation">
<div style="width:640px">
<img src="../../../../assets/concept-animations/conformal-quantile-still.svg" data-motion-src="../../../../assets/concept-animations/conformal-quantile-motion.svg" alt="Eight ordered illustrative calibration scores select the seventh score 0.54 as the split-conformal threshold; candidate labels A and B are included, while C is excluded." width="640" height="360">
</div>
</div>

*Original animated teaching visual (CC BY-SA 4.0).* With eight illustrative calibration scores and α=0.25, the finite-sample index is ceil((8+1)(1−0.25))=7; the seventh sorted score is q=0.54. For a separate illustrative test input, candidate-label nonconformity scores (A: 0.19, B: 0.48, C: 0.71) give the set **{A, B}**. The animation reveals the calibration scores, threshold, and set membership in that order. **The displayed values are invented for teaching, not empirical coverage or model measurements.** The marginal coverage statement requires exchangeability; it is not a per-input guarantee. MkDocs provides Play/Pause; the [GitHub static preview](../../../../assets/concept-animations/conformal-quantile-still.svg) shows the completed set. Scroll horizontally on narrow screens. See Shafer & Vovk (2008) and Angelopoulos & Bates (2023) in References.

## Variants

- **Split conformal** uses one calibration set, which is the simplest and most common form.
- **Full conformal** refits the model for each candidate label, which is more expensive but uses the data more efficiently.
- **Adaptive scores** change the nonconformity measure so that the sets are smaller where the model is confident.

## Results and limits

- The coverage guarantee holds in finite samples under exchangeability, without assumptions on the model. This is the main attraction of the method.
- The guarantee is marginal. Coverage can be too high for some inputs and too low for others, including subgroups, which matters for fairness and medical use.
- Set size depends on the quality of the underlying model. A poor model gives large, uninformative sets that still satisfy the guarantee.
- Under distribution shift, the exchangeability assumption fails, and the guarantee no longer holds without adjustment.

## Applications

- **Classification with abstention**: returning a set of labels and flagging large sets for human review (Angelopoulos & Bates, 2023).
- **Regression intervals**: prediction intervals with guaranteed coverage for forecasts and measurements (Lei et al., 2018).
- **Medical prediction**: quantifying the uncertainty of diagnostic models in a model-agnostic way.

## Open questions

- Conditional coverage, which holds for each input or subgroup, is generally not achievable without strong assumptions.
- Handling distribution shift with valid coverage, for example by weighting the calibration data, is an active research area.
- Balancing set size and coverage in high-dimensional outputs, such as structured prediction, is difficult.

## References

### Seminal papers

- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J. & Wasserman, L. (2018). Distribution-free predictive inference for regression. *Journal of the American Statistical Association* 113(523), 1094–1111. https://doi.org/10.1080/01621459.2017.1307116 — Gives distribution-free prediction intervals for regression using split conformal methods.
- Shafer, G. & Vovk, V. (2008). A tutorial on conformal prediction. *Journal of Machine Learning Research* 9. https://www.jmlr.org/papers/v9/shafer08a.html — Tutorial introducing the framework and its validity guarantees.

### Surveys and textbooks

- Angelopoulos, A. N. & Bates, S. (2023). Conformal prediction: a gentle introduction. *Foundations and Trends in Machine Learning* 16(4), 494–591. https://doi.org/10.1561/2200000101 — Gentle introduction to conformal methods, including split and adaptive variants.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — Documents the miscalibration of neural classifiers that motivates calibrated uncertainty alongside coverage guarantees.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on predictive uncertainty and intervals.
