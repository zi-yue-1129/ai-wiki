---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - preconditioning
aliases:
  - Shampoo
  - Shampoo optimiser
  - Shampoo 最佳化器
---

# Shampoo

Shampoo is a preconditioned stochastic optimiser for tensor-valued parameters. It keeps one preconditioning matrix per tensor dimension and uses their products to rescale the gradient, so it captures structure that a diagonal method such as Adam does not. Gupta, Koren and Singer (2018) introduced it. The family overview is [Second-Order and Quasi-Newton Methods](second-order.md), and the diagonal relative is [Adam](adaptive/adam.md).

## Overview

Adaptive methods rescale each coordinate separately, which ignores correlations between parameters. Full-matrix AdaGrad uses a matrix preconditioner that captures correlations, but for a parameter with \(d\) entries it needs a \(d\times d\) matrix, which is too large for a neural network. Shampoo treats a matrix or tensor parameter as a tensor with one index per dimension and keeps a small preconditioner per dimension. For a matrix parameter \(W\in\mathbb{R}^{m\times n}\) it keeps an \(m\times m\) and an \(n\times n\) matrix, which are much smaller than the full preconditioner.

## Problem

Full-matrix adaptive methods can adapt to correlations in the gradient, but their cost makes them impractical for deep networks. Gupta et al. ask whether the structure of a tensor parameter allows a preconditioner that keeps most of the benefit at a cost closer to that of diagonal methods.

## Core idea

For each dimension \(j\) of the parameter tensor, accumulate a statistic built from the gradient unfolded along that dimension. Use the inverse fourth roots of these statistics as the preconditioners on each side. The update is the gradient multiplied by the preconditioner for each dimension.

## Algorithm

For a matrix parameter \(W\) with gradient \(G_t\), keep two accumulators:

\[
L_t = L_{t-1} + G_t G_t^\top, \qquad R_t = R_{t-1} + G_t^\top G_t
\]

Then update the parameters with

\[
W_{t+1} = W_t - \eta\, L_t^{-1/4}\, G_t\, R_t^{-1/4}
\]

The paper uses a delayed update: it recomputes the roots only once every 20 to 100 steps, and reports that this had almost no impact on accuracy while lowering the amortised cost per step. The preconditioners are initialised as \(\epsilon I\), so a small constant acts as damping before inverting. The rule generalises to tensors by applying one such matrix to each dimension.

## Results

The abstract reports that the per-step runtime of Shampoo is "comparable to that of simple gradient methods such as SGD, AdaGrad, and Adam", even though the update rule is more complex. In experiments with state-of-the-art deep learning models, the paper reports Shampoo "converging considerably faster than commonly used optimizers". The abstract gives no numeric figures, so comparisons should be taken from the paper's experiments.

## Limitations

- Computing the inverse roots is expensive, so the paper recomputes them on a delayed schedule. The refresh interval and the damping constant are extra hyperparameters.
- The method is most natural for matrix and tensor parameters. For vectors such as biases, it reduces to a diagonal method.
- The abstract's convergence comparison is an empirical claim. Its advantage over Adam depends on how well the preconditioners are tuned.

## Connections

- [Adaptive methods](adaptive/index.md) is the family of diagonal preconditioners that Shampoo generalises, with [Adam](adaptive/adam.md) as its main representative.
- [Second-Order and Quasi-Newton Methods](second-order.md) is the overview where Shampoo sits beside L-BFGS and K-FAC.
- [K-FAC](kfac.md) is a related structured preconditioner built from the Fisher matrix rather than gradient statistics.
- [Mathematics](../math/index.md) covers the matrix square roots and Kronecker structure used in the update.

## Applications

- Training large neural networks, where the matrix parameters of attention and feed-forward layers are the natural targets.
- Research on faster optimisers for large language models, which often compares against Adam.

## Open questions

- How should the inverse roots be refreshed so that the cost is bounded without losing the convergence advantage?
- Which tensor shapes benefit most from the structured preconditioner, and where does a diagonal method suffice?

## References

### Seminal papers

- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — Introduces Shampoo, a per-dimension matrix preconditioner for tensor parameters with runtime comparable to first-order methods.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. ICML. https://arxiv.org/abs/1503.05671 — A different structured preconditioner for neural networks, built from the Fisher matrix.
- Liu, D. C. & Nocedal, J. (1989). *On the Limited Memory BFGS Method for Large Scale Optimization*. Mathematical Programming, 45, 503–528. https://doi.org/10.1007/BF01589116 — The quasi-Newton method for large problems that uses curvature without storing a matrix.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural gradient, which structured preconditioners aim to approximate.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive and preconditioned stochastic methods and their trade-offs.
