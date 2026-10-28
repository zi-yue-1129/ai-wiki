---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/transformer
tags:
  - generative models
  - normalising flows
  - unsupervised learning
aliases:
  - 流模型
  - Flow-based generative models
  - Normalising flows
  - Flow matching
---

# Flow-Based Generative Models

Flow-based generative models build a distribution by transforming a simple one through a chain of invertible maps. Because each map can be inverted and its Jacobian determinant is tractable, the exact likelihood of any data point can be computed, which the [VAE](../vae/index.md) and [GAN](../gan/index.md) cannot do. This page compares the two main branches: normalising flows with discrete invertible layers, and flow matching, which learns a continuous velocity field. The method pages are [Normalising Flows](normalising-flows/index.md) and [Flow Matching](flow-matching/index.md). The family-level comparison is on the [Generative Models](../generative-models/index.md) page.

## Overview

Dinh, Krueger and Bengio (2014) introduced the idea with NICE, which maps data to a space where the components are independent. Dinh, Sohl-Dickstein and Bengio (2017) added affine coupling layers to make the maps more expressive while keeping the determinant cheap. Rezende and Mohamed (2015) had already made the general case for normalising flows, as a way to build flexible posterior approximations in variational inference. Flow matching (Lipman et al., 2023) approached the same goal from the continuous-time side, training a velocity field that moves noise to data.

## Key concepts

- **Change of variables**: if \(x = f(z)\) with \(z\sim p_z\) and \(f\) invertible, then \(\log p_x(x) = \log p_z(f^{-1}(x)) + \log\lvert\det \partial f^{-1}/\partial x\rvert\).
- **Coupling layer**: a transform that updates half of the dimensions using a function of the other half, so that the Jacobian is triangular.
- **Velocity field**: in flow matching, a time-dependent vector field whose ODE carries noise to data.
- **Continuous normalising flow**: a flow defined by an ODE, which gives an exact likelihood through the instantaneous change of variables.

## How it works

Normalising flows stack invertible layers \(f = f_K \circ \cdots \circ f_1\) and evaluate the likelihood with the change-of-variables formula above. Sampling draws \(z\) from the base distribution and applies \(f\). Training maximises the exact log-likelihood by gradient descent, with no adversarial game and no approximate posterior.

Flow matching instead defines a path \(x_t\) from noise \(x_0\) to data \(x_1\), trains a network \(v_\theta(x,t)\) to regress the path's velocity, and samples by solving the ODE \(\mathrm{d}x/\mathrm{d}t = v_\theta(x,t)\) from \(t=0\) to \(t=1\). Training needs no simulation of the ODE, which is the main practical difference from earlier continuous flows.

## Key methods

- [Normalising flows (Dinh et al., 2017; Kingma & Dhariwal, 2018)](normalising-flows/index.md): discrete invertible layers with exact likelihoods. Real NVP uses affine coupling; Glow adds invertible 1×1 convolutions.
- [Flow matching (Lipman et al., 2023)](flow-matching/index.md): regression on a velocity field along a probability path, with ODE sampling. It also covers the diffusion paths as special cases.

## Connections

- Diffusion models and flow matching share the same continuous-time view, see [DDPM](../diffusion/ddpm.md) and the [Diffusion Models](../diffusion/index.md) page.
- Flow matching is the training objective behind several recent image and video generators, which use Transformer denoisers, see [DiT](../../../../models/transformer/dit/index.md).
- The change-of-variables idea is the same one behind density estimation in [clustering and mixtures](../../clustering/index.md).
- Variational inference with flows uses the same machinery for posteriors, see [probabilistic methods](../../../probabilistic/index.md).

## Applications

Density estimation and anomaly detection with exact likelihoods, image and audio synthesis, molecular and conformation generation, and posterior approximation in Bayesian inference.

## Open questions

- Architectural limits: invertibility constrains layers, and flows often trade quality for exact likelihood.
- Sample quality at high resolution compared with diffusion and GAN models.
- How many ODE steps flow matching needs in practice, and how much distillation can cut it.

## References

### Seminal papers

- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Introduces additive coupling layers for exact-likelihood density estimation.
- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — Uses normalising flows to build flexible variational posteriors.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR. https://arxiv.org/abs/1605.08803 — Introduces affine coupling layers for images.
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS (arXiv). https://arxiv.org/abs/1807.03039 — Adds invertible 1×1 convolutions and actnorm to coupling-based flows.
- Lipman, Y., et al. (2023). *Flow Matching for Generative Modeling*. ICLR (arXiv). https://arxiv.org/abs/2210.02747 — Trains continuous normalising flows by simulation-free regression on probability paths.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — A survey of normalising flows and their use in density estimation and inference.

## Further learning

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*. Link: https://blog.evjang.com/2018/01/nf2.html — An accessible walkthrough of modern flow architectures and their Jacobians.
