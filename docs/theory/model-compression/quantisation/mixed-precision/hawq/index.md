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

HAWQ (Hessian AWare Quantization) chooses a bit-width for each layer of a network from the curvature of the loss in that layer. Layers whose loss is sensitive to perturbation keep more bits, and layers that are insensitive receive fewer. It is a method in the [mixed-precision](../index.md) family of [quantisation](../../index.md).

## Problem

Choosing bit-widths by hand or by exhaustive search is slow, and simple size-based rules do not reflect how sensitive each layer is to rounding. Two layers of the same size can respond very differently to the same rounding error.

## Core idea

Use the Hessian of the loss with respect to each layer's weights as a measure of sensitivity. The paper bases each layer's relative precision on the Hessian spectrum of that layer, so layers with high curvature are quantised more carefully. The bit budget is then spent on the most sensitive layers first.

## Equation or algorithm

The paper's abstract describes choosing each layer's relative quantisation precision from the layer's Hessian spectrum. The full Hessian of a large network is too big to form, so the method works with Hessian-based quantities that can be estimated from the loss and its gradients. Each layer receives a sensitivity score, and bit-widths are then chosen to reduce the total sensitivity under the memory constraint. The exact estimator and the search procedure are in the paper's method section, which should be read for the details.

## Results

The abstract states that HAWQ allows automatic selection of the relative quantisation precision of each layer, based on the Hessian spectrum. The paper's tables give the accuracy results for specific networks, and should be read there.

## Limitations

Hessian estimates are noisy and cost extra computation on every calibration pass. The sensitivity measure summarises each layer by a single number, which may hide rare but important directions in the loss. How well it extends to very large transformers needs more study.

## Open issues and related variants

- **Predicting behaviour.** Whether Hessian sensitivity predicts the effect of rounding on reasoning and long-context behaviour, rather than on average loss, is not known.
- **Related:** [GPTQ](../../post-training/gptq/index.md) uses the same second-order information to compensate rounding errors within a layer, rather than to choose widths between layers.

## Connections

HAWQ extends the uniform-precision idea of [quantisation](../../index.md). Its budgets are set by the memory and latency limits of the target [hardware](../../../../../engineering/hardware/index.md), and curvature-based sensitivity is also used in [pruning](../../../pruning/index.md) to decide which weights to remove.

## References

### Seminal papers

- Dong, Z., Yao, Z., Gholami, A., Mahoney, M., Keutzer, K. (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — Assigns per-layer relative precision from each layer's Hessian spectrum.
- Frantar, E., Ashkboos, S., Hoefler, T., Alistarh, D. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Uses second-order information to compensate rounding within a layer, the uniform-precision counterpart.
- Jacob, B., Kligys, S., Chen, B., Zhu, M., Tang, M., Howard, A., Adam, H., Kalenichenko, D. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Uniform 8-bit integer inference, the baseline that mixed precision improves on.

### Surveys and textbooks

- Gholami, A., Kim, S., Dong, Z., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews mixed-precision schemes and the sensitivity measures they use.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — Keeps the few outlier dimensions of large transformers in 16 bits and the rest in 8 bits, a different allocation within a matrix.
