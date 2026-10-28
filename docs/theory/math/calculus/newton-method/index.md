---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
aliases:
  - 牛頓法
  - 牛頓迭代
  - Newton's method
  - Newton method
  - 二階泰勒模型
tags:
  - optimization
  - curvature
---

# Newton's Method

Newton's method minimises a second-order Taylor model of the loss at each step, using the Hessian to choose the step. Near a minimum with a positive-definite Hessian it converges very quickly, but the Hessian is too costly to store and solve with for large networks. This is why [second-order methods](../../../optimization/second-order.md) approximate it. It is the second-order method of the [calculus and optimisation foundations](../index.md) page.

## Overview

Newton's method is a classical algorithm of numerical analysis, originally developed for solving equations. Applied to minimisation, it is the root-finding iteration applied to the gradient:

$$
x_{k+1}=x_k-\big[\nabla^2 f(x_k)\big]^{-1}\nabla f(x_k).
$$

Dennis and Schnabel (1996) give the standard treatment. Pearlmutter (1994) showed how to multiply the Hessian by a vector exactly, at about the cost of a gradient evaluation and without forming the matrix. That result underlies many curvature-aware methods for large models.

## Key concepts

- **Second-order model**: $m(\delta)=f(x)+\nabla f(x)^\top\delta+\tfrac12\delta^\top H\,\delta$, with $H=\nabla^2 f(x)$. It is the second-order Taylor expansion from the [overview](../index.md).
- **Newton step**: $\delta=-H^{-1}\nabla f(x)$. When $H$ is positive definite, this is the unique minimiser of $m$.
- **Quadratic convergence**: near a minimiser where the Hessian is positive definite and Lipschitz, the error after one step is at most a constant times the square of the error before it.
- **Saddle-free Newton**: a variant that replaces $H$ by $|H|=(H^2)^{1/2}$, so that steps always point downhill. Dauphin and colleagues (2014) propose it to escape saddle points.

## How it works

Each iteration computes $g_k=\nabla f(x_k)$ and $H_k=\nabla^2 f(x_k)$, solves $H_k d_k=-g_k$, and updates $x_{k+1}=x_k+\alpha_k d_k$. The system is solved by Cholesky factorisation when $H_k$ is positive definite. The step length $\alpha_k$ comes from a line search, and it is 1 near a minimum.

A quadratic shows the method at its best. Let $f(x)=\tfrac12 x^\top A x-b^\top x$ with $A$ positive definite. Then $\nabla f(x)=Ax-b$ and $H=A$, so one Newton step from any $x_0$ gives $x_1=A^{-1}b$, the exact minimiser. Gradient descent would need many steps on an ill-conditioned $A$.

Where $H$ is indefinite, the Newton step may point uphill or towards a saddle. Practical implementations then modify $H$ or add a trust region. When $H$ is too large to factor, the Newton–conjugate gradient method solves the system approximately, using only Hessian-vector products.

## Results

The results come from theory and a few studies of neural networks. None is a benchmark table.

- **Local convergence.** With a positive-definite, Lipschitz Hessian, the iteration converges quadratically once it is near a minimiser. This is a textbook theorem, proved in Nocedal and Wright (2006) and Dennis and Schnabel (1996).
- **Saddle-free variant.** Dauphin and colleagues (2014) report numerical evidence that the method escapes high-dimensional saddle points faster than gradient descent and quasi-Newton methods, and optimises better on deep and recurrent networks. Their abstract gives no single figure.
- **Hessian spectrum.** Sagun, Bottou and LeCun (2016) find a bulk of eigenvalues near zero and outlying eigenvalues away from it. Ghorbani and colleagues (2019) show that large isolated eigenvalues appear during training in networks without batch normalisation, and that batch normalisation largely removes them.

## Limitations

- **Cost.** A model with $d$ parameters has a Hessian with $d^2$ entries, and solving with it costs about $d^3$ operations. Both are infeasible for modern networks.
- **Attraction to stationary points.** With an indefinite Hessian, Newton's method can converge to a saddle point or a maximum. Saddle-free variants address this at extra cost.
- **Locality.** The quadratic model is accurate only near the current point, so line searches and trust regions are needed far from a minimum.
- **Noise.** Mini-batch Hessians are estimated from little data, so the curvature used in each step is uncertain.

## Open questions

- **Curvature at scale.** Whether structured approximations such as K-FAC or Shampoo, described in the [second-order methods](../../../optimization/second-order.md) page, keep enough curvature for deep networks at acceptable cost is open.
- **Spectral structure.** The bulk-and-outliers pattern suggests that low-rank curvature could be exploited, but turning it into a practical preconditioner is unsettled.
- **Saddle handling.** Whether saddle-free variants beat simpler noise-based methods in practice is unclear.

## References

### Seminal papers

- Dauphin, Y. et al. (2014). Identifying and attacking the saddle point problem in high-dimensional non-convex optimization. arXiv. https://arxiv.org/abs/1406.2572 — Proposes the saddle-free Newton method, which uses the absolute Hessian so its steps point downhill.
- Pearlmutter, B. A. (1994). Fast Exact Multiplication by the Hessian. *Neural Computation*. https://doi.org/10.1162/neco.1994.6.1.147 — Shows how to compute Hessian-vector products exactly, at about the cost of a gradient.
- Sagun, L., Bottou, L. & LeCun, Y. (2016). Eigenvalues of the Hessian in Deep Learning: Singularity and Beyond. arXiv. https://arxiv.org/abs/1611.07476 — Studies the Hessian spectrum of a loss before and after training.
- Ghorbani, B., Krishnan, S. & Xiao, Y. (2019). An Investigation into Neural Net Optimization via Hessian Eigenvalue Density. arXiv. https://arxiv.org/abs/1901.10159 — Estimates the Hessian spectrum of large networks during training.

### Surveys and textbooks

- Dennis, J. E. & Schnabel, R. B. (1996). *Numerical Methods for Unconstrained Optimization and Nonlinear Equations*. SIAM. https://doi.org/10.1137/1.9781611971200 — Standard treatment of Newton and quasi-Newton methods and their convergence.
- Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization*. Springer. https://doi.org/10.1007/978-0-387-40065-5 — Newton, line-search and trust-region methods, and the Newton–conjugate gradient variant.
