---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
  - brain-mind/cognitive-science
tags:
  - uncertainty
  - generative models
  - theory/math
aliases:
  - 馬可夫鏈蒙地卡羅
  - 馬可夫鏈蒙特卡羅
  - 蒙地卡羅馬可夫鏈
  - MCMC
  - Markov chain Monte Carlo
  - 哈密頓蒙地卡羅
  - 吉布斯取樣
  - 朗之萬動力學
  - Langevin dynamics
---

# Markov Chain Monte Carlo

Markov chain Monte Carlo (MCMC) is a family of algorithms that draw samples from a probability distribution by simulating a Markov chain whose long-run distribution is that target. It is the standard tool for Bayesian inference when the distribution is known only up to a constant, and it is asymptotically exact: given enough steps, its samples represent the target.

## Overview

Bayesian inference ends with a posterior distribution $p(\theta\mid D)$ over parameters or hidden causes. Its normaliser, $p(D)=\int p(D\mid\theta)\,p(\theta)\,d\theta$, is usually intractable, so the posterior can be evaluated only up to an unknown constant. Most questions asked of a posterior, such as its mean or its credible intervals, are expectations under it, and these can be estimated from samples without computing the constant.

Monte Carlo methods replace an integral with an average over samples. Drawing independent samples from a complicated, high-dimensional distribution is usually impossible, so MCMC builds a chain of dependent samples, each produced from the one before, whose stationary distribution is the target. The idea came from statistical physics, where Metropolis et al. (1953) used random moves to estimate the equation of state of interacting molecules. Andrieu et al. (2003) give a tutorial for machine learning, and Robert and Casella (2004) cover the statistical theory in a textbook.

MCMC is the main alternative to [variational inference](../variational-inference/index.md). Sampling methods are asymptotically exact but can be slow to converge. Variational methods are fast but approximate, and the relative accuracy of the two is still debated.

## Key concepts

- **Target distribution** $\pi$: the distribution to be sampled. It is often known only as an unnormalised density $\tilde\pi(x)$, where $\pi(x) = \tilde\pi(x)/Z$ and the constant $Z$ is unknown.
- **Markov chain**: a sequence $x_1, x_2, \dots$ in which each state depends only on the previous one, through a transition kernel $T(x' \mid x)$.
- **Stationary distribution**: a distribution that the chain leaves unchanged. Under mild conditions the chain converges to it from almost any starting point.
- **Detailed balance**: a sufficient condition for stationarity, $\pi(x)\,T(x'\mid x) = \pi(x')\,T(x\mid x')$. Many MCMC algorithms are designed to satisfy it.
- **Burn-in**: the early part of a run, which is discarded because the chain has not yet forgotten its starting point.
- **Autocorrelation and effective sample size**: successive samples are correlated, so $N$ draws carry less information than $N$ independent ones. The effective sample size is the number of independent draws that would give the same precision.
- **Mixing**: how quickly the chain moves across the whole target. Poor mixing is the main practical difficulty.

## How it works

Once the chain has converged, the average of a function along one long run estimates the expectation under the target:

$$
\hat f = \frac{1}{N}\sum_{t=1}^{N} f(x_t) \;\approx\; \mathbb{E}_{\pi}[f(x)].
$$

This holds because the chain is ergodic. The design task is to find a transition kernel $T$ that leaves $\pi$ invariant and mixes quickly. The usual procedure has five steps:

1. Choose a starting point $x_0$.
2. Repeatedly apply a transition that keeps $\pi$ invariant.
3. Discard the burn-in and, if storage is limited, keep every $k$-th sample (thinning).
4. Check the diagnostics listed below.
5. Compute the estimates from the retained samples.

```mermaid
flowchart LR
    T["Target known up to a constant"] --> K["Transition kernel that leaves the target invariant"]
    K --> C["Chain x_1, x_2, ..."]
    C --> B["Discard burn-in and check diagnostics"]
    B --> E["Average f(x_t) over the retained samples"]
```

The methods differ in how they build the transition. [Metropolis–Hastings](metropolis-hastings/index.md) proposes a move and accepts or rejects it. [Gibbs sampling](gibbs-sampling/index.md) updates one variable at a time from its full conditional distribution. [Hamiltonian Monte Carlo](hamiltonian-monte-carlo/index.md) uses the gradient of the log density to simulate dynamics that propose distant moves. [Langevin dynamics](langevin-dynamics/index.md) moves in the direction of the gradient with added noise.

### Diagnostics

No finite run proves convergence, so practitioners check the output. Four checks are common.

- **Trace plots.** A converged chain looks like stationary noise around a fixed level. A slow drift or a long flat stretch suggests that the burn-in is too short or the chain is stuck.
- **Gelman–Rubin statistic.** Several chains are started from dispersed points, and their between-chain and within-chain variances are compared. A value near 1 indicates agreement (Gelman & Rubin, 1992). Vehtari et al. (2019) show that the original statistic has serious flaws and propose a rank-normalised version.
- **Effective sample size.** The autocorrelation of the chain sets how many independent draws the run is worth. Geyer (1992) argues that inference should rest on one long run, with the Monte Carlo error estimated from the autocorrelation of that run.
- **Practice.** Kass et al. (1998) record a roundtable discussion of how to run and monitor chains in applied work.

## Key methods

Four landmark methods are compared below. Each has its own page.

| Method | Origin | What separates it |
|---|---|---|
| [Metropolis–Hastings](metropolis-hastings/index.md) | 1953; generalised 1970 | General and simple: propose, then accept or reject. Random-walk proposals explore slowly in high dimensions |
| [Gibbs sampling](gibbs-sampling/index.md) | 1984 | Always accepts. Each step samples one variable from its full conditional, which must be available |
| [Hamiltonian Monte Carlo and NUTS](hamiltonian-monte-carlo/index.md) | 1987; NUTS 2011 | Uses gradients to make distant, accepted moves. NUTS chooses the path length automatically |
| [Langevin dynamics](langevin-dynamics/index.md) | 1996; score-based 2019 | Drifts along the gradient with noise. Its score-based form drives modern diffusion-style generators |

## Connections

- **Bayesian methods.** MCMC is the sampling half of approximate inference, which the [parent overview](../index.md) describes next to variational methods. Gibbs sampling suits graphical models, where each variable's conditional depends only on its neighbours. Geman and Geman (1984) used this idea to restore degraded images under a Markov random field prior.
- **Generative models.** Song and Ermon (2019) generate samples by annealed Langevin dynamics, using a score estimated from data. Song et al. (2020) place score-based models and diffusion models in one framework of stochastic differential equations, in which a Langevin-type corrector refines the samples. See [Diffusion Models](../../unsupervised/density-and-generative-models/diffusion/index.md) and [DDPM](../../unsupervised/density-and-generative-models/diffusion/ddpm.md).
- **Brain and mind.** One hypothesis holds that the brain represents uncertainty by sampling. Fiser et al. (2010) review how neural activity could encode samples from a posterior, and Berkes et al. (2011) argue that spontaneous cortical activity carries hallmarks of an optimal internal model. Behavioural evidence is more mixed. Vul et al. (2014) find that people often act on one or a few samples from the posterior, far fewer than a long MCMC run would use. See [Cognitive Science](../../../../brain-mind/cognitive-science/index.md).

## Applications

- **Statistical software.** Stan, PyMC and NumPyro run MCMC, and Stan's default sampler is NUTS (Carpenter et al., 2017).
- **Image models.** Early Bayesian image restoration relied on Gibbs sampling over Markov random fields (Geman & Geman, 1984).

## Open questions

- **Mixing.** No general method guarantees fast mixing for multimodal or very high-dimensional targets, and diagnostics can miss a chain that never leaves one mode.
- **Scale.** An exact sampler may need the whole dataset at each step. Minibatch variants are faster but give up exact stationarity.
- **Automatic tuning.** Step sizes and proposal scales are still often set by hand. Adapting them while keeping the target exact is an active area.
- **Brain sampling.** Whether neural circuits sample, and how many samples they would need, is open. The behavioural evidence points to very few.

## References

### Seminal papers

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of State Calculations by Fast Computing Machines. *Journal of Chemical Physics*. https://doi.org/10.1063/1.1699114 — Introduces the Metropolis method, a Markov chain of random moves accepted by an energy criterion, for statistical-physics calculations.
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika*. https://doi.org/10.1093/biomet/57.1.97 — Generalises the acceptance rule to proposals that need not be symmetric, giving the Metropolis–Hastings algorithm.
- Geman, S. & Geman, D. (1984). Stochastic Relaxation, Gibbs Distributions, and the Bayesian Restoration of Images. *IEEE TPAMI*. https://doi.org/10.1109/TPAMI.1984.4767596 — Uses Gibbs sampling over Markov random fields for Bayesian image restoration.
- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B*. https://doi.org/10.1016/0370-2693(87)91197-X — Introduces Hamiltonian dynamics with a Metropolis correction for simulations in lattice field theory.
- Hoffman, M. D. & Gelman, A. (2011). The No-U-Turn Sampler: Adaptively Setting Path Lengths in Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1111.4246 — Introduces NUTS, which sets the number of leapfrog steps automatically and tunes the step size on the fly.
- Song, Y. & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. arXiv. https://arxiv.org/abs/1907.05600 — Generates samples with annealed Langevin dynamics driven by an estimated score of the data distribution.
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2020). Score-Based Generative Modeling through Stochastic Differential Equations. arXiv. https://arxiv.org/abs/2011.13456 — Unifies score-based and diffusion models through forward and reverse-time SDEs with a predictor-corrector sampler.

### Surveys and textbooks

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An Introduction to MCMC for Machine Learning. *Machine Learning*. https://doi.org/10.1023/A:1020281327116 — A tutorial that explains the main MCMC algorithms for readers from machine learning.
- Robert, C. P. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer. https://doi.org/10.1007/978-1-4757-4145-2 — A graduate textbook covering the theory and practice of Monte Carlo and MCMC methods.
- Neal, R. M. (2012). MCMC using Hamiltonian dynamics. arXiv. https://arxiv.org/abs/1206.1901 — A tutorial chapter on Hamiltonian Monte Carlo and its use within Metropolis-type samplers.
- Fiser, J., Berkes, P., Orbán, G. & Lengyel, M. (2010). Statistically optimal perception and learning: from behavior to neural representations. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2010.01.003 — A review of how Bayesian inference could be implemented by neural representations, including sampling-based codes.

### Articles and documentation

- Berkes, P., Orbán, G., Lengyel, M. & Fiser, J. (2011). Spontaneous Cortical Activity Reveals Hallmarks of an Optimal Internal Model of the Environment. *Science*. https://doi.org/10.1126/science.1195870 — Reports that spontaneous cortical activity shows the statistical hallmarks of an optimal internal model.
- Vul, E., Goodman, N., Griffiths, T. L. & Tenenbaum, J. B. (2014). One and Done? Optimal Decisions From Very Few Samples. *Cognitive Science*. https://doi.org/10.1111/cogs.12101 — Argues that human decisions can be explained by using very few posterior samples.
- Geyer, C. J. (1992). Practical Markov Chain Monte Carlo. *Statistical Science*. https://doi.org/10.1214/ss/1177011137 — Argues for basing inference on a single long run and estimating Monte Carlo error from autocorrelation.
- Gelman, A. & Rubin, D. B. (1992). Inference from Iterative Simulation Using Multiple Sequences. *Statistical Science*. https://doi.org/10.1214/ss/1177011136 — The original multi-chain convergence diagnostic, which compares within-chain and between-chain variance.
- Vehtari, A., Gelman, A., Simpson, D., Carpenter, B. & Bürkner, P.-C. (2019). Rank-normalization, folding, and localization: An improved R-hat for assessing convergence of MCMC. arXiv. https://arxiv.org/abs/1903.08008 — Shows flaws in the classic R-hat and proposes a more reliable rank-normalised version.
- Kass, R. E., Carlin, B. P., Gelman, A. & Neal, R. M. (1998). Markov Chain Monte Carlo in Practice: A Roundtable Discussion. *The American Statistician*. https://doi.org/10.1080/00031305.1998.10480547 — A discussion among practitioners of how to run, monitor and report MCMC analyses.
- Betancourt, M. (2017). A Conceptual Introduction to Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1701.02434 — Explains geometrically why Hamiltonian Monte Carlo works well and how it should be tuned.
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., et al. (2017). Stan: A Probabilistic Programming Language. *Journal of Statistical Software*. https://doi.org/10.18637/jss.v076.i01 — Describes the Stan system, which implements NUTS and is widely used for Bayesian inference.
