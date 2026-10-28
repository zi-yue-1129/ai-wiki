---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- theory/model-compression
tags:
- AI hardware
- number formats
- mixed precision
- training
aliases:
  - Mixed-precision training
  - Mixed precision
  - 混合精度訓練
---

# Mixed-Precision Training

Mixed-precision training stores most values and runs most arithmetic in 16-bit floating point, while keeping a single-precision copy of the weights and scaling the loss so that small gradients survive. Micikevicius et al. (2017) report that this reduces the memory used by deep learning models by nearly two times, across several architectures. It is a training technique, and it sits in the [co-design overview](index.md) as the number-format lever for training.

## Problem

Training a network keeps the weights, the activations and the gradients in memory, and each of them is usually stored as a 32-bit float. Memory limits the size of model and batch that fits on a chip, and the bandwidth needed to move 32-bit values limits speed. Storing values in 16 bits halves the bytes moved for each one, but 16-bit values have a smaller range and precision, and training can lose accuracy or become unstable with them.

## Key concepts

- **Half precision:** a 16-bit floating-point format for activations and gradients, with less range and precision than 32-bit.
- **Master weights:** a single-precision copy of the weights, which accumulates the gradient updates after each optimiser step, so small updates are not lost to rounding.
- **Loss scaling:** multiplying the loss by a constant before the backward pass, so that small gradients do not underflow in half precision, and dividing the gradients by the same constant before the weight update.

## How it works

Each training step follows these stages:

1. Copy the single-precision master weights into a half-precision copy.
2. Run the forward pass and the backward pass in half precision, with the loss scaled.
3. Undo the loss scaling on the gradients.
4. Apply the update to the single-precision master weights.

The arithmetic and the stored activations run at the lower width, which is where the memory and bandwidth saving comes from. The master weights and the update remain at full width, which keeps small changes from being rounded away.

## Results

Micikevicius et al. (2017) report that using this approach reduces the memory consumption of deep learning models by nearly two times. They recommend keeping a single-precision copy of the weights that accumulates the gradients after each optimiser step, and scaling the loss to handle the loss of information in half-precision gradients. They tested convolutional, recurrent and generative adversarial networks.

Micikevicius et al. (2022) extend the idea to 8-bit floating-point formats, E4M3 and E5M2. They report that on models up to 175 billion parameters, training with these formats effectively matches the result quality of 16-bit training, with the hyperparameters left unchanged. That result is for training; the lower-precision inference methods covered in [quantisation](../../../theory/model-compression/quantisation/index.md) are a separate line of work.

## Limitations

The saving is less than a full halving of all memory, because the master weights stay in single precision and the optimiser state is not reduced by this method. Half-precision gradients can lose information, which is why loss scaling is needed, and the scale must be chosen so that values neither underflow nor overflow. The paper's experiments cover the architectures listed above, so results on other models need their own checks.

## Open questions

- **How far below 16 bits training can go.** The FP8 results show that 8-bit formats can match 16-bit quality on large models, but which operations and which stages of training tolerate the lower precision is still being worked out.
- **Hardware support.** Whether a chip runs half-precision and 8-bit arithmetic at the speed its memory saving suggests depends on the hardware, which is why the [accelerators](../accelerators/index.md) comparison matters.

## Connections

Mixed precision is one of the three levers in the [co-design overview](index.md). The memory it saves is the cost that [memory hierarchy and bandwidth](../memory-hierarchy/index.md) describes, and the same idea of fewer bits per value appears in the inference side of [quantisation](../../../theory/model-compression/quantisation/index.md). [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) is a kernel that works within the same memory constraints.

## References

### Seminal papers

- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shows that 16-bit training reduces memory use by nearly two times across architectures, with master weights and loss scaling.
- Micikevicius, P., et al. (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — Proposes two 8-bit floating-point encodings that match 16-bit training quality on models up to 175 billion parameters.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys how dataflow and number format choices shape the efficiency of DNN hardware.

### Articles and documentation

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — Shows the inference-side counterpart: per-channel 8-bit quantisation keeps many CNNs within 2% of floating-point accuracy.
- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the primary bottleneck for AI serving, which is the pressure this method relieves.
