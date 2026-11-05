---
status: draft
last_reviewed: 2026-11-05
tags:
  - causal inference
  - double machine learning
  - treatment effects
aliases:
  - Double machine learning
  - DML
  - 雙重機器學習
  - 雙重／去偏機器學習
  - 去偏機器學習
---

# Double/Debiased Machine Learning

Double/debiased machine learning (DML) estimates one causal parameter, such as an average treatment effect, when the rest of the model is fitted with flexible machine learning. It is the estimation step behind the [causal inference overview](index.md), where flexible learners are used without biasing the effect.

## Problem

Consider the partially linear model (Chernozhukov et al. 2018):

$$Y = D\theta_0 + g_0(X) + U, \qquad D = m_0(X) + V,$$

where $Y$ is the outcome, $D$ the treatment, $X$ a possibly high-dimensional set of covariates, $\theta_0$ the effect of interest, and $U$ and $V$ noise terms. The functions $g_0$ and $m_0$ are *nuisance functions*. They are not the target, but they must be estimated to isolate $\theta_0$.

If a flexible learner is fitted to $Y$ on $(D, X)$ and the coefficient on $D$ is read off, the regularisation applied to $X$ leaks into the estimate of $\theta_0$. The result is a bias that does not shrink fast enough for valid confidence intervals.

## Core idea

Robinson (1988) showed that $\theta_0$ can be recovered by regressing residualised outcomes on residualised treatments, which removes $X$ from both. Define the conditional expectations $\ell_0(X) = E[Y \mid X]$ and $m_0(X) = E[D \mid X]$. The orthogonal (Neyman) score is

$$\psi(W;\theta,\eta) = \big(Y - \ell(X) - \theta\,(D - m(X))\big)\,(D - m(X)),$$

where $\eta = (\ell, m)$ collects the nuisance functions. Its expectation is zero at the true $\theta_0$ and the true nuisances. Because the score is orthogonal to the nuisances, first-order errors in the machine-learning estimates of $\ell$ and $m$ do not pass directly into $\hat\theta$. This insensitivity is what "orthogonal" refers to.

With the nuisances estimated, the score gives the familiar residual-on-residual estimator

$$\hat\theta = \frac{\sum_i (D_i - \hat m(X_i))\,(Y_i - \hat\ell(X_i))}{\sum_i (D_i - \hat m(X_i))^2}.$$

## Algorithm

The method adds cross-fitting, a sample-splitting step that stops the nuisance models from overfitting the observations they are evaluated on:

1. Split the sample at random into $K$ folds (commonly $K = 5$ or $10$).
2. For each fold $k$, fit $\hat\ell$ and $\hat m$ on the other folds, then compute the residuals $\hat U_i = Y_i - \hat\ell(X_i)$ and $\hat V_i = D_i - \hat m(X_i)$ for the observations in fold $k$.
3. Pool all residuals and compute $\hat\theta = \sum_i \hat V_i \hat U_i \big/ \sum_i \hat V_i^2$.
4. Estimate the variance from the empirical variance of the score, $\hat\psi_i = \hat V_i \hat U_i - \hat\theta \hat V_i^2$, and form the interval $\hat\theta \pm 1.96\,\hat\sigma/\sqrt{n}$, where $\hat\sigma^2 = \frac{1}{n}\sum_i \hat\psi_i^2 \big/ \big(\frac{1}{n}\sum_i \hat V_i^2\big)^2$.

## Results

The framework's central claim is asymptotic. The 2016 preprint's abstract says the de-biased estimator built from an orthogonal score typically converges at the fastest possible $1/\sqrt{n}$ rate and is approximately unbiased and normal, which supports confidence intervals. The guarantee holds under conditions on the nuisance estimators. The paper's simulations and empirical examples are the finite-sample evidence and are not reproduced here.

## Limitations

- **No unmeasured confounding.** DML estimates a causal effect only when the covariates $X$ block all confounding. The estimator cannot check this assumption.
- **Nuisance accuracy.** The guarantee needs the machine-learning estimates of $\ell$ and $m$ to be accurate enough that their errors, multiplied together, shrink fast enough.
- **One low-dimensional parameter.** The framework targets a single average effect. Effects that vary across people need a different method, such as [causal forests](causal-forests.md).
- **Model form.** The partially linear model is an assumption. The framework extends to other models, but each needs its own score.
- **Compute.** Cross-fitting fits the nuisance models $K$ times.

## Connections

DML turns the flexible models discussed in the [causal inference overview](index.md) into a valid estimator for one effect. For effects that differ across individuals, see [causal forests](causal-forests.md). The general learning theory behind fitting flexible models is in the [Machine Learning](../machine-learning/index.md) chapter.

## Applications

- Estimating the effect of a policy, price or treatment when many observed controls are available. The 2024 survey by Chernozhukov et al. collects worked examples.
- Software: the DoubleML packages implement the framework for Python and R.

## Open questions

- How to keep the nuisance-rate conditions satisfied in very high dimensions and with complex dependence in the data.
- Extending the orthogonal score beyond the partially linear model and average effects, to instrumental variables, panel data and dynamic treatments.
- Inference when overlap is weak, that is, when treatment is almost fully determined by $X$.

## References

### Seminal papers

- Robinson, P. M. (1988). Root-N-Consistent Semiparametric Regression. *Econometrica*, 56(4), 931. doi:[10.2307/1912705](https://doi.org/10.2307/1912705) — Introduces the residual-on-residual estimator in the partially linear model, which the DML score generalises.
- Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W. & Robins, J. (2016). *Double/Debiased Machine Learning for Treatment and Causal Parameters*. arXiv. https://arxiv.org/abs/1608.00060 — Preprint of the framework: orthogonal scores and cross-fitting for flexible nuisance models.
- Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W. & Robins, J. (2018). Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1–C68. doi:[10.1111/ectj.12097](https://doi.org/10.1111/ectj.12097) — The published version of the framework, with the general theory of the orthogonal estimator.
- Chernozhukov, V., Chetverikov, D., Demirer, M., Duflo, E., Hansen, C., Newey, W. & Robins, J. (2017). Double/Debiased/Neyman Machine Learning of Treatment Effects. *American Economic Review*, 107(5), 261–265. doi:[10.1257/aer.p20171038](https://doi.org/10.1257/aer.p20171038) — A short summary of the framework for applied economists.

### Surveys and textbooks

- Chernozhukov, V., Hansen, C., Kallus, N., Spindler, M. & Syrgkanis, V. (2024). *Applied Causal Inference Powered by ML and AI*. arXiv. https://arxiv.org/abs/2403.02467 — Book-length introduction to combining machine learning with causal inference, including DML.

### Articles and documentation

- DoubleML. *DoubleML documentation*. https://docs.doubleml.org/stable/index.html — Software documentation for the Python and R packages that implement the framework, with worked examples.
