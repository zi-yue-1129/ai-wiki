---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- mixed precision
aliases:
  - Mixed-precision quantisation
  - HAWQ
  - 混合精度量化
---

# Mixed-Precision Quantisation

Mixed-precision quantisation gives different layers, or different parts of a layer, different bit-widths. Some parts of a network are sensitive to rounding and keep more bits; others tolerate very few. The question is how to allocate the bits, given a budget on total memory or latency. It is a refinement of uniform [quantisation](../index.md).

## Overview

A uniform scheme uses the same width everywhere, which wastes bits on insensitive layers and loses accuracy on sensitive ones. Mixed precision searches for an allocation that meets the budget and keeps the loss small. The search needs a measure of sensitivity. Simple heuristics use the layer's size or its output error after rounding. More principled methods use the curvature of the loss, approximated by the Hessian.

## Key concepts

- **Bit allocation.** Assigning a width to each layer, often from a small set such as 4, 8 and 16 bits.
- **Sensitivity.** How much the loss changes when a layer is rounded. Sensitivity depends on the layer and on the bit-width.
- **Budget.** A target size or latency, which turns bit allocation into a constrained optimisation problem.
- **Mixed-precision decomposition.** Within one matrix multiplication, separating outlier dimensions that keep high precision, as in [LLM.int8()](../post-training/llm-int8/index.md).

## Comparison of approaches

| Approach | Unit of allocation | Sensitivity measure | Page |
| --- | --- | --- | --- |
| Hessian-based layer allocation | Whole layers | Top eigenvalue (HAWQ) or trace (HAWQ-V2) of each layer's Hessian | [HAWQ](hawq/index.md) |
| Outlier decomposition | Dimensions within a matrix multiplication | Magnitude of activation outliers | [LLM.int8()](../post-training/llm-int8/index.md) |

Layer-level allocation suits convolutional networks, where layers differ a lot in sensitivity. Outlier decomposition suits large transformers, where a few dimensions dominate the error.

## Trade-offs

- **Accuracy at a fixed budget.** Mixed precision usually beats uniform precision at the same average width, but the gain depends on how well sensitivity is estimated.
- **Hardware support.** Mixed bit-widths complicate kernels. Hardware that offers only a few formats limits the allocation that can be used.
- **Search cost.** Sensitivity estimation adds calibration time before any compression happens.

## More variants and open issues

- **Variant:** floating-point formats with a per-block exponent, such as FP8 and FP4 formats supported by recent accelerators, which blur the line between mixed precision and number format design; see [AI hardware](../../../../engineering/hardware/index.md).
- **Open issue:** whether Hessian-based sensitivity predicts the effect of rounding on reasoning and long-context behaviour, not only on average loss.
- **Open issue:** how to allocate bits jointly with pruning, a combination that [pruning](../../pruning/index.md) covers only in part.

## Connections

Mixed precision is a direct response to the outlier problem discussed in the parent [quantisation](../index.md) page, and it uses the same curvature ideas that [GPTQ](../post-training/gptq/index.md) uses to compensate rounding errors. The memory budgets it targets are set by the [memory hierarchy](../../../../engineering/hardware/index.md) of the target device.

## References

### Seminal papers

- Dong, Z., Yao, Z., Gholami, A., Mahoney, M., Keutzer, K. (2019). *HAWQ: Hessian AWare Quantization of Neural Networks with Mixed-Precision*. arXiv:1905.03696. https://arxiv.org/abs/1905.03696 — Assigns per-layer bit-widths using the top Hessian eigenvalue as the sensitivity measure, instead of an exhaustive search.
- Dong, Z., et al. (2020). *HAWQ-V2: Hessian Aware trace-Weighted Quantization of Neural Networks*. arXiv:1911.03852. https://arxiv.org/abs/1911.03852 — Replaces the top-eigenvalue measure with a trace-weighted one that uses more of the Hessian spectrum.
- Wang, K., et al. (2019). *HAQ: Hardware-Aware Automated Quantization with Mixed Precision*. arXiv:1811.08886. https://arxiv.org/abs/1811.08886 — Searches per-layer bit-widths with hardware-aware feedback instead of a fixed sensitivity rule.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Second-order rounding compensation at 3 and 4 bits, the uniform-precision baseline for LLMs.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods, including mixed-precision schemes.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — Mixed-precision decomposition that keeps outlier dimensions in 16 bits.
- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Uniform 8-bit integer inference, the baseline that mixed precision improves on.
