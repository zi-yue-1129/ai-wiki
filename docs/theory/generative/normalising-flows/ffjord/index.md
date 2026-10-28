---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/automatic-differentiation
tags:
  - generative models
  - normalising flows
  - density estimation
aliases:
  - FFJORD
  - Free-form continuous dynamics
  - 自由形式連續動力學
  - Continuous normalising flow
  - 連續正規化流
---

# FFJORD

FFJORD (Grathwohl et al., 2018) is a [normalising flow](../index.md) in which the transformation is the solution of an ordinary differential equation (ODE) whose dynamics are an unrestricted neural network. Its log-density is estimated with Hutchinson's trace estimator, so the full Jacobian trace is never computed. The result is a continuous model with unbiased density estimation and no architectural restrictions on the network.

## Overview

A discrete flow needs a structured map so that its Jacobian determinant is cheap, as coupling and autoregressive designs provide. A continuous flow avoids this. The data are carried through time by an ODE, and the change in log-density is governed by the trace of the Jacobian of the dynamics, which is easier to handle than a determinant. Chen et al. (2018) introduced continuous normalising flows (CNFs) in this form and trained them by maximum likelihood with an ODE solver.

Computing the trace exactly costs roughly as much as \(D\) evaluations of the dynamics (Grathwohl et al., 2018), which is expensive at high dimension. FFJORD keeps the continuous form and estimates the trace stochastically.

## Key concepts

- **Continuous normalising flow**: a map \(z(t_1) = z(t_0) + \int_{t_0}^{t_1} f(z(t), t)\,dt\) defined by dynamics \(f\). It is invertible because the ODE can be solved backwards in time.
- **Instantaneous change of variables**: along a trajectory, the rate of change of the log-density equals the negative trace of the Jacobian of the dynamics.
- **Hutchinson's trace estimator**: for a random vector \(\varepsilon\) with zero mean and identity covariance, \(\operatorname{Tr}(A) = \mathbb{E}_\varepsilon[\varepsilon^\top A \varepsilon]\). Gaussian or Rademacher noise are typical.
- **Vector–Jacobian product**: \(\varepsilon^\top \partial f / \partial z\), which reverse-mode automatic differentiation computes at roughly the cost of evaluating \(f\).

## How it works

Let the data \(x\) be the state at time \(t_0\) and the base sample the state at time \(t_1\). The paper's form of the instantaneous change-of-variables rule gives

\[
\log p(x) = \log \mathcal{N}\big(z(t_1); 0, I\big) + \int_{t_0}^{t_1} \operatorname{Tr}\!\left(\frac{\partial f}{\partial z(t)}\right) dt
\]

The trace is replaced by the unbiased estimate \(\mathbb{E}_\varepsilon[\varepsilon^\top (\partial f / \partial z)\,\varepsilon]\). The noise vector is held fixed during each ODE solve, which keeps the dynamics deterministic within the solve.

Training proceeds as follows:

1. Draw a noise vector \(\varepsilon\) for each ODE solve.
2. Integrate the state and the accumulated trace term from the data to the base. The trace term grows at the rate \(\varepsilon^\top (\partial f/\partial z)\varepsilon\), computed by one vector–Jacobian product.
3. Average the log-density of the base sample under the standard normal, plus the accumulated term, over the minibatch.
4. Backpropagate through the solver with the adjoint method, whose memory does not grow with the number of solver steps, and update the parameters.

Sampling draws a base sample and integrates the same dynamics backwards to \(t_0\).

## Results

The paper evaluates five tabular datasets and, for images, MNIST and CIFAR-10, reporting bits per dimension where lower is better:

| Model | MNIST | CIFAR-10 |
|---|---|---|
| RealNVP | 1.06 | 3.49 |
| Glow | 1.05 | 3.35 |
| FFJORD (multi-scale) | 0.99 | 3.40 |
| FFJORD (single flow, convolutional encoder–decoder) | 1.05 | — |

A single FFJORD flow matches Glow and RealNVP on MNIST, where those models must compose many flows. On CIFAR-10 the multi-scale FFJORD comes close to Glow, and the paper says it uses less than 2% as many parameters. On tabular data FFJORD is the best reversible model by a wide margin, but autoregressive models do better, and FFJORD outperforms MAF on all but one dataset.

## Limitations

- **Speed.** Each likelihood and sample needs ODE solves, and the paper states that the approach is slower than competing methods.
- **Estimator variance.** The variance of the trace estimator grows with the squared Frobenius norm of the matrix, according to the paper.
- **Simulation during training.** Maximum-likelihood training needs the ODE solver in the loop. Tong et al. (2023) identify this as the limitation that holds continuous flows back, which motivated simulation-free objectives.

## Open questions

- Can continuous flows be trained without simulating the ODE, and at what cost in density quality? [Flow matching](../../flow-matching/index.md) and stochastic interpolants (Albergo and Vanden-Eijnden, 2022) answer this for generation, but the trade-offs for exact likelihood are still being measured.
- How many noise samples per solve are needed for a stable likelihood?

## References

### Seminal papers

- Grathwohl, W., Chen, R. T. Q., Bettencourt, J., Sutskever, I. & Duvenaud, D. (2018). *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*. arXiv. https://arxiv.org/abs/1810.01367 — The paper itself: the unbiased trace estimator, the free-form dynamics and the density results discussed here.
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. NeurIPS. https://arxiv.org/abs/1806.07366 — Defines continuous normalising flows through an ODE and trains them by maximum likelihood with the adjoint method.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — Trains continuous normalising flows by regression onto known vector fields, avoiding simulation during training.
- Tong, A. et al. (2023). *Improving and generalizing flow-based generative models with minibatch optimal transport*. arXiv. https://arxiv.org/abs/2302.00482 — Generalises conditional flow matching for continuous normalising flows and discusses the limits of simulation-based maximum-likelihood training.
- Albergo, M. S. & Vanden-Eijnden, E. (2022). *Building Normalizing Flows with Stochastic Interpolants*. arXiv. https://arxiv.org/abs/2209.15571 — Learns the velocity field of a continuous flow with a quadratic loss, avoiding backpropagation through ODE solvers.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Surveys flows, including continuous-time designs and the trade-offs between density evaluation and sampling.
