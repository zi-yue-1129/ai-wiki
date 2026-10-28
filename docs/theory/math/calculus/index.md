---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/deep-learning
tags:
  - mathematics
  - calculus
  - optimisation
aliases:
  - 微積分
  - 最佳化基礎
  - Calculus
  - Calculus and optimisation foundations
---

# Calculus and Optimisation Foundations

Training a model means changing its parameters to reduce a loss, and calculus tells us how the loss responds to each change. This page covers the calculus that the optimisation and deep-learning pages assume: gradients, Jacobians and Hessians, the chain rule, Taylor expansion, convexity and constrained optimisation. It is part of the [mathematics overview](../index.md).

## Overview

A loss \(L(\theta)\) is a function of a parameter vector \(\theta\). Its gradient \(\nabla_\theta L\) points in the direction of fastest increase, so stepping against it reduces the loss. How far to step, and in which directions the loss curves most, are answered by the second derivatives collected in the Hessian. Both ideas are local: they describe the loss in a small neighbourhood of the current parameters.

Most of the calculus used in AI is first-order (gradients, the chain rule) and some second-order (curvature, Newton's method). Constraints enter through Lagrange multipliers, which appear in support vector machines and in constrained reinforcement-learning objectives.

## Key concepts

- **Partial derivative and gradient**: \(\partial L/\partial\theta_j\) measures how the loss changes with parameter \(j\). The gradient collects them into a vector.
- **Jacobian**: the matrix of all first derivatives of a vector-valued function, such as a layer's outputs with respect to its inputs.
- **Hessian**: the matrix of second derivatives \(H_{jk} = \partial^2 L / \partial\theta_j\partial\theta_k\). It describes curvature.
- **Chain rule**: the derivative of a composition is the product of derivatives along the path. Backpropagation applies this rule systematically through a network.
- **Taylor expansion**: a local polynomial approximation, \(L(\theta+\delta) \approx L(\theta) + \nabla L^\top\delta + \tfrac12\delta^\top H\delta\).
- **Convexity**: a convex function has no spurious local minima, so a local minimum is a global one.

## How it works

The chain rule is the engine of training. For a network with parameters \(w\) feeding a hidden value \(z\) and then an output \(y\),

\[
\frac{\partial L}{\partial w} = \frac{\partial L}{\partial y}\cdot\frac{\partial y}{\partial z}\cdot\frac{\partial z}{\partial w}.
\]

Backpropagation (Rumelhart et al., 1986) computes these products from the output backwards, reusing intermediate results, so the cost of one gradient is about the cost of one forward pass.

Gradient descent uses the gradient alone: \(\theta \leftarrow \theta - \eta\nabla L\). Newton's method uses the Hessian as well, rescaling the step by \(H^{-1}\), and it converges much faster near a minimum when the Hessian is well behaved, at a much higher cost per step. The second-order Taylor expansion explains both. See the pages on [Newton's method](newtons-method.md) and [Lagrange multipliers](lagrange-multipliers.md).

## Key methods

Three landmark tools organise the calculus of training. Each has its own page or links to one.

- [Newton's method](newtons-method.md): uses the Hessian to take curvature-scaled steps; fast near a minimum, expensive in high dimensions.
- [Lagrange multipliers](lagrange-multipliers.md): turns a constrained problem into an unconstrained one with extra multipliers; the basis of support vector machines and KKT conditions.
- Stochastic gradient descent: replaces the full gradient with a noisy estimate from a mini-batch. The convergence theory goes back to Robbins and Monro (1951); see the [optimisation section](../../optimization/index.md) for the methods built on it.

## Connections

- [Linear algebra](../linear-algebra/index.md) supplies the Hessian's eigenvalues, which set the curvature along each direction and the conditioning of a problem.
- [Probability and statistics](../probability-statistics/index.md) explains why the negative log-likelihood is the usual loss to differentiate.
- [Optimisation](../../optimization/index.md) builds on this page with first-order and adaptive methods.
- Brain and cognition: gradient-based learning is a standard model of synaptic plasticity in artificial networks. Whether the brain implements anything like backpropagation is an open question; see the [neuroscience-AI connections](../../../brain-mind/neuroai/index.md) for the debate.

## Applications

- **Training neural networks**: every parameter update uses gradients computed by backpropagation (Rumelhart et al., 1986).
- **Support vector machines**: the dual problem is derived with Lagrange multipliers (Cortes & Vapnik, 1995).
- **Ill-conditioned problems**: second-order information explains why some problems are much harder for gradient descent than others (Boyd & Vandenberghe, 2004).
- **Large-scale machine learning**: stochastic and second-order methods are compared in the survey by Bottou et al. (2018).

## Open questions

- Loss landscapes of deep networks are non-convex, yet gradient methods often find good solutions. The reasons are only partly understood.
- Second-order methods can speed up training, but their cost in very large models is high. Practical approximations trade accuracy for speed in ways that are still being studied.

## References

### Seminal papers

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature* 323, 533–536. https://doi.org/10.1038/323533a0 — Shows that the chain rule can be applied efficiently to compute gradients in multilayer networks.
- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics* 22(3), 400–407. https://doi.org/10.1214/aoms/1177729586 — Introduces stochastic approximation, the theoretical basis of stochastic gradient descent.
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning* 20(3), 273–297. https://doi.org/10.1007/BF00994018 — Uses constrained optimisation with multipliers to define the support vector machine.

### Surveys and textbooks

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Free online text; covers convex sets, Newton's method, duality and the KKT conditions.
- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Shows Newton–Raphson updates for logistic regression and gives the mathematical background on derivatives.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers gradient-based optimisation and its use in training models.

### Articles and documentation

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization methods for large-scale machine learning. *SIAM Review*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Surveys stochastic, second-order and other optimisation methods for machine learning, with their trade-offs.
