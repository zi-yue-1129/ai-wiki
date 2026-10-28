---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - architecture
  - efficient inference
aliases:
  - Swin Transformer
  - Shifted windows
  - 移位視窗
  - 階層式視覺 Transformer
---

# Swin Transformer: shifted windows (Liu et al., 2021)

Swin Transformer is a hierarchical vision Transformer that computes self-attention inside small local windows and shifts the windows between layers, so that cost grows linearly with image size. It is the second landmark variant in the [Vision Transformer](../index.md) topic, and it was designed as a general backbone for detection and segmentation as well as classification.

## Overview

The original [ViT](../vit/index.md) keeps one feature resolution and computes attention over all patches, so its cost grows with the square of the image area. Dense tasks such as detection and segmentation need fine-resolution, multi-scale features, which ViT does not provide. Swin builds a feature pyramid like a CNN and restricts attention to windows, which keeps the cost manageable. Its authors compare it with the [ResNet](../../../cnn/backbones-and-scaling/resnet/index.md) backbones used in detection and report that it is a better backbone for those tasks, not only for classification.

## Key concepts

- **Patch merging**: each stage concatenates each 2 × 2 group of neighbouring tokens and projects them, halving the resolution and doubling the width.
- **Window attention**: self-attention is computed inside non-overlapping M × M windows. The default window size is M = 7.
- **Shifted windows**: in alternate layers the window grid is displaced by half a window, so tokens in neighbouring windows can exchange information.
- **Relative position bias**: a learned bias that depends on the offset between two tokens in a window, in place of absolute position embeddings.

## How it works

A 4 × 4 patch embedding turns the image into tokens of width C. Four stages follow, with resolutions H/4, H/8, H/16 and H/32. Each stage contains Swin blocks, and each stage after the first begins with a patch merging layer. Two successive blocks compute

$$
\hat z^l = \text{W-MSA}(\text{LN}(z^{l-1})) + z^{l-1}, \quad z^l = \text{MLP}(\text{LN}(\hat z^l)) + \hat z^l
$$

$$
\hat z^{l+1} = \text{SW-MSA}(\text{LN}(z^l)) + z^l, \quad z^{l+1} = \text{MLP}(\text{LN}(\hat z^{l+1})) + \hat z^{l+1}
$$

where W-MSA uses regular windows and SW-MSA uses shifted windows. Attention includes a relative position bias B:

$$
\text{Attention}(Q,K,V) = \text{SoftMax}\!\left(\frac{QK^\top}{\sqrt{d}} + B\right)V
$$

The cost is \(\Omega(\text{W-MSA}) = 4hwC^2 + 2M^2hwC\), which is linear in the number of patches \(hw\) for a fixed window size, while global attention is quadratic in \(hw\). To shift windows efficiently, the feature map is cyclically rolled and a mask stops tokens from attending across the wrapped boundary, so the number of windows stays the same. The variants Swin-T and Swin-S use C = 96 with depths {2, 2, 6, 2} and {2, 2, 18, 2}; Swin-B and Swin-L use C = 128 and 192, with the same depth pattern as Swin-S.

## Results

Table 1 of the paper reports ImageNet-1K top-1 accuracy at 224 × 224. Swin-T reaches 81.3% with 29M parameters, against 79.8% for DeiT-S. Swin-B reaches 83.5%, against 81.8% for DeiT-B. With ImageNet-22K pre-training, Swin-B reaches 86.4% at 384 and Swin-L reaches 87.3%. On COCO, Swin-L with HTC++ reaches 58.7 box AP on test-dev with multi-scale testing, and with UperNet Swin-L reaches 53.5 mIoU on ADE20K validation.

The ablations use Swin-T. Shifting the windows adds 1.1% top-1 on ImageNet-1K over a single regular partition. Relative position bias adds 1.2% top-1 over no position encoding, and 0.8% over absolute embeddings. The paper also compares shifted windows with sliding windows. The two reach similar accuracy (81.3% against 81.4%), but the shifted version is faster by a factor of roughly 1.5 to 4, depending on the implementation.

## Limitations

- **Fixed window size.** Each layer sees a window of M × M tokens, so global context builds up only through depth and shifting. The default M = 7 is fixed throughout the paper's experiments.
- **Implementation.** The authors note that their version uses built-in PyTorch functions, and that a kernel-level optimisation was beyond the paper's scope.
- **Competition from CNNs.** [ConvNeXt](../../../cnn/backbones-and-scaling/convnext/index.md) later showed that a pure convolutional network can match Swin at similar cost, which weakens the claim that windowed attention is the key ingredient.

## Open questions

- Whether the hierarchy or the windowing is the more important part of the design. The paper's ablations focus on shifting and position bias, so the hierarchy is tested less directly.
- How windowed attention should scale to very large images or video, where the window grid and relative bias must change.
- Whether a single backbone can serve vision and language, a goal the authors state at the end of the paper.

## References

### Seminal papers

- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. arXiv; ICCV 2021. https://arxiv.org/abs/2103.14030 — The original paper, introducing shifted-window attention and the hierarchical Swin backbone.
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv; ICLR 2021. https://arxiv.org/abs/2010.11929 — The single-resolution ViT that Swin is designed to improve for dense tasks.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — The self-attention and Transformer block that Swin modifies.
- He, K., et al. (2016). *Deep Residual Learning for Image Recognition*. arXiv; CVPR 2016. https://arxiv.org/abs/1512.03385 — The residual CNN backbone that Swin is compared with in detection experiments.
- Lin, T.-Y., et al. (2017). *Feature Pyramid Networks for Object Detection*. arXiv; CVPR 2017. https://arxiv.org/abs/1612.03144 — Builds multi-scale feature pyramids, the structure Swin's hierarchy is designed to feed.
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. arXiv; CVPR 2022. https://arxiv.org/abs/2201.03545 — ConvNeXt, a pure CNN that matches or outperforms Swin at similar cost.
