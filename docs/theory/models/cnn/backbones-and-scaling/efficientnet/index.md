---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - Compound Scaling
  - EfficientNet
  - 複合縮放
tags:
  - model scaling
  - efficiency
  - computer vision
last_reviewed: 2026-10-28
---

# EfficientNet and Compound Scaling

EfficientNet is a family of convolutional networks introduced by Tan and Le in 2019 in "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". The paper proposes compound scaling, which grows a network's depth, width and input resolution together with one coefficient instead of scaling a single dimension.

## Problem

Scaling one dimension (depth, width or input resolution) gives diminishing gains, and tuning several of them by hand is tedious and often sub-optimal.

## Core idea

Scale all three dimensions together with one coefficient φ, so that the network grows in a fixed proportion. The constants are found by a small grid search on a baseline network, EfficientNet-B0, which a multi-objective architecture search produced.

## Equation or algorithm

\[
d = \alpha^{\phi}, \qquad w = \beta^{\phi}, \qquad r = \gamma^{\phi}
\]

Here d, w and r scale depth, width and input resolution. The constants satisfy \(\alpha \cdot \beta^2 \cdot \gamma^2 \approx 2\) with \(\alpha, \beta, \gamma \geq 1\). FLOPS then grow by roughly \(2^{\phi}\). For φ = 1 the search gave α = 1.2, β = 1.1 and γ = 1.15.

## Results

- EfficientNet-B7 reaches 84.3% top-1 accuracy on ImageNet with 66M parameters and 37B FLOPS.
- The paper reports that it is 8.4× smaller and 6.1× faster at inference than GPipe, which reaches 84.3% with 557M parameters.

## Limitations

- Searching the constants directly on large models was too costly, so they were searched once on the baseline network.
- The paper notes that the effect of scaling "heavily depends on the baseline network".
- The architecture search optimised FLOPS rather than latency.

## Connections

- [Backbones and scaling](../index.md) sets compound scaling beside residual connections and the later modernised CNNs.
- [Residual Networks](../resnet/index.md) covers the residual connections that make very deep backbones trainable. The two pages answer different questions: how to train deep networks, and how to choose their size.
- [Convolution variants](../../convolution-variants/index.md) covers depthwise separable convolution, which cuts computation for mobile and embedded devices.
- [CNN](../../index.md) gives the wider family context, including the trade-offs of convolutional models.
- [Computer vision](../../../computer-vision/index.md) covers the tasks these backbones are used for.

## Open issues and further variants

- **Constants on large models.** Searching the constants on large models was too costly, so they were fixed on the baseline. How well they carry over to other baselines is an open question.
- **FLOPS and latency.** The architecture search optimised FLOPS rather than latency, so the search objective and the speed that matters on hardware can differ.
- **Training speed.** A follow-up from the same authors, EfficientNetV2, searches for models that train faster as well as being smaller (see the references).

## References

### Seminal papers

- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — Compound scaling of depth, width and resolution.
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". arXiv:1704.04861 — Depthwise separable convolutions as building blocks for efficient on-device vision.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt, a modernised pure CNN that matches Transformer baselines.
- Tan, M. & Le, Q. V. (2021). "EfficientNetV2: Smaller Models and Faster Training". arXiv:2104.00298 — A follow-up from the same authors that searches for models that train faster as well as being smaller.
