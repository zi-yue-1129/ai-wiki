---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - adaptive methods
  - second-order
aliases:
  - SOAP
  - Shampoo with Adam in the preconditioner's eigenbasis
  - 預條件子特徵基中的 Adam
---

# SOAP

SOAP runs Adam inside the eigenbasis of Shampoo's preconditioner. Shampoo preconditions the gradient with matrix statistics, and SOAP keeps those statistics but applies Adam's per-coordinate scaling in the rotated coordinates they define. Vyas et al. (2024) introduced it to make Shampoo more stable and efficient. The parent overview is [Adaptive Methods](index.md), and the matrix method it builds on is [Shampoo](../shampoo.md).

## Overview

Shampoo is powerful but needs its preconditioner roots recomputed and tuned. SOAP keeps the matrix structure and replaces the inverse-root update with Adam's update in a rotated space, which reduces the need for those choices.

## Problem

Shampoo's update uses inverse roots of matrix statistics, which are expensive to compute and sensitive to how often they are refreshed. The question is whether the matrix geometry can be kept while the per-step behaviour is made more stable.

## Core idea

Compute the eigenbasis of Shampoo's left and right preconditioner matrices. Transform the gradient into that basis, run Adam there, and transform the update back. In the rotated space, Adam's diagonal scaling is equivalent to a Shampoo-style matrix preconditioner, but without taking inverse roots at every step.

## Algorithm

Let \(L\) and \(R\) be the Shampoo statistics for a matrix parameter, with eigenvectors \(Q_L\) and \(Q_R\), refreshed periodically. The gradient \(G\) is rotated to \(\tilde G = Q_L^\top G\, Q_R\). Adam is applied to \(\tilde G\), and the resulting update is rotated back. The eigenbases are updated at a lower frequency, as in Shampoo.

## Key results

In the large-batch regime, the abstract reports that SOAP reduces the number of iterations by over 40% and the wall-clock time by over 35% compared with AdamW. It reports about 20% improvements in both measures compared with Shampoo. The abstract does not describe the models in detail, so this page quotes only these figures.

## Limitations

- The eigenbases still need periodic recomputation, which costs compute and adds a hyperparameter for their refresh frequency.
- Storage is larger than Adam's, because the matrix statistics and eigenbases must be kept for each matrix parameter.
- The benefit is reported against AdamW and Shampoo in specific settings, so it should be checked on a new problem.

## Connections

- [Shampoo](../shampoo.md) is the matrix preconditioner whose eigenbasis SOAP uses.
- [Adam](adam.md) provides the per-coordinate update that SOAP runs in the rotated space.
- [AdamW](adamw.md) is the baseline for the efficiency comparison.
- [Second-order methods](../second-order.md) covers the curvature-based family that Shampoo and SOAP belong to.

## Applications

- Pre-training large language models, where Shampoo-style methods are studied for efficiency.

## Open questions

- How often should the eigenbases be refreshed, and does the answer depend on model size?
- Does the rotated-space Adam update keep its advantage when the eigenbases are stale?

## References

### Seminal papers

- Vyas, N., Morwani, D., Zhao, R., Kwun, M., Shapira, I., Brandfonbrener, D., Janson, L. & Kakade, S. (2024). *SOAP: Improving and Stabilizing Shampoo using Adam*. arXiv. https://arxiv.org/abs/2409.11321 — Runs Adam in the eigenbasis of Shampoo's preconditioner, and reports efficiency gains over AdamW and Shampoo.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML 2018, PMLR 80. https://proceedings.mlr.press/v80/gupta18a.html — The matrix preconditioner that SOAP builds on. Checked: the PMLR entry lists the same title and authors.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The per-coordinate update that SOAP applies in the rotated space.
- Loshchilov, I. & Hutter, F. (2019). *Decoupled Weight Decay Regularization*. ICLR 2019. https://arxiv.org/abs/1711.05101 — AdamW, the baseline in SOAP's efficiency comparison.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs in large-scale training.
