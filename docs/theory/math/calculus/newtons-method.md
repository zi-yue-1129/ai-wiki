---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
tags:
  - mathematics
  - optimisation
  - second-order
aliases:
  - 牛頓法
  - Newton-Raphson
  - Newton's method
---

# Newton's Method

Newton's method finds a minimum by repeatedly minimising a local quadratic approximation of the loss. It uses the Hessian to scale each step, so it moves far along flat directions and carefully along steep ones. It converges quickly near a minimum, but each step needs the Hessian. Part of [Calculus and optimisation foundations](index.md).

## Overview

Gradient descent takes steps of fixed size in the direction of the negative gradient. That size is the same in every direction, so a loss that is steep in one direction and flat in another zigzags and progresses slowly. Newton's method corrects this by using the curvature. It fits a quadratic model around the current point and jumps to that quadratic's minimum.

## Key concepts

- **Second-order model**: \(L(\theta+\delta)\approx L(\theta)+\nabla L^\top\delta+\tfrac12\delta^\top H\delta\), with \(H\) the Hessian.
- **Newton step**: the \(\delta\) that minimises the model, \(\delta = -H^{-1}\nabla L\).
- **Positive definiteness**: the step is a descent step when \(H\) is positive definite. Otherwise the method may head toward a saddle or a maximum.
- **Quadratic convergence**: near a minimum with a positive-definite Hessian, the error roughly squares at each step.

## How it works

The update is

\[
\theta_{k+1} = \theta_k - H_k^{-1}\nabla L(\theta_k).
\]

In practice the linear system \(H_k\delta = -\nabla L\) is solved rather than inverting \(H_k\). Each iteration therefore needs the gradient, the Hessian and a linear solve. For a model with \(n\) parameters the Hessian has \(n^2\) entries, which is impractical for large networks.

The Hessian's eigenvalues decide the behaviour. Directions with large eigenvalues are steep, and the Newton step shrinks movement there. Directions with small eigenvalues are flat, and the step grows. A pure Newton step can therefore overshoot or move toward a saddle point, which is why practical versions add damping or use a line search.

Logistic regression is the classic example where the Newton method is practical, because the parameter count is small. Bishop (2006) shows the resulting iterative reweighted least squares update.

## Key methods

- [Gradient descent](../../optimization/index.md): the first-order alternative, cheaper per step and slower near a minimum.
- Quasi-Newton methods, such as L-BFGS, approximate the Hessian from gradient differences and avoid forming it. They are covered in the [optimisation section](../../optimization/index.md).

## Connections

- [Calculus and optimisation foundations](index.md) gives the Taylor expansion and the Hessian that the method needs.
- [Linear algebra](../linear-algebra/index.md) explains how the Hessian's eigenvalues control the step size in each direction.
- Brain and cognition: the method is a computational tool here, not a model of neural processing.

## Applications

- **Logistic regression**: Newton updates, often called iteratively reweighted least squares (Bishop, 2006).
- **Convex optimisation**: interior-point methods use Newton steps on barrier-modified problems (Boyd & Vandenberghe, 2004).
- **Large-scale learning**: second-order methods are discussed as an alternative to stochastic gradient descent, with trade-offs in cost (Bottou et al., 2018).

## Open questions

- Scalable second-order methods for deep networks remain an active research area, because forming and inverting the Hessian is too costly at scale.
- Saddle points are common in high-dimensional loss landscapes, and Newton-type steps can be attracted to them unless they are modified.

## References

### Seminal papers

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Compares second-order and first-order methods for large-scale learning, including the cost of Hessian information.
- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Presents Newton's method with its convergence analysis and the damped version used in practice.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Shows the Newton–Raphson update for logistic regression.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; discusses Newton's method in the context of fitting generalised linear models.
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — Covers the linear solves that each Newton step requires.
