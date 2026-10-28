---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/probability-statistics
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - probabilistic models
  - sampling
  - bayesian
aliases:
  - 馬可夫鏈蒙地卡羅
  - MCMC
  - Markov chain Monte Carlo
---

# Markov Chain Monte Carlo

Markov chain Monte Carlo (MCMC) approximates a probability distribution by drawing samples from a Markov chain whose stationary distribution is that distribution. It is the main tool for sampling from posteriors that cannot be integrated exactly. Part of [Probabilistic & Bayesian methods](../index.md).

## Overview

Many Bayesian computations need expectations under a posterior \(p(\theta\mid D)\), which is only known up to a normalising constant. MCMC builds a chain \(\theta^{(1)}, \theta^{(2)}, \dots\) whose long-run distribution is the target. Averages over the chain estimate expectations, and the normalising constant is never needed. The chain must mix, meaning it moves across the whole distribution rather than staying in one region.

The basic recipe is to propose a move and accept it with a probability that preserves the target distribution. The [Metropolis–Hastings](metropolis-hastings.md), [Gibbs sampling](gibbs-sampling.md) and [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md) algorithms are the best-known ways of doing this.

## Key concepts

- **Markov chain**: a sequence in which each state depends only on the previous one. Its stationary distribution is the target.
- **Detailed balance**: a sufficient condition for a chain to leave the target invariant, requiring that flows between any two states balance.
- **Burn-in**: the initial samples, discarded because the chain has not yet reached the target.
- **Mixing and autocorrelation**: strongly correlated samples carry less information. The effective sample size measures how many independent-equivalent draws a chain provides.
- **Diagnostics**: convergence checks such as comparing several chains, or measuring the potential scale reduction, to detect whether a chain has explored the target.

## How it works

For a target \(\pi(\theta)\), a generic MCMC step is: propose \(\theta'\) from a proposal distribution, accept it with probability \(\alpha\), and otherwise stay at \(\theta\). Choosing \(\alpha\) so that detailed balance holds makes \(\pi\) the stationary distribution. Andrieu et al. (2003) give a general introduction for machine learning readers, covering these conditions and the standard algorithms in one framework.

Using samples, the expectation of any function \(f\) is estimated by \(\frac{1}{N}\sum_{t} f(\theta^{(t)})\), after discarding burn-in. Its error decreases roughly as \(1/\sqrt{N_{\text{eff}}}\), so effective sample size, not just the number of draws, sets the precision.

## Key methods

- [Metropolis–Hastings](metropolis-hastings.md): proposes moves from any proposal distribution and accepts them with the Metropolis–Hastings ratio. The most general method.
- [Gibbs sampling](gibbs-sampling.md): samples each variable from its conditional distribution in turn. No accept step is needed, and it suits models with conjugate conditionals.
- [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md): uses gradients and simulated dynamics to make distant, high-acceptance proposals. It is the basis of the No-U-Turn Sampler in Stan and similar tools.

## Connections

- [Variational inference](../variational-inference/index.md) is the optimisation-based alternative. It is faster but biased, while MCMC is asymptotically exact.
- [Probability and statistics](../../../math/probability-statistics/index.md) gives the posterior and expectation calculations that MCMC approximates.
- [Score-based diffusion models](../../unsupervised/density-and-generative-models/diffusion/index.md) generate samples by reversing a noising process. Their sampling methods are closely related to Langevin dynamics, a gradient-based MCMC method.
- Brain and cognition: sampling-based accounts of perception propose that neural activity samples from a posterior over hidden causes. This is an active hypothesis, not a settled result.

## Applications

- **Bayesian regression and hierarchical models**: posterior samples give credible intervals (Gelman et al., 2013).
- **Probabilistic programming**: general-purpose samplers such as HMC/NUTS run inference for user-written models (Hoffman & Gelman, 2014).
- **Scientific inference**: parameter estimation in physics, ecology and epidemiology, where the likelihood is complex.

## Open questions

- Diagnosing convergence is hard, because a chain can look converged while missing a distant mode.
- High-dimensional and multimodal posteriors mix slowly, and adaptive methods help but have their own theoretical gaps.
- Combining MCMC with large neural networks, where gradients are noisy and the posterior is huge, remains difficult.

## References

### Seminal papers

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics* 21(6), 1087–1092. https://doi.org/10.1063/1.1699114 — Introduces the Metropolis algorithm for sampling from a Boltzmann distribution.
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — Generalises the Metropolis rule to asymmetric proposals.
- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B* 195(2), 216–222. https://ui.adsabs.harvard.edu/abs/1987PhLB..195..216D/abstract — Introduces the hybrid (Hamiltonian) Monte Carlo method.

### Surveys and textbooks

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50, 5–43. https://doi.org/10.1023/A:1020281327116 — Tutorial on MCMC for machine learning, covering Metropolis–Hastings, Gibbs and their relations.
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. In *Handbook of Markov Chain Monte Carlo*. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — Review of HMC, its tuning, and its advantages over random-walk samplers.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers MCMC methods and their diagnostics.

### Articles and documentation

- Hoffman, M. D. & Gelman, A. (2014). The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research* 15. https://jmlr.org/papers/v15/hoffman14a.html — Introduces NUTS, which tunes the path length of HMC automatically.
