---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 二階最佳化
  - 擬牛頓法
  - Second-order optimisation
  - Quasi-Newton methods
related:
  - theory/math
tags:
  - optimization
  - curvature
---

# Second-Order and Quasi-Newton Methods

Second-order methods use curvature, the matrix of second derivatives of the loss or an approximation to it, to choose the step. Newton's method is the classic case. Its cost is too high for large networks, so practical methods approximate the curvature, as quasi-Newton methods such as L-BFGS do, or approximate its structure, as K-FAC and Shampoo do.

## Overview

Gradient descent uses only the slope of the loss. Around a point \(\theta\), the second-order Taylor expansion is \(L(\theta+\delta)\approx L(\theta)+\nabla L^\top\delta+\tfrac12\delta^\top H\delta\), where \(H=\nabla^2 L\) is the Hessian. Minimising this quadratic gives the Newton step \(\delta=-H^{-1}\nabla L\). The step accounts for the curvature in each direction, so it can move far along flat directions and take short steps along steep ones. This is why Newton's method converges in far fewer iterations when the quadratic model is accurate.

## Key concepts

- **Hessian**: the \(d\times d\) matrix of second derivatives. Storing it takes \(O(d^2)\) memory and inverting it takes \(O(d^3)\) time, which is impractical when \(d\) is in the millions.
- **Quasi-Newton approximation**: a matrix built from successive gradient differences, which approximates the inverse Hessian without computing it.
- **Fisher information**: an expected outer product of gradients, which for many models is a positive semidefinite stand-in for the Hessian. Natural gradient descent preconditions the gradient with its inverse (Amari, 1998).
- **Kronecker factorisation**: an approximation that writes a layer's curvature block as a Kronecker product of two smaller matrices, so that it can be inverted cheaply.
- **Preconditioner**: any matrix that rescales the gradient before the step. Adaptive methods use diagonal preconditioners, and second-order methods use full or structured ones.

## How it works

Three steps summarise the family:

1. Form a model of the loss around the current point, using gradient information and sometimes curvature.
2. Compute a step that minimises that model, possibly after preconditioning with an approximate inverse curvature.
3. Move, and update the approximation with the new gradients.

The approximations differ in how they keep step 2 affordable. Quasi-Newton methods keep a low-rank history, K-FAC keeps a Kronecker-factored estimate of the Fisher matrix, and Shampoo keeps one matrix per tensor dimension.

## Key methods

Three methods are covered on their own pages. They differ in what curvature they approximate and how they store it.

| Method | Curvature used | What separates it |
|---|---|---|
| [L-BFGS](lbfgs.md) (Liu & Nocedal, 1989) | Gradient differences from the last \(m\) steps | Limited-memory quasi-Newton. It stores \(m\) pairs of vectors instead of a matrix, and is designed for full-batch problems |
| [K-FAC](kfac/index.md) (Martens & Grosse, 2015) | Fisher matrix, approximated layer by layer as a Kronecker product | Natural-gradient approximation that inverts small factors, and is used for neural-network training with minibatches |
| [Shampoo](shampoo.md) (Gupta et al., 2018) | One preconditioner matrix per tensor dimension, built from gradient statistics | Structure-aware preconditioning for tensors, with per-step cost comparable to first-order methods, according to its abstract |

## Connections

- [Adaptive methods](adaptive/index.md) use diagonal preconditioners. Shampoo is the matrix-valued generalisation, and its page is linked from there.
- [SGD and momentum](sgd-and-momentum/index.md) is the first-order baseline that these methods are compared with.
- [Mathematics](../math/index.md) covers the Taylor expansion, positive semidefinite matrices and the Kronecker product used here.
- [Learning-rate schedules](learning-rate-schedules.md) matter here too, because a Newton-type step already contains a scale, and a schedule can shrink or grow it.

## Applications

- L-BFGS is used for smaller problems, such as fitting logistic regression and some scientific models, where full-batch gradients are affordable.
- K-FAC and related natural-gradient methods have been used in large-scale neural network training.
- Matrix preconditioners such as Shampoo have been studied for training large models, as a route to faster convergence.

## Open questions

- Can a second-order method be made as cheap as SGD per step in the full range of model sizes, with no loss in wall-clock time?
- How accurate must the curvature approximation be before the convergence advantage is kept in stochastic training?
- Do the approximations keep their advantage when batch sizes are very large, where the gradient noise changes?

## References

### Seminal papers

- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — Introduces L-BFGS, a limited-memory quasi-Newton method for large problems.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — Introduces natural gradient descent, which preconditions the gradient with the inverse Fisher information.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — Introduces K-FAC, a Kronecker-factored approximation to the natural gradient for neural networks.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — A matrix-structured preconditioner for stochastic optimisation over tensors.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including quasi-Newton and natural-gradient variants and their trade-offs.
