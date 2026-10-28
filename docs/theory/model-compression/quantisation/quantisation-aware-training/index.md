---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- quantisation
- quantisation-aware training
aliases:
  - Quantisation-aware training
  - QAT
  - 量化感知訓練
---

# Quantisation-Aware Training

Quantisation-aware training (QAT) trains a network while simulating the rounding it will face at inference time, so that the weights adapt to the quantised grid. It is the training-aware counterpart of [post-training quantisation](../post-training/index.md), and it usually recovers more accuracy at the same bit-width, at the cost of a training run.

## Overview

In QAT, the forward pass applies fake quantisation: each weight or activation is rounded to the grid and mapped back to a real number, so the loss sees the rounding error. The backward pass cannot differentiate rounding, which is a step function with zero gradient almost everywhere. The standard fix is the **straight-through estimator** (STE): the gradient of the rounding operation is taken to be one, so gradients pass through as if no rounding happened. The same device is used by [BinaryConnect](../binary-and-ternary/binaryconnect/index.md) for binary weights.

## Key concepts

- **Fake quantisation.** Rounding applied during training, keeping activations in floating point so that the computation is still differentiable through the STE.
- **Step size.** The scale of the quantisation grid. In classic QAT it is set from statistics of the tensor; in learned schemes it is a trainable parameter.
- **Calibration versus training.** PTQ fits scales on a small batch and stops. QAT updates the weights for many steps, so the network can move its values onto the grid.
- **Batch normalisation folding.** Deployed models usually fold batch-norm into the preceding convolution before quantising, and QAT is run on the folded graph so that training matches deployment.

## Comparison of methods

| Method | What is learned or fixed | Typical bit-width | Page |
| --- | --- | --- | --- |
| Learned step size (LSQ) | Step size learned by gradient descent with the weights | 2 to 4 bits | [LSQ](lsq/index.md) |
| Integer-only inference | Every operation simulated in integers, including residual additions | 8 bits | [Integer-only inference](integer-only-inference/index.md) |

LSQ is the method to try first when accuracy at low bit-widths matters and a training run is affordable. Integer-only inference is the choice when the target device has no floating-point units, such as many mobile chips, and the training graph must match the integer kernels exactly.

## Trade-offs

- **Accuracy versus training cost.** QAT recovers more accuracy than PTQ at low bit-widths, and it needs a training run that PTQ avoids.
- **Gradient approximation.** The STE is biased, and the approximation becomes worse at very low bit-widths.
- **Scale of models.** For models with billions of parameters, full QAT is expensive, so PTQ methods such as [GPTQ](../post-training/gptq/index.md) are more common for LLMs.

## More variants and open issues

- **Quantisation-aware fine-tuning of LLMs** with low-rank adapters, which are discussed under [training](../../../../engineering/training/index.md).
- **Open issue:** whether learned step sizes stay stable when the calibration distribution changes after deployment.
- **Open issue:** how QAT interacts with outlier channels, which PTQ methods handle explicitly with [LLM.int8()](../post-training/llm-int8/index.md).

## Connections

QAT depends on the number formats that the [hardware](../../../../engineering/hardware/index.md) supports, and its cost depends on the training pipeline described under [training](../../../../engineering/training/index.md). Methods that use binary or ternary weights are in [binary and ternary](../binary-and-ternary/index.md), and the bit-allocation question is in [mixed precision](../mixed-precision/index.md).

## References

### Seminal papers

- Esser, S. K., et al. (2019). *Learned Step Size Quantization*. arXiv:1902.08153. https://arxiv.org/abs/1902.08153 — Learns the quantisation step size by gradient descent, reaching full-precision accuracy at 3 bits.
- Jacob, B., et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Quantisation-aware training that keeps every operation in integer arithmetic.
- Courbariaux, M., Bengio, Y., David, J.-P. (2015). *BinaryConnect: Training Deep Neural Networks with Binary Weights during Propagations*. arXiv:1511.00363. https://arxiv.org/abs/1511.00363 — Trains with binary weights in the forward pass and full-precision weights for updates.

### Surveys and textbooks

- Gholami, A., et al. (2021). *A Survey of Quantization Methods for Efficient Neural Network Inference*. arXiv:2103.13630. https://arxiv.org/abs/2103.13630 — Reviews precision reduction methods and their trade-offs, including training-aware ones.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — A post-training alternative to QAT for large language models, covered on the post-training pages.
