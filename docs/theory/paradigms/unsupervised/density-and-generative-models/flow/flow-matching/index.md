---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/transformer
tags:
  - flow matching
  - generative models
  - continuous normalising flows
aliases:
  - 流匹配
  - Flow matching
  - Conditional flow matching
---

# Flow Matching

Flow matching trains a continuous-time generative model by regressing a velocity field onto known velocities along paths from noise to data. Unlike earlier continuous normalising flows, it needs no simulation of an ODE during training, so it scales to large images. Sampling integrates an ODE from noise to data. The family overview, including discrete normalising flows, is on the [Flow-Based Models](../index.md) page, and the diffusion relative is on the [Diffusion Models](../../diffusion/index.md) page.

## Overview

Lipman et al. (2023) proposed flow matching for training continuous normalising flows. The key observation is that the velocity field can be learned by regressing on the velocity of a conditional path, one for each data point, and the marginal velocity field is then recovered. The authors show that the diffusion paths used by score-based models are one family of such paths, so flow matching generalises diffusion training. They also highlight optimal-transport paths, which give straighter trajectories and faster sampling in their experiments.

Later work keeps the same regression idea and changes one of three things: the interpolant between noise and data, the way noise and data points are paired, or the way the trajectories are straightened.

## Key concepts

- **Probability path** \(p_t\): a family of distributions that moves from a simple noise distribution at \(t=0\) to the data distribution at \(t=1\).
- **Conditional path** \(p_t(x\mid x_1)\): a path that starts from noise and ends at a single data point \(x_1\).
- **Velocity field** \(v_\theta(x,t)\): the network that defines the ODE \(\mathrm{d}x/\mathrm{d}t = v_\theta(x,t)\).
- **Optimal-transport path**: a conditional path whose interpolation is the straight line between noise and data, which gives simple velocities.

## How it works

Take a noise sample \(x_0\sim\mathcal N(0,I)\) and a data point \(x_1\). With the optimal-transport path used by the paper, the point on the path at time \(t\) is \(x_t = (1-t)\,x_0 + t\,x_1\), and its velocity is \(u_t = x_1 - x_0\). Training minimises

\[
\mathcal L_{\text{CFM}}(\theta) = \mathbb E_{t,\,x_0,\,x_1}\big\lVert v_\theta(x_t, t) - (x_1 - x_0)\big\rVert^2
\]

Because the conditional velocities are known in closed form, this regression needs no ODE solve. The minimiser is the marginal velocity field that generates the data distribution. Sampling draws \(x_0\) from the noise and solves the ODE from \(t=0\) to \(t=1\) with a standard numerical solver.

## Key methods

- [Conditional flow matching (Lipman et al., 2023)](conditional-flow-matching.md): the regression objective with Gaussian optimal-transport paths. This is the base method, and it covers diffusion paths as special cases.
- [Rectified flow (Liu et al., 2022)](rectified-flow.md): regression onto straight-line interpolants, with a reflow procedure that straightens trajectories for few-step sampling.
- [Stochastic interpolants (Albergo & Vanden-Eijnden, 2023)](stochastic-interpolants.md): a general interpolant framework that unifies flows and diffusions, with the choice of interpolant left open.
- [Minibatch OT flow matching (Tong et al., 2024)](minibatch-ot-flow-matching.md): pairs noise and data points by an optimal transport plan computed on each minibatch.

## Connections

- Flow matching and diffusion share the same continuous-time view, and diffusion paths are a special case, see [DDPM](../../diffusion/ddpm.md) and [DDIM](../../diffusion/ddim.md).
- Its denoiser is typically a Transformer over latent patches, see [DiT](../../../../../models/transformer/dit/index.md).
- The ODE sampler is a numerical integration problem, linked to the optimisation methods in [Optimisation](../../../../../optimization/index.md).

## Applications

Text-to-image and video generation with latent flow models, and generation of molecular conformations and other continuous data where a velocity field is a natural parameterisation.

## Open questions

- Which probability path gives the best trade-off between sample quality and the number of ODE steps.
- How many steps are needed in practice, and how much distillation can reduce them.
- Whether flow matching fully replaces diffusion training for very large models, and how the two compare on conditional generation.

## References

### Seminal papers

- Lipman, Y., et al. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — Introduces conditional flow matching for training continuous normalising flows without simulation.
- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv. https://arxiv.org/abs/2209.03003 — Learns a velocity field that follows straighter paths, which allows sampling with fewer steps.
- Albergo, M. S. & Vanden-Eijnden, E. (2023). *Building Normalizing Flows with Stochastic Interpolants*. ICLR. https://arxiv.org/abs/2209.15571 — A stochastic-interpolant framework that bridges flows and diffusion and gives a regression target for the velocity.
- Tong, A., et al. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — Pairs noise and data with minibatch optimal transport, giving straighter conditional paths for flow matching.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Background on continuous and discrete flows, useful for the likelihood side of the method.
