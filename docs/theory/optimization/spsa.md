---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - zeroth-order
  - stochastic approximation
aliases:
  - SPSA
  - Simultaneous perturbation stochastic approximation
  - 同時擾動隨機逼近
---

# Simultaneous Perturbation Stochastic Approximation (SPSA)

SPSA estimates the gradient of a noisy loss from two evaluations, perturbing all parameters at once. Spall (1992) introduced it for stochastic approximation problems where the gradient is unavailable or costly. The parent overview is [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md).

## Overview

SPSA is a zeroth-order method: it uses only function values. Its gradient estimate is cheap in function evaluations, and the update rule that consumes it is ordinary stochastic gradient descent.

## Problem

Minimise \(f(\theta)\) when only noisy measurements \(y(\theta)\) of the loss are available. Finite differences need \(2p\) evaluations for \(p\) parameters. For a model with millions of parameters, that is too many evaluations per step.

## Core idea

Perturb every parameter at the same time along a random vector \(\Delta_k\) whose entries are \(\pm 1\) with equal probability. Two evaluations at \(\theta_k \pm c_k\Delta_k\) then give a gradient estimate for every coordinate at once.

## Algorithm

Let \(\Delta_k\) have independent entries equal to \(\pm 1\), and let \(c_k > 0\) be a perturbation size. The gradient estimate is

\[
\hat g_k(\theta_k) = \frac{y(\theta_k + c_k\Delta_k) - y(\theta_k - c_k\Delta_k)}{2c_k}\,\Delta_k^{-1},
\]

where the division is coordinate-wise. For \(\pm 1\) entries, \(\Delta_k^{-1} = \Delta_k\). The update is

\[
\theta_{k+1} = \theta_k - a_k \hat g_k(\theta_k),
\]

with gain \(a_k\) and perturbation \(c_k\) that decrease with the iteration count \(k\). Each iteration uses two evaluations, whatever the dimension.

## Key results

Spall (1992) gives conditions on the gain and perturbation sequences under which the iterates converge, in the stochastic approximation sense. This page does not quote numerical results from the paper.

## Limitations

- The estimate is noisy, because every coordinate shares the same two evaluations. Many iterations are needed, and the variance grows with the number of parameters.
- The gain and perturbation sequences must be tuned. Their choice strongly affects convergence speed.
- Per iteration it is slower than gradient descent with backpropagation, so it is used where evaluations are cheap relative to gradients, or where gradients cannot be computed.

## Connections

- [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md) is the overview where SPSA sits beside evolution strategies and CMA-ES.
- [Evolution strategies](evolution-strategies.md) estimate a gradient from a population rather than from two perturbations.
- [CMA-ES](cma-es.md) is a gradient-free method that adapts a covariance rather than a gradient estimate.
- [SGD and momentum](sgd-and-momentum/index.md) provides the update rule that SPSA's gradient estimate is combined with.

## Applications

- Parameter tuning of systems where only noisy measurements of performance are available.
- Fine-tuning language models with forward passes only, as in MeZO (Malladi et al., 2023), which adapts SPSA-style estimation to large models.

## Open questions

- How should the perturbation size be chosen for networks with millions of parameters?
- Does SPSA combined with momentum or adaptive scaling reach the accuracy of backpropagation-based fine-tuning at scale?

## References

### Seminal papers

- Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. *IEEE Transactions on Automatic Control*, 37(3), 332–341. https://doi.org/10.1109/9.119632 — Introduces SPSA, a gradient approximation built from simultaneous perturbations of all parameters.
- Malladi, S., et al. (2023). *Fine-Tuning Language Models with Just Forward Passes*. arXiv. https://arxiv.org/abs/2305.17333 — Applies a zeroth-order gradient estimator to fine-tuning, with memory close to that of inference.
- Salimans, T., et al. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv. https://arxiv.org/abs/1703.03864 — Another gradient-free estimator, based on a population, shown to scale to over a thousand workers.

### Surveys and textbooks

- Hansen, N. (2016). *The CMA Evolution Strategy: A Tutorial*. arXiv. https://arxiv.org/abs/1604.00772 — Tutorial on a different gradient-free method, for comparison with SPSA.
- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of the gradient-based stochastic methods that SPSA's update rule belongs to.
