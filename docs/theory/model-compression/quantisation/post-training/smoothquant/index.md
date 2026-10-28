---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- large language models
aliases:
  - SmoothQuant
  - 平滑量化
---

# SmoothQuant

SmoothQuant is a post-training method that makes both weights and activations of a large language model quantisable to 8 bits. It moves the difficulty of activation outliers into the weights, using a per-channel scaling that leaves the layer's output mathematically unchanged.

## Problem

Activations in large language models contain outlier channels with much larger values than the rest. Quantising them to 8 bits loses accuracy, while the weights are easy to quantise. Weight-only methods avoid the problem by keeping activations in floating point, which gives no integer speed-up.

## Core idea

Scale each input channel down in the activations and up in the corresponding weights, so that both become easier to quantise. The scaling is chosen per channel and balances the difficulty between the two.

## Equation or algorithm

For a linear layer \(Y = XW\), the method computes \(Y = (X\,\mathrm{diag}(s)^{-1})(\mathrm{diag}(s)\,W)\) with scales \(s\) chosen from activation and weight statistics. The rescaled activations and weights are then quantised to 8 bits.

## Results

The abstract reports up to 1.56 times speed-up and 2 times memory reduction for large language models with negligible accuracy loss.

## Limitations

The scales are chosen from calibration data, and a poor choice moves the outlier problem into the weights. The method is designed for 8-bit arithmetic, so lower bit-widths need other methods.

## Open issues and related variants

- **Balance of difficulty.** The rule that splits the difficulty between activations and weights is heuristic; better rules for different layers are open.
- **Related:** [LLM.int8()](../llm-int8/index.md) keeps outliers in 16 bits instead of moving them.

## Connections

SmoothQuant is the activation-side counterpart of [AWQ](../awq/index.md). It makes integer matrix multiplication practical, which is the arithmetic that [hardware](../../../../../engineering/hardware/index.md) with 8-bit tensor units runs fastest.

## References

### Seminal papers

- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., Han, S. (2022). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — Moves activation outliers into the weights for 8-bit inference, with up to 1.56 times speed-up.
- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — Keeps outliers in 16 bits instead of moving them.
- Lin, J., et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. arXiv:2306.00978. https://arxiv.org/abs/2306.00978 — Activation-aware scaling for weight-only quantisation.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — The weight-only alternative with second-order compensation.
