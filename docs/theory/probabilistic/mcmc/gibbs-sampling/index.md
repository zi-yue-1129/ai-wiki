---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - uncertainty
  - theory/math
aliases:
  - 吉布斯取樣
  - 吉布斯取樣器
  - Gibbs sampling
  - Gibbs sampler
---

# Gibbs Sampling

Gibbs sampling is an [MCMC](../index.md) method that updates one variable at a time, drawing each from its full conditional distribution given the current values of all the others. It has no rejection step, so every draw is accepted. It is the natural sampler for models whose conditional distributions are simple, such as many graphical models and hierarchical Bayesian models.

## Overview

Consider a joint distribution over several variables $x = (x_1, \dots, x_d)$. The full conditional of $x_j$ is $p(x_j \mid x_{-j})$, the distribution of that variable with all the others held fixed. In many models this conditional has a known form, such as a normal or gamma distribution, even when the joint does not. Gibbs sampling exploits that structure by cycling through the variables and drawing from each conditional in turn.

The method is named after the Gibbs distributions of statistical physics. Geman and Geman (1984) applied it to Bayesian image restoration with Markov random field priors, which is among its best-known early uses. In statistics, the method became widely known in the early 1990s, and Casella and George (1992) give an accessible explanation of why it works.

Gibbs sampling is a special case of Metropolis–Hastings in which the proposal is the full conditional, so the acceptance probability is always one (Andrieu et al., 2003). See the [Metropolis–Hastings](../metropolis-hastings/index.md) page for the general algorithm.

## Key concepts

- **Full conditional**: the distribution of one variable given all the rest. It is the only quantity the sampler needs.
- **Scan**: one pass through all the variables. Systematic scans visit the variables in a fixed order, and random scans choose them at random.
- **Blocked Gibbs**: a version that updates a group of variables jointly when their joint conditional is easy to sample.
- **Conjugacy**: when the prior and the likelihood are conjugate, the full conditionals are standard distributions, which makes the sampler simple to write.

## How it works

For $d$ variables, one iteration of the sampler is:

1. Choose initial values $x^{(0)} = (x_1^{(0)}, \dots, x_d^{(0)})$.
2. For $t = 1, \dots, N$:
    - draw $x_1^{(t)} \sim p(x_1 \mid x_2^{(t-1)}, \dots, x_d^{(t-1)})$;
    - draw $x_2^{(t)} \sim p(x_2 \mid x_1^{(t)}, x_3^{(t-1)}, \dots, x_d^{(t-1)})$;
    - continue in the same way for each variable, always using the newest values.

Each update leaves the joint distribution invariant, so the composition of the updates does too. Because the conditional given the others is exact, no proposal is rejected. Graphical models make the updates local: a variable's full conditional depends only on its Markov blanket, which is its neighbours in the graph. This is what makes Gibbs sampling efficient in large structured models.

## Results

Geman and Geman (1984) used Gibbs sampling, with a slowly decreasing temperature to reach a maximum a posteriori estimate, to restore degraded images under a Markov random field prior. The paper's main contribution is the framework that connects Gibbs distributions, Markov random fields and Bayesian estimation, and it gives convergence results for the annealed procedure. The paper is an early demonstration that a sampler can solve a high-dimensional estimation problem in image analysis. It does not provide the benchmark comparisons common in later machine learning papers.

Casella and George (1992) explain the sampler through worked examples of its behaviour. Their examples are analytic illustrations rather than benchmarks.

## Limitations

- **Requires conditionals.** The sampler needs to draw from each full conditional. When a conditional is not a standard distribution, a further sampler, such as a Metropolis step, must be nested inside.
- **Correlated variables.** When variables are strongly correlated, each one-at-a-time update can move only a little, and the chain mixes slowly along the direction of correlation.
- **Scan order.** The stationary distribution does not depend on the order of the updates, but the speed of mixing can, and the best order is not always obvious.
- **Multimodality.** A chain that is started in one mode may stay there for many scans.

## Open questions

- Which blocking and ordering strategies give the best mixing for a given class of graphical models?
- How can Gibbs-type updates be combined with gradient information, as in some recent hybrid samplers, without losing exactness?

## References

### Seminal papers

- Geman, S. & Geman, D. (1984). Stochastic Relaxation, Gibbs Distributions, and the Bayesian Restoration of Images. *IEEE TPAMI*. https://doi.org/10.1109/TPAMI.1984.4767596 — Applies Gibbs sampling over Markov random fields to Bayesian restoration of degraded images.

### Surveys and textbooks

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An Introduction to MCMC for Machine Learning. *Machine Learning*. https://doi.org/10.1023/A:1020281327116 — A tutorial that covers the Gibbs sampler as a special case of Metropolis-Hastings.
- Robert, C. P. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer. https://doi.org/10.1007/978-1-4757-4145-2 — A textbook treatment of the Gibbs sampler, its convergence and its use in hierarchical models.

### Articles and documentation

- Casella, G. & George, E. I. (1992). Explaining the Gibbs Sampler. *The American Statistician*. https://doi.org/10.1080/00031305.1992.10475878 — An accessible explanation of why the Gibbs sampler works, with simple worked examples.
- Kass, R. E., Carlin, B. P., Gelman, A. & Neal, R. M. (1998). Markov Chain Monte Carlo in Practice: A Roundtable Discussion. *The American Statistician*. https://doi.org/10.1080/00031305.1998.10480547 — A practitioner discussion of running and checking MCMC samplers, including Gibbs samplers.
