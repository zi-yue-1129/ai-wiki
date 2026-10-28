---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - quasi-Newton
aliases:
  - L-BFGS
  - Limited-memory BFGS
  - 有限記憶 BFGS
---

# L-BFGS

L-BFGS is a limited-memory quasi-Newton method. It approximates the inverse Hessian from the last few pairs of parameter and gradient differences, and it never stores the full matrix. Liu and Nocedal (1989) introduced it for large-scale optimisation. The family overview is [Second-Order and Quasi-Newton Methods](second-order.md).

## Overview

The BFGS method builds an approximation to the inverse Hessian from observed gradient changes. Full BFGS stores a $d \times d$ matrix, which costs $O(d^2)$ memory and $O(d^2)$ time per step, and this is too much when $d$ is in the millions. L-BFGS keeps only the last $m$ pairs $(s_k, y_k)$, where $s_k = \theta_{k+1} - \theta_k$ and $y_k = \nabla L_{k+1} - \nabla L_k$. The product of the approximate inverse with the gradient is then computed with a two-loop recursion in $O(md)$ time.

## Problem

Gradient descent is slow on ill-conditioned problems, where the curvature differs widely across directions. Newton's method handles this, but it needs the Hessian. Liu and Nocedal ask whether the curvature information in a short history of gradients is enough to get most of the benefit of BFGS, at a memory cost that scales linearly with the number of variables.

## Core idea

Keep a short history of $(s_k, y_k)$ pairs, and use them to define an implicit inverse-Hessian approximation. The approximation is never formed as a matrix. Each step is a search direction obtained by applying the recursion to the current gradient, followed by a line search that chooses the step length.

## Algorithm

1. Compute the gradient $g_k$ at the current point.
2. Use the two-loop recursion over the stored pairs to compute the direction $d_k = -H_k g_k$, where $H_k$ is the implicit inverse-Hessian approximation.
3. Choose a step length $\alpha_k$ with a line search that satisfies the Wolfe conditions.
4. Set $\theta_{k+1} = \theta_k + \alpha_k d_k$, compute $s_k$ and $y_k$, and keep only the most recent $m$ pairs.

The memory parameter $m$ is typically small, and it trades approximation quality against storage.

## Results

Liu and Nocedal report numerical experiments on large-scale problems. The tables and figures of that paper were not checked for this page, so no figures are quoted here. Readers should consult the paper for the test problems and timings.

## Limitations

- The method assumes that the objective is deterministic and the gradients are exact. The curvature pairs $(s_k, y_k)$ become unreliable when the gradients come from minibatches, which is why L-BFGS is most used in full-batch settings.
- A line search is needed at each step, and each trial point costs a gradient evaluation.
- The memory $m$ limits how much curvature history is kept. Problems whose curvature changes quickly may need a larger $m$ or a restart.

## Connections

- [Second-Order and Quasi-Newton Methods](second-order.md) is the overview, where L-BFGS sits beside K-FAC and Shampoo.
- [Kronecker-factored curvature (K-FAC)](kfac.md) is the stochastic, neural-network-specific alternative.
- [SGD and momentum](sgd-and-momentum/index.md) is the first-order method that L-BFGS is typically compared with on the same problems.
- [Mathematics](../math/index.md) covers the Wolfe conditions and the Hessian used in the derivation.

## Applications

- Fitting logistic regression, conditional random fields and other models where the loss is smooth and deterministic.
- Scientific and engineering optimisation problems in which gradients are exact and affordable.

## Open questions

- How should the curvature pairs be built when the gradients are noisy, so that L-BFGS can be used in stochastic training?
- What is the best choice of $m$ for a given problem class?

## References

### Seminal papers

- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — Introduces L-BFGS and reports its numerical performance on large problems.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — A stochastic curvature method for neural networks, contrasted with full-batch quasi-Newton.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural-gradient idea that quasi-Newton methods approximate in a different way.

### Surveys and textbooks

- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*. 2nd ed. Springer. https://doi.org/10.1007/978-0-387-40065-5 — Textbook treatment of quasi-Newton methods, including limited-memory updates and the Wolfe line search.
- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey that discusses quasi-Newton methods and their use with stochastic gradients.
