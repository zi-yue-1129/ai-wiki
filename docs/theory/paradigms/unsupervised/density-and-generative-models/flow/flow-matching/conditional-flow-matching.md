---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md
tags:
  - flow matching
  - continuous normalising flows
  - generative models
aliases:
  - Conditional flow matching
  - CFM
  - 條件流匹配
---

# Conditional Flow Matching

Conditional flow matching (CFM) is the training objective introduced by Lipman et al. (2023) for continuous normalising flows. It regresses a neural velocity field onto the velocity of a simple conditional path that connects one noise sample to one data point, and it does this without simulating an ODE during training. The family overview is on the [Flow Matching](index.md) page, and the parent comparison is on [Flow-Based Models](../index.md).

## Overview

Continuous normalising flows (Chen et al., 2018) define a generative model through an ODE. Training them by maximum likelihood requires solving that ODE at every gradient step, which is expensive. Flow matching avoids this cost by training the velocity field with plain regression. The paper shows that the gradient of a simple per-sample objective equals the gradient of an intractable marginal one, so the cheap objective trains the same model. It also shows that diffusion paths are one special case and that optimal-transport paths give straighter trajectories.

## Key concepts

- **Conditional path** \(p_t(x\mid x_1)\): a distribution over \(x\) at time \(t\), given a data point \(x_1\). At \(t=0\) it is noise, and at \(t=1\) it is concentrated on \(x_1\).
- **Conditional vector field** \(u_t(x\mid x_1)\): the velocity that generates the conditional path.
- **Marginal path and field**: the mixture over \(x_1\) of the conditional paths and fields. The marginal field generates the data distribution at \(t=1\).
- **Gaussian conditional path**: \(p_t(x\mid x_1) = \mathcal N\big(x \mid \mu_t(x_1), \sigma_t(x_1)^2 I\big)\), with mean and scale functions chosen by the designer.

## How it works

The flow matching loss \(\mathcal L_{\text{FM}}(\theta) = \mathbb E_{t, x\sim p_t}\lVert v_\theta(t,x) - u_t(x)\rVert^2\) uses the marginal field \(u_t(x)\), which is an integral over all data points and cannot be computed. Lipman et al. replace it with the conditional loss

\[
\mathcal L_{\text{CFM}}(\theta) = \mathbb E_{t\sim\mathcal U[0,1],\; x_1\sim q(x_1),\; x\sim p_t(x\mid x_1)}\big\lVert v_\theta(t, x) - u_t(x\mid x_1)\big\rVert^2
\]

The paper's Theorem 2 states that \(\mathcal L_{\text{FM}}\) and \(\mathcal L_{\text{CFM}}\) differ by a constant that does not depend on \(\theta\), so they have identical gradients. Minimising the tractable loss therefore trains the same model. Sampling draws \(x_0\sim\mathcal N(0,I)\) and integrates \(\mathrm{d}x/\mathrm{d}t = v_\theta(t,x)\) from \(t=0\) to \(t=1\) with a standard ODE solver.

## Key methods

### Flow Matching for Generative Modeling (Lipman et al., 2023)

- **Problem:** continuous normalising flows give exact likelihoods but need an ODE solve for each training step. Diffusion models train cheaply but are tied to a fixed stochastic process.
- **Core idea:** regress the velocity field onto the conditional velocity of a chosen probability path. The per-sample target is unbiased for the marginal field, and no ODE is simulated during training.
- **Equation or algorithm:** the paper's optimal-transport path, with \(\sigma_{\min}\) a small constant, has mean \(\mu_t(x_1)=t\,x_1\), scale \(\sigma_t = 1-(1-\sigma_{\min})t\), flow \(\psi_t(x)=(1-(1-\sigma_{\min})t)\,x + t\,x_1\), and conditional field \(u_t(x\mid x_1) = \dfrac{x_1 - (1-\sigma_{\min})x}{1-(1-\sigma_{\min})t}\). With \(\sigma_{\min}\to 0\) the path is the straight line from noise to data at constant speed. Each training step draws \(t\), a data point \(x_1\), and a noise point \(x_0\sim\mathcal N(0,I)\), forms \(x_t=\psi_t(x_0)\), and regresses \(v_\theta(t, x_t)\) onto \(u_t(x_t\mid x_1)\). For \(\sigma_{\min}=0\) this target is \(x_1 - x_0\).
- **Results:** Table 1 of the paper reports unconditional ImageNet results. At 32×32, the optimal-transport path gives 3.53 bits/dim, FID 5.02 and 122 function evaluations, against 3.54, FID 6.37 and 193 for the diffusion path. At 64×64, the figures are 3.31 bits/dim and FID 14.45 for the optimal-transport path, against 3.33 and FID 16.88 for the diffusion path. At 128×128 the paper reports only the optimal-transport model, with 2.90 bits/dim and FID 20.9. The paper also states that on ImageNet 32×32 the optimal-transport sampler reaches the same error threshold with roughly 60% of the function evaluations of the diffusion path.
- **Limitations:** generation needs several ODE evaluations (122 to 193 in Table 1), so sampling is slower than a single network pass. Exact likelihood needs one more ODE integration. The paper compares paths empirically and does not prove that the optimal-transport path is best in general.

## Connections

- [Rectified flow](rectified-flow.md) uses the same straight-line target and adds a reflow procedure that straightens trajectories further.
- [Minibatch OT flow matching](minibatch-ot-flow-matching.md) keeps this objective but changes how noise and data points are paired.
- [Stochastic interpolants](stochastic-interpolants.md) generalise the choice of interpolant in this objective.
- The diffusion path is a special case, see [DDPM](../../diffusion/ddpm.md).
- The denoiser in large-scale systems is often a Transformer, see [DiT](../../../../../models/transformer/dit/index.md).

## Open questions

- Which conditional path gives the best trade-off between sample quality and the number of ODE steps for a given data type.
- Whether the regression target should use a more informed pairing of noise and data than independent sampling.

## References

### Seminal papers

- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — Introduces conditional flow matching and the optimal-transport conditional path used in this page.
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. arXiv. https://arxiv.org/abs/1806.07366 — Introduces continuous-depth models whose training requires ODE solves, which flow matching avoids.
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — Regresses onto the same straight-line direction and adds reflow.
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — Gives a general interpolant framework with a regression objective for the velocity.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. NeurIPS. https://arxiv.org/abs/2006.11239 — The diffusion models whose paths are a special case of the conditional path family.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Background on continuous and discrete flows and their likelihoods.
