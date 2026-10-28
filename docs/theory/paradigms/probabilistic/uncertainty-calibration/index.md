---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
  - theory/paradigms/probabilistic/variational-inference
  - theory/math/probability-statistics
tags:
  - uncertainty quantification
  - calibration
  - predictive uncertainty
aliases:
  - 不確定性量化
  - 校準
  - Uncertainty quantification
  - Calibration
  - Predictive uncertainty
---

# Uncertainty Quantification and Calibration

Uncertainty quantification asks how much a model's prediction can be trusted and how to represent what it does not know. Calibration asks whether the predicted probabilities match observed frequencies. Part of [Probabilistic & Bayesian methods](../index.md).

## Overview

A model that says "90% confident" should be right about nine times in ten, for predictions made with that confidence. Modern neural networks often fail this test: they are accurate but overconfident. Two kinds of uncertainty are usually distinguished. **Aleatoric** uncertainty comes from noise in the data and cannot be reduced by more data. **Epistemic** uncertainty comes from the model's lack of knowledge and can shrink as data grow. Methods for uncertainty address one or both.

## Key concepts

- **Calibration**: the predicted probability of an event matches its frequency. A perfectly calibrated forecaster's stated probabilities are reliable, which DeGroot and Fienberg (1983) formalised for forecasters.
- **Proper scoring rule**: a loss, such as the Brier score, that is minimised only by reporting the true probabilities (Brier, 1950).
- **Expected calibration error**: a binned summary of the gap between confidence and accuracy, defined in the [calibration metric page](expected-calibration-error.md).
- **Prediction set**: a set of possible labels with a guaranteed probability of containing the true label. This is the output of conformal prediction.

## How it works

Methods fall into three groups. **Post-hoc calibration** adjusts a trained model's probabilities on held-out data. [Temperature scaling](temperature-scaling.md) is the simplest example and is effective for neural classifiers (Guo et al., 2017). **Ensembles** average the predictions of several models trained with different randomness, which improves both accuracy and calibration (Lakshminarayanan et al., 2017). **Conformal prediction** wraps any predictor and returns sets with a coverage guarantee under a mild assumption on the data (Angelopoulos & Bates, 2023).

Bayesian approaches represent a distribution over parameters rather than a single set of weights. Exact posteriors are rarely available for neural networks, and approximations such as dropout-based inference have been used to estimate uncertainty (Gal & Ghahramani, 2016).

## Key methods

- [Conformal prediction](conformal-prediction.md): distribution-free prediction sets with a coverage guarantee.
- [Temperature scaling](temperature-scaling.md): a single parameter that rescales logits to fix overconfidence.
- [Deep ensembles](deep-ensembles.md): several networks trained independently whose predictions are averaged.
- [Expected calibration error](expected-calibration-error.md): a binned measure of miscalibration.

## Connections

- [Variational inference](../variational-inference/index.md) and [Markov chain Monte Carlo](../mcmc/index.md) give full posterior approximations that are the principled route to epistemic uncertainty.
- [Probability and statistics](../../../math/probability-statistics/index.md) provides the scoring rules and the calibration concepts.
- [Bayesian deep learning](../index.md) is the wider context in which these methods are used.

## Applications

- **Medical AI**: flagging predictions that need human review, where calibrated probabilities and coverage guarantees matter (Angelopoulos & Bates, 2023).
- **Safety and decision making**: deciding when to act or abstain based on how uncertain the model is.
- **Forecasting**: reporting probabilities that users can rely on, which requires calibrated outputs.

## Open questions

- Calibration under distribution shift is harder than in-distribution calibration, and most post-hoc methods assume the test data look like the calibration data.
- Conformal guarantees are marginal, not conditional on the input, so coverage can differ between subgroups.
- Separating aleatoric from epistemic uncertainty reliably in practice remains difficult, and the decomposition depends on the chosen model.

## References

### Seminal papers

- Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review* 78(1), 1–3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 — Introduces the Brier score, a proper scoring rule for probability forecasts.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning*, PMLR 70. https://proceedings.mlr.press/v70/guo17a.html — Shows that modern networks are miscalibrated and that temperature scaling corrects it.
- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. In *Advances in Neural Information Processing Systems* 30. https://proceedings.neurips.cc/paper/2017/hash/9ef2ed4b7fd2c810847ffa5fa85bce38-Abstract.html — Proposes deep ensembles as a scalable way to estimate predictive uncertainty.
- Angelopoulos, A. N. & Bates, S. (2023). Conformal prediction: a gentle introduction. *Foundations and Trends in Machine Learning* 16(4), 494–591. https://doi.org/10.1561/2200000101 — Introduces conformal prediction and its coverage guarantees.

### Surveys and textbooks

- DeGroot, M. H. & Fienberg, S. E. (1983). The comparison and evaluation of forecasters. *The Statistician* 32(1/2), 12–22. https://doi.org/10.2307/2987588 — Defines calibration and the decomposition of forecast scores.
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning*, PMLR 48. https://proceedings.mlr.press/v48/gal16.html — Interprets dropout as approximate Bayesian inference for uncertainty.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers calibration, scoring rules and Bayesian uncertainty.
