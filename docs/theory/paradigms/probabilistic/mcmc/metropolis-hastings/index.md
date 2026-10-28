---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - uncertainty
  - theory/math
aliases:
  - Metropolis–Hastings 演算法
  - 大都會-黑斯廷斯演算法
  - Metropolis-Hastings
  - Metropolis algorithm
  - MH
---

# Metropolis–Hastings

Metropolis–Hastings is the basic [Markov chain Monte Carlo](../index.md) algorithm. It proposes a move from the current state and accepts it with a probability chosen so that the target distribution is left invariant. Almost every other MCMC method is either a special case of it or a variant of its accept–reject step.

## Overview

The algorithm needs only an unnormalised density of the target, so the normalising constant that makes Bayesian inference hard never has to be computed. It works for any target that can be evaluated, and it needs no gradients. The method was introduced by Metropolis et al. (1953) for equations of state in statistical physics. Hastings (1970) generalised the acceptance rule to proposals that need not be symmetric, which is the form in use today. Chib and Greenberg (1995) give a clear account of the acceptance rule and its derivation.

The price of this generality is slow exploration: random-walk proposals need many small steps, and the number needed grows quickly with dimension.

## Key concepts

- **Proposal distribution** $q(x' \mid x)$: the rule that suggests a new state $x'$ from the current state $x$. A random-walk proposal adds Gaussian noise to $x$.
- **Acceptance probability**: the chance of moving to the proposal, given by the ratio of target and proposal densities.
- **Rejection**: if the proposal is refused, the chain stays where it is, which slows mixing.
- **Step size**: the scale of the proposal. Large steps are often rejected, and small steps move slowly, so the scale must be balanced.

## How it works

Let $\tilde\pi$ be the unnormalised target. A proposal $x'$ is accepted with probability

$$
\alpha(x, x') = \min\!\left(1,\; \frac{\tilde\pi(x')\,q(x \mid x')}{\tilde\pi(x)\,q(x' \mid x)}\right).
$$

The normalising constant cancels in the ratio. For a symmetric proposal, $q(x\mid x') = q(x'\mid x)$, and the factor reduces to the Metropolis ratio $\tilde\pi(x')/\tilde\pi(x)$. The algorithm is:

1. Set $x_0$ to any state where $\tilde\pi(x_0) > 0$.
2. For $t = 1, \dots, N$, draw $x' \sim q(\cdot \mid x_{t-1})$.
3. Draw $u \sim \mathrm{Uniform}(0, 1)$. If $u < \alpha(x_{t-1}, x')$, set $x_t = x'$; otherwise set $x_t = x_{t-1}$.

Detailed balance holds for this rule. Moving from $x$ to $x'$ has probability $q(x'\mid x)\,\alpha(x,x')$, and the ratio of the two directions of the flow equals the ratio of target densities, so the target is stationary. The chain is then used as described on the [parent page](../index.md).

In practice, early samples depend on the starting point, so burn-in is discarded, and the acceptance rate is monitored while tuning the step size.

## Results

Metropolis et al. (1953) applied the method to a two-dimensional system of rigid spheres. They compared the simulated equation of state with the free-volume equation and with a four-term virial expansion. The paper shows that a simple chain of random moves can compute properties that are hard to obtain analytically. It reports no benchmark in the modern sense, so its evidence is qualitative agreement with reference results.

For Metropolis–Hastings in statistics, the main theoretical guidance comes later. Roberts and Rosenthal (1998) show, for a closely related gradient-based proposal, that the acceptance rate that makes the algorithm most efficient in high dimensions is about 0.574, and that the cost grows more slowly with dimension than for random-walk proposals.

## Limitations

- **Slow exploration.** Random-walk proposals move in small, diffusive steps. In high dimensions the step size must shrink, and the number of steps needed grows rapidly.
- **Correlated targets.** If the target is a narrow ridge that is not aligned with the coordinate axes, a proposal that changes one coordinate at a time is almost always rejected.
- **Tuning.** The proposal scale must be set by hand or by adaptive schemes that preserve the target, which adds practical complexity.
- **Multimodal targets.** A chain started in one mode can take a very long time to find the others.

## Open questions

- How should proposals be adapted during a run without losing the guarantee that the target is exact?
- Which proposals scale best for a given family of targets, beyond the Gaussian-like cases that the optimal-scaling theory covers?

## References

### Seminal papers

- Metropolis, N., Rosenbluth, A. W., Rosenbluth, M. N., Teller, A. H. & Teller, E. (1953). Equation of State Calculations by Fast Computing Machines. *Journal of Chemical Physics*. https://doi.org/10.1063/1.1699114 — Introduces the accept–reject chain for computing equations of state of interacting particles.
- Hastings, W. K. (1970). Monte Carlo sampling methods using Markov chains and their applications. *Biometrika*. https://doi.org/10.1093/biomet/57.1.97 — Generalises the acceptance rule to asymmetric proposals, giving the form used today.

### Surveys and textbooks

- Chib, S. & Greenberg, E. (1995). Understanding the Metropolis-Hastings Algorithm. *The American Statistician*. https://doi.org/10.1080/00031305.1995.10476177 — A clear derivation of the acceptance rule and an account of how it is used in practice.
- Robert, C. P. & Casella, G. (2004). *Monte Carlo Statistical Methods*. Springer. https://doi.org/10.1007/978-1-4757-4145-2 — A textbook treatment of Metropolis-Hastings and related samplers with their theory.
- Andrieu, C., de Freitas, N., Doucet, A. & Jordan, M. I. (2003). An Introduction to MCMC for Machine Learning. *Machine Learning*. https://doi.org/10.1023/A:1020281327116 — A tutorial that presents Metropolis-Hastings as the basic building block of MCMC for machine learning.

### Articles and documentation

- Roberts, G. O. & Rosenthal, J. S. (1998). Optimal Scaling of Discrete Approximations to Langevin Diffusions. *JRSS B*. https://doi.org/10.1111/1467-9868.00123 — Gives the optimal acceptance rate and the dimension scaling for Metropolis-type proposals derived from Langevin diffusions.
- Geyer, C. J. (1992). Practical Markov Chain Monte Carlo. *Statistical Science*. https://doi.org/10.1214/ss/1177011137 — Practical advice on running Metropolis-Hastings chains and estimating their Monte Carlo error.
