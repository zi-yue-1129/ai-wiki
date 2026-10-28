---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- mixed precision
aliases:
  - HAWQ
  - Hessian AWare Quantization
  - Hessian-aware quantisation
  - 海森感知量化
---

# HAWQ

HAWQ (Hessian AWare Quantization) chooses a bit-width for each layer of a network from the curvature of the loss in that layer. Layers whose loss changes sharply under perturbation keep more bits, and layers that are flat under perturbation receive fewer. It is a method in the [mixed-precision](../index.md) family of [quantisation](../../index.md).

## Problem

Choosing bit-widths by hand or by exhaustive search is slow, and simple size-based rules do not reflect how sensitive each layer is to rounding. Two layers of the same size can respond very differently to the same rounding error.

## Core idea

Use the Hessian of the loss with respect to each layer's weights as a measure of sensitivity. The top eigenvalue, or the average of the spectrum, indicates how strongly the loss curves in that layer's directions. Rank the layers by this value, and assign more bits to the sensitive ones until the bit budget is met.

## Equation or algorithm

The Hessian is large, so only its top eigenvalue is needed. The method estimates it with power iteration, which uses Hessian-vector products that can be computed with automatic differentiation without forming the full matrix. Each layer receives a sensitivity score, and bit-widths are then chosen to minimise the total sensitivity under the memory constraint.

## Results

The abstract states that HAWQ allows automatic selection of the relative quantisation precision of each layer, based on the Hessian spectrum. The paper's tables give the accuracy results for specific networks, and should be read there.

## Limitations

Hessian estimates are noisy, and the power iteration costs extra computation on every calibration pass. The method was developed for convolutional networks. Its extension to very large transformers needs more study, and the sensitivity measure is an average that may hide rare but important layers.

## Open issues and related variants

- **Predicting behaviour.** Whether Hessian sensitivity predicts the effect of rounding on reasoning and long-context behaviour, rather than on average loss, is not known.
- **Related:** [GPTQ](../../post-training/gptq/index.md) uses the same second-order information to compensate rounding errors within a layer, rather than to choose widths between layers.

## Connections

HAWQ extends the uniform-precision idea of [quantisation](../../index.md). Its budgets are set by the memory and latency limits of the target [hardware](../../../../../engineering/hardware/index.md), and curvature-based sensitivity is also used in [pruning](../../../pruning/index.md) to decide which weights to remove.

## References

### Seminal papers

- Dong, Z., Yao, Z., Gholami, A., Mahoney, M., Keutzer, K. (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — Assigns per-layer bit-widths from each layer's Hessian spectrum.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Uses second-order information to compensate rounding within a layer, the uniform-precision counterpart.
- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Uniform 8-bit integer inference, the baseline that mixed precision improves on.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews mixed-precision schemes and the sensitivity measures they use.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — Mixed-precision decomposition that keeps outlier dimensions in 16 bits, a different allocation within a matrix.
