---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
tags:
  - flow matching
  - stochastic interpolants
  - diffusion models
aliases:
  - Stochastic interpolants
  - 隨機插值
---

# Stochastic Interpolants

Stochastic interpolants are a framework by Albergo and Vanden-Eijnden (2023) for building a time-dependent path between two distributions and learning a velocity field along it. The framework covers flow matching and diffusion models as two members of one family. The follow-up work by Albergo, Boffi and Vanden-Eijnden adds a noise term to the interpolant and connects the construction more closely to diffusion. The family overview is on the [Flow Matching](index.md) page.

## Overview

Earlier flow and diffusion methods each fix one way of connecting noise to data. A stochastic interpolant is a general function \(I(t, x_0, x_1)\) of a noise sample \(x_0\) and a data sample \(x_1\), with boundary conditions that place \(x_0\) at \(t=0\) and \(x_1\) at \(t=1\). Any choice of interpolant gives a probability path, and a velocity field can be learned for it. This separates the choice of path from the training method.

## Key concepts

- **Interpolant** \(I(t, x_0, x_1)\): a function with \(I(0, x_0, x_1) = x_0\) and \(I(1, x_0, x_1) = x_1\), and with \(|\partial_t I| \le C_1 |x_0 - x_1|\). The paper's example is the trigonometric choice \(\cos(\tfrac{\pi}{2}t)\,x_0 + \sin(\tfrac{\pi}{2}t)\,x_1\).
- **Probability path**: the distribution of \(I_t = I(t, x_0, x_1)\) when \(x_0\) and \(x_1\) are drawn independently from their marginals \(\rho_0\) and \(\rho_1\).
- **Velocity**: the time derivative \(\partial_t I_t\). Its conditional expectation given \(I_t = x\) is the marginal velocity field \(v(t, x)\).

## How it works

The paper learns a velocity estimate \(\hat v_t\) by minimising

\[
G(\hat v) = \mathbb E\big[\lVert \hat v_t(I_t)\rVert^2 - 2\,\partial_t I_t \cdot \hat v_t(I_t)\big]
\]

The unique minimiser is the marginal velocity \(v(t, x) = \mathbb E[\partial_t I_t \mid I_t = x]\). The paper notes that the squared-error form \(\mathbb E\lVert \hat v_t(I_t) - \partial_t I_t\rVert^2\) has the same first variations as \(G\), so it can be used in its place. Its value at the optimum is not zero in general, so it is a different objective with the same stationary direction. Sampling integrates the learned ODE from \(t=0\) to \(t=1\).

## Key methods

### Building Normalizing Flows with Stochastic Interpolants (Albergo & Vanden-Eijnden, 2023)

- **Problem:** flow and diffusion models are usually presented as separate constructions, which makes it hard to compare their paths or to choose one for a new problem.
- **Core idea:** define the path by an interpolant between samples from two distributions, and learn the velocity along it by regression. Any interpolant satisfying the boundary conditions is allowed.
- **Equation or algorithm:** the regression objective \(G(\hat v)\) above, with the interpolant chosen by the designer. Each step draws \(t\), \(x_0\) and \(x_1\), forms \(I_t\), and updates \(\hat v\) on the objective. Sampling uses the probability flow ODE.
- **Results:** the paper reports density estimation and image generation experiments rather than one benchmark. On the five tabular datasets in its table, the method beats FFJORD on four, while FFJORD is slightly better on BSDS300. On CIFAR-10 and ImageNet 32×32 the FID values are, in the paper's words, "proximal to those from diffusions, though slightly behind the best results." The paper also reports image experiments at 128×128.
- **Limitations:** the paper states that the drift and diffusion coefficients of the associated SDE are singular at \(t=0\) and \(t=1\), so the ODE is the practical sampler. The choice of interpolant is left to the designer.

### Stochastic Interpolants: A Unifying Framework for Flows and Diffusions (Albergo, Boffi & Vanden-Eijnden, 2023)

- **Problem:** the 2022 framework uses a deterministic interpolant, so it does not cover the stochastic sampler family in one construction with flows.
- **Core idea:** add a noise term to the interpolant. The general stochastic interpolant is \(x_t = I(t, x_0, x_1) + \gamma(t)\,z\), with \(z\sim\mathcal N(0, I)\) independent of \((x_0, x_1)\), \(\gamma(0)=\gamma(1)=0\) and \(\gamma(t)>0\) on \((0,1)\). The density of \(x_t\) matches the target at \(t=0\) and \(t=1\) exactly, which is what the paper means by bridging two densities in finite time.
- **Equation or algorithm:** the drift is learned with the quadratic velocity objective \(\mathcal L_b[\hat b] = \int_0^1 \mathbb E\big[\tfrac12\lvert\hat b(t, x_t)\rvert^2 - (\partial_t I + \dot\gamma(t)\,z)\cdot\hat b(t, x_t)\big]\,\mathrm dt\), whose minimiser is \(b(t, x) = \mathbb E[\dot x_t \mid x_t = x]\). The score is learned with \(\mathcal L_s[\hat s] = \int_0^1 \mathbb E\big[\tfrac12\lvert\hat s(t, x_t)\rvert^2 + \gamma^{-1}(t)\,z\cdot\hat s(t, x_t)\big]\,\mathrm dt\), with minimiser \(s = -\gamma^{-1}\eta_z\), where \(\eta_z(t, x) = \mathbb E[z \mid x_t = x]\). Forward and backward SDEs with diffusion coefficient \(\varepsilon(t)\) share the same marginals, and the paper shows that score-based diffusion models can be rewritten as one-sided interpolants after a change of time.
- **Results:** the paper is mainly a framework and proof paper. Its experiments section covers two-dimensional and 128-dimensional Gaussian mixtures and image generation. The numerical results were not checked in full for this page, so no figures are quoted here.
- **Limitations:** the SDE coefficients are singular at the endpoints, as in the 2022 paper. The paper also shows that optimising the interpolant recovers the Schrödinger bridge, but it notes that this optimisation is not needed in practice, since any fixed interpolant gives a bias-free model.

## Connections

- [Conditional flow matching](conditional-flow-matching.md) is one interpolant in this framework, namely the Gaussian optimal-transport path.
- [Rectified flow](rectified-flow.md) uses the linear interpolant \(t\,x_1 + (1-t)\,x_0\).
- [DDPM](../../diffusion/ddpm.md) and the [Diffusion Models](../../diffusion/index.md) page cover the diffusion side of the framework.

## Open questions

- Which interpolant gives the best sampling efficiency for a given data type.
- How the SDE and ODE samplers compare in quality and speed, given that the SDE coefficients are singular at the endpoints.

## References

### Seminal papers

- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — Introduces the interpolant framework, the regression objective \(G(\hat v)\), and the tabular and image experiments described on this page.
- Albergo, M. S., Boffi, N. M. & Vanden-Eijnden, E. (2023). *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*. arXiv. https://arxiv.org/abs/2303.08797 — Adds the noise term \(\gamma(t) z\), the forward and backward SDEs, and the quadratic drift and score objectives described on this page.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — The conditional flow matching objective, which is a special case of the interpolant framework.

### Diffusion background

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). *Score-Based Generative Modeling through Stochastic Differential Equations*. ICLR. https://arxiv.org/abs/2011.13456 — The SDE view of diffusion models, which the stochastic-interpolant SDEs generalise.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*. ICML. https://arxiv.org/abs/1503.03585 — The early diffusion model that the interpolant framework generalises.
