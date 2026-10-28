---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - A ConvNet for the 2020s
  - ConvNeXt
  - ConvNeXt 網路
tags:
  - convolutional networks
  - architecture design
  - computer vision
last_reviewed: 2026-10-28
---

# ConvNeXt

ConvNeXt is a pure convolutional network introduced by Liu et al. in 2022 in "A ConvNet for the 2020s" ([arXiv:2201.03545](https://arxiv.org/abs/2201.03545)). The authors start from a ResNet and modernise its design one step at a time, borrowing choices from Transformers. The resulting network outperforms Swin Transformer baselines of similar size on ImageNet-1K, COCO detection and ADE20K segmentation.

## Problem

Transformer models such as Swin had become strong baselines for vision, and the question was how much of their advantage comes from the core operation, self-attention, and how much from design and training choices. The paper answers the second half of this question by re-examining a convolutional network with a modern recipe and design, and measuring each change on ImageNet-1K.

## Core idea

The paper starts from ResNet-50 and applies a sequence of changes, each measured by its ImageNet-1K accuracy:

- Macro design: the stage ratio is changed to 3:3:9:3, and the stem becomes a 4×4 stride-4 "patchify" layer.
- Block design: a depthwise convolution in the style of ResNeXt, with width increased to 96, and an inverted bottleneck whose hidden width is four times the input width.
- Kernel: a 7×7 depthwise kernel, moved up in the block. The paper reports that the gains saturate at 7×7.
- Activations and normalisation: GELU replaces ReLU, a single activation remains in each block, one LayerNorm replaces BatchNorm, and separate 2×2 stride-2 layers handle downsampling.

The paper's ResNet-50 baseline scores 76.13% top-1 in its recipe, and the full sequence reaches 81.97% for ConvNeXt-T in the same ImageNet-1K regime. The authors note that Swin-T scores 81.30% in that table.

## Equation or algorithm

A ConvNeXt block, in the form the paper describes, is a residual block with the following steps:

\[
y = x + \text{PWConv}_2\!\left(\text{GELU}\!\left(\text{PWConv}_1\!\left(\text{LN}\!\left(\text{DWConv}_{7\times 7}(x)\right)\right)\right)\right)
\]

Here DWConv is the 7×7 depthwise convolution, LN is layer normalisation, and the two pointwise (1×1) convolutions form the inverted bottleneck, expanding the width fourfold and then projecting it back.

## Results

All figures are from the paper's tables. Top-1 accuracy is on ImageNet-1K unless stated otherwise.

- At 224², ConvNeXt-T reaches 82.1% with 29M parameters and 4.5G FLOPs, against Swin-T at 81.3% with 28M and 4.5G. ConvNeXt-B reaches 83.8% with 89M and 15.4G, against Swin-B at 83.5% with 88M and 15.4G. ConvNeXt-L reaches 84.3% with 198M and 34.4G.
- With ImageNet-22K pretraining, ConvNeXt-XL (350M parameters) reaches 87.0% at 224² and 87.8% at 384².
- COCO object detection with Cascade Mask R-CNN and 22K pretraining gives box AP of 54.0 for ConvNeXt-B against 53.0 for Swin-B, and 54.8 for ConvNeXt-L against 53.9 for Swin-L.
- ADE20K segmentation with UperNet and 22K pretraining gives mIoU of 53.1 for ConvNeXt-B against 51.7 for Swin-B.
- On throughput, the paper reports that ConvNeXt is faster than Swin on a V100 at similar parameter counts, and that on an A100 it can have much higher throughput.

## Limitations

- The authors state that "ConvNeXt may be more suited for certain tasks, while Transformers may be more flexible for others". They suggest cross-attention may be preferable for multi-modal learning, and that Transformers may be more flexible for discretized, sparse or structured outputs.
- Depthwise convolution models are known to be slower and to use more memory at equal FLOPs. The paper reports throughput comparable to or above Swin across its tasks, and it gives training memory of 17.4 GB for ConvNeXt-B against 18.5 GB for Swin-B in Cascade Mask R-CNN.
- Each design choice had been studied before. The paper's contribution is to combine them, and the authors describe their scaling findings as "encouraging but not yet completely convincing".

## Connections

- [Backbones and scaling](../index.md) names ConvNeXt as the modernised pure CNN, beside residual connections and compound scaling.
- [ResNet](../resnet/index.md) is the starting point of the modernisation, and the residual block is kept in the final design.
- [VGG](../vgg/index.md) is the plain stack of 3×3 convolutions. ConvNeXt uses larger 7×7 depthwise kernels, and the paper's comparison with Transformers is a different question from VGG's depth study.
- [EfficientNet](../efficientnet/index.md) addresses the same backbone question by scaling, not by redesigning the block.
- [Convolution variants](../../convolution-variants/index.md) covers depthwise convolution, which ConvNeXt uses with a 7×7 kernel.
- [CNN](../../index.md) gives the wider context of convolutional models against Transformers.

## Open issues and further variants

- **Dependence on pretraining.** Without ImageNet-22K pretraining the gains are small. On COCO box AP, ConvNeXt-T and Swin-T both score 50.4, and on ADE20K ConvNeXt-T scores 46.7 against 45.8 for Swin-T. Whether the advantage holds in other data regimes is open.
- **Convolution against attention.** The paper suggests that much of the Transformer advantage is separable from attention, but whether the attention operation matters for multi-modal or structured outputs is not settled by this work.
- **Large kernels and hardware.** Gains from the 7×7 depthwise kernel saturate, and depthwise kernels cost memory and speed on some hardware. How this trade-off changes on other hardware is a practical open question.

## References

### Seminal papers

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". [arXiv:2201.03545](https://arxiv.org/abs/2201.03545) — ConvNeXt, a modernised pure CNN that matches Transformer baselines.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — Residual connections that allow very deep CNNs to train.
- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". [arXiv:1409.1556](https://arxiv.org/abs/1409.1556) — Stacks of small 3×3 convolutions, the plain deep design behind VGG.
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". [arXiv:1905.11946](https://arxiv.org/abs/1905.11946) — Compound scaling of depth, width and input resolution.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
