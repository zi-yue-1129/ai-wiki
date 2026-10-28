---
related:
- brain-mind/neuroai
aliases:
  - Convolution Variants
  - Depthwise Separable Convolution
  - Dilated Convolution
  - 卷積變體
  - 深度可分離卷積
tags:
  - convolution
  - efficient inference
  - computer vision
last_reviewed: 2026-10-28
---

# Convolution Variants

The convolution operation has several variants, each changing one of its three properties: the set of positions it samples (the receptive field), the way channels are mixed, or the spatial layout of the output. Choosing a variant sets the receptive field size at a given depth, the number of parameters, and the cost per layer. Most image architectures are built from one or two of these forms.

## Overview

| Variant | What changes | Main benefit | Main cost |
|---|---|---|---|
| Standard | Dense kernel over neighbourhood, all channels mixed | Expressive, well understood | Cost grows with kernel size and channels |
| Dilated | Gaps between kernel taps | Larger receptive field, same parameters | Gridding artefacts if used carelessly |
| Depthwise separable | Spatial filter per channel, then 1×1 mixing | Much lower cost | Less expressive per layer |
| Transposed | Learned upsampling | Decoders and generation | Checkerboard artefacts |
| Deformable | Sampling positions learned per location | Adapts to object shape | Irregular memory access, slower |

## Approaches

### Dilated convolution

A dilated convolution spaces the kernel taps apart. Yu and Koltun (2015) used stacks of dilated layers for dense prediction, growing the receptive field exponentially with depth while keeping the feature map at full resolution. This suits segmentation, where pixel-level output is needed, but stacked dilations can leave gaps in the sampled pixels, which later designs address with mixed dilation rates.

### Depthwise separable convolution

A standard convolution mixes space and channels in one step. A depthwise separable convolution splits the two: a single spatial filter per channel, followed by a 1×1 convolution that mixes channels. The Xception architecture, which took this design furthest, reports better ImageNet accuracy than Inception V3 with a similar parameter count. MobileNet-style networks use the same factorisation for on-device inference.

### Deformable convolution

A regular kernel samples a fixed grid around each position. Deformable convolutions learn offsets for each sampling point, so the kernel can follow the shape of an object. Dai et al. (2017) showed gains for detection and segmentation, at the cost of irregular memory access that makes the operation slower on some hardware.

### Transposed convolution

Transposed convolutions are used to upsample feature maps in decoders, for segmentation and generation. A common problem is the checkerboard pattern that appears when the stride does not divide the kernel size evenly. Resize-then-convolve designs are often used to avoid it.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Dilated convolution | 2015 | Spaced kernel taps enlarge the receptive field without extra parameters | [Dilated convolution](dilated-convolution/index.md) |
| Depthwise separable convolution (Xception) | 2016 | A spatial filter per channel, then 1×1 channel mixing | [Depthwise separable convolution](depthwise-separable-convolution/index.md) |
| Deformable convolution | 2017 | Learned sampling offsets let the kernel follow object shape | [Deformable convolution](deformable-convolution/index.md) |

## Trade-offs

- **Receptive field versus resolution.** Dilation and downsampling both enlarge the receptive field, but downsampling loses spatial detail that dilation keeps.
- **Parameters versus accuracy.** Separable convolutions save parameters and computation, but a network built only from them can lose capacity unless its width is increased.
- **Hardware.** Depthwise operations are memory bound on many accelerators, so a lower operation count does not always mean lower latency.

## Connections

These variants are the building blocks of the [CNN family](../index.md), and the same locality idea appears in [attention variants](../../transformer/attention-variants/index.md), where local windows replace fixed kernels. The receptive-field question also connects to the wider [computer vision](../../computer-vision/index.md) tasks.

## Open issues and further variants

- **Learning the sampling pattern.** Deformable convolutions learn where to sample, but they add irregular computation. Hardware-friendly learned sampling remains an open engineering problem.
- **Global context.** Dilated and large-kernel convolutions extend context, yet they do not match full attention on tasks needing long-range relations.
- **Equivariance.** Standard and dilated convolutions are equivariant to translation only. Extending them to rotations and other transformations is an active area of research.

## References

### Seminal papers

- Yu, F. & Koltun, V. (2015). "Multi-Scale Context Aggregation by Dilated Convolutions". [arXiv:1511.07122](https://arxiv.org/abs/1511.07122) — Dilated convolutions for dense prediction with exponentially growing receptive fields.
- Dai, J., et al. (2017). "Deformable Convolutional Networks". [arXiv:1703.06211](https://arxiv.org/abs/1703.06211) — Learns sampling offsets so the convolution adapts to object shape.
- Chollet, F. (2016). "Xception: Deep Learning with Depthwise Separable Convolutions". [arXiv:1610.02357](https://arxiv.org/abs/1610.02357) — Shows that factorising spatial and channel mixing can outperform standard Inception-style designs at lower cost.
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". [arXiv:1704.04861](https://arxiv.org/abs/1704.04861) — Depthwise separable convolutions as building blocks for efficient on-device vision.
- Chen, L.-C., et al. (2016). "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs". [arXiv:1606.00915](https://arxiv.org/abs/1606.00915) — Atrous convolution with fully connected CRFs for dense segmentation.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
