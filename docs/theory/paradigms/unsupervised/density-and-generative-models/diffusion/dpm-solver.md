---
status: draft
last_reviewed: 2026-11-25
tags:
  - diffusion models
  - sampling
  - ODE solvers
aliases:
  - DPM-Solver
  - DPM 求解器
  - 擴散 ODE 求解器
  - 免訓練快速求解器
---

# DPM-Solver: a fast ODE solver for diffusion sampling

DPM-Solver (Lu et al., 2022) is a training-free solver for the ordinary differential equation (ODE) that a trained diffusion model defines. It produces good samples in about 10 to 20 network evaluations, using the same model that a slow sampler would use. The family-level picture is on the [Diffusion Models](index.md) page. The sampler it generalises is [DDIM](ddim.md), which the paper shows to be its first-order special case.

## Overview

A diffusion model can be sampled by integrating an ODE from noise to data. The ODE is deterministic, so a numerical solver can take large steps, and the cost of sampling is the number of steps times the cost of one evaluation of the network. Generic ODE solvers treat the whole right-hand side as a black box. DPM-Solver instead uses the form of the diffusion ODE. Part of its solution can be computed exactly, and only the rest has to be approximated, which allows a few large steps to stay accurate.

## Problem

Sampling a diffusion model with a standard numerical solver needs hundreds or thousands of steps to reach high quality. Lu et al. (2022) ask whether a dedicated solver, built for diffusion ODEs and needing no retraining, can reach that quality in about 10 steps. The paper frames this as a problem for "fast and training-free sampling" of diffusion probabilistic models.

## Core idea

The diffusion ODE has the form \( \frac{dx_t}{dt} = f(t)\,x_t + \frac{g^2(t)}{2\sigma_t}\,\epsilon_\theta(x_t, t) \), where \(f\) and \(g\) define the forward noising process and \(\epsilon_\theta\) is the noise-prediction network. The key steps in the paper are:

1. **Change the time variable.** Define the half log-signal-to-noise ratio \( \lambda_t = \log(\alpha_t / \sigma_t) \). This quantity decreases strictly with \(t\), so it can replace \(t\) as the integration variable.
2. **Integrate the linear part exactly.** Because the ODE is semi-linear, the solution from time \(s\) to time \(t\) is an exact linear scaling of the earlier state plus an integral of the network output:

\[
x_t = \frac{\alpha_t}{\alpha_s}\,x_s - \alpha_t \int_{\lambda_s}^{\lambda_t} e^{-\lambda}\,\hat\epsilon_\theta(\hat x_\lambda, \lambda)\,d\lambda .
\]

3. **Approximate only the integral.** Expand the network output in a Taylor series in \(\lambda\) around the start of each step. Keeping \(k\) terms gives a solver of order \(k\), and the integral of each term has a closed form. The paper names the resulting solvers DPM-Solver-1, -2 and -3.

For the handcrafted schedule, the paper places the time steps uniformly in \(\lambda\) rather than in \(t\). The paper also proposes an adaptive step-size schedule, and reports both.

## Algorithm

With \(h_i = \lambda_{t_i} - \lambda_{t_{i-1}}\), the first-order update (DPM-Solver-1) is

\[
\tilde x_{t_i} = \frac{\alpha_{t_i}}{\alpha_{t_{i-1}}}\,\tilde x_{t_{i-1}} - \sigma_{t_i}\left(e^{h_i} - 1\right)\epsilon_\theta(\tilde x_{t_{i-1}}, t_{i-1}).
\]

The second and third order solvers evaluate the network at one or two intermediate times inside each step, and combine the results. The paper's fast variant for a fixed budget of evaluations uses DPM-Solver-3 steps wherever possible. If the number of evaluations is not divisible by three, one DPM-Solver-1 or DPM-Solver-2 step is added to use up the budget exactly.

The first-order update is the same as a DDIM step. The paper shows this by writing the DDIM update in the \(\lambda\) variable, which gives an identical formula. DPM-Solver therefore contains DDIM as its lowest-order member, and adds higher orders above it.

## Results

The abstract reports 4.70 FID in 10 function evaluations and 2.87 FID in 20 on CIFAR-10, and a 4 to 16 times speed-up over the previous training-free samplers on several datasets.

The paper's comparison table for a discrete-time model on CIFAR-10, with a linear noise schedule, compares DPM-Solver with DDIM at the same number of evaluations. The ε in the table is the smallest time step used in sampling, which the paper sets to 10⁻³ or 10⁻⁴:

| Sampler (CIFAR-10, discrete-time model) | FID at 10 evaluations | FID at 20 evaluations |
|---|---|---|
| [DDIM](ddim.md) | 13.58 | 6.94 |
| DPM-Solver, type 1, ε = 10⁻³ | 6.37 | 4.28 |
| DPM-Solver, type 2, ε = 10⁻⁴ | 10.16 | 3.72 |

At 10 evaluations the type-1 solver is clearly better than type 2 in this table, and at 20 evaluations the type-2 solver is better. The paper says the same pattern holds more generally: type 1 with ε = 10⁻³ may be better for a small number of evaluations, and type 2 with ε = 10⁻⁴ for a large number.

## Limitations

- **Designed for sampling, not for likelihoods.** The paper notes that the solver is built for fast sampling and "may be not suitable for accelerating the likelihood evaluations of DPMs".
- **Not real-time.** The paper states that diffusion models with DPM-Solver are still not fast enough for real-time applications, where GANs remain much faster.
- **Settings matter.** The best time limit and solver order depend on the number of evaluations, as the table above shows. A single setting is not best across the whole range.
- **Experiments are on the authors' models.** The reported results use pretrained models and datasets chosen by the authors. Later work that tests these samplers on other models is needed to judge how far the gains carry over.

## Connections

- DDIM is the first-order member of DPM-Solver. The [DDIM](ddim.md) page describes its sampler and results.
- Distillation gives a different route to few-step sampling. It changes the model by training, where DPM-Solver changes only the sampler. See [Progressive distillation](progressive-distillation.md) and [Consistency models and fast samplers](consistency-models.md).
- The probability-flow ODE that DPM-Solver integrates comes from the stochastic-differential-equation view of diffusion, described by Song et al. (2021) and summarised on the [Score SDE](score-sde.md) page.

## Open questions

- How far can a training-free solver go when the model is strongly conditioned, for example with classifier-free guidance?
- Is the uniform spacing in \(\lambda\) the best schedule for every model, or only a good default?
- How much of the gap to a many-step sampler remains at 10 evaluations, and does it close with a better model rather than a better solver?

## References

### Seminal papers

- Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C. & Zhu, J. (2022). *DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps*. In *NeurIPS 2022*. https://arxiv.org/abs/2206.00927 — Introduces the exact semi-linear solution of the diffusion ODE and the DPM-Solver family of orders 1 to 3, with results at 10 to 20 evaluations.
- Song, J., Meng, C. & Ermon, S. (2021). *Denoising Diffusion Implicit Models*. In *ICLR 2021*. https://arxiv.org/abs/2010.02502 — The deterministic, non-Markovian sampler that DPM-Solver-1 reproduces.
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). *Score-Based Generative Modeling through Stochastic Differential Equations*. In *ICLR 2021*. https://arxiv.org/abs/2011.13456 — Defines the probability-flow ODE that DPM-Solver integrates.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. In *NeurIPS 2020*. https://arxiv.org/abs/2006.11239 — The trained model and noise-prediction objective that the solver samples from.

### Surveys and textbooks

- Yang, L., Zhang, Z., Song, Y., Hong, S., Xu, R., Zhao, Y., Zhang, W., Cui, B. & Yang, M.-H. (2022). *Diffusion Models: A Comprehensive Survey of Methods and Applications*. arXiv. https://arxiv.org/abs/2209.00796 — Survey of diffusion models that covers fast samplers alongside the training methods.
