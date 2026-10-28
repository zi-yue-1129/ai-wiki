---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/probability-statistics
tags:
  - probabilistic models
  - sampling
aliases:
  - 吉布斯抽樣
  - Gibbs sampling
  - Gibbs sampler
---

# Gibbs Sampling

Gibbs sampling draws from a joint distribution by repeatedly sampling each variable from its conditional distribution given all the others. Every proposal is accepted, so it needs no accept–reject step. It is the standard sampler for models with conjugate conditionals. Part of [Markov chain Monte Carlo](index.md).

## Overview

Suppose a joint distribution over variables \((\theta_1,\dots,\theta_d)\) is hard to sample directly, but each conditional \(p(\theta_j\mid\theta_{-j})\) is easy. Gibbs sampling cycles through the variables and resamples each from its conditional. The resulting chain has the joint distribution as its stationary distribution. In hierarchical Bayesian models, many conditionals are standard distributions, which makes the method convenient.

## Key concepts

- **Full conditional**: \(p(\theta_j\mid\theta_{-j})\), the distribution of one variable with all others fixed.
- **Scan order**: systematic scans update variables in a fixed order, and random scans pick one at random.
- **Blocking**: updating several correlated variables together, which usually improves mixing.
- **Collapsed Gibbs sampling**: integrating out some variables analytically, which can reduce correlation between the rest.

## How it works

One sweep of the sampler is:

1. For \(j = 1,\dots,d\), draw \(\theta_j^{(t+1)} \sim p(\theta_j \mid \theta_1^{(t+1)},\dots,\theta_{j-1}^{(t+1)}, \theta_{j+1}^{(t)},\dots,\theta_d^{(t)})\).

Each update is a Metropolis–Hastings move whose proposal is the full conditional, so its acceptance probability equals one (Andrieu et al., 2003). Detailed balance then holds for each step, and the joint distribution is invariant.

The method can mix slowly when variables are strongly correlated, because each update only moves along one coordinate at a time. Blocking and reparameterisation are the common remedies.

## Key methods

- [Metropolis–Hastings](metropolis-hastings.md): the general method of which Gibbs sampling is a special case with every proposal accepted.
- [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md): handles correlated variables better by moving along the joint distribution's geometry, at the cost of gradients.

## Connections

- [Markov chain Monte Carlo](index.md) gives the framework and diagnostics.
- [Probability and statistics](../../../math/probability-statistics/index.md) provides the conditional distributions and conjugacy that make Gibbs steps easy to compute.
- Gibbs sampling and mean-field variational inference are closely related in conjugate models. The sampler draws from the posterior, while mean-field updates approximate it, see [variational inference](../variational-inference/index.md).

## Applications

- **Hierarchical Bayesian models**: conjugate conditionals make Gibbs sampling efficient for many standard models (Gelman et al., 2013).

## Open questions

- Correlated posteriors can make Gibbs sampling extremely slow, and diagnosing this is difficult without comparing several chains.
- Automatic choice of blocking and scan order is not solved in general.

## References

### Seminal papers

- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — Gives the general acceptance-ratio framework that contains the Gibbs update as a special case.
- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50. https://www.cs.ox.ac.uk/publications/publication7533-abstract.html — Shows that the Gibbs update is a Metropolis–Hastings move with acceptance probability one.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Chapter on sampling covers Gibbs sampling with worked examples.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers Gibbs sampling for graphical models.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — Uses Gibbs sampling in hierarchical models and discusses its convergence checks.
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — Compares Gibbs-type and gradient-based samplers in correlated settings.
