---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- large language models
aliases:
  - LLM.int8()
  - LLM.int8
  - 8-bit inference
  - LLM.int8() 量化
---

# LLM.int8()

LLM.int8() is a post-training method for 8-bit inference in large transformers. It keeps a few outlier hidden dimensions in 16-bit precision and computes the rest in 8 bits, so that models which would lose quality under plain 8-bit quantisation keep full-precision performance at about half the memory.

## Problem

Large transformers develop a few hidden-state dimensions with very large magnitudes. Quantising everything to 8 bits degrades quality sharply once a model is large enough, so the model does not fit in memory at full quality.

## Core idea

Split each matrix multiplication. The few outlier dimensions are computed in 16-bit precision, and the rest in 8-bit integers with vector-wise scales. The method is called mixed-precision decomposition.

## Equation or algorithm

The product of the input \(X\) and weights \(W\) is written as a sum over normal dimensions, quantised to int8, plus a sum over outlier dimensions computed in fp16. Each row of \(X\) and column of \(W\) has its own scale.

## Results

The abstract reports that the method cuts the memory needed for inference by half while keeping full-precision performance.

## Limitations

The outlier path adds overhead, and the method targets 8-bit precision. Lower-bit inference needs other methods such as [GPTQ](../gptq/index.md) or [AWQ](../awq/index.md).

## Open issues and related variants

- **Outlier detection.** The threshold that marks a dimension as an outlier is set by hand; automatic selection is an open practical question.
- **Related:** [SmoothQuant](../smoothquant/index.md) removes outliers from the activations instead of computing them separately.

## Connections

The outlier problem is the same one that [mixed precision](../../mixed-precision/index.md) addresses by giving sensitive parts more bits. The memory savings matter most for [serving](../../../../../engineering/mlops/index.md).

## References

### Seminal papers

- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — Mixed-precision 8-bit matrix multiplication that keeps outlier dimensions in 16 bits.
- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., Han, S. (2023). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. ICML 2023. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — The alternative that moves outliers into the weights.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Compresses weights to 3 and 4 bits after training.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Places LLM.int8() among precision reduction methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Earlier integer-only inference for convolutional networks.
