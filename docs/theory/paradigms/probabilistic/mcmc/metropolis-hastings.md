---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/probability-statistics
tags:
  - probabilistic models
  - sampling
aliases:
  - Metropolis–Hastings
  - Metropolis-Hastings algorithm
  - 梅特羅波利斯–黑斯廷斯演算法
---

# Metropolis–Hastings

The Metropolis–Hastings algorithm draws samples from a target distribution by proposing moves from a simple distribution and accepting them with a ratio that preserves the target. It is the most general MCMC method and the starting point for the others. Part of [Markov chain Monte Carlo](index.md).

## Overview

To sample from \(\pi(\theta)\) without knowing its normalising constant, the algorithm proposes a new state \(\theta'\) from a proposal \(q(\theta'\mid\theta)\). It accepts the proposal with probability \(\alpha\), which depends only on ratios of \(\pi\) and \(q\). The normalising constant cancels, which is why the method works for posteriors. The proposal can be any distribution that can reach the whole target.

## Key concepts

- **Proposal distribution**: \(q(\theta'\mid\theta)\), chosen by the user. Random-walk Gaussian proposals are the common default.
- **Acceptance ratio**: \(\alpha = \min\!\big(1, \frac{\pi(\theta')\,q(\theta\mid\theta')}{\pi(\theta)\,q(\theta'\mid\theta)}\big)\).
- **Symmetric proposal**: when \(q(\theta'\mid\theta)=q(\theta\mid\theta')\), the ratio reduces to \(\pi(\theta')/\pi(\theta)\), the original Metropolis rule.
- **Acceptance rate tuning**: a proposal that is too wide is rejected often, and one that is too narrow moves slowly. Good practice targets a moderate acceptance rate.

## How it works

The algorithm for one step is:

1. Given the current state \(\theta\), propose \(\theta' \sim q(\cdot\mid\theta)\).
2. Compute \(\alpha\) from the acceptance ratio above.
3. With probability \(\alpha\) set the next state to \(\theta'\); otherwise keep \(\theta\).

Metropolis et al. (1953) introduced the symmetric version for physical systems. Hastings (1970) generalised it to asymmetric proposals, which is the form used today. Detailed balance with respect to \(\pi\) follows from the choice of \(\alpha\), so \(\pi\) is the stationary distribution of the chain.

## Key methods

- [Gibbs sampling](gibbs-sampling.md): a special case in which every proposal is accepted, because each move samples from an exact conditional distribution.
- [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md): uses gradient information to propose distant states that are still likely to be accepted.

## Connections

- [Markov chain Monte Carlo](index.md) gives the general framework and the diagnostics used with it.
- [Probability and statistics](../../../math/probability-statistics/index.md) explains the posterior that the algorithm targets.
- [Variational inference](../variational-inference/index.md) is the faster but approximate alternative to sampling.

## Applications

- **Bayesian estimation**: posterior sampling for models without conjugate structure (Andrieu et al., 2003).
- **Statistical physics**: the original application, sampling configurations of interacting particles (Metropolis et al., 1953).

## Open questions

- Random-walk proposals scale poorly with dimension, because the acceptance rate falls as the number of parameters grows.
- Tuning the proposal scale requires trial runs, and adaptive versions can break detailed balance unless designed carefully.

## References

### Seminal papers

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics* 21(6), 1087–1092. https://doi.org/10.1063/1.1699114 — Introduces the symmetric Metropolis acceptance rule.
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — Generalises the rule to asymmetric proposals and gives the acceptance ratio used today.

### Surveys and textbooks

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50, 5–43. https://doi.org/10.1023/A:1020281327116 — Derives the Metropolis–Hastings algorithm and its detailed-balance proof for machine-learning readers.
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — Compares random-walk Metropolis with the gradient-based alternative in high dimensions.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; presents Metropolis–Hastings with worked proposals and acceptance rules.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Chapter on sampling methods covers the Metropolis algorithm.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — Covers Metropolis-type samplers and the tuning of proposal scale for posterior simulation.
