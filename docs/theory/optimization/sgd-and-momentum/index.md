---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - gradient descent
aliases:
  - 隨機梯度下降
  - 動量
  - 隨機梯度下降法
  - Stochastic gradient descent
  - SGD with momentum
---

# SGD and Momentum

Stochastic gradient descent (SGD) and its momentum variants are the simplest optimisers used for deep learning. They use one learning rate for every parameter and rely on the gradient alone. They remain the default for many vision models and are the baseline against which adaptive methods are compared. The [overview](../index.md) places them among the other families.

## Overview

Gradient descent moves the parameters against the gradient of the training loss, \(\theta \leftarrow \theta - \eta\, \nabla L(\theta)\). Computing the gradient on the full dataset is expensive, so practical training uses a mini-batch \(B\) and the gradient \(g_t = \nabla_\theta \frac{1}{|B|}\sum_{i\in B} \ell_i(\theta)\). The step is cheap and its direction is noisy, but on average it points the right way.

## Key concepts

- **Mini-batch**: a random subset of the data used to estimate the gradient at one step.
- **Learning rate \(\eta\)**: the step size. Too large makes the loss diverge; too small makes training slow.
- **Momentum**: a running average of past gradients that smooths the direction and speeds progress along consistent slopes.
- **Nesterov momentum**: a variant that evaluates the gradient at a look-ahead point.
- **Learning-rate schedule**: a rule that changes \(\eta\) during training, covered in [Learning-rate schedules](../learning-rate-schedules.md).

## How it works

### Plain SGD

For a convex, \(L\)-smooth loss, gradient descent with \(\eta = 1/L\) decreases the loss at rate \(O(1/T)\) after \(T\) steps, and at a linear rate if the loss is strongly convex. A stochastic gradient is an unbiased estimate of the full gradient, so the expected update is correct but adds variance. With decreasing step sizes, the Robbins–Monro conditions \(\sum_t \eta_t = \infty\) and \(\sum_t \eta_t^2 < \infty\) guarantee convergence.

The noise is not only a cost. It helps the optimiser leave saddle points and is often associated with convergence to flatter minima, a link that is still debated.

### Heavy-ball momentum

The full method, with its analysis, is on the [Heavy-ball momentum](heavy-ball.md) page.

Polyak's heavy-ball method keeps a velocity:

\[
\begin{aligned}
v_t &= \beta\, v_{t-1} + g_t \\
\theta_t &= \theta_{t-1} - \eta\, v_t
\end{aligned}
\]

Directions that repeat accumulate, and directions that flip sign cancel. This damps oscillation in narrow valleys of the loss surface, where plain gradient descent zig-zags.

### Nesterov momentum

The full method, with its guarantees, is on the [Nesterov momentum](nesterov.md) page.

Nesterov's variant computes the gradient at the look-ahead point \(\theta_{t-1} - \eta\beta v_{t-1}\) rather than at \(\theta_{t-1}\). This corrects the velocity before it is applied, and it is widely used when training convolutional networks with SGD.

## Comparison

| Method | Gradient evaluated at | Update in one line | Detail |
|---|---|---|---|
| Plain SGD | Current parameters | \(\theta \leftarrow \theta - \eta g\) | This page |
| Heavy-ball | Current parameters | Accumulate velocity, then step | [Heavy-ball momentum](heavy-ball.md) |
| Nesterov | Look-ahead point | Correct velocity before the step | [Nesterov momentum](nesterov.md) |

## Practical notes

- Momentum values around \(\beta = 0.9\) are common defaults.
- Batch size and learning rate interact. Larger batches usually allow larger learning rates, up to a point.
- SGD with momentum often generalises well on image classification. [Wilson et al. (2017)](https://arxiv.org/abs/1705.08292) report that adaptive methods can find solutions that generalise worse than SGD.

## Connections

- [Adaptive methods](../adaptive/index.md) rescale each coordinate of the same update.
- [Deep learning](../../deep-learning/index.md) explains the backpropagation step that produces \(g_t\).
- [NeuroAI](../../../brain-mind/neuroai/index.md) discusses why exact gradient steps are hard to match in biological learning.

## Applications

- Training convolutional and classification networks with SGD and Nesterov momentum.
- Baseline optimiser in benchmarks that compare new methods.

## Open questions

- Why does SGD noise tend to find solutions that generalise, and how strong is this effect across architectures?
- How should momentum be tuned when the batch size is very large?

## References

### Seminal papers

- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. doi:[10.1214/aoms/1177729586](https://doi.org/10.1214/aoms/1177729586) — Introduces stochastic approximation with decreasing step sizes, the basis of SGD.
- Polyak, B. T. (1964). Some methods of speeding up the convergence of iteration methods. *USSR Computational Mathematics and Mathematical Physics*. doi:[10.1016/0041-5553(64)90137-5](https://doi.org/10.1016/0041-5553(64)90137-5) — Introduces heavy-ball momentum and analyses its acceleration on quadratic problems.
- Wilson, A. C., Roelofs, R., Stern, M., Srebro, N. & Recht, B. (2017). The Marginal Value of Adaptive Gradient Methods in Machine Learning. NeurIPS. https://arxiv.org/abs/1705.08292 — Shows that adaptive methods can find solutions that generalise worse than SGD, on a constructed problem and on several deep networks.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). Optimization Methods for Large-Scale Machine Learning. *SIAM Review*. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods and their convergence behaviour on large datasets.
- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*, Chapter 8. MIT Press. https://www.deeplearningbook.org/ — Textbook treatment of SGD, momentum and training in practice, free online.

### Articles and documentation

- Stanford CS231n, *Optimization* lecture notes. https://cs231n.github.io/optimization-1/ — Clear, illustrated notes on gradient descent, learning rates and momentum.
