---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/math/automatic-differentiation
tags:
  - optimization
  - uncertainty
aliases:
  - 哈密頓蒙地卡羅
  - 混合蒙地卡羅
  - 不掉頭取樣器
  - Hamiltonian Monte Carlo
  - HMC
  - NUTS
  - No-U-Turn Sampler
---

# Hamiltonian Monte Carlo and NUTS

Hamiltonian Monte Carlo (HMC) is an [MCMC](../index.md) method that uses the gradient of the log density to propose distant moves. It simulates the physical dynamics of a particle moving on the negative log density, then corrects the result with an accept–reject step. The No-U-Turn Sampler (NUTS) removes the need to set the simulation length by hand, and it is the default sampler in Stan.

## Overview

Random-walk proposals, such as those in [Metropolis–Hastings](../metropolis-hastings/index.md), explore a distribution slowly because each proposal is a small, nearly random step. HMC takes its proposals from a physical model instead. The particle moves over a landscape whose height is the negative log density, so it travels far while staying probable. The method was introduced by Duane et al. (1987) for simulations in lattice field theory, under the name hybrid Monte Carlo. Neal (2012) brought it to statistics with a tutorial, and Betancourt (2017) gives a geometric account of why it works well on difficult targets.

HMC needs a differentiable target, with gradients usually supplied by [automatic differentiation](../../../../math/automatic-differentiation/index.md). Its main drawback is tuning the step size and the number of steps, and NUTS removes the second of these choices.

## Key concepts

- **Position and momentum**: the sampler introduces an auxiliary momentum $p$ for each parameter $q$. Position $q$ is the variable of interest and momentum is discarded after each step.
- **Hamiltonian**: the total energy $H(q, p) = U(q) + K(p)$, the sum of a potential energy $U(q) = -\log\tilde\pi(q)$ and a kinetic energy $K(p)$.
- **Leapfrog integrator**: a numerical scheme that approximates the dynamics with step size $\varepsilon$. It is time-reversible and volume-preserving, which the accept–reject step relies on.
- **Mass matrix** $M$: a matrix that rescales the momentum. Choosing it well is important when the parameters have very different scales.
- **Trajectory length**: the number of leapfrog steps. Too few gives random-walk behaviour, and too many wastes computation.

## How it works

The Hamiltonian dynamics are

$$
\frac{dq}{dt} = M^{-1}p, \qquad \frac{dp}{dt} = \nabla_q \log\tilde\pi(q).
$$

Because the energy is conserved along exact dynamics, a state at the end of a trajectory has the same probability as the start. Errors from the discrete integrator are corrected by an accept–reject step. One HMC update is:

1. Draw a momentum $p \sim \mathcal{N}(0, M)$.
2. Run $L$ leapfrog steps from $(q, p)$. Each leapfrog step updates $p$ by half a step using the gradient at $q$, then moves $q$ by a full step, then updates $p$ by another half step using the gradient at the new $q$.
3. Accept the endpoint $(q^*, p^*)$ with probability $\min\!\big(1, \exp\{H(q,p) - H(q^*,p^*)\}\big)$, otherwise keep $q$.

NUTS replaces the fixed $L$ with an adaptive rule. Starting from the current state, it doubles a trajectory in a random direction and builds a binary tree of states. It stops when the trajectory begins to double back on itself, which is detected by a U-turn condition on the momentum at the two ends. The step size is adapted during warm-up by primal–dual averaging (Hoffman & Gelman, 2011). Stan implements this scheme as its default sampler (Carpenter et al., 2017).

## Results

Hoffman and Gelman (2011) compare NUTS with a well-tuned standard HMC on several models. Their main claim is that NUTS performs at least as efficiently as the tuned HMC and sometimes more efficiently, while requiring no user intervention or costly tuning runs. The paper also introduces the step-size adaptation that makes this possible. The evidence is an empirical comparison on a set of test models, and the paper makes no claim of a universal speed-up.

## Limitations

- **Gradients needed.** Any target with discrete variables, or whose density cannot be differentiated, falls outside the method's domain unless it is reparameterised.
- **Geometry.** HMC's efficiency depends on the shape of the target. Betancourt (2017) explains why it succeeds on well-behaved geometries, and difficult geometries, such as narrow funnels in hierarchical models, can cause it to struggle.
- **Tuning.** The mass matrix and step size must still be set well. Riemannian variants can adapt the geometry automatically, but at extra cost (Girolami & Calderhead, 2011).
- **Multimodality.** Like other local samplers, HMC explores one mode at a time.

## Open questions

- How should the mass matrix be learned during a run, and how well do such schemes work in very high dimensions?
- Can HMC-type samplers be made efficient for discrete parameters, which many models contain?

## References

### Seminal papers

- Duane, S., Kennedy, A. D., Pendleton, B. J. & Roweth, D. (1987). Hybrid Monte Carlo. *Physics Letters B*. https://doi.org/10.1016/0370-2693(87)91197-X — Introduces hybrid Monte Carlo, which combines Hamiltonian dynamics with a Metropolis correction, for lattice field theory.
- Hoffman, M. D. & Gelman, A. (2011). The No-U-Turn Sampler: Adaptively Setting Path Lengths in Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1111.4246 — Introduces NUTS, which stops the trajectory automatically when it doubles back and adapts the step size.

### Surveys and textbooks

- Neal, R. M. (2012). MCMC using Hamiltonian dynamics. arXiv. https://arxiv.org/abs/1206.1901 — A tutorial on Hamiltonian dynamics as a proposal mechanism for MCMC, with practical advice on tuning.

### Articles and documentation

- Betancourt, M. (2017). A Conceptual Introduction to Hamiltonian Monte Carlo. arXiv. https://arxiv.org/abs/1701.02434 — Explains the geometry behind HMC's performance and how the sampler should be applied in practice.
- Girolami, M. & Calderhead, B. (2011). Riemann Manifold Langevin and Hamiltonian Monte Carlo Methods. *JRSS B*. https://doi.org/10.1111/j.1467-9868.2010.00765.x — Extends HMC and Langevin methods to a Riemannian geometry that adapts the proposals automatically.
- Carpenter, B., Gelman, A., Hoffman, M. D., Lee, D., Goodrich, B., Betancourt, M., et al. (2017). Stan: A Probabilistic Programming Language. *Journal of Statistical Software*. https://doi.org/10.18637/jss.v076.i01 — Describes Stan, the software that implements NUTS as its default sampler.
