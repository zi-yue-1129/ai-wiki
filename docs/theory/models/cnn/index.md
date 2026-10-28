---
related:
- brain-mind/neuroai
- theory/models/computer-vision
aliases:
  - Convolutional Neural Networks
  - CNN
  - 卷積神經網路
tags:
  - convolutional networks
  - architecture
  - computer vision
last_reviewed: 2026-10-28
---

# Convolutional Neural Networks

A convolutional neural network (CNN) computes its features with the same small filter applied at every position of a grid. Because the filter is shared across positions, the network has far fewer parameters than a fully connected layer over the same input, and it builds in the assumption that a useful pattern can appear anywhere. CNNs are the family behind most image models before the rise of Transformers, and they remain common for images, audio spectrograms and time series. They are the architecture family whose inductive bias, locality and translation equivariance, was most directly inspired by the visual cortex. The [Computer Vision](../computer-vision/index.md) page covers the tasks they are used for.

## Core idea

A convolutional layer slides a learned kernel over its input, producing one output value per position and per filter. Stacking layers grows the receptive field, so deeper units see larger regions of the input. Pooling or strided convolution reduces the spatial resolution, and a final layer turns the features into predictions. The design choices that matter most are the form of the convolution, and how the layers are stacked and scaled. These are the two components below.

## Components and variants

- [Convolution variants](convolution-variants/index.md): standard, dilated, depthwise separable, transposed and deformable convolutions, and what each trades off.
- [Backbones and scaling](backbones-and-scaling/index.md): residual connections, the evolution from AlexNet to ConvNeXt, and compound scaling.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| AlexNet | 2012 | A large deep convolutional network trained on GPUs | [AlexNet](backbones-and-scaling/alexnet/index.md) |
| Deep residual learning (ResNet) | 2015 | Shortcut connections make very deep networks trainable | [ResNet](backbones-and-scaling/resnet/index.md) |
| Compound scaling (EfficientNet) | 2019 | One coefficient scales depth, width and resolution together | [EfficientNet](backbones-and-scaling/efficientnet/index.md) |
| U-Net | 2015 | Encoder–decoder with skip connections for dense prediction | [U-Net](unet/index.md) |

ResNet makes very deep backbones trainable, and EfficientNet chooses depth, width and resolution together rather than one at a time.

## Trade-offs

- **Inductive bias.** Locality and weight sharing make CNNs data-efficient on images, but they can limit the modelling of long-range dependencies unless the receptive field is enlarged.
- **Efficiency.** Depthwise separable designs cut computation sharply, which matters for mobile and embedded devices.
- **Versus Transformers.** Vision Transformers model global relations directly, but they usually need more data or pretraining. CNN and Transformer ideas now mix freely, as in ConvNeXt, which adopted Transformer design choices inside a convolutional network.

## Where it is used

Image classification, object detection and segmentation backbones, medical imaging, remote sensing, speech front ends, and the visual encoders of many multimodal systems.

## Connections

The receptive field of a CNN grows with depth, a property that the [recurrent](../rnn/index.md) and [attention](../transformer/attention-variants/index.md) families handle in other ways. The convolutional idea of local filtering in a shared spatial layout is also a common point of comparison with cortical receptive fields in [NeuroAI](../../../brain-mind/neuroai/index.md): deep CNN features have been compared with activity in visual cortex, though the match is partial.

## Open issues and further variants

- **Long-range context.** Large kernels, dilation and attention layers all try to extend the receptive field. How much long-range modelling a pure CNN needs for dense prediction is not settled.
- **Robustness.** CNNs are sensitive to small transformations and texture cues, and the best way to make them invariant or robust is an open question.
- **Designing architectures.** Most designs still come from manual search. Automated search methods exist, but their gains over well-tuned hand designs are often small.

## References

### Seminal papers

- LeCun, Y., Bottou, L., Bengio, Y. & Haffner, P. (1998). "Gradient-based learning applied to document recognition". *Proceedings of the IEEE* 86(11). https://doi.org/10.1109/5.726791 — Introduces the LeNet family of convolutional networks trained by gradient descent.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — Residual connections that allow very deep CNNs to train.
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — Compound scaling of depth, width and resolution.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt, a modernised pure CNN that matches Transformer baselines.
