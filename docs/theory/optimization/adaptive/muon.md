---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/models/transformer
tags:
  - optimization
  - adaptive methods
  - matrix parameters
aliases:
  - Muon
  - MomentUm Orthogonalized by Newton-Schulz
  - 正交化動量
---

# Muon

Muon updates each weight matrix with its momentum orthogonalised, so that the update has equal size in all directions of the matrix. The orthogonalisation is computed approximately with a few Newton–Schulz iterations. Liu et al. (2025) show that it scales to large language models, reporting about twice the compute efficiency of AdamW. The parent overview is [Adaptive Methods](index.md).

## Overview

Muon applies to matrix-shaped parameters, such as the weight matrices of linear and attention layers. It is a momentum method whose update direction is changed to be orthogonal, which removes the directions of the update that are already dominant.

## Problem

Momentum updates to a weight matrix are often dominated by a few singular directions, so most of the step is spent along them. The question is whether equalising the singular values of the update improves training efficiency.

## Core idea

Compute momentum as usual, then replace the momentum matrix by its orthogonal factor, the matrix \(UV^\top\) from its singular value decomposition \(M = U\Sigma V^\top\). All singular values of the update then equal one, so every direction receives equal weight.

## Algorithm

For a weight matrix \(W\) with gradient \(G_t\), update the momentum \(M_t = \mu M_{t-1} + G_t\). Then orthogonalise \(M_t\), approximately, with a few Newton–Schulz iterations, which avoid an explicit SVD, and apply \(W_{t+1} = W_t - \eta\,\mathrm{Orth}(M_t)\). Liu et al. (2025) report that two ingredients are needed to scale Muon: weight decay, and a careful adjustment of the per-parameter update scale.

## Key results

The abstract reports about 2× computational efficiency compared with AdamW under compute-optimal training, based on scaling-law experiments. The authors also introduce Moonlight, a 3B/16B mixture-of-experts model trained on 5.7 trillion tokens with Muon, which they report reaches better performance with fewer training FLOPs than prior models.

## Limitations

- The orthogonalisation applies to matrix parameters. Other parameters, such as vectors and embeddings, need a different optimiser or rule.
- The Newton–Schulz iterations add compute at each step, which must be offset by the efficiency gain.
- The efficiency figure is reported for compute-optimal training of language models, so it does not transfer automatically to other tasks.

## Connections

- [Adaptive Methods](index.md) is the overview where Muon sits beside Adam, Lion and the memory-light variants.
- [Shampoo](../shampoo.md) and [SOAP](soap.md) also use matrix structure, through preconditioners rather than orthogonalisation.
- [Adam](adam.md) is the baseline of the efficiency comparison.
- [Transformer](../../models/transformer/index.md) is the architecture in which the matrix parameters Muon targets are most common.

## Applications

- Pre-training large language models, including sparse mixture-of-experts models.

## Open questions

- Which parameters should be orthogonalised, and how should the others be handled?
- How does the cost of the Newton–Schulz iterations change with matrix size and model scale?

## References

### Seminal papers

- Liu, J., Su, J., Yao, X., et al. (2025). *Muon is Scalable for LLM Training*. arXiv. https://arxiv.org/abs/2502.16982 — Shows that Muon, with weight decay and update-scale adjustment, scales to large language models and reports about 2× compute efficiency over AdamW.
- Gupta, V., Koren, T. & Singer, Y. (2018). *Shampoo: Preconditioned Stochastic Tensor Optimization*. ICML. https://arxiv.org/abs/1802.09568 — A matrix-structured method for the same class of parameters.
- Vyas, N., et al. (2024). *SOAP: Improving and Stabilizing Shampoo using Adam*. arXiv. https://arxiv.org/abs/2409.11321 — Another matrix-structured method, for comparison with Muon's orthogonalisation.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The baseline for the efficiency comparison.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic methods and their trade-offs in large-scale training.
