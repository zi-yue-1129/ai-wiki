---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/paradigms/reinforcement-learning
tags:
  - optimization
  - zeroth-order
  - evolutionary
  - reinforcement learning
aliases:
  - Evolution strategies
  - OpenAI-ES
  - 演化策略
---

# Evolution Strategies

Evolution strategies (ES) estimate the gradient of an expected reward by sampling a population of perturbed parameters and weighting each sample by its score. Salimans et al. (2017) showed that this simple scheme scales to very many parallel workers and can train policies that compete with reinforcement learning. The parent overview is [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md).

## Overview

ES is a zeroth-order method. It needs only the reward of each sampled policy, not its gradient, so it applies to simulators and black-box environments.

## Problem

Maximise an expected reward \(F(\theta)\), where \(F\) may be non-differentiable, or where backpropagation through the environment is impossible. Policy gradients need the reward to be differentiable along the path of the policy, which is not always the case.

## Core idea

Smooth the objective by adding Gaussian noise to the parameters:

\[
F_\sigma(\theta) = \mathbb{E}_{\varepsilon \sim \mathcal{N}(0, I)}\big[F(\theta + \sigma\varepsilon)\big].
\]

The gradient of the smoothed objective can be written without differentiating \(F\):

\[
\nabla_\theta F_\sigma(\theta) = \frac{1}{\sigma}\,\mathbb{E}_{\varepsilon}\big[F(\theta + \sigma\varepsilon)\,\varepsilon\big].
\]

## Algorithm

Sample \(n\) noise vectors \(\varepsilon_1,\dots,\varepsilon_n\) from \(\mathcal{N}(0, I)\), evaluate the reward \(F_i = F(\theta + \sigma\varepsilon_i)\) for each, and form the estimate

\[
g = \frac{1}{n\sigma}\sum_{i=1}^{n} F_i\,\varepsilon_i.
\]

Then update \(\theta \leftarrow \theta + \alpha g\), where \(\alpha\) is a learning rate. Each worker evaluates some of the samples, so only scalar rewards and the random seeds need to be shared between workers.

## Key results

The abstract reports that ES scales to over a thousand parallel workers, communicates only scalars, and solves 3D humanoid walking in 10 minutes. It also reports competitive results on most Atari games after one hour of training. The abstract gives no per-game scores, so this page does not quote them.

## Limitations

- Each update needs a whole population of rollouts, so ES is sample-hungry compared with gradient methods that use one trajectory per step.
- The variance of the estimate grows with the number of parameters, so large networks need large populations.
- The smoothing scale \(\sigma\) and the learning rate \(\alpha\) must be tuned, and the results depend strongly on them.
- Its advantages in the paper rely on massive parallelism, so the comparison is not a like-for-like one on a single machine.

## Connections

- [Zeroth-Order and Evolutionary Optimisation](zeroth-order-and-evolutionary.md) is the overview where ES sits beside SPSA and CMA-ES.
- [SPSA](spsa.md) estimates a gradient from two perturbations instead of a population.
- [CMA-ES](cma-es.md) adapts a covariance matrix over the same kind of population.
- [Reinforcement learning](../paradigms/reinforcement-learning/index.md) provides the policy-gradient methods that ES is compared against.

## Applications

- Training locomotion policies in physics simulators, as in the humanoid walking result.
- Training agents on Atari from pixels, where reward is available but not differentiable.

## Open questions

- At equal numbers of environment interactions, how does ES compare with policy gradient methods?
- Can the population size be reduced for large networks without losing the gradient estimate's quality?

## References

### Seminal papers

- Salimans, T., Ho, J., Chen, X., Sidor, S. & Sutskever, I. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv. https://arxiv.org/abs/1703.03864 — Shows that ES scales to over a thousand parallel workers and is competitive with reinforcement learning on MuJoCo and Atari.
- Spall, J. C. (1992). Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. *IEEE Transactions on Automatic Control*, 37(3), 332–341. https://doi.org/10.1109/9.119632 — The gradient-free estimator that ES is an alternative to for black-box objectives.
- Malladi, S., et al. (2023). *Fine-Tuning Language Models with Just Forward Passes*. arXiv. https://arxiv.org/abs/2305.17333 — A later zeroth-order method for language-model fine-tuning, for comparison with ES.

### Surveys and textbooks

- Hansen, N. (2016). *The CMA Evolution Strategy: A Tutorial*. arXiv. https://arxiv.org/abs/1604.00772 — Tutorial on the covariance-adapting member of the evolution strategy family.
- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of gradient-based stochastic methods, the baseline against which ES is compared.
