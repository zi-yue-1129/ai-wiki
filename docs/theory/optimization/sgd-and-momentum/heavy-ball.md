---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - momentum
aliases:
  - 重球動量
  - 重球法
  - Heavy-ball momentum
  - Polyak momentum
---

# Heavy-Ball Momentum

Heavy-ball momentum, introduced by Polyak (1964), adds a velocity term to gradient descent. Each update keeps a fraction of the previous step, so the iterate builds speed along directions where the gradient is consistent and slows down where it oscillates. The method is the origin of the momentum term used in SGD today. The overview is on the [SGD and Momentum](index.md) page.

## Overview

On an ill-conditioned quadratic, plain gradient descent zig-zags across a narrow valley and makes slow progress along it. Polyak asked whether adding a term proportional to the previous step could speed this up. He showed that a second-order recurrence, with a suitable step size and momentum coefficient, converges faster on quadratic problems than plain gradient descent. The name comes from the image of a heavy ball rolling in the loss surface.

## Key concepts

- **Velocity** \(v_t\): the running sum of past gradients, scaled by the momentum coefficient \(\beta\).
- **Momentum coefficient** \(\beta\): how much of the previous velocity is kept. Typical values are around 0.9.
- **Oscillation damping**: components of the gradient that flip sign cancel in the velocity, while consistent components accumulate.
- **Heavy-ball recurrence**: the update rule in the form of a second-order difference equation, which is how Polyak analysed it.

## How it works

The update uses a velocity:

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + g_t \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

Unrolled, the step is a weighted sum of all past gradients with weights that decay geometrically at rate \(\beta\). This is why it is an exponential moving average of gradients, and why it damps oscillation. Polyak's analysis on quadratic objectives shows the best choice of \(\eta\) and \(\beta\) gives a convergence rate better than plain gradient descent for the same conditioning.

## Key methods

### Heavy-ball method (Polyak, 1964)

- **Problem:** gradient descent on ill-conditioned problems zig-zags and converges slowly.
- **Core idea:** add a velocity term that accumulates past steps, so consistent directions speed up and oscillating directions cancel.
- **Equation or algorithm:** the two-line update above, with \(\eta\) the learning rate and \(\beta\) the momentum coefficient.
- **Results:** the paper analyses acceleration on quadratic problems, showing faster convergence than plain gradient descent for suitable parameter choices. The numerical constants come from that analysis and are not repeated here.
- **Limitations:** the analysis is for quadratic objectives. For general smooth convex functions, the heavy-ball method with fixed parameters is not known to reach the optimal \(O(1/T^2)\) rate of Nesterov's variant ([Nesterov momentum](nesterov.md)). [Lessard et al. (2016)](https://arxiv.org/abs/1408.3595) compare the rates of the two methods numerically.

## Connections

- [Nesterov momentum](nesterov.md) is the variant that evaluates the gradient at a look-ahead point.
- The momentum-plus-scaling combination in [Adam](../adaptive/adam.md) uses a first moment that is this same velocity idea.
- The parent [SGD and Momentum](index.md) page covers plain SGD and the momentum overview.

## Open questions

- How should \(\beta\) and \(\eta\) be coupled when the batch size is large and the gradient noise is small?

## References

### Seminal papers

- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:[10.1016/0041-5553(64)90137-5](https://doi.org/10.1016/0041-5553(64)90137-5) — Introduces heavy-ball momentum and analyses its acceleration on quadratic problems.
- Sutskever, I., Martens, J., Dahl, G. & Hinton, G. (2013). On the importance of initialization and momentum in deep learning. ICML. https://proceedings.mlr.press/v28/sutskever13.html — Shows that momentum with careful initialisation trains deep and recurrent networks.
- Lessard, L., Recht, B. & Packard, A. (2016). Analysis and Design of Optimization Algorithms via Integral Quadratic Constraints. *SIAM Journal on Optimization*. doi:[10.1137/15M1009597](https://doi.org/10.1137/15M1009597) — Derives numerical convergence bounds for the gradient, heavy-ball and Nesterov methods on convex functions.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of momentum and stochastic gradient methods and their convergence behaviour.
- Bubeck, S. (2014). Convex Optimization: Algorithms and Complexity. https://arxiv.org/abs/1405.4980 — Monograph on the complexity of gradient-based methods, including accelerated variants.

### Articles and documentation

- Stanford CS231n, *Optimization* lecture notes. https://cs231n.github.io/optimization-1/ — Illustrated notes on momentum and its effect on the update direction.
