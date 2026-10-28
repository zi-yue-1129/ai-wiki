---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
tags:
  - optimization
  - gradient descent
aliases:
  - 梯度下降
  - 梯度下降法
  - Gradient descent
  - Convergence rate
  - 收斂速率
---

# Gradient Descent and Its Convergence

Gradient descent minimises a differentiable function by repeatedly stepping against its gradient. Its guarantees come from calculus: a Taylor bound on how far the function can rise after a step, and convexity, which relates a small gradient to the distance to the minimum. It is the first-order method of the [calculus and optimisation foundations](../index.md) page.

## Overview

Given a loss $f$ and a starting point $x_0$, the method iterates $x_{k+1}=x_k-\eta\nabla f(x_k)$, where $\eta$ is the step size, or learning rate. [Stochastic gradient descent](../../../optimization/sgd-and-momentum/index.md) replaces the exact gradient with a noisy estimate from a mini-batch.

Polyak (1963) gave a simple condition under which gradient methods converge linearly. Nesterov (2004) sets out the rates for smooth convex functions and an accelerated variant that improves them. Karimi, Nutini and Schmidt (2016) showed that Polyak's condition gives linear convergence without convexity.

## Key concepts

- **Step size** $\eta$: a step that is too large overshoots the minimum; one that is too small makes slow progress.
- **$L$-smoothness**: the gradient is $L$-Lipschitz, $\lVert\nabla f(x)-\nabla f(y)\rVert\le L\lVert x-y\rVert$.
- **Convexity**: $f(y)\ge f(x)+\nabla f(x)^\top(y-x)$ for all $x, y$. The tangent plane at any point lies below the graph.
- **Strong convexity** with modulus $\mu>0$ adds the term $\tfrac{\mu}{2}\lVert y-x\rVert^2$ to the right-hand side. The condition number $\kappa=L/\mu$ measures how unevenly the function curves.
- **Polyak–Łojasiewicz (PL) condition**: $\tfrac12\lVert\nabla f(x)\rVert^2\ge\mu\,(f(x)-f^*)$, where $f^*$ is the minimum value. It does not require convexity.

## How it works

The analysis rests on the quadratic upper bound from the [overview](../index.md). For an $L$-smooth function,

$$
f(y)\le f(x)+\nabla f(x)^\top(y-x)+\tfrac{L}{2}\lVert y-x\rVert^2 .
$$

Put $y=x-\eta\nabla f(x)$ and take $\eta=1/L$. The bound gives

$$
f(x_{k+1})\le f(x_k)-\frac{1}{2L}\lVert\nabla f(x_k)\rVert^2 .
$$

Each step lowers the loss by an amount proportional to the squared gradient. A step above $2/L$ can make the loss grow, even on a quadratic, so $1/L$ is a safe choice when $L$ is known.

**Convex case.** Convexity relates the gap $f(x_k)-f^*$ to the gradient norm. With the decrease above, the gap after $T$ steps is bounded by a constant times $L\lVert x_0-x^*\rVert^2/T$, an $O(1/T)$ rate. Nesterov's accelerated method improves this to $O(1/T^2)$ for the same class of functions.

**Strongly convex case.** The gap shrinks geometrically, by a factor of at most $1-1/\kappa$ per step.

**Under the PL condition.** The same argument gives a linear rate with factor $1-\mu/L$ per step. Karimi and colleagues (2016) apply this to least squares, logistic regression and support-vector machines, among others.

## Results

The evidence is theoretical. The bounds are proved in the cited monographs and need no benchmark, and their practical reach is limited by the assumptions:

- For smooth convex losses, the $O(1/T)$ and geometric rates hold as stated in Nesterov (2004) and Bubeck (2014).
- Karimi and colleagues (2016) show that the PL condition, which strong convexity implies, suffices for linear convergence, and they apply it to several machine-learning problems.
- Deep-network losses are neither convex nor globally smooth. The guarantees therefore describe a simpler class and do not directly certify the training of a network.

## Limitations

- **Assumptions.** The guarantees need $L$, which is often unknown or varies across parameter space. Backtracking line search, covered in Boyd and Vandenberghe (2004), chooses steps without knowing $L$.
- **Ill-conditioning.** A large $\kappa$ makes plain gradient descent zig-zag along narrow valleys. Preconditioning, covered in the [second-order methods](../../../optimization/second-order.md) page, addresses this.
- **Saddle points.** The method can stall near saddle points, where the gradient is small. Dauphin and colleagues (2014) argue that such points dominate in high dimensions.
- **First-order only.** The method ignores curvature, which [Newton's method](../newton-method/index.md) exploits.
- **Generalisation.** A rate for minimising the training loss says nothing about test performance.

## Open questions

- **Non-convex training.** Why a fixed step size often works on non-convex training losses, when the classical bound $1/L$ is unknown in advance, is not fully explained.
- **Reach of the PL condition.** Whether the PL condition or similar ones hold along deep-network training trajectories is open.
- **Acceleration in practice.** Whether the worst-case gains of accelerated methods carry over to stochastic training of deep networks is debated.

## References

### Seminal papers

- Polyak, B. T. (1963). Gradient methods for the minimisation of functionals. *USSR Computational Mathematics and Mathematical Physics*. https://doi.org/10.1016/0041-5553(63)90382-3 — Analyses gradient methods and gives the simple condition for linear convergence.
- Karimi, H., Nutini, J. & Schmidt, M. (2016). Linear Convergence of Gradient and Proximal-Gradient Methods Under the Polyak-Łojasiewicz Condition. arXiv. https://arxiv.org/abs/1608.04636 — Proves linear convergence under the PL inequality, which needs no convexity.
- Dauphin, Y. et al. (2014). Identifying and attacking the saddle point problem in high-dimensional non-convex optimization. arXiv. https://arxiv.org/abs/1406.2572 — Argues that saddle points slow training in high dimensions.

### Surveys and textbooks

- Nesterov, Y. (2004). *Introductory Lectures on Convex Optimization*. Springer. https://doi.org/10.1007/978-1-4419-8853-9 — Analysis of gradient methods on smooth convex functions, including the accelerated method.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://doi.org/10.1017/CBO9780511804441 — Gradient descent with line search, alongside the theory of convex functions.
- Bubeck, S. (2014). Convex Optimization: Algorithms and Complexity. arXiv. https://arxiv.org/abs/1405.4980 — Monograph on convex complexity, including gradient and accelerated gradient schemes.

