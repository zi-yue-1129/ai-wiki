---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/paradigms/evolutionary
  - theory/paradigms/reinforcement-learning
tags:
  - optimization
  - zeroth-order
  - evolutionary
aliases:
  - Zeroth-order optimisation
  - Evolution strategies
  - 零階最佳化
  - 演化策略
---

# Zeroth-Order and Evolutionary Optimisation

Some objectives can be evaluated but not differentiated: a simulator, a black-box score, a reward from an environment, or a loss through a non-differentiable step. Zeroth-order methods estimate a search direction from function values alone. Evolutionary methods search by sampling candidates and keeping the good ones. Both trade many function evaluations for the absence of gradients.

## Overview

Part of the [Optimisation](index.md) folder. Each method has its own page, and this one compares them. The population-based view of the same ideas is in [Evolutionary & Swarm Intelligence](../paradigms/evolutionary/index.md).

## Key concepts

- **Zeroth-order oracle:** access to \(f(\theta)\) but not to \(\nabla f(\theta)\).
- **Gradient estimate from differences:** evaluating \(f\) at perturbed points gives a finite-difference estimate of the directional derivative. Using one direction per step costs only a few evaluations, but its variance grows with the number of parameters.
- **Smoothing:** many estimators differentiate a Gaussian-smoothed objective \(F_\sigma(\theta) = \mathbb{E}_\varepsilon[f(\theta+\sigma\varepsilon)]\), which exists even when \(f\) itself is not differentiable.
- **Population:** evolutionary methods keep a distribution over candidates and move it toward the candidates with the best scores.

## How it works

Each step perturbs the current parameters, evaluates the objective at the perturbed points, and combines the results into an update. Two families follow. Estimator methods such as SPSA turn a small number of evaluations into a gradient-like step, which is then used in an ordinary update rule. Population methods such as evolution strategies sample many candidates, weight them by score, and move the sampling distribution toward the good ones.

Each step is slower than backpropagation, but no derivatives are needed. This matters when the objective is non-differentiable, when the system is a black box, or when only noisy measurements are available.

## Key methods

| Method | Idea | Function evaluations per step | Page |
|---|---|---|---|
| SPSA (Spall, 1992) | Perturb all parameters at once with a random sign vector | 2 | [SPSA](spsa.md) |
| Evolution strategies (Salimans et al., 2017) | Estimate the gradient of a smoothed reward from a population | Population size | [Evolution strategies](evolution-strategies.md) |
| CMA-ES (Hansen, 2016) | Adapt a covariance matrix to the shape of the good region | Population size | [CMA-ES](cma-es.md) |

MeZO (Malladi et al., 2023) applies the SPSA estimator to fine-tuning language models, and its memory use is discussed on the [SPSA](spsa.md) page.

## Connections

- [Evolutionary & Swarm Intelligence](../paradigms/evolutionary/index.md) covers the population view and the wider family of nature-inspired search.
- [Reinforcement learning](../paradigms/reinforcement-learning/index.md) uses zeroth-order estimates when the reward is not differentiable. Evolution strategies are an alternative to policy gradients there.
- [Second-order methods](second-order.md) use more information about the objective than these methods do, at a higher cost per step.

## Applications

- Training policies in simulated environments, where the reward is available but not differentiable.
- Fine-tuning large models when storing gradients and optimiser states is too costly, as in MeZO.
- Tuning systems with few parameters and noisy measurements, where CMA-ES is a common baseline.

## Open questions

- How does the cost per step of population methods scale to the millions or billions of parameters in modern networks?
- When do zeroth-order estimates with few evaluations match gradient methods on the same problem, and how many evaluations are needed?

## References

### Seminal papers

- Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. *IEEE Transactions on Automatic Control*, 37(3), 332–341. https://doi.org/10.1109/9.119632 — Introduces SPSA, a gradient approximation built from simultaneous perturbations of all parameters.
- Salimans, T., et al. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv. https://arxiv.org/abs/1703.03864 — Shows that evolution strategies scale to over a thousand parallel workers and are competitive with reinforcement learning on MuJoCo and Atari.
- Hansen, N. (2016). *The CMA Evolution Strategy: A Tutorial*. arXiv. https://arxiv.org/abs/1604.00772 — Tutorial on CMA-ES, a randomised method for non-linear, non-convex real-parameter optimisation.
- Malladi, S., et al. (2023). *Fine-Tuning Language Models with Just Forward Passes*. arXiv. https://arxiv.org/abs/2305.17333 — Fine-tunes language models with a zeroth-order estimator (MeZO), using about the memory of inference.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of gradient-based stochastic methods, the baseline against which these gradient-free methods are compared.
