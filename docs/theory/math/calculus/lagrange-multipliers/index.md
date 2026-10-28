---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/paradigms/supervised/kernel-methods-svm
tags:
  - optimization
  - learning theory
aliases:
  - 拉格朗日乘數
  - KKT 條件
  - Karush–Kuhn–Tucker 條件
  - Lagrange multipliers
  - KKT conditions
  - Lagrangian
---

# Lagrange Multipliers and the KKT Conditions

Lagrange multipliers turn a constrained minimisation into conditions on gradients, by adding each constraint to the objective with a weight that is itself a variable. The Karush–Kuhn–Tucker (KKT) conditions extend the method to inequality constraints. They underlie the dual problem of support-vector machines and the trust-region constraints used in constrained reinforcement learning.

## Overview

Many learning problems minimise a loss subject to constraints, such as a bound on the weights, a margin that training examples must respect, or a limit on how far a new policy may move. With constraints, the minimum can lie on the boundary of the feasible set, where the gradient need not vanish.

Lagrange's method handles equality constraints by requiring a combined function to be stationary. Kuhn and Tucker (1951) extended it to inequality constraints, and the conditions are now called the KKT conditions. Boyd and Vandenberghe (2004) treat convex problems in full, where the conditions are also sufficient. This is the third landmark method of the [calculus and optimisation foundations](../index.md) page.

## Key concepts

- **Problem form**: minimise $f(x)$ subject to $g_i(x)\le 0$ for $i=1,\dots,m$ and $h_j(x)=0$ for $j=1,\dots,p$.
- **Lagrangian**: $\mathcal{L}(x,\lambda,\nu)=f(x)+\sum_i\lambda_i g_i(x)+\sum_j\nu_j h_j(x)$, with inequality multipliers $\lambda_i\ge 0$.
- **Multiplier as sensitivity**: relaxing an inequality $g_i(x)\le c$ by changing $c$ lowers the optimal value $p^*(c)$ at rate $-\lambda_i^*$. A large multiplier marks a binding, costly constraint.
- **Active constraint**: one that holds with equality at the optimum. Only active constraints can have nonzero multipliers.
- **Dual function**: $d(\lambda,\nu)=\inf_x\mathcal{L}(x,\lambda,\nu)$. For feasible multipliers with $\lambda\ge 0$ it lower-bounds the optimal value, and maximising it gives the dual problem.
- **Constraint qualification**: a regularity condition, such as linear independence of the active constraint gradients, that guarantees multipliers exist at an optimum.

## How it works

At a constrained minimiser, no feasible direction decreases $f$. Under a constraint qualification, the gradient of $f$ is then a combination of the gradients of the active constraints, with the right signs, and the Lagrange multipliers are the coefficients of that combination. For a minimiser $x^*$ the first-order conditions are the KKT conditions:

$$
\begin{aligned}
&\nabla f(x^*)+\sum_i\lambda_i^*\nabla g_i(x^*)+\sum_j\nu_j^*\nabla h_j(x^*)=0 &&\text{(stationarity)}\\
&g_i(x^*)\le 0,\qquad h_j(x^*)=0 &&\text{(primal feasibility)}\\
&\lambda_i^*\ge 0 &&\text{(dual feasibility)}\\
&\lambda_i^*\,g_i(x^*)=0 &&\text{(complementary slackness)}
\end{aligned}
$$

Complementary slackness says that a constraint with a positive multiplier is active, and an inactive constraint has a zero multiplier. This is why only a few constraints shape the solution.

**A worked example.** Minimise $\tfrac12\lVert x\rVert^2$ subject to $a^\top x=b$, where $a\ne 0$. The Lagrangian is $\tfrac12\lVert x\rVert^2+\nu(a^\top x-b)$. Stationarity gives $x=-\nu a$, and feasibility then gives $\nu=-b/\lVert a\rVert^2$. The solution is $x^*=(b/\lVert a\rVert^2)\,a$, the point on the hyperplane nearest the origin.

**Duality in practice.** For a convex problem satisfying Slater's condition, the primal and dual optimal values agree, and the KKT conditions are necessary and sufficient. Some solvers, such as those for support-vector machines, therefore work with the dual problem.

## Results

The evidence is theoretical, with two applications and no benchmark table.

- **KKT conditions.** Kuhn and Tucker (1951) state first-order conditions for a constrained optimum under a regularity assumption. Nocedal and Wright (2006) cover them as the basis of constrained optimisation, and Boyd and Vandenberghe (2004) show that they are sufficient for convex problems.
- **Support-vector machines.** Cortes and Vapnik (1995) introduced the soft-margin machine, whose training problem is a quadratic program solved through its Lagrangian dual. The nonzero multipliers identify the support vectors, the training points on or inside the margin.
- **Trust-region policy optimisation.** Schulman and colleagues (2015) update a policy within a KL bound, solving the constrained problem with approximations. Their experiments report robust performance on locomotion and Atari tasks.

## Limitations

- **Necessity, not sufficiency.** For nonconvex problems the KKT conditions are necessary at a local minimiser, but a point satisfying them may be a local maximum or a saddle.
- **Constraint qualifications.** When constraints are degenerate, for example when two coincide, multipliers may not exist and the KKT conditions may fail at the optimum.
- **Approximation.** Practical methods approximate the problem, so the theory's guarantees no longer hold exactly.

## Open questions

- **Constrained training of deep networks.** Safety, fairness or resource constraints can be written as inequalities on a network's outputs. Guaranteeing them with nonconvex losses and stochastic gradients is not settled.
- **Stability of primal-dual methods.** Alternating updates of parameters and multipliers can oscillate, and stable conditions for deep learning are open.
- **Choice of constraint.** Whether a KL bound or another divergence is the best trust region is still debated.

## References

### Seminal papers

- Kuhn, H. W. & Tucker, A. W. (1951). Nonlinear Programming. *Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability*. https://doi.org/10.1525/9780520411586-036 — Gives the first-order conditions for a constrained optimum, the origin of the KKT conditions.
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning*. https://doi.org/10.1007/BF00994018 — Introduces the soft-margin support-vector machine, trained through its Lagrangian dual.
- Schulman, J. et al. (2015). Trust Region Policy Optimization. arXiv. https://arxiv.org/abs/1502.05477 — Optimises policies within a KL trust region, using practical approximations.

### Surveys and textbooks

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://doi.org/10.1017/CBO9780511804441 — Textbook on duality, Slater's condition and the KKT conditions for convex problems.
- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*. Springer. https://doi.org/10.1007/978-0-387-40065-5 — Covers the KKT conditions, constraint qualifications and constrained methods.
