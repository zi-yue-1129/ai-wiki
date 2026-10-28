---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- large language models
aliases:
  - AWQ
  - Activation-aware weight quantisation
  - 激活感知權重量化
---

# AWQ

AWQ (activation-aware weight quantisation) is a post-training method for weight-only quantisation of large language models. It chooses which weights to protect from activation statistics rather than from weight magnitude, and it scales those channels before rounding so that their relative error falls.

## Problem

Weights that matter most are not the largest in magnitude. Quantising all weights uniformly loses accuracy on the few channels that carry large activations.

## Core idea

Identify salient channels from activation statistics. Scale those channels up before quantisation, so that their relative rounding error falls. The inverse scale is absorbed into the previous operation, so the network is mathematically unchanged in full precision.

## Equation or algorithm

For a channel with scale \(s\), the layer computes \((W\,\mathrm{diag}(s)) \cdot (\mathrm{diag}(s)^{-1}X)\). The scales are chosen by a grid search that minimises the output error on calibration data.

## Results

The authors report that protecting only about 1% of salient weights greatly reduces quantisation error. The paper received the best paper award at MLSys 2024.

## Limitations

The scale search costs calibration time. The method targets weight-only quantisation, so activations stay at higher precision.

## Open issues and related variants

- **Activation distribution shift.** Scales chosen on calibration data may not fit inputs far from that distribution.
- **Related:** [GPTQ](../gptq/index.md) compensates rounding errors instead of rescaling channels; [SmoothQuant](../smoothquant/index.md) rescales for activation quantisation as well.

## Connections

AWQ is one of the main ways of making [serving](../../../../../engineering/mlops/index.md) of large models cheaper, and its format depends on the kernels the target [hardware](../../../../../engineering/hardware/index.md) supports.

## References

### Seminal papers

- Lin, J., et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. MLSys 2024. https://arxiv.org/abs/2306.00978 — Scales salient channels by activation statistics, with the observation that protecting about 1% of weights greatly reduces error.
- Frantar, E., et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv:2210.17323. https://arxiv.org/abs/2210.17323 — Rounds weights with second-order error compensation instead.
- Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., Han, S. (2023). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. ICML 2023. arXiv:2211.10438. https://arxiv.org/abs/2211.10438 — Scales activations and weights for 8-bit integer inference.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Places activation-aware scaling among precision reduction methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — The mixed-precision 8-bit baseline for comparison.
