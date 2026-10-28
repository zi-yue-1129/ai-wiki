---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/mlops
- engineering/hardware
- theory/models/transformer/kv-cache
tags:
- model compression
- quantisation
- low-precision inference
aliases:
  - Quantization
  - Quantisation
  - Post-training quantisation
  - 量化
  - 量子化
---

# Quantisation

Quantisation stores and computes with numbers that use fewer bits, such as 8-bit integers, 4-bit integers or 8-bit floating point, in place of 16- or 32-bit floats. It is the most widely deployed form of [model compression](../index.md), because it reduces memory and often speeds up matrix multiplication on hardware built for low precision.

## Overview

Uniform affine quantisation maps a real value \(x\) to a \(b\)-bit integer \(q\):

\[
q = \operatorname{clip}\!\left(\operatorname{round}\!\left(\frac{x}{s}\right) + z,\ 0,\ 2^b - 1\right), \qquad \hat{x} = s\,(q - z)
\]

where \(s\) is a scale and \(z\) a zero point. Choosing \(s\) from the range of the values sets the rounding error. Using one scale per tensor is cheap but sensitive to outliers. Per-channel scales, or per-group scales over blocks of weights, are more accurate. Groups of 128 weights are a common setting in GPTQ and AWQ.

## Key concepts

- **Weight-only versus weight-and-activation quantisation.** Weight-only methods keep activations in 16 bits, which saves memory but not much compute. Quantising activations as well allows integer matrix multiplication, but activations contain outliers that make this harder.
- **Post-training quantisation (PTQ).** The model is quantised after training, using a small calibration set to pick scales. It needs no training run.
- **Quantisation-aware training (QAT).** Rounding is simulated during training. Gradients pass through the rounding with a straight-through estimator, so the weights adapt to the grid.
- **Outliers.** A small number of channels in large transformers carry values much larger than the rest. Handling them is the central difficulty of low-bit quantisation.
- **Number formats.** INT8 and INT4 use integer arithmetic. FP8 and FP4 keep a floating-point exponent, which handles a wide range of values better and is supported by recent accelerators; see [AI hardware](../../../engineering/hardware/index.md).

## Comparison of families

| Family | Training run needed | Typical bit-width | Best suited to | Page |
| --- | --- | --- | --- | --- |
| Post-training (PTQ) | No, a calibration set only | 8 bits, 4 bits for weight-only | Large language models | [Post-training](post-training/index.md) |
| Quantisation-aware training | Yes | 2 to 8 bits | Smaller models and deployment targets with strict limits | [Quantisation-aware training](quantisation-aware-training/index.md) |
| Binary and ternary | Yes | 1 to 2 bits | Convolutional networks on specialised hardware | [Binary and ternary](binary-and-ternary/index.md) |
| Mixed precision | Depends on the method | Varies by layer | Budgets that a uniform width cannot meet | [Mixed precision](mixed-precision/index.md) |

PTQ is the usual choice for large language models, because a training run at that scale is expensive. QAT and the training-based families recover more accuracy at low bit-widths when a training run is affordable.

## Post-training methods at a glance

- [LLM.int8()](post-training/llm-int8/index.md): keeps outlier dimensions in 16 bits and runs the rest in 8 bits.
- [GPTQ](post-training/gptq/index.md): second-order rounding with error compensation, at 3 and 4 bits.
- [AWQ](post-training/awq/index.md): protects salient channels by scaling them according to activation statistics.
- [SmoothQuant](post-training/smoothquant/index.md): moves activation outliers into the weights, enabling 8-bit weights and activations.

## Trade-offs

- **Bits versus quality.** Going from 8 to 4 bits halves the weight memory again, but the quality loss grows and depends on the task and method, so it should be measured on the tasks that matter.
- **Calibration cost versus accuracy.** PTQ is cheap but limited; QAT recovers more accuracy at the price of a training run.
- **Format versus hardware.** A format that saves memory may not speed up inference unless the chip and kernel library support it.

## Connections

Quantisation is a standard step in [serving large models](../../../engineering/mlops/index.md), and the number formats it can use depend on the [hardware](../../../engineering/hardware/index.md). Biological neurons are noisy and transmit information with limited precision (Faisal, Selen & Wolpert, 2008), so the question of how much precision a useful system needs is also asked in neuroscience. The [training](../../../engineering/training/index.md) pages cover how quantised models are fine-tuned.

## Applications

- **On-device inference:** integer-only quantisation was designed for mobile devices, where latency and model size matter (Jacob et al., 2017).
- **Large language models:** weight-only 4-bit and 8-bit methods reduce the memory needed to serve a model on one GPU (Dettmers et al., 2022; Frantar et al., 2022; Lin et al., 2023).
- **Low-power vision:** efficient networks for cameras and robots use the same reduced-precision methods (Gholami et al., 2021).

## Open questions

- **Four bits and below.** Quality at 2 and 3 bits, especially for reasoning, is still an active research area.
- **Outliers in activations.** Methods differ in how they treat outliers in keys, values and activations, and no single rule is clearly best.
- **Evaluation.** Small drops in benchmark scores can hide large changes in behaviour, such as refusal or calibration. Better tests are needed.
- **Training-time quantisation at scale.** Quantisation-aware pre-training of very large models is harder to tune than post-training methods.

## References

### Seminal papers

- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Quantisation-aware training that keeps every operation in integer arithmetic, aimed at on-device inference on mobile hardware.
- Dettmers, T., Lewis, M., Belkada, Y., Zettlemoyer, L. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. NeurIPS. https://arxiv.org/abs/2208.07339 — Mixed-precision 8-bit inference that keeps outlier dimensions in 16 bits.
- Frantar, E., et al. (2023). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. ICLR. https://arxiv.org/abs/2210.17323 — Layer-wise, second-order error compensation for 3 and 4 bit weights.
- Lin, J., et al. (2023). *AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration*. MLSys 2024. https://arxiv.org/abs/2306.00978 — Chooses per-channel scales from activation statistics to protect salient weights.
- Xiao, G., et al. (2023). *SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models*. ICML 2023. https://arxiv.org/abs/2211.10438 — Migrates activation outliers into weights so that both can be 8-bit.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. Book chapter in *Low-Power Computer Vision*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods and their trade-offs.

### Neuroscience

- Faisal, A. A., Selen, L. P. J. & Wolpert, D. M. (2008). Noise in the nervous system. *Nature Reviews Neuroscience*, 9, 292–303. https://doi.org/10.1038/nrn2258 — Reviews the sources of noise in neurons and what they imply for how precisely the nervous system can represent information.
