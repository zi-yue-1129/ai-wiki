---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - adaptive methods
  - sparse features
aliases:
  - AdaGrad
  - Adaptive gradient
  - 自適應梯度
---

# AdaGrad

AdaGrad scales the step size of each parameter by the square root of the sum of all its past squared gradients. Parameters that have received large or frequent gradients take smaller steps, and rarely updated parameters keep larger steps. Duchi, Hazan and Singer (2011) introduced it for online learning and stochastic optimisation. The parent overview is [Adaptive Methods](index.md).

## Overview

AdaGrad is the first widely used per-coordinate adaptive method. Its later variants, RMSProp and Adam, replace the running sum with an exponential average, which fixes its main weakness.

## Problem

With a single global learning rate, features that occur rarely receive tiny updates, while frequent features receive large ones. In sparse problems such as text with bag-of-words features, the learning rate must suit both kinds of coordinate.

## Core idea

Keep, for each coordinate \(i\), the running sum of its squared gradients. Divide the step on that coordinate by the square root of the sum. Coordinates with a history of large gradients get smaller steps, and coordinates with little history keep steps near the base rate.

## Algorithm

Let \(g_t\) be the gradient at step \(t\), and \(G_{t} = \sum_{s \le t} g_s \odot g_s\) the accumulated squared gradients, with \(\odot\) the elementwise product. The update is

\[
\theta_{t+1} = \theta_t - \eta\, \frac{g_t}{\sqrt{G_t} + \epsilon},
\]

where the division is elementwise, \(\eta\) is the base learning rate, and \(\epsilon\) is a small constant for numerical stability.

## Key results

The abstract of Duchi et al. (2011) presents a family of subgradient methods that dynamically incorporate knowledge of the geometry of the data observed in earlier iterations. It describes the effect as finding needles in haystacks, meaning rare but informative features are no longer drowned out by frequent ones. This page does not quote numerical results, because the abstract gives none.

## Limitations

- The accumulated sum never decreases, so the effective step size shrinks steadily. Training can stall before convergence, especially in deep networks, which motivated RMSProp and Adam.
- The base learning rate still needs tuning, and the best value depends on the problem.
- Storage is one accumulator per parameter, the same memory cost as the other per-coordinate methods.

## Connections

- [Adaptive Methods](index.md) is the overview where AdaGrad sits beside RMSProp, Adam and the later variants.
- [RMSProp](rmsprop.md) replaces the sum with an exponential average, which keeps the step size from shrinking to zero.
- [Adam](adam.md) combines the per-coordinate scaling with a momentum term and bias correction.
- [Shampoo](../shampoo.md) extends the per-coordinate idea to full matrix preconditioners.

## Applications

- Training linear models and embeddings on sparse features, where the method was designed to help.
- Early deep-learning experiments, before the exponential-average variants became standard.

## Open questions

- Can the accumulator be reset or decayed in a principled way without losing the benefit on sparse features?
- How does AdaGrad's geometry-aware scaling compare with the matrix preconditioners of Shampoo and SOAP on deep networks?

## References

### Seminal papers

- Duchi, J., Hazan, E. & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. *Journal of Machine Learning Research*, 12, 2121–2159. https://jmlr.org/papers/v12/duchi11a.html — Introduces AdaGrad, which scales each coordinate by its accumulated squared gradients.
- Tieleman, T. & Hinton, G. (2012). *Lecture 6.5 — RMSProp: Divide the gradient by a running average of its recent magnitude*. Coursera lecture notes, *Neural Networks for Machine Learning*. — The exponential-average fix for AdaGrad's shrinking step size.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — Extends the per-coordinate AdaGrad idea to full matrix preconditioners.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — Combines the per-coordinate scaling with momentum and bias correction.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs in large-scale training.
