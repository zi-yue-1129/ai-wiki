---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- post-training quantisation
aliases:
  - Post-training quantisation
  - Post-training quantization
  - PTQ
  - 訓練後量化
---

# Post-Training Quantisation

Post-training quantisation (PTQ) converts a trained model to lower precision without retraining it. A small calibration set is used to choose the scales, and the rounding is then fixed or adjusted layer by layer. PTQ is the most common route for large language models, where a full quantisation-aware training run is too expensive.

## Overview

The simplest PTQ is round-to-nearest: compute a scale per tensor or per group, and round each value to the nearest grid point. It is fast but loses accuracy at 4 bits and below, because rounding one weight ignores its effect on the outputs. The methods on this page improve on the baseline in different ways: they choose the rounding with second-order information (GPTQ), protect the weights that matter most (AWQ), move activation outliers into the weights (SmoothQuant), or keep outlier dimensions in higher precision (LLM.int8()).

## Key concepts

- **Calibration set.** A few hundred to a few thousand inputs, used to measure activation statistics and to choose scales or to compute reconstruction errors.
- **Per-group scales.** Grouping weights into blocks of 32 to 128 values gives each block its own scale, which reduces the damage from outliers.
- **Layer-wise objective.** Most PTQ methods minimise the output error of one layer, \(\lVert WX - \hat{W}X \rVert^2\), rather than the weight error.
- **Weight-only versus weight-and-activation.** Weight-only methods save memory but keep the arithmetic in floating point; weight-and-activation methods can use integer arithmetic.

## Methods

Each method has its own page:

- [LLM.int8()](llm-int8/index.md): mixed-precision decomposition that keeps outlier dimensions in 16 bits.
- [GPTQ](gptq/index.md): second-order rounding with error compensation, at 3 and 4 bits.
- [AWQ](awq/index.md): protects salient channels by scaling them according to activation statistics.
- [SmoothQuant](smoothquant/index.md): moves activation outliers into the weights, enabling 8-bit weights and activations.

## Trade-offs

- **Cost versus accuracy.** PTQ needs minutes to hours of calibration. Methods that solve a layer-wise problem cost more, but keep more accuracy at low bit-widths.
- **Bit-width.** Most methods are reliable at 8 bits and become sensitive at 4 bits and below.
- **Kernel support.** A method is useful only when the inference library can run its format quickly.

## Connections

PTQ is the default in LLM serving, described under [MLOps and deployment](../../../../engineering/mlops/index.md). The number formats that PTQ targets are set by [AI hardware](../../../../engineering/hardware/index.md). For the trained-with-rounding alternative, see [quantisation-aware training](../quantisation-aware-training/index.md).

## Open issues

- **Below four bits.** Quality at 2 and 3 bits, especially for reasoning, is not yet solved by PTQ alone.
- **Calibration bias.** The calibration set can favour some domains; the effect on other domains is not well measured.
- **Combining methods.** Whether GPTQ-style rounding and AWQ-style scaling can be applied together without interference is an open engineering question.

## References

### Seminal papers

- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Layer-wise second-order rounding for 3 and 4 bit weights.
- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — Mixed-precision 8-bit inference that keeps outlier dimensions in 16 bits.
- Lin, J., et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. arXiv:2306.00978. https://arxiv.org/abs/2306.00978 — Chooses per-channel scales from activation statistics to protect salient weights.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods and their trade-offs.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Xiao, G., et al. (2022). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — Migrates activation outliers into the weights for 8-bit weights and activations.
