---
status: complete
last_reviewed: 2026-10-28
related:
- engineering/hardware
- theory/model-compression
tags:
- AI hardware
- number formats
- FP8
- training
- quantisation
aliases:
  - FP8 formats
  - E4M3
  - E5M2
  - FP8 格式
---

# FP8 Formats for Deep Learning

FP8 is an 8-bit floating-point format for deep learning. Micikevicius et al. (2022) propose two encodings of it, E4M3 and E5M2, and report that they can be used for training and inference with results that effectively match 16-bit training, without changing hyperparameters. It is the next step after [mixed-precision training](mixed-precision.md), which moved values from 32 bits to 16. Each value now takes half the bytes again, and it sits in the [co-design overview](index.md) as the most aggressive number-format lever for training.

## Problem

Storing and moving 16-bit values already halves the traffic that 32-bit values need. An 8-bit format halves that traffic once more, which matters when memory bandwidth limits speed, as the [memory hierarchy](../memory-hierarchy/index.md) page describes. With only 8 bits, the format must divide its bits between range, set by the exponent, and precision, set by the mantissa, and no single split suits every tensor. The paper therefore defines two encodings that split the bits differently.

## Key concepts

- **E4M3:** 4 exponent bits and 3 mantissa bits. It gives more precision and less range. The paper extends its dynamic range by not representing infinities and by using a single bit pattern for NaN. Its largest normal value is 448.
- **E5M2:** 5 exponent bits and 2 mantissa bits. It gives more range and less precision, and it follows the IEEE 754 conventions for special values. Its largest normal value is 57,344.
- **Scaling factor:** a number multiplied into a tensor before it is cast to FP8, so that the tensor's largest magnitude falls near the format's maximum. Values that still overflow saturate to that maximum.

## Key methods

### FP8 training with E4M3 and E5M2 (Micikevicius et al., 2022)

- **Problem:** an 8-bit format must split its bits between range and precision, and overflow is far more common than at 16 bits.
- **Core idea:** use E4M3 for weights and activations and E5M2 for gradients, with a scaling factor per tensor. The inputs of matrix multiplications and convolutions are rounded to FP8, while the arithmetic runs at 16 bits or higher.
- **Equations:** each tensor is cast as \(x_{\text{FP8}} = \mathrm{cast}(s \cdot x)\), where \(s\) is chosen so that the tensor's largest magnitude lands near the format's maximum, 448 for E4M3 and 57,344 for E5M2.
- **Results:** FP8 training matches 16-bit training within run-to-run variation on most models. The 175-billion-parameter model reached perplexity 6.68 against 6.65 for bfloat16, compared at 75% of training.
- **Limitations:** the experiments simulate FP8 in software, and the paper leaves the scaling heuristics to implementations. Skipping updates on overflow, the 16-bit remedy, is a poor fit for FP8.

## How it works

The paper simulates FP8 training by rounding the inputs of each matrix multiplication and convolution to FP8. The arithmetic is carried out in 16-bit or bfloat16, and the outputs stay at higher precision. Within this setup the paper recommends E4M3 for weights and activations, and E5M2 for activation gradients, which have a wider range.

Scaling is done in software. Each tensor is multiplied by a scaling factor before the cast, and some networks need a separate factor for each tensor. The paper also notes that the skip-the-update response to overflow used in 16-bit mixed-precision training is a poor fit for FP8, because overflows are much more common at this width.

## Results

The paper reports that FP8 training effectively matches 16-bit training on a range of image and language tasks, with hyperparameters unchanged. The models include convolutional networks, recurrent networks and Transformers, with language models up to 175 billion parameters.

For the 175-billion-parameter model, the FP8 run reached a perplexity of 6.68, against 6.65 for the bfloat16 baseline. That comparison is taken at 75% of the training run, because the baseline had not finished. The paper reports that MobileNet v2 was the only vision model whose result fell outside run-to-run variation.

The paper also applies FP8 to post-training quantisation of language models that had not quantised well to 8-bit integers. Quantising a 1.3-billion-parameter GPT model's residual connections with a single exponent bias raised its perplexity to 12.59, against 10.19 for the baseline. Per-tensor calibration brought it to 10.44.

## Limitations

- **Simulated, not native.** The training experiments simulate FP8 in software. Real FP8 hardware was not used for them, so speed claims need a separate measurement.
- **Scaling is outside the paper.** The paper leaves the scaling-factor heuristics and the rounding mode to implementations.
- **Scope of tensors.** Only matrix-multiplication and convolution inputs were quantised in the main experiments, and moving more tensors to FP8 is left for future work. For image models, the first convolution and the last fully connected layer were also quantised.
- **Sensitivity to the format choice.** Some networks need per-tensor scaling rather than a shared exponent bias, so a single recipe does not cover every model.

## Open questions

- **Which tensors can use FP8.** The paper leaves open how much of the rest of training, such as optimiser state and reductions, can move to FP8 without losing quality.
- **The vision gap.** Whether the MobileNet v2 result is a real effect or noise is not settled in the paper.
- **Hardware support.** How much speed FP8 gives depends on the chip, which is why the [accelerators](../accelerators/index.md) comparison matters.

## Connections

FP8 extends the idea of [mixed-precision training](mixed-precision.md), which keeps master weights in single precision and scales the loss. The bytes it saves are the traffic described in [memory hierarchy and bandwidth](../memory-hierarchy/index.md), and the inference-side use of low-bit formats is covered in [quantisation](../../../theory/model-compression/quantisation/index.md).

## References

### Seminal papers

- Micikevicius, P., et al. (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — Defines the E4M3 and E5M2 encodings and reports FP8 training that effectively matches 16-bit results, up to 175 billion parameters.
- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Introduces 16-bit training with master weights and loss scaling, which FP8 training builds on.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the energy and throughput trade-offs of DNN hardware, including hardware–algorithm co-design.

### Articles and documentation

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — Shows that per-channel 8-bit integer quantisation keeps many CNNs within 2% of floating-point accuracy, the integer counterpart of FP8 inference.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory, rather than compute, has become the primary bottleneck for AI applications, particularly serving, which is the pressure that lower-bit formats relieve.
