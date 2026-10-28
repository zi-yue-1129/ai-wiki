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

Stochastic interpolants are a framework by Albergo and Vanden-Eijnden (2023) for building a time-dependent path between two distributions and learning a velocity field along it. The framework covers flow matching and diffusion models as two members of one family. The follow-up work by Albergo, Boffi and Vanden-Eijnden extends the framework to noise terms and connects it more closely to diffusion. The family overview is on the [Flow Matching](index.md) page.

## Overview

Earlier flow and diffusion methods each fix one way of connecting noise to data. A stochastic interpolant is a general function \(I_t(x_0, x_1)\) of a noise sample \(x_0\) and a data sample \(x_1\), with boundary conditions that place \(x_0\) at \(t=0\) and \(x_1\) at \(t=1\). Any choice of interpolant gives a probability path, and a velocity field can be learned for it. This separates the choice of path from the training method.

## Key concepts

- **Interpolant** \(I_t(x_0, x_1) = a_t\,x_0 + b_t\,x_1\), with \(a_0 = 1\), \(a_1 = 0\), \(b_0 = 0\) and \(b_1 = 1\). The paper's example is \(\cos(\tfrac{\pi}{2}t)\,x_0 + \sin(\tfrac{\pi}{2}t)\,x_1\).
- **Probability path**: the distribution of \(I_t\) when \(x_0\) and \(x_1\) are drawn independently from their marginals \(\rho_0\) and \(\rho_1\).
- **Velocity**: the time derivative \(\partial_t I_t\), whose conditional expectation given \(I_t = x\) defines the marginal velocity field.

## How it works

The paper learns a velocity estimate \(\hat v_t\) by minimising

\[
G(\hat v) = \mathbb E\big[\lVert \hat v_t(I_t)\rVert^2 - 2\,\partial_t I_t \cdot \hat v_t(I_t)\big]
\]

The paper notes that the squared-error form \(\mathbb E\lVert \hat v_t(I_t) - \partial_t I_t\rVert^2\) has the same first variations, so it can be used as an alternative. Its minimiser is the conditional expectation of \(\partial_t I_t\) given \(I_t\), which is the marginal velocity. The method then integrates the learned ODE from \(t=0\) to \(t=1\) to sample.

## Key methods

### Building Normalizing Flows with Stochastic Interpolants (Albergo & Vanden-Eijnden, 2023)

- **Problem:** flow and diffusion models are usually presented as separate constructions, which makes it hard to compare their paths or to choose one for a new problem.
- **Core idea:** define the path by an interpolant between samples from two distributions, and learn the velocity along it by regression. Any interpolant satisfying the boundary conditions is allowed.
- **Equation or algorithm:** the regression objective \(G(\hat v)\) above, with the interpolant chosen by the designer. Each step draws \(t\), \(x_0\) and \(x_1\), forms \(I_t\), and updates \(\hat v\) on the objective.
- **Results:** the paper's main contribution is the framework and its objective, rather than a benchmark table.
- **Limitations:** the paper's method uses only the probability flow ODE. It also notes that the coefficients of the SDE that resamples the path are singular at \(t=0\) and \(t=1\). The choice of interpolant is left to the designer.

### Stochastic Interpolants: A Unifying Framework for Flows and Diffusions (Albergo, Boffi & Vanden-Eijnden, 2023)

- **Problem:** the 2022 framework allows no noise term in the interpolant, which limits how the same construction covers diffusion models.
- **Core idea:** add a noise term to the interpolant. The resulting stochastic interpolants connect two distributions exactly at finite time and unify flow-based and diffusion-based generative models.
- **Equation or algorithm:** the general interpolant with a noise component, trained with a regression objective of the same type. The arXiv abstract gives the unification claim, and the full equations should be checked in the paper before reuse.
- **Limitations:** the framework itself is general, so practical performance depends on the choice of interpolant and on the training and sampling procedure used with it.

## Connections

- [Conditional flow matching](conditional-flow-matching.md) is one interpolant in this framework, namely the Gaussian optimal-transport path.
- [Rectified flow](rectified-flow.md) uses the linear interpolant \(t\,x_1 + (1-t)\,x_0\).
- [DDPM](../../diffusion/ddpm.md) and the [Diffusion Models](../../diffusion/index.md) page cover the diffusion side of the framework.

## Open questions

- Which interpolant gives the best sampling efficiency for a given data type.
- How the SDE and ODE samplers compare in quality and speed.

## References

### Seminal papers

- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — Introduces the interpolant framework and the regression objective \(G(\hat v)\) described on this page.
- Albergo, M. S., Boffi, N. M. & Vanden-Eijnden, E. (2023). *Stochastic Interpolants: A Unifying Framework for Flows and Diffusions*. arXiv. https://arxiv.org/abs/2303.08797 — Extends the framework with noise terms and connects flows and diffusions.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — The conditional flow matching objective, which is a special case of the interpolant framework.

### Diffusion background

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). *Score-Based Generative Modeling through Stochastic Differential Equations*. ICLR. https://arxiv.org/abs/2011.13456 — The SDE view of diffusion models, which the stochastic-interpolant SDE generalises.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). *Deep Unsupervised Learning using Nonequilibrium Thermodynamics*. ICML. https://arxiv.org/abs/1503.03585 — The early diffusion model that the interpolant framework generalises.
