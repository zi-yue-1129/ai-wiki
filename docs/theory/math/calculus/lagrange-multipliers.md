---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/paradigms/supervised
tags:
  - mathematics
  - optimisation
  - constrained optimisation
aliases:
  - 拉格朗日乘數法
  - 拉格朗日乘子
  - Lagrange multiplier
  - KKT conditions
---

# Lagrange Multipliers

Lagrange multipliers solve optimisation problems with equality or inequality constraints. They replace the constrained problem with an unconstrained one that has extra variables, the multipliers, one for each constraint. Support vector machines and constrained reinforcement-learning objectives are built this way. Part of [Calculus and optimisation foundations](index.md).

## Overview

Many learning problems have constraints. A margin classifier must separate the classes, a policy must stay close to a reference policy, and a probability vector must sum to one. Solving \(\min_x f(x)\) subject to \(g(x)=0\) directly is hard, because the feasible set is curved. The Lagrange approach adds \(\lambda g(x)\) to the objective and asks where the combined function is stationary.

## Key concepts

- **Lagrangian**: \(\mathcal{L}(x,\lambda) = f(x) + \lambda\, g(x)\). Its stationary points give candidate solutions.
- **Multiplier**: \(\lambda\) measures how much the optimal value would change if the constraint were relaxed.
- **Inequality constraints**: \(h(x)\le 0\) add a non-negative multiplier \(\mu\ge 0\) and a complementary slackness condition \(\mu\,h(x)=0\).
- **KKT conditions**: the first-order necessary conditions for constrained optimisation with inequalities, named after Karush, Kuhn and Tucker.
- **Duality**: the dual problem maximises the Lagrangian over the primal variables. It can be easier to solve, and it is how kernels enter support vector machines.

## How it works

For a single equality constraint, a stationary point of \(\mathcal{L}\) satisfies

\[
\nabla f(x) + \lambda \nabla g(x) = 0, \qquad g(x)=0.
\]

Geometrically, at the optimum the gradient of the objective is parallel to the gradient of the constraint. For inequality constraints the KKT conditions add \(\mu\ge 0\) and \(\mu\,h(x)=0\). The support vector machine is the classic example: its dual problem involves only the training points that lie on the margin, whose multipliers are non-zero (Cortes & Vapnik, 1995).

Lagrange multipliers also appear in deep learning as penalty terms with fixed or adaptive weights, when an inequality constraint is enforced by a penalty rather than solved exactly.

## Key methods

- [Newton's method](newtons-method.md): a second-order method that can be applied to the Lagrangian's stationarity conditions, as an alternative to the first-order KKT approach.
- Interior-point methods: handle inequality constraints by barrier terms, a related but distinct approach described in Boyd and Vandenberghe (2004).

## Connections

- [Calculus and optimisation foundations](index.md) gives the gradient calculus that the stationarity conditions use.
- [Linear algebra](../linear-algebra/index.md) shows how constraints on weight norms relate to projections.
- The support vector machine appears in [supervised learning](../../paradigms/supervised/index.md).

## Applications

- **Support vector machines**: maximum-margin classifiers solved through the dual problem (Cortes & Vapnik, 1995).
- **Constrained policy updates**: trust-region methods limit how far a policy moves per update using a constraint on the KL divergence (see [reinforcement learning](../../paradigms/reinforcement-learning/index.md)).
- **Fairness and safety constraints**: constrained training problems use multipliers to enforce a measurable requirement (Boyd & Vandenberghe, 2004).

## Open questions

- Constrained training of large models, with stochastic gradients, can be unstable. The multiplier updates interact with the parameter updates in ways that are not fully understood.
- Non-convex constraints have no general duality guarantee, so KKT conditions are necessary but may not yield a global solution.

## References

### Seminal papers

- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning* 20. https://link.springer.com/doi/10.1007/BF00994018 — Applies constrained optimisation with multipliers to derive the support vector machine.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Presents Lagrange duality, the KKT conditions and their use in convex problems.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Covers constrained optimisation and the Lagrangian in its treatment of support vector machines.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers the constrained formulations used for kernel methods.

### Articles and documentation

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Surveys optimisation methods for learning, including constrained formulations and their practical costs.
