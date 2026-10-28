---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - zeroth-order
  - evolutionary
aliases:
  - CMA-ES
  - Covariance matrix adaptation evolution strategy
  - 協方差矩陣自適應演化策略
---

# CMA-ES

CMA-ES (covariance matrix adaptation evolution strategy) is a randomised method for real-parameter optimisation without gradients. It samples candidates from a Gaussian, ranks them by score, and adapts the mean, the step size and the covariance matrix of the Gaussian. Hansen (2016) gives a tutorial on the method. The parent overview is [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md).

## Overview

CMA-ES is a population method. It is aimed at non-linear, non-convex problems where gradients are unavailable, and it learns the shape of the search distribution from the samples it has already evaluated.

## Problem

Minimise a black-box objective \(f:\mathbb{R}^n \to \mathbb{R}\) that may be non-convex and ill-conditioned. Fixed random search does not adapt to elongated or rotated valleys, so the search takes many evaluations to make progress along them.

## Core idea

Keep a Gaussian search distribution with mean \(m\), step size \(\sigma\) and covariance \(C\). The distribution is moved and reshaped so that the good samples become likely. The covariance adapts to the directions in which the search has been making progress, which is what lets it follow elongated valleys.

## Algorithm

At each iteration:

1. Sample \(\lambda\) candidates \(x_i \sim m + \sigma\,\mathcal{N}(0, C)\).
2. Evaluate and rank them by \(f(x_i)\).
3. Move the mean \(m\) toward a weighted average of the best \(\mu\) candidates.
4. Update the covariance \(C\) from the selected steps, and the step size \(\sigma\) from an evolution path that tracks whether the steps have been consistent.

The rank-based update makes the method invariant to monotone transformations of \(f\), because only the order of the scores matters.

## Key results

The tutorial describes CMA-ES as a stochastic, randomised method for real-parameter optimisation, aimed at non-linear, non-convex functions. It gives no benchmark numbers in the abstract, so this page does not quote any.

## Limitations

- Updating the covariance matrix costs memory and computation that grow with the square of the number of parameters, so the method suits problems with hundreds of parameters rather than millions.
- The population size \(\lambda\) affects how well the method escapes local minima, and the default is a compromise rather than a setting that suits every problem.
- Without a gradient, progress per evaluation is typically slower than gradient methods on smooth problems.

## Connections

- [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md) is the overview where CMA-ES sits beside SPSA and evolution strategies.
- [Evolution strategies](evolution-strategies.md) share the population-based sampling of CMA-ES, but do not adapt a full covariance matrix in the same way.
- [SPSA](spsa.md) estimates a gradient from two perturbations and does not adapt a distribution.
- [Second-order methods](second-order.md) also model the local shape of the objective, using gradients rather than samples.

## Applications

- Tuning a small number of parameters of a simulator or controller, where evaluations are costly and gradients are unavailable.
- Continuous design problems in engineering, where the objective is a black-box simulation.

## Open questions

- How can covariance adaptation be made affordable for models with millions of parameters?
- When should the population size be increased to escape local minima, and can that be decided automatically?

## References

### Seminal papers

- Hansen, N. (2016). *The CMA Evolution Strategy: A Tutorial*. arXiv. https://arxiv.org/abs/1604.00772 — Tutorial on CMA-ES, a stochastic, randomised method for non-linear, non-convex real-parameter optimisation.
- Salimans, T., et al. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv. https://arxiv.org/abs/1703.03864 — A population-based gradient estimator for policies, the main alternative to CMA-ES in large-scale settings.
- Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. *IEEE Transactions on Automatic Control*, 37(3), 332–341. https://doi.org/10.1109/9.119632 — The gradient-free estimator from the other side of the same comparison.
- Malladi, S., et al. (2023). *Fine-Tuning Language Models with Just Forward Passes*. arXiv. https://arxiv.org/abs/2305.17333 — A zeroth-order method for large models, where covariance adaptation is not affordable.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. *SIAM Review*, 60(2), 223–311. https://doi.org/10.1137/16M1080173 — Survey of gradient-based stochastic methods, the baseline against which gradient-free methods are compared.
