---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - adaptive methods
aliases:
  - RMSProp
  - Root mean square propagation
  - 均方根傳播
---

# RMSProp

RMSProp scales each parameter's step by a running average of its recent squared gradients, rather than by the sum over all of training. The average forgets old gradients, so the step size does not shrink to zero. Tieleman and Hinton introduced it in lecture notes in 2012, and it was never published as a paper. The parent overview is [Adaptive Methods](index.md).

## Overview

RMSProp is a small change to AdaGrad: an exponential moving average replaces the cumulative sum. It is the adaptive scaling used in Adam without the momentum term.

## Problem

AdaGrad's accumulated sum grows without bound, so its effective learning rate decays steadily. In non-convex deep networks, this decay can stop learning long before a good solution is reached.

## Core idea

Keep an exponential average of each coordinate's squared gradients, and divide the gradient by its square root. The average has a memory of a few tens of steps, so the scale tracks the current gradient magnitude instead of the whole history.

## Algorithm

With decay rate \(\beta\), the running average is updated as

\[
v_t = \beta\, v_{t-1} + (1 - \beta)\, g_t \odot g_t,
\]

and the parameters move by

\[
\theta_{t+1} = \theta_t - \eta\, \frac{g_t}{\sqrt{v_t} + \epsilon}.
\]

Typical values are \(\beta\) near 0.9, with a small \(\epsilon\) for numerical stability. The division is elementwise.

## Key results

RMSProp has no paper, so this page quotes no benchmark numbers. Its effect is documented in the lecture notes and in later comparisons, notably Kingma and Ba (2015), which uses the same scaling inside Adam.

## Limitations

- It has no bias correction for the average at the start of training, unlike Adam, so the first steps can be unusually large.
- It has no momentum term, so it does not smooth the direction of the update.
- The decay rate and learning rate both need tuning.

## Connections

- [AdaGrad](adagrad.md) is the method RMSProp modifies, by replacing the sum with an average.
- [Adam](adam.md) adds momentum and bias correction to the same scaling.
- [Adaptive Methods](index.md) is the overview where RMSProp sits beside the other per-coordinate variants.

## Applications

- Training recurrent networks and early deep models, where it was widely used before Adam became the default.

## Open questions

- Does the choice of decay rate matter as much as the learning rate for non-stationary gradients?
- How does RMSProp's behaviour change when it is combined with the bias correction of Adam?

## References

### Seminal papers

- Tieleman, T. & Hinton, G. (2012). *Lecture 6.5 — RMSProp: Divide the gradient by a running average of its recent magnitude*. Coursera lecture notes, *Neural Networks for Machine Learning*. — The original, unpublished introduction of RMSProp.
- Duchi, J., Hazan, E. & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. *Journal of Machine Learning Research*, 12. https://jmlr.org/papers/v12/duchi11a.html — The cumulative-sum method that RMSProp replaces with an average.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — Uses the same exponential average of squared gradients, with momentum and bias correction.
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — The decoupled weight decay used with adaptive methods of this family.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs.
