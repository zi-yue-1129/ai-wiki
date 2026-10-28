---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/healthcare
tags:
  - uncertainty
  - calibration
  - evaluation
aliases:
  - 保形預測
  - 共形預測
  - Conformal Prediction
  - distribution-free prediction
---

# Conformal Prediction

Conformal prediction wraps any predictive model so that its outputs carry a finite-sample coverage guarantee. For regression it returns an interval, and for classification a set of labels, that contains the true answer with a probability the user chooses. The guarantee needs no particular model and no assumption about the shape of the data distribution. The method is one of the approaches compared on the [uncertainty and calibration](../index.md) page.

## Overview

Angelopoulos and Bates (2021) describe conformal prediction as a user-friendly way to build uncertainty sets for black-box models. The sets are valid in a distribution-free sense, their guarantees hold at finite sample sizes, and the method works with any pre-trained model, including a neural network.

It answers a different question from [calibration](../index.md). Calibration asks whether the probabilities are honest. Conformal prediction asks whether the sets contain the truth as often as promised, and a set can be valid even when the underlying probabilities are poor. Lei et al. (2016) laid the groundwork for regression with any estimator.

## Key concepts

- **Coverage level.** The target probability \(1-\alpha\), for example 90%.
- **Nonconformity score.** A number \(s(x, y)\) that measures how poorly label \(y\) fits input \(x\). For regression it can be the absolute residual \(|y - \hat\mu(x)|\). For classification it can be one minus the predicted probability of the label.
- **Exchangeability.** The calibration data and the new test point must be exchangeable, meaning their order carries no information. Independent and identically distributed data satisfies this.
- **Marginal versus conditional coverage.** The guarantee holds on average over inputs. It does not promise the same coverage for every subgroup or every input.

## How it works

Given \(n\) calibration pairs with scores \(s_1, \dots, s_n\), let \(\hat{q}\) be the \(\lceil (n+1)(1-\alpha)\rceil\)-th smallest score. The prediction set for a new input is

\[
C(x) = \{\, y : s(x, y) \le \hat{q} \,\},
\]

and if the calibration and test pairs are exchangeable,

\[
P\big(Y_{n+1} \in C(X_{n+1})\big) \ge 1 - \alpha.
\]

For regression with the absolute-residual score, the set is the interval \([\hat\mu(x) - \hat{q}, \hat\mu(x) + \hat{q}]\).

The procedure is as follows.

1. Split the labelled data into a training set and a calibration set.
2. Train any model on the training set.
3. Compute the nonconformity scores on the calibration set.
4. Compute \(\hat{q}\) from those scores at the chosen level.
5. For each new input, return every label whose score falls at or below \(\hat{q}\).

## Results

Lei et al. (2016) develop split and full conformal inference for regression. The abstract states that the resulting prediction bands guarantee finite-sample marginal coverage even when the usual assumptions fail, and it compares the variants by the trade-off between interval length and computation. Romano et al. (2019) combine conformal prediction with quantile regression, with a theoretical guarantee of valid coverage and shorter intervals than other conformal methods in experiments on popular regression datasets. Angelopoulos et al. (2020) modify a conformal classifier to output sets with a formal finite-sample coverage guarantee for any model. On ImageNet and ImageNet-V2, with ResNet-152 and other classifiers, they report sets that are often 5 to 10 times smaller than those from a stand-alone Platt scaling baseline.[^1] Exact numbers are in the papers.

## Limitations

- **Marginal guarantee.** Coverage holds on average. Some subgroups or unusual inputs may be covered less often than the nominal level.
- **Exchangeability.** Distribution shift and time series break the assumption. The tutorial discusses extensions for these settings, which need care.
- **Coverage is not calibration.** A set with correct coverage does not certify that the probabilities behind it are right, so the two tools answer different questions.
- **Informative only if the model is good.** A weak model gives large, less useful sets.

## Open questions

- How close to conditional coverage can practical methods get, and at what cost in set size?
- Can coverage be maintained under distribution shift without new labels?
- How should the guarantees be extended to structured outputs and to models that abstain? The tutorial covers both.

## Connections

[Temperature scaling](../temperature-scaling/index.md) fixes probabilities after training, and conformal prediction fixes the sets. Both use a held-out split, and the Platt scaling baseline in the Angelopoulos et al. (2020) comparison shows how the two relate. The [probabilistic methods](../../../probabilistic/index.md) page covers the Bayesian route to intervals, which depends on the model and prior being specified correctly. Conformal prediction avoids that dependence by making a distribution-free claim instead. It has no direct brain-mind link; it is a statistical guarantee, not a model of cognition.

## References

### Seminal papers

- Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J. & Wasserman, L. (2016). Distribution-free predictive inference for regression. arXiv. https://arxiv.org/abs/1604.04173 — Develops split and full conformal inference for regression, with finite-sample marginal coverage for any estimator.
- Romano, Y., Patterson, E. & Candès, E. J. (2019). Conformalized quantile regression. arXiv. https://arxiv.org/abs/1905.03222 — Combines conformal prediction with quantile regression to produce intervals that adapt to varying noise, with valid coverage.
- Angelopoulos, A. N., Bates, S., Malik, J. & Jordan, M. I. (2020). Uncertainty sets for image classifiers using conformal prediction. arXiv. https://arxiv.org/abs/2009.14193 — Modifies a conformal classifier to produce small prediction sets with a formal coverage guarantee for image classifiers.

### Surveys and textbooks

- Angelopoulos, A. N. & Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv. https://arxiv.org/abs/2107.07511 — Hands-on tutorial with Python examples, covering the basic method and its extensions to shift, time series and structured outputs.

### Articles and documentation

- Ovadia, Y. et al. (2019). Can you trust your model's uncertainty? Evaluating predictive uncertainty under dataset shift. NeurIPS. https://arxiv.org/abs/1906.02530 — Benchmark of predictive uncertainty under dataset shift, the setting in which exchangeability is most at risk.

[^1]: From the abstract of Angelopoulos et al. (2020), which reports it on ImageNet and ImageNet-V2.
