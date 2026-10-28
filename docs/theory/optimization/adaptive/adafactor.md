---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/models/transformer
tags:
  - optimization
  - adaptive methods
  - memory efficiency
aliases:
  - Adafactor
  - 因式分解自適應學習率
---

# Adafactor

Adafactor is an adaptive optimiser that stores its second-moment estimates in factored form. For a weight matrix it keeps only row and column sums of the squared-gradient average, instead of one value per parameter. Shazeer and Stern (2018) introduced it to train large models when the optimiser state is too large to store in full. The parent overview is [Adaptive Methods](index.md).

## Overview

Adam keeps two state values per parameter, a first moment and a second moment. For a large model, that state can be as large as the model itself. Adafactor reduces the second-moment part from a full matrix to a row vector and a column vector, and can also drop the first moment.

## Problem

The memory used by per-parameter second moments equals the number of parameters. For very large models, this can exceed what the accelerator can hold alongside the weights and activations, forcing smaller models or batches.

## Core idea

For a matrix parameter \(W \in \mathbb{R}^{n \times m}\), the second moment of the squared gradient, \(V\), is approximated by a rank-one factorisation built from its row sums \(R\) and column sums \(C\):

\[
\hat V_{ij} \approx \frac{R_i\, C_j}{\sum_k R_k}.
\]

Only \(n + m\) values are stored instead of \(n m\). Vectors, such as biases, keep a full second moment, because the factorisation does not apply to them.

## Algorithm

At each step, update the row and column sums of the squared gradients with an exponential average, form the factored estimate \(\hat V\), and scale the gradient by \(1/\sqrt{\hat V}\). The paper also uses an update-clipping rule and a relative step size, which this page does not reproduce in full.

## Key results

The abstract reports that combining the method with dropped momentum gives results comparable to the published Adam setting on Transformer translation (WMT 2014 English–German). It describes the auxiliary storage as very small. This page does not quote more specific numbers.

## Limitations

- The rank-one factorisation is an approximation, so the per-parameter scaling is less accurate than Adam's.
- Vector parameters keep a full second moment, so the saving applies mainly to matrices.
- The method has several design choices, such as clipping and the step-size schedule, that change the behaviour and must be set with care.

## Connections

- [Adaptive Methods](index.md) is the overview where Adafactor sits beside Adam and its other variants.
- [Adam](adam.md) is the full-state method that Adafactor approximates in memory.
- [AdaGrad](adagrad.md) is an earlier per-coordinate method whose accumulator Adafactor also reduces.
- [Shampoo](../shampoo.md) uses matrix statistics to scale updates, at a higher memory cost.

## Applications

- Pre-training large Transformer models, where optimiser memory limits the batch size or model size.

## Open questions

- How much accuracy is lost by the factorisation at very large scale, compared with full second moments?
- Can the factorisation be made to respect the matrix structure of attention and feed-forward layers more closely?

## References

### Seminal papers

- Shazeer, N. & Stern, M. (2018). *Adafactor: Adaptive Learning Rates with Sublinear Memory Cost*. ICML 2018, PMLR 80, pp. 4596–4604. https://proceedings.mlr.press/v80/shazeer18a.html — Factors the second-moment estimate of matrix parameters into row and column sums, reducing memory from linear to sublinear in the number of parameters.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — The full second-moment method that Adafactor approximates in memory.
- Chen, X., et al. (2023). *Symbolic Discovery of Optimization Algorithms*. arXiv. https://arxiv.org/abs/2302.06675 — Lion, another optimiser motivated by memory use, for comparison with Adafactor's saving.
- Duchi, J., Hazan, E. & Singer, Y. (2011). Adaptive Subgradient Methods for Online Learning and Stochastic Optimization. *Journal of Machine Learning Research*, 12. https://jmlr.org/papers/v12/duchi11a.html — The cumulative per-coordinate accumulator that Adafactor's factored estimate generalises.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of adaptive stochastic methods and their trade-offs in large-scale training.
