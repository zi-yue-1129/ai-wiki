---
related:
- theory/models/transformer
aliases:
  - Backbones and Scaling
  - Residual Networks
  - ResNet
  - EfficientNet
  - 骨幹網路與縮放
  - 殘差網路
tags:
  - residual connections
  - model scaling
  - computer vision
last_reviewed: 2026-10-28
---

# Backbones and Scaling

A CNN backbone is the stack of layers that turns raw pixels into features, which a task head then uses for classification, detection or segmentation. The history of backbones is largely a history of two problems: making networks deep enough to help without becoming untrainable, and deciding how to grow a network when more compute is available. The first is solved by residual connections, the second by scaling rules.

## Overview

| Idea | Representative model | What it solves |
|---|---|---|
| Deep stacks of convolutions | AlexNet, VGG | Learning features end to end at scale |
| Residual connections | ResNet | Training very deep networks |
| Compound scaling | EfficientNet | Choosing depth, width and resolution together |
| Modernised convolutions | ConvNeXt | Matching Transformer baselines with a pure CNN |

## Approaches

### Residual connections

A residual block learns a correction \(F(x)\) and adds it back to its input, so the block outputs \(x + F(x)\). He et al. (2015) showed that without this shortcut, deeper plain networks had higher training error than shallower ones, which points to optimisation difficulty rather than overfitting. With shortcuts the gradient has a direct path through the network, and networks of hundreds of layers became trainable. Residual connections are now used in almost every deep architecture, including Transformers.

### Compound scaling

A bigger network can be made by adding depth, width or input resolution. EfficientNet argued that increasing only one of these saturates quickly, and proposed scaling all three together by a fixed ratio chosen with a small search. The resulting family gave better accuracy per unit of compute than scaling a single dimension.

### Modernised pure CNNs

Liu et al. (2022) started from a ResNet and changed its design step by step, borrowing choices from Transformers, such as larger kernels, fewer activation functions, layer normalisation and an inverted bottleneck. The resulting ConvNeXt matched Transformer baselines on image classification and detection. The result suggests that much of the gap between CNNs and Transformers came from training recipes and design details rather than from the core operation.

## Trade-offs

- **Depth versus width.** Deeper networks represent more complex functions, but they cost more memory during training, and width often gives better hardware efficiency.
- **Accuracy per compute.** Scaling laws in the family are useful, but the best ratio depends on the target hardware and data.
- **Pretraining.** Large CNN backbones pretrained on big datasets transfer well, which is why the same architecture is often judged by its pretrained results.

## Connections

Residual connections are the same idea as the skip connections in [Transformers](../../transformer/index.md), and they appear in [MLPs](../../mlp/index.md) too. The scaling question returns in the [Transformer](../../transformer/index.md) family, where model size and data size are set together. Brain connections are indirect: deep CNN layers have been compared with the hierarchy of visual areas in [NeuroAI](../../../../brain-mind/neuroai/index.md).

## Open issues and further variants

- **Scaling rules across families.** The compound scaling rule was derived for one family. Whether it transfers to other families, and how to scale them, is not settled.
- **Why residuals work.** Several explanations, from gradient flow to ensemble-like behaviour, are supported by experiments, and their relative importance is debated.
- **Architecture search.** Automated search can find competitive backbones, but the cost of search is high and the results depend on the search space.

## References

### Seminal papers

- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — Residual connections that make very deep CNNs trainable, the basis of later backbones.
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — Compound scaling of depth, width and input resolution.
- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". arXiv:1409.1556 — Stacks of small 3×3 convolutions, the plain deep design behind VGG.
- Huang, G., et al. (2017). "Densely Connected Convolutional Networks". arXiv:1608.06993 — Connects each layer to all later layers, reusing features and easing gradient flow.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — Step-by-step modernisation of a ResNet that matches Transformer baselines.
