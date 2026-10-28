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
  - Learned step size
  - 量化感知訓練
---

# Quantisation-Aware Training

Quantisation-aware training (QAT) trains a network while simulating the rounding it will face at inference time, so that the weights adapt to the quantised grid. It is the training-aware counterpart of [post-training quantisation](../index.md), and it usually recovers more accuracy at the same bit-width, at the cost of a training run.

## Overview

In QAT, the forward pass applies fake quantisation: each weight or activation is rounded to the grid and mapped back to a real number, so the loss sees the rounding error. The backward pass cannot differentiate rounding, which is a step function with zero gradient almost everywhere. The standard fix is the **straight-through estimator** (STE): the gradient of the rounding operation is taken to be one, so gradients pass through as if no rounding happened. Binarised training with this estimator was popularised by [BinaryConnect](../binary-and-ternary/index.md).

## Key concepts

- **Fake quantisation.** Rounding applied during training, keeping activations in floating point so that the computation is still differentiable through the STE.
- **Step size.** The scale of the quantisation grid. In classic QAT it is set from statistics of the tensor; in learned schemes it is a trainable parameter.
- **Calibration versus training.** PTQ fits scales on a small batch and stops. QAT updates the weights for many steps, so the network can move its values onto the grid.
- **Batch normalisation folding.** Deployed models usually fold batch-norm into the preceding convolution before quantising, and QAT is run on the folded graph so that training matches deployment.

## Key methods

### Learned Step Size Quantisation (Esser et al., 2019)

- **Problem:** Fixed rules for the step size are not tuned to the loss, and at 2 to 4 bits the choice matters a great deal.
- **Core idea:** Treat the step size as a parameter and learn it by gradient descent together with the weights. The gradient with respect to the step size is obtained through the rounding function with the straight-through approximation.
- **Equation or algorithm:** The quantised value is \(\hat{x} = s \cdot \operatorname{round}(\operatorname{clip}(x/s, -Q_n, Q_p))\), and \(s\) is updated from the loss, with a gradient scale chosen so that the step size learns at a sensible rate relative to the weights.
- **Results:** The abstract says the method achieves the highest accuracy to date on ImageNet for models quantised to 2, 3 and 4 bits, and that 3-bit models reach full-precision baseline accuracy.
- **Limitations:** Training cost is the cost of a full or long fine-tuning run. The results are for image classification, and the method needs labelled training data.

### Integer-only inference (Jacob et al., 2017)

- **Problem:** Mobile devices run integer arithmetic far more efficiently than floating point, but a network trained in floats loses accuracy when converted.
- **Core idea:** Simulate integer-only inference during training, so that every operation, including the non-linearities and the residual additions, is computed on quantised values.
- **Equation or algorithm:** The affine mapping of real values to 8-bit integers with a scale and zero point, applied to weights and activations, with integer matrix multiplication followed by a rescale.
- **Results:** The abstract reports that the improvements are significant even on MobileNets, a model family already designed for efficient inference. It gives no single headline number.
- **Limitations:** The scheme is designed for convolutional networks of the time, and its gains on large transformers are not covered by the paper.

## Trade-offs

- **Accuracy versus training cost.** QAT recovers more accuracy than PTQ at low bit-widths, and it needs a training run that PTQ avoids.
- **Gradient approximation.** The STE is biased, and the approximation becomes worse at very low bit-widths.
- **Scale of models.** For models with billions of parameters, full QAT is expensive, so PTQ methods such as [GPTQ](../index.md) are more common for LLMs.

## More variants and open issues

- **Quantisation-aware fine-tuning of LLMs** with low-rank adapters, which are discussed under [training](../../../../engineering/training/index.md).
- **Open issue:** whether learned step sizes stay stable when the calibration distribution changes after deployment.
- **Open issue:** how QAT interacts with outlier channels, which PTQ methods handle explicitly with [LLM.int8()](../index.md).

## Connections

QAT depends on the number formats that the [hardware](../../../../engineering/hardware/index.md) supports, and its cost depends on the training pipeline described under [training](../../../../engineering/training/index.md). Methods for keeping a model's behaviour during reduced precision are discussed under [quantisation](../index.md).

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

- Dettmers, T., et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale*. arXiv:2208.07339. https://arxiv.org/abs/2208.07339 — A post-training alternative to QAT for large language models, covered on the parent page.
