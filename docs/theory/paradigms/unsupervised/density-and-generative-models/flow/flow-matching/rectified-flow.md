---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching
  - theory/paradigms/unsupervised/density-and-generative-models/flow
  - theory/models/transformer
tags:
  - flow matching
  - rectified flow
  - few-step sampling
aliases:
  - Rectified flow
  - Reflow
  - 修正流
---

# Rectified Flow

Rectified flow learns an ODE whose trajectories are as straight as possible, so that sampling is accurate even with very few solver steps. Liu, Gong and Liu (2022) proposed it together with a reflow procedure that straightens the trajectories further. The family comparison is on the [Flow Matching](index.md) and [Flow-Based Models](../index.md) pages.

## Overview

Sampling with an ODE solver costs one network evaluation per step, so curved trajectories are expensive to integrate accurately. Rectified flow trains the drift on straight segments between paired noise and data points. When the learned trajectories are close to straight, a single Euler step already gives a useful sample. The training target is the same straight-line direction used by [conditional flow matching](conditional-flow-matching.md). The new ingredient is reflow, which changes how the pairs are formed.

## Key concepts

- **Linear interpolation**: \(X_t = t\,X_1 + (1-t)\,X_0\), where \(X_0\) is drawn from the noise distribution \(\pi_0\) and \(X_1\) from the data distribution \(\pi_1\).
- **Drift**: a time-dependent vector field \(v(z,t)\) that defines the ODE \(\mathrm{d}Z_t = v(Z_t,t)\,\mathrm{d}t\), which carries samples from \(\pi_0\) to \(\pi_1\).
- **Reflow**: a new training round on pairs \((Z^k_0, Z^k_1)\) produced by simulating the previous rectified flow.

## How it works

Draw \(X_0\sim\pi_0\) and \(X_1\sim\pi_1\) independently, form \(X_t\) as above, and fit the drift by least squares over time:

\[
\min_v \int_0^1 \mathbb E\big[\lVert (X_1 - X_0) - v(X_t, t)\rVert^2\big]\,\mathrm{d}t
\]

Reflow then takes a trained flow with \(k\) rounds, simulates it from \(\pi_0\) to obtain endpoint pairs \((Z^k_0, Z^k_1)\), and trains a new rectified flow on those pairs, giving \(Z^{k+1} = \mathrm{RectFlow}\big((Z^k_0, Z^k_1)\big)\). Each round makes the paths straighter. The paper cautions that too many rounds accumulate estimation error.

## Key methods

### Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow (Liu, Gong & Liu, 2022)

- **Problem:** ODE-based generative models need many solver steps because curved trajectories are poorly approximated by coarse integrators.
- **Core idea:** fit the drift to the straight direction \(X_1 - X_0\) along linear interpolants, then apply reflow to couple noise and data along straighter paths.
- **Equation or algorithm:** the least-squares objective and reflow update above. Each reflow round trains on the endpoint pairs of the previous flow.
- **Results:** the abstract states that nearly straight flows give high-quality samples even with a single Euler step. On CIFAR-10 (unconditional, DDPM++ architecture), Table 1(a) gives the one-step rows. The text quotes an FID of 4.85 for the distilled two-round rectified flow. In the same table, that row's one-step entry is 12.21, with 4.85 printed in parentheses beside it. With adaptive RK45 simulation, the one-round flow reaches FID 2.58 at about 127 function evaluations. The paper gives no ImageNet FID. Its high-resolution results are shown only qualitatively.
- **Limitations:** reflow needs a simulation of the previous model for every round, which costs compute. Too many rounds accumulate error. The first round uses independent pairs, so the choice of coupling is not addressed there, which is one motivation for [minibatch OT flow matching](minibatch-ot-flow-matching.md).

## Connections

- [Conditional flow matching](conditional-flow-matching.md) uses the same straight-line target without reflow.
- [Stochastic interpolants](stochastic-interpolants.md) give a framework in which this linear interpolant is one choice.
- Esser et al. (2024) scale rectified flow to high-resolution text-to-image transformers, see the references below.

## Open questions

- How many reflow rounds are worth their cost, and how to stop before error accumulates.
- Whether straight trajectories remain the best target for large conditional models.

## References

### Seminal papers

- Liu, X., Gong, C. & Liu, Q. (2022). *Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow*. arXiv; ICLR 2023. https://arxiv.org/abs/2209.03003 — Introduces rectified flow and the reflow procedure described on this page.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2023). *Flow Matching for Generative Modeling*. ICLR. https://arxiv.org/abs/2210.02747 — The conditional flow matching objective with which rectified flow is compared.
- Tong, A., Fatras, K., Malkin, N., Huguet, G., Zhang, Y., Rector-Brooks, J., Wolf, G. & Bengio, Y. (2024). *Improving and Generalizing Flow-Based Generative Models with Minibatch Optimal Transport*. TMLR. https://arxiv.org/abs/2302.00482 — Addresses the coupling of noise and data that the first rectified-flow round leaves open.

### Scaling and applications

- Esser, P., et al. (2024). *Scaling Rectified Flow Transformers for High-Resolution Image Synthesis*. arXiv. https://arxiv.org/abs/2403.03206 — Applies rectified flow with a transformer to high-resolution text-to-image generation, and reports that the approach outperforms established diffusion formulations.

### Background

- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. arXiv. https://arxiv.org/abs/1806.07366 — The continuous-depth framework in which the flow is defined and sampled by an ODE solver.
