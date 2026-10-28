---
related:
- theory/models/cnn/backbones-and-scaling
- theory/models/cnn
aliases:
  - Very Deep Convolutional Networks
  - VGG
  - VGG 網路
tags:
  - convolutional networks
  - model depth
  - computer vision
last_reviewed: 2026-10-28
---

# VGG

VGG is a family of deep convolutional networks introduced by Simonyan and Zisserman in their 2015 paper "Very Deep Convolutional Networks for Large-Scale Image Recognition" ([arXiv:1409.1556](https://arxiv.org/abs/1409.1556)). The paper shows that a simple, uniform stack of 3×3 convolutions, with 11 to 19 weight layers, reaches strong ImageNet accuracy, and it makes depth the main variable under study.

## Problem

The paper asks how the depth of a convolutional network affects accuracy on large-scale image recognition. To isolate depth, the other architecture choices are kept fixed while more convolutional layers are added. The authors make this possible by using very small 3×3 filters in every layer, so that depth can grow without changing the filter design.

## Core idea

Every convolutional layer uses 3×3 filters with stride 1, and max pooling separates the groups of convolutions. Two stacked 3×3 layers have a 5×5 effective receptive field, and three have a 7×7 field. The paper argues that three 3×3 layers add three non-linearities where one 7×7 layer adds one, which "makes the decision function more discriminative", and that they use fewer weights. For C input and output channels, three 3×3 layers need 27C² weights and one 7×7 layer needs 49C². The paper reads this as a regularisation of the 7×7 filters.

## Equation or algorithm

The configurations (A to E in the paper's Table 1) differ in how many convolutions each stage contains. The forward pass has the same shape in every configuration:

```
input: 224×224 RGB crop
for each of the 5 stages:
    repeat n_s times: 3×3 convolution (stride 1) followed by ReLU
    2×2 max pooling (stride 2)
flatten, then
    fully connected 4096 + ReLU
    fully connected 4096 + ReLU
    fully connected 1000, then softmax
```

The weight comparison behind the 3×3 choice is

\[
3 \cdot (3 \cdot 3 \cdot C^2) = 27C^2 \qquad \text{versus} \qquad 7 \cdot 7 \cdot C^2 = 49C^2 .
\]

## Results

All figures are ILSVRC (ImageNet) error rates from the paper.

- Single-scale training at a fixed size of 256, validation top-1 and top-5 error: configuration B (13 weight layers) reaches 28.7% and 9.9%, D (16 weight layers) 27.0% and 8.8%, and E (19 weight layers) 27.3% and 9.0%. With scale jittering during training (sizes 256 to 512) and testing at 384, D reaches 25.6% and 8.1%, and E reaches 25.5% and 8.0%.
- The paper's best single network on the validation set reaches 24.8% top-1 and 7.5% top-5 error.
- A combination of two networks reaches 23.7% top-1 and 6.8% top-5 validation error.
- The ILSVRC-2014 submission, an ensemble of seven models, reaches 7.3% top-5 test error, which the paper reports as second place in the competition.
- The parameter counts in the paper's Table 2 are 133 million for configurations A and B and 144 million for configuration E.

## Limitations

- Training is expensive. The paper reports that a single net took 2 to 3 weeks on four NVIDIA Titan Black GPUs.
- Error saturates at 19 layers. The authors say that even deeper models might help on larger datasets, but they did not test this.
- Local response normalisation did not improve configuration A, and it increased memory use and computation time.
- Multi-crop evaluation gives only slight gains, and the authors say the extra computation does not justify those gains in practice.
- For most experiments the validation set was used as the test set.

## Connections

- [Backbones and scaling](../index.md) places VGG as the plain deep design. [ResNet](../resnet/index.md) adds shortcut connections so that networks can go deeper, and [EfficientNet](../efficientnet/index.md) scales depth, width and resolution together.
- [ConvNeXt](../convnext/index.md) revisits the stacked-convolution idea with larger 7×7 depthwise kernels inside a ResNet-style design.
- [Convolution variants](../../convolution-variants/index.md) covers the standard convolution that VGG stacks.
- [CNN](../../index.md) gives the wider family context.
- [Computer vision](../../../computer-vision/index.md) covers the image classification task that VGG was built for.

## Open issues and further variants

- **Depth beyond 19 layers.** The paper reports saturation at 19 layers. Residual connections later made much deeper networks trainable, so the point where plain stacks stop helping is tied to optimisation as well as to depth.
- **Training cost.** Training took weeks on four GPUs. How to reach the same depth and accuracy trade-off at lower cost is still open, and later families such as EfficientNet compare accuracy with computation directly.

## References

### Seminal papers

- Simonyan, K. & Zisserman, A. (2015). "Very Deep Convolutional Networks for Large-Scale Image Recognition". [arXiv:1409.1556](https://arxiv.org/abs/1409.1556) — Stacks of small 3×3 convolutions, the plain deep design behind VGG.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — Residual connections that allow very deep CNNs to train.
- Huang, G., et al. (2017). "Densely Connected Convolutional Networks". [arXiv:1608.06993](https://arxiv.org/abs/1608.06993) — Connects each layer to all later layers, reusing features and easing gradient flow.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". [arXiv:2201.03545](https://arxiv.org/abs/2201.03545) — ConvNeXt, a modernised pure CNN that matches Transformer baselines.
