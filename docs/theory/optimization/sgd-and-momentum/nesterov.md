---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - momentum
aliases:
  - Nesterov 加速梯度
  - Nesterov 動量
  - Nesterov momentum
  - Nesterov accelerated gradient
---

# Nesterov Momentum

Nesterov momentum is a variant of heavy-ball momentum that computes the gradient at a look-ahead point, the position the momentum is about to carry the parameters to, rather than at the current point. This corrects the velocity before it is applied. It is the momentum form most often used with SGD for convolutional networks. The overview is on the [SGD and Momentum](index.md) page, and the method it modifies is [heavy-ball momentum](heavy-ball.md).

## Overview

Heavy-ball momentum can overshoot, because the velocity is applied before the gradient at the new point is known. Nesterov proposed evaluating the gradient at the point the velocity alone would reach. The resulting method has a provably better worst-case rate than plain gradient descent on smooth convex problems, which heavy-ball is not known to achieve in general.

## Key concepts

- **Look-ahead point**: \(\theta_{t-1} - \eta\beta v_{t-1}\), where the momentum alone would take the parameters.
- **Corrected velocity**: the new velocity uses the gradient at the look-ahead point, so it responds to the curvature ahead.
- **Acceleration**: a faster convergence rate than plain gradient descent on smooth convex problems.

## How it works

Nesterov's accelerated gradient in the common deep-learning form is

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + \nabla L\big(\theta_{t-1} - \eta\beta\, v_{t-1}\big) \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

Compared with heavy-ball, only the place where the gradient is evaluated changes. In practice, frameworks often implement an equivalent rearrangement that evaluates the gradient at the current point and rewrites the parameter update, so the look-ahead does not need an extra forward pass.

## Key methods

### Accelerated gradient (Nesterov, 1983; see Nesterov, 2004)

- **Problem:** gradient descent on smooth convex problems has a worst-case rate of \(O(1/T)\), and momentum methods such as heavy-ball do not improve that rate in general.
- **Core idea:** evaluate the gradient at a look-ahead point that the momentum alone would reach, so the step is corrected before it is taken.
- **Equation or algorithm:** the update above, with \(\eta\) the step size and \(\beta\) the momentum coefficient, which must be chosen from the smoothness and convexity constants for the theory to hold.
- **Results:** Nesterov (2004) and Bubeck (2014) show that the method has a faster worst-case convergence rate than plain gradient descent for smooth convex functions. This page follows their presentation, and the numerical constants are not repeated here.
- **Limitations:** the guarantees are for smooth convex problems. Deep networks are neither, so the benefit in practice is empirical and depends on tuning.

## Connections

- [Heavy-ball momentum](heavy-ball.md) is the method this variant corrects.
- The parent [SGD and Momentum](index.md) page compares plain SGD and momentum in practice.
- [Adam](../adaptive/adam.md) uses a momentum term of the same kind, without the look-ahead.

## Open questions

- Does the look-ahead correction matter for stochastic gradients with large noise?
- Under what conditions does Nesterov momentum outperform heavy-ball for deep networks?

## References

### Seminal papers

- Sutskever, I., Martens, J., Dahl, G. & Hinton, G. (2013). On the importance of initialization and momentum in deep learning. ICML. https://proceedings.mlr.press/v28/sutskever13.html — Shows that Nesterov-style momentum, with careful initialisation, trains deep and recurrent networks.

- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:[10.1016/0041-5553(64)90137-5](https://doi.org/10.1016/0041-5553(64)90137-5) — The heavy-ball method that Nesterov's variant modifies.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Chapter 8. MIT Press. https://www.deeplearningbook.org/ — Textbook treatment of momentum and Nesterov momentum in training, free online.
- Bubeck, S. (2014). Convex Optimization: Algorithms and Complexity. https://arxiv.org/abs/1405.4980 — Monograph that presents accelerated gradient descent and its complexity analysis.
- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of momentum variants and their behaviour in stochastic training.
- Nesterov, Y. (2004). *Introductory Lectures on Convex Optimization: A Basic Course*. Springer. doi:[10.1007/978-1-4419-8853-9](https://doi.org/10.1007/978-1-4419-8853-9) — Textbook treatment of accelerated gradient methods and their worst-case rates on smooth convex functions.
