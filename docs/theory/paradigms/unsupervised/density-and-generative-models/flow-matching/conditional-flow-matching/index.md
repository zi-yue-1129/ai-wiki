---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - generative models
  - diffusion models
aliases:
  - 條件流匹配
  - 條件式流匹配
  - CFM
  - Conditional flow matching
  - Flow matching
---

# Conditional Flow Matching

Conditional flow matching (CFM) is the regression objective that Lipman et al. (2022) introduced as *flow matching*. It trains a continuous normalising flow by fitting a velocity field to the known velocities of conditional probability paths, so the flow never has to be simulated during training. It is the foundational method of the [Flow Matching and Rectified Flow](../index.md) topic.

## Overview

Continuous normalising flows define a generative model by an ODE: a velocity field moves samples from a simple base distribution to the data distribution. Maximum-likelihood training of such models needs the ODE solution, and its gradient, at every step, which is expensive. Lipman et al. (2022) proposed training the velocity field by regression on *fixed conditional paths*. Each path is defined for one data point, so its velocity is known in closed form. The authors show that regressing on these conditional velocities trains the same model as regressing on the intractable marginal velocity.

The framework works for any family of Gaussian conditional paths, and diffusion paths are one such family. The paper highlights optimal-transport displacement paths as an efficient choice, developed in [OT-CFM](../ot-cfm/index.md).

## Key concepts

- **Conditional probability path** \(p_t(x \mid x_1)\): a distribution that moves from a base distribution at \(t=0\) to a narrow distribution around the data point \(x_1\) at \(t=1\).
- **Conditional velocity** \(u_t(x \mid x_1)\): the velocity field that generates the conditional path.
- **Marginal velocity**: the average of the conditional velocities over data points, given the current position. It generates the marginal path, but it cannot be computed in practice.
- **Gaussian path**: a path whose distribution at each time is Gaussian, with mean and standard-deviation schedules \(\mu_t\) and \(\sigma_t\).
- **Simulation-free training**: training that never runs the ODE solver.

## How it works

Take the Gaussian conditional path with mean \(\mu_t(x_1) = t\,x_1\) and standard deviation \(\sigma_t = 1-(1-\sigma_{\min})\,t\), for a small constant \(\sigma_{\min} > 0\). A sample at time \(t\) is \(x = \mu_t(x_1) + \sigma_t\,x_0\), with \(x_0 \sim \mathcal{N}(0, I)\). The flow that generates this path has the conditional velocity

\[
u_t(x \mid x_1) = \frac{x_1 - (1-\sigma_{\min})\,x}{1-(1-\sigma_{\min})\,t}
\]

Training then follows these steps:

1. Sample a data point \(x_1\), a time \(t \sim \mathcal{U}[0,1]\) and noise \(x_0 \sim \mathcal{N}(0, I)\).
2. Form the point \(x = t\,x_1 + \sigma_t\,x_0\) on the path.
3. Take a gradient step on \(\|v_\theta(x, t) - u_t(x \mid x_1)\|^2\).

The paper shows that the gradient of this conditional loss equals the gradient of the marginal loss, up to a constant. The trained network therefore approximates the marginal velocity field, even though the regression targets are conditional.

Sampling draws \(x(0) \sim \mathcal{N}(0, I)\) and integrates \(\frac{dx}{dt} = v_\theta(x, t)\) up to \(t=1\) with any ODE solver. Each solver step costs one network evaluation. The same ODE also yields exact likelihoods through the change-of-variables formula.

## Results

The paper trains models on ImageNet and compares them with diffusion-based methods. According to its abstract:

- Flow matching trained on ImageNet gives consistently better results than alternative diffusion-based methods, measured by likelihood and by sample quality.
- Using diffusion paths inside flow matching gives a more robust and stable alternative for training diffusion models.
- Optimal-transport displacement paths are more efficient than diffusion paths, with faster training and sampling and better generalisation.

The abstract does not report the numerical scores, so none are quoted here. The paper's tables give them.

## Limitations

- The abstract reports ImageNet experiments. It does not establish performance on other data types, which the authors note as a direction the framework opens rather than a result.
- The choice of Gaussian path is a design decision. The regression is exact for whichever path is used, but which path works best is an empirical question.
- Sampling still needs several ODE steps when paths are curved. Fewer steps require straighter paths, the motivation for [rectified flow](../rectified-flow/index.md).
- Exact likelihood evaluation through the ODE requires integrating a divergence term, which adds cost.

## Open questions

- Which family of conditional paths gives the best quality at scale, and does the answer depend on the type of data?
- How should the schedules \(\mu_t\) and \(\sigma_t\), including \(\sigma_{\min}\), be chosen?
- How do the objective and the sampler interact with guidance and with distillation to fewer steps?

## References

### Seminal papers

- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — The paper itself: the conditional regression objective, the Gaussian paths and the ImageNet experiments described here.
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. NeurIPS. https://arxiv.org/abs/1806.07366 — Defines continuous-depth networks trained through ODE solvers, the model class whose costly training flow matching avoids.
- Grathwohl, W. et al. (2018). *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*. arXiv. https://arxiv.org/abs/1810.01367 — A continuous normalising flow trained by maximum likelihood, which requires solving the ODE during training.
- Song, Y. et al. (2020). *Score-Based Generative Modeling through Stochastic Differential Equations*. arXiv. https://arxiv.org/abs/2011.13456 — Shows that a diffusion model's SDE has a probability-flow ODE with the same marginal densities, the deterministic view on which flow models build.

### Surveys and textbooks

- Lipman, Y. et al. (2024). *Flow Matching Guide and Code*. arXiv. https://arxiv.org/abs/2412.06264 — A self-contained review of flow matching's mathematics, design choices and extensions, with worked examples.
- Holderrieth, P. & Erives, E. (2025). *An Introduction to Flow Matching and Diffusion Models*. arXiv. https://arxiv.org/abs/2506.02070 — A tutorial that derives the conditional flow matching objective from first principles.
