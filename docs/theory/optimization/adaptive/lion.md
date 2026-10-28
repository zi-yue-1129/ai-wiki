---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - adaptive methods
  - memory efficiency
aliases:
  - Lion
  - EvoLved Sign Momentum
  - 符號動量
---

# Lion

Lion is an optimiser discovered by program search, whose update uses only the sign of a momentum-based quantity. Every parameter therefore moves by the same magnitude in each step. It keeps a single momentum buffer, where Adam keeps two. Chen et al. (2023) introduced it, reporting gains in accuracy and compute on image, language and diffusion tasks. The parent overview is [Adaptive Methods](index.md).

## Overview

Lion trades the per-coordinate scaling of Adam for a sign operation. This removes the second-moment state and makes the update's size uniform across parameters, which changes how the learning rate must be set.

## Problem

Adam's two state buffers double the memory needed by the optimiser. For large models, this state can limit the batch size or the model size, so a method with one buffer and comparable quality is attractive.

## Core idea

Compute the update from the sign of an interpolation between the momentum and the current gradient. The sign gives each coordinate the same step size, and the momentum buffer is updated separately with a different decay rate.

## Algorithm

With momentum \(m_t\), interpolation factor \(\beta_1\) and momentum decay \(\beta_2\), the update is

\[
c_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t,\qquad
\theta_{t+1} = \theta_t - \eta\,\big(\operatorname{sign}(c_t) + \lambda\theta_t\big),\qquad
m_t = \beta_2 m_{t-1} + (1 - \beta_2) g_t,
\]

where \(\lambda\) is a decoupled weight decay. The sign of \(c_t\) is \(\pm 1\) per coordinate, so the step has the same magnitude in every coordinate.

## Key results

The abstract reports that Lion improves ViT accuracy on ImageNet by up to 2% and saves up to 5× pre-training compute on JFT. It reports diffusion-model FID gains with up to 2.3× less training compute, and language results similar to or better than Adam. The abstract notes that Lion needs a smaller learning rate than Adam, because the sign update has a larger norm.

## Limitations

- The sign discards magnitude information, so coordinates with very different gradient scales are treated alike in each step.
- The learning rate and weight decay must be retuned relative to Adam, since the update norm differs.
- The results cover specific tasks, and the abstract makes no claim for every architecture.

## Connections

- [Adaptive Methods](index.md) is the overview where Lion sits beside Adam, AdamW and the memory-light variants.
- [Adam](adam.md) is the two-buffer method that Lion simplifies.
- [AdamW](adamw.md) provides the decoupled weight decay that Lion also uses.
- [Adafactor](adafactor.md) is another memory-saving approach, which factorises the second moment instead of removing it.

## Applications

- Training vision transformers and diffusion models, where the paper reports gains.
- Pre-training large models where optimiser memory is a bottleneck.

## Open questions

- Why does the sign update work as well as it does, and does it generalise across tasks beyond those reported?
- How should the learning rate be scaled when moving between Adam and Lion?

## References

### Seminal papers

- Chen, X., Liang, C., Huang, D., Real, E., Wang, K., Liu, Y., Pham, H., Dong, X., Luong, T., Hsieh, C.-J., Lu, Y. & Le, Q. V. (2023). *Symbolic Discovery of Optimization Algorithms*. arXiv. https://arxiv.org/abs/2302.06675 — Introduces Lion, a sign-based optimiser that keeps a single momentum buffer.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The two-buffer method that Lion is compared against.
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — The decoupled weight decay used in Lion's update.
- Shazeer, N. & Stern, M. (2018). *Adafactor: Adaptive Learning Rates with Sublinear Memory Cost*. arXiv. https://arxiv.org/abs/1804.04235 — Another memory-saving adaptive method, for comparison.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs in large-scale training.
