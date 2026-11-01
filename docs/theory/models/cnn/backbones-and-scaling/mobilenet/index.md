---
related:
  - theory/models/cnn/backbones-and-scaling
  - theory/models/cnn/convolution-variants/depthwise-separable-convolution
  - engineering/on-device-edge/tinyml-and-mobile-runtimes
tags:
  - efficient architectures
  - mobile vision
  - computer vision
last_reviewed: 2026-11-01
aliases:
  - MobileNet
  - MobileNetV1
  - 行動網路
  - 深度可分離卷積網路
---

# MobileNets (Howard et al., 2017)

MobileNets are a family of image-classification networks built from depthwise separable convolutions. They trade a small amount of accuracy for a large reduction in computation, so that a convolutional network can run on a phone or other small device. Howard et al. (2017) introduced the design together with two global settings that choose the size of the network.

## Overview

A standard convolution must mix information across space and across channels at the same time. Each output value depends on a small spatial window and on every input channel, so the cost grows with the product of the two. MobileNets split these two jobs into separate steps, which lowers the cost substantially. The paper targets mobile and embedded vision, where the trade-off between latency and accuracy matters most (Howard et al., 2017).

## Key concepts

- **Depthwise convolution**: applies one spatial filter to each input channel separately.
- **Pointwise convolution**: a 1×1 convolution that mixes channels at each position.
- **Width multiplier (α)**: scales the number of channels in every layer.
- **Resolution multiplier (ρ)**: scales the input image size, and so the spatial size of every feature map.

## Problem

The authors want a family of networks for mobile and embedded vision in which the trade-off between latency and accuracy can be set to a given budget. They achieve this with one architecture and two global hyper-parameters, instead of designing a new network for each budget (Howard et al., 2017).

## Core idea

Replace each standard convolution with a depthwise separable convolution: a depthwise convolution that filters each channel spatially, followed by a pointwise convolution that combines channels. The network stacks 28 such layers when depthwise and pointwise convolutions are counted separately. The two global settings then reduce the cost further. The width multiplier thins every layer, and the resolution multiplier reduces the input image size (Howard et al., 2017).

## Equations

Let the kernel be D_K by D_K, the input have M channels and the output N channels, and the feature map be D_F by D_F. A standard convolution costs

\[
D_K^2 \cdot M \cdot N \cdot D_F^2
\]

A depthwise separable convolution costs

\[
D_K^2 \cdot M \cdot D_F^2 + M \cdot N \cdot D_F^2
\]

The ratio of the two is

\[
\frac{1}{N} + \frac{1}{D_K^2}
\]

For 3×3 kernels this ratio approaches 1/9 when N is large, which is why the paper describes the saving as 8 to 9 times less computation (Howard et al., 2017).

The two multipliers enter the same formula. With width multiplier α and resolution multiplier ρ, the cost becomes

\[
D_K^2 \cdot \alpha M \cdot \rho D_F^2 + \alpha M \cdot \alpha N \cdot \rho D_F^2
\]

The paper states that the width multiplier reduces computation and parameters roughly by α², and the resolution multiplier reduces computation by ρ². The width multiplier takes values in (0, 1], with typical settings 1, 0.75, 0.5 and 0.25. The resolution multiplier is usually set so that the input is 224, 192, 160 or 128 pixels (Howard et al., 2017).

## Results

The table below reports ImageNet top-1 accuracy at 224-pixel input, with Mult-Adds and parameters for each width setting:

| Width multiplier | Top-1 accuracy | Mult-Adds | Parameters |
|---|---|---|---|
| 1.0 | 70.6% | 569 million | 4.2 million |
| 0.5 | 63.7% | 149 million | 1.3 million |
| 0.25 | 50.6% | 41 million | 0.5 million |

These figures are the paper's own (Howard et al., 2017, Table 6). The full model at width 1.0 is the reference point, and the smaller settings show the trade-off that the multiplier controls.

The paper also applies MobileNets to object detection, fine-grained classification, face attributes and large-scale geo-localisation, and reports strong performance compared with other popular models (Howard et al., 2017).

## Successors

Sandler et al. (2018) introduce MobileNetV2, which uses inverted residual blocks with linear bottlenecks. The abstract states that it is important to remove non-linearities in the narrow layers. It also builds SSDLite for detection and a reduced DeepLabv3 for segmentation (Sandler et al., 2018). Howard et al. (2019) use architecture search to design MobileNetV3 (Howard et al., 2019).

## Connections

- [Depthwise separable convolution](../../convolution-variants/depthwise-separable-convolution/index.md) is the operation that makes MobileNets cheap, and it has its own page.
- [ResNet](../resnet/index.md) and [EfficientNet](../efficientnet/index.md) pursue accuracy at larger scales. MobileNets sit at the efficient end of the same family of trade-offs.
- [Tiny ML and mobile runtimes](../../../../../engineering/on-device-edge/tinyml-and-mobile-runtimes/index.md) describe the software that runs such models on devices.

## Applications

MobileNets target on-device vision. The papers apply them to image classification, object detection, segmentation, fine-grained recognition, face attributes and geo-localisation (Howard et al., 2017; Sandler et al., 2018).

## Limitations

- **Accuracy at small width.** The 0.25 setting loses about 20 percentage points of top-1 accuracy compared with the full model, so the trade-off is steep at the low end.
- **Cost is a proxy.** The paper reports multiply-adds and parameters. These counts describe computation and storage, not the latency measured on a particular device.
- **Later revisions.** MobileNetV2 and MobileNetV3 changed the block design and the search process, so results for the first version should not be compared with results for later ones without noting the version.

## Open questions

- How well multiply-adds predict latency on new accelerators, and whether depthwise convolutions run as efficiently as their low cost suggests.
- Whether architecture search, as used for MobileNetV3, gives gains that a hand-designed block cannot reach at the same cost.

## References

### Seminal papers

- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv. https://arxiv.org/abs/1704.04861 — Introduces depthwise separable convolutions in a family of networks with width and resolution multipliers.
- Sandler, M. et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks*. arXiv. https://arxiv.org/abs/1801.04381 — The second version, with inverted residual blocks and linear bottlenecks, and applications to detection and segmentation.
- Howard, A. et al. (2019). *Searching for MobileNetV3*. arXiv. https://arxiv.org/abs/1905.02244 — The third version, designed with architecture search.

### Surveys and related models

- Chollet, F. (2016). *Xception: Deep Learning with Depthwise Separable Convolutions*. arXiv. https://arxiv.org/abs/1610.02357 — Builds a large network from depthwise separable convolutions, the same operation used in MobileNets.
- Iandola, F. N. et al. (2016). *SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size*. arXiv. https://arxiv.org/abs/1602.07360 — A contemporary compact network designed for a small parameter budget, which shows the same goal from a different design.
