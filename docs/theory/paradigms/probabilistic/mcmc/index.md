---
status: complete
last_reviewed: 2026-11-19
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

Markov chain Monte Carlo (MCMC) estimates expectations using a sequence of dependent draws from a Markov chain designed to preserve a target distribution. It is widely used for posterior inference when direct independent sampling is difficult. Part of [Probabilistic & Bayesian methods](../index.md).[^intro]

## Overview

Many Bayesian computations need expectations under a posterior $\pi(\theta)=p(\theta\mid D)$ known only up to a normalising constant. MCMC constructs transitions from the current state to the next. Under suitable convergence conditions, averages along the chain approach expectations under $\pi$.[^intro]

The [Metropolis–Hastings](metropolis-hastings.md), [Gibbs sampling](gibbs-sampling.md) and [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md) pages explain particular transition rules. Choosing a valid rule and assessing how efficiently its output explores the target are both part of using MCMC.

## Key concepts

- **Markov property** means that, conditional on the current state, the next state is independent of earlier states.
- **Stationary distribution** is a distribution preserved by a transition. Starting a chain in that distribution keeps each subsequent state's marginal distribution the same.
- **Mixing** describes how quickly the chain explores its target and loses the effect of its starting state.
- **Warmup or burn-in** is an initial segment excluded from the reported sample. Warmup can also adapt sampler settings, as in NUTS.[^nuts]
- **Effective sample size (ESS)** describes Monte Carlo precision for a particular estimated quantity, accounting for dependence between draws.[^stan]

## How it works

### Preserve the target and establish convergence

For a finite state space, let $P_{ij}$ be the probability of moving from state $i$ to state $j$. Each row sums to one. With $\pi$ written as a row vector, stationarity requires

$$
\pi P=\pi.
$$

A sufficient condition is **detailed balance**, $\pi_iP_{ij}=\pi_jP_{ji}$, which balances the stationary probability flow in each direction. For a finite chain, irreducibility and aperiodicity ensure convergence to its unique stationary distribution. Irreducibility means every state can be reached from every other state, and aperiodicity rules out returns restricted to a fixed cycle. Continuous state spaces require corresponding general-state-space conditions.[^intro]

The identity matrix preserves every distribution, but a chain using it stays at its initial state forever. Thus checking stationarity alone cannot establish that a run explores the target.

### Estimate a quantity and its Monte Carlo error

For $N$ retained draws and a scalar function $f$, estimate

$$
\widehat{\mu}_f=\frac{1}{N}\sum_{t=1}^{N} f(\theta^{(t)}).
$$

Keep repeated states after a rejected proposal when forming ordinary chain averages. They represent time spent at that state.[^intro]

For a stationary chain, write $\rho_f(k)$ for the lag-$k$ autocorrelation of $f(\theta^{(t)})$. With finite variance, a summable autocorrelation series and a valid Markov chain central limit theorem, define the integrated autocorrelation time and the corresponding asymptotic ESS by[^stan]

$$
\tau_f=1+2\sum_{k=1}^{\infty}\rho_f(k),
\qquad
N_{\mathrm{eff},f}=\frac{N}{\tau_f}.
$$

The approximate Monte Carlo standard error of the estimated mean is

$$
\operatorname{MCSE}(\widehat{\mu}_f)
\approx
\sqrt{\frac{\operatorname{Var}_{\pi}(f)}{N_{\mathrm{eff},f}}}.
$$

This measures error in the numerical estimate of an expectation. A posterior standard deviation instead describes uncertainty in the model's target distribution. ESS depends on $f$, so a mean and a tail probability can have different precision from the same draws.[^diagnostics]

### Two chains with the same target

Consider an illustrative two-state target $\pi=(1/4,3/4)$ over states $A,B$. For $0<a<1/4$, define

$$
P_a=
\begin{pmatrix}
1-3a & 3a\\
a & 1-a
\end{pmatrix}.
$$

The flows balance because $(1/4)(3a)=(3/4)a$. Both states communicate and have self-transitions, so the chain converges to $\pi$. Yet the rate depends strongly on $a$.

For $f(B)=1$ and $f(A)=0$, the stationary mean is $3/4$ and the variance is $3/16$. The centred function is an eigenvector of $P_a$ with eigenvalue $\lambda=1-4a$. Consequently $\rho_f(k)=\lambda^k$ and $\tau_f=(1+\lambda)/(1-\lambda)$.

| Transition parameter | $\lambda$ | $\tau_f$ | Asymptotic ESS for $N=1000$ |
|---|---:|---:|---:|
| $a=1/6$ | $1/3$ | $2$ | $500$ |
| $a=1/100$ | $0.96$ | $49$ | $20.4$ |

These are analytic calculations for stationary chains. The second chain spends longer in each state, leaving substantially less information about the probability of $B$ for the same number of draws. A valid stationary distribution does not determine sampling efficiency.

## Key methods

- [Metropolis–Hastings](metropolis-hastings.md) proposes moves and applies an acceptance ratio that accounts for both forward and reverse proposals.[^intro]
- [Gibbs sampling](gibbs-sampling.md) draws from full conditional distributions, updating variables or blocks.[^intro]
- [Hamiltonian Monte Carlo](hamiltonian-monte-carlo.md) uses gradients and simulated dynamics to explore continuous targets.[^neal] NUTS adapts the trajectory length.[^nuts]

## Connections and applications

- [Variational inference](../variational-inference/index.md) approximates a posterior by optimisation. MCMC and VI have different sources of error and computational costs.
- [Probability and statistics](../../../math/probability-statistics/index.md) gives the posterior and expectation calculations that MCMC approximates.
- Posterior samples support Bayesian estimates, credible intervals and predictions. Probabilistic programming systems use samplers such as NUTS for user-defined models.[^nuts]

## Diagnostics and limitations

- **Compare multiple chains.** Use dispersed initial values and inspect trace or rank plots. Rank-normalised split and folded $\widehat{R}$ diagnostics detect differences in location and scale between chains. Vehtari et al. recommend $\widehat{R}<1.01$ as part of a broader diagnostic assessment.[^diagnostics]
- **Check the quantities being reported.** Inspect bulk and tail ESS, and compute MCSE for the actual mean, quantile or probability of interest. Rank-based bulk ESS is a diagnostic and does not directly supply the MCSE of a raw posterior mean.[^diagnostics]
- **Assess exploration.** Discarding a chosen number of warmup draws does not establish convergence. Chains can agree while all miss an isolated mode, so diagnostics provide evidence about a finite run with limited access to the state space.[^diagnostics]
- **Consider cost per effective draw.** Small steps can create strong positive autocorrelation. HMC can reduce random-walk behaviour, but its gradients and trajectory calculations also cost computation.[^neal] Compare precision for the quantity of interest within a computational budget.

[^intro]: Andrieu et al. (2003), §3, explain transition kernels, stationary distributions, convergence conditions and the standard MCMC algorithms.
[^stan]: Stan Development Team, *Posterior Analysis*, derives autocorrelation-based ESS and the Monte Carlo standard error of a mean.
[^diagnostics]: Vehtari et al. (2021), §§2–4, develop rank-based diagnostics, local ESS and Monte Carlo error estimates, and discuss the limits of convergence checks.
[^neal]: Neal (2011) reviews Hamiltonian dynamics, random-walk behaviour and computational tradeoffs in MCMC.
[^nuts]: Hoffman & Gelman (2014) describe NUTS, its path-length selection and warmup adaptation.

## References

### Seminal papers

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of state calculations by fast computing machines. *Journal of Chemical Physics* 21(6), 1087–1092. https://doi.org/10.1063/1.1699114 — Introduces the Metropolis algorithm for sampling from a Boltzmann distribution.
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika* 57(1), 97–109. https://doi.org/10.1093/biomet/57.1.97 — Generalises the Metropolis rule to asymmetric proposals.
- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B* 195(2), 216–222. https://doi.org/10.1016/0370-2693(87)91197-X — Introduces the hybrid (Hamiltonian) Monte Carlo method.

### Surveys and textbooks

- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An introduction to MCMC for machine learning. *Machine Learning* 50, 5–43. https://www.cs.ubc.ca/~nando/papers/mlintro.pdf — Tutorial on MCMC for machine learning, covering Metropolis–Hastings, Gibbs and their relations.
- Neal, R. M. (2011). MCMC using Hamiltonian dynamics. In *Handbook of Markov Chain Monte Carlo*. arXiv:1206.1901. https://arxiv.org/abs/1206.1901 — Review of HMC, its tuning, and its advantages over random-walk samplers.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers MCMC methods and their diagnostics.

- Vehtari, A., Gelman, A., Simpson, D., Carpenter, B. & Bürkner, P.-C. (2021). *Rank-normalization, folding, and localization: An improved R-hat for assessing convergence of MCMC*. Bayesian Analysis. https://arxiv.org/abs/1903.08008 — Develops rank-based convergence diagnostics and effective sample sizes for different parts of a distribution.

### Articles and documentation

- Hoffman, M. D. & Gelman, A. (2014). The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research* 15. https://jmlr.org/papers/v15/hoffman14a.html — Introduces NUTS, which tunes the path length of HMC automatically.

- Stan Development Team. *Stan Reference Manual: Posterior Analysis*. https://mc-stan.org/docs/reference-manual/analysis.html — Explains multiple-chain diagnostics, autocorrelation, effective sample size and Monte Carlo standard errors.
