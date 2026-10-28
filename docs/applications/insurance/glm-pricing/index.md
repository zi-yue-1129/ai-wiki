---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/linear-models
tags:
  - regression
  - tabular data
aliases:
  - 廣義線性模型
  - 廣義線性模型定價
  - Tweedie
  - GLM
  - Generalized linear models
---

# Generalised Linear Models for Insurance Pricing (Nelder & Wedderburn 1972)

A generalised linear model (GLM) relates the mean of a response, such as a claim count or claim cost, to a weighted sum of explanatory variables through a link function. It is the standard tool for insurance tariffs, and it is one of the methods described on the parent page [Insurance and Actuarial Science](../index.md).

## Overview

Ordinary linear regression assumes a normal response with constant variance. Insurance data break both assumptions: claim counts are whole numbers, most policies have no claims, and claim costs are positive and skewed. Nelder and Wedderburn (1972) generalised regression so that the response may follow any distribution from the exponential family, with a link function connecting its mean to a linear predictor. Jørgensen (1987) extended this to exponential dispersion models, which add a dispersion parameter and include the Tweedie family.

In tariff work the log link is the usual choice. Effects then multiply, so each coefficient becomes a relativity, the factor by which a risk is priced relative to a base level. That multiplicative structure is easy to explain to regulators and to underwriters, which explains much of the method's persistence. [Ohlsson and Johansson (2010)](https://doi.org/10.1007/978-3-642-10791-7) describe the full practice.

## Key concepts

- **Linear predictor and link**: $\eta_i = x_i^\top \beta$ and $g(\mu_i) = \eta_i$. With a log link, $\mu_i = \exp(x_i^\top \beta)$.
- **Exposure offset**: a policy that runs for half a year should produce about half the claims. This is handled by adding $\log v_i$ to the linear predictor, where $v_i$ is the exposure.
- **Relativity**: $\exp(\beta_j)$, the multiplicative effect of a rating factor level.
- **Tweedie distribution**: a compound Poisson sum of gamma-distributed claims, with variance $\mathrm{Var}(Y) = \phi\,\mu^{p}$ and power $1 < p < 2$. It has a point mass at zero and a continuous positive part, which fits total cost per policy directly.
- **Dispersion modelling**: letting the dispersion $\phi$ depend on covariates, as in double generalised linear models.

## How it works

For claim counts, the usual model is a Poisson GLM with log link and exposure offset. Its parameters are estimated by maximum likelihood, equivalently by minimising the Poisson deviance. The fitting algorithm is iteratively reweighted least squares, which repeatedly solves a weighted regression until the coefficients converge.

A typical workflow for a tariff runs as follows.

1. Choose the response distribution and link for each part of the price: counts with Poisson, costs with gamma, or total cost with Tweedie.
2. Add the exposure offset and encode categorical factors as dummy variables.
3. Fit the model by iteratively reweighted least squares, and check the fit against held-out data.
4. Test interactions and smooth terms, such as splines for age, one at a time.
5. Convert the coefficients to relativities, and combine the frequency and severity relativities into the tariff.

## Results

Nelder and Wedderburn's paper is a framework paper. Its contribution is a single fitting procedure that covers many standard models, not a benchmark result. The insurance-specific evidence comes from later applied work. Smyth and Jørgensen (2002) reconsider tariffs built from aggregated claims data. According to their abstract, modelling the dispersion of claim costs as well as their mean increases the precision of the estimated tariffs, and the approach still works when only total claim cost, and not the number of claims, has been recorded.

## Limitations

- **Linearity on the link scale.** Non-linear effects and interactions must be specified by hand, which takes time and expertise. Machine learning methods can find them automatically.
- **Distributional assumptions.** A wrong variance function, or a family that does not fit the data, produces biased tariffs even when the mean structure is right.
- **Manual feature engineering.** Much of the predictive work sits in choices made by the analyst, which makes results depend on the team.
- **Transparency is not fairness.** A GLM can be fully transparent and still price through proxies for protected characteristics. The auditing questions are discussed on the parent page and on [Fairness Definitions](../../../society/ethics/fairness-definitions.md).

## Open questions

- On standard insurance datasets with the same features, how much predictive accuracy do GLMs give up against boosted trees and interpretable neural networks, out of sample?
- Can the mean and the dispersion be modelled jointly with richer structures, such as random effects for regions, without losing the readability that makes GLM tariffs acceptable?

## References

### Seminal papers

- Nelder, J. A. & Wedderburn, R. W. M. (1972). Generalized Linear Models. *Journal of the Royal Statistical Society, Series A*. https://doi.org/10.2307/2344614 — Introduces generalised linear models, with a link function and a fitting procedure shared across distributions.
- Jørgensen, B. (1987). Exponential Dispersion Models. *Journal of the Royal Statistical Society, Series B*. https://doi.org/10.1111/j.2517-6161.1987.tb01685.x — Extends the GLM error family to exponential dispersion models, the family that includes the Tweedie distributions.
- Smyth, G. K. & Jørgensen, B. (2002). Fitting Tweedie's Compound Poisson Model to Insurance Claims Data: Dispersion Modelling. *ASTIN Bulletin*. https://doi.org/10.2143/ast.32.1.1020 — Applies double generalised linear models to Tweedie claims data, modelling dispersion as well as the mean.

### Surveys and textbooks

- Ohlsson, E. & Johansson, B. (2010). *Non-Life Insurance Pricing with Generalized Linear Models*. Springer. https://doi.org/10.1007/978-3-642-10791-7 — Practitioner-oriented textbook on building non-life tariffs with GLMs, including factor selection and validation.
- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — Covers GLMs and neural networks for actuarial data, with the fitting theory behind them.
- Wüthrich, M. V. & Buser, C. (2017). Data Analytics for Non-Life Insurance Pricing. SSRN. https://doi.org/10.2139/ssrn.2870308 — Lecture notes on pricing data, GLMs and tree-based models for non-life insurance.
