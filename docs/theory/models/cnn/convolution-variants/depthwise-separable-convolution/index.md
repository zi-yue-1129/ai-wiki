---
related:
- theory/models/cnn/convolution-variants
- theory/models/cnn
aliases:
  - Depthwise Separable Convolution
  - DSC
  - 深度可分離卷積
tags:
  - convolution
  - efficient inference
  - mobile vision
last_reviewed: 2026-10-28
---

# Depthwise Separable Convolution

A depthwise separable convolution factorises a standard convolution into two steps: a spatial filter applied to each channel separately, followed by a 1×1 convolution that mixes the channels. Chollet (2016) took this design furthest in Xception, in "Xception: Deep Learning with Depthwise Separable Convolutions", where the Inception modules are replaced by depthwise separable convolutions with residual connections.

## Problem

A standard convolution does spatial filtering and channel mixing in one operation, so its cost grows with the kernel size and with the product of the input and output channel counts. Inception modules showed that splitting these two jobs can work well, but the Inception family still mixes several kinds of operation. The Xception paper asks what happens when that split is taken to its extreme.

## Core idea

The Xception paper describes a depthwise separable convolution as "a spatial convolution performed independently over each channel of an input," followed by "a 1x1 convolution, projecting the channels output by the depthwise convolution onto a new channel space." It states that such a convolution "can be understood as an Inception module with a maximally large number of towers." The name Xception stands for "Extreme Inception": the architecture is built entirely from these blocks, with residual connections. MobileNets (Howard et al., 2017) use the same factorisation as building blocks for efficient on-device vision.

## Equation or algorithm

For an input with \(C_{\text{in}}\) channels, an output with \(C_{\text{out}}\) channels, a \(k \times k\) kernel and an output of size \(H \times W\), a standard convolution costs about \(k^2 C_{\text{in}} C_{\text{out}} HW\) multiply-adds. The depthwise separable form costs \(k^2 C_{\text{in}} HW\) for the depthwise step plus \(C_{\text{in}} C_{\text{out}} HW\) for the 1×1 step, so its ratio to the standard cost is \(1/C_{\text{out}} + 1/k^2\). This ratio follows from the definitions above and is not a figure reported in the paper.

## Results

On ImageNet, using single-crop, single-model evaluation, Xception reaches a top-1 score of 0.790 and a top-5 score of 0.945, against 0.782 and 0.941 for Inception V3. The paper says the two networks have nearly the same number of parameters, 23,626,728 for Inception V3 and 22,855,952 for Xception in its Table 3. It concludes that the gains come from a more efficient use of the model parameters rather than from added capacity. On the JFT dataset, the paper reports a 4.3% relative improvement on FastEval14k MAP@100 (6.50 against 6.78, with fully connected layers).

## Limitations

The paper states several caveats. Its optimisation settings were tuned for Inception V3, and the authors did not attempt to tune the optimisation hyperparameters for Xception. ImageNet results are reported on the validation set, and the JFT models "were not trained to full convergence." Removing the non-linearity between the depthwise and pointwise steps gave faster convergence and better final performance on ImageNet, but the authors say the presence or absence of that non-linearity "might matter." In the paper's own timing, Xception is marginally slower than Inception V3 (28 against 31 steps per second in Table 3), despite the similar parameter count.

## Connections

The [convolution variants](../index.md) page compares this factorisation with the other forms, and the [CNN family](../../index.md) page places it among the building blocks of CNNs. The approach to efficient backbones, and how such backbones are scaled, is covered in the [backbones and scaling](../../backbones-and-scaling/index.md) page, including [EfficientNet](../../backbones-and-scaling/efficientnet/index.md). The [dilated convolution](../dilated-convolution/index.md) and [deformable convolution](../deformable-convolution/index.md) pages cover the other two forms of change, which alter the sampling positions rather than how channels are mixed. The [attention variants](../../../transformer/attention-variants/index.md) page covers a different route to efficiency, through local windows.

## Open issues and further variants

- **Intermediate non-linearity.** The paper leaves open whether the non-linearity between the depthwise and pointwise steps matters. Removing it helped on ImageNet in the paper's experiments, but the effect was not explained.
- **Intermediate designs.** The paper states that "there is no reason to believe that depthwise separable convolutions are optimal," and leaves the points between Inception-style modules and the fully depthwise form to future work.
- **Operations versus speed.** A lower operation count does not automatically mean lower latency. The approach text notes that depthwise operations are memory bound on many accelerators, and the paper's own timing shows Xception slightly slower despite similar size.

## References

### Seminal papers

- Chollet, F. (2016). "Xception: Deep Learning with Depthwise Separable Convolutions". arXiv:1610.02357 — Shows that factorising spatial and channel mixing can outperform standard Inception-style designs at lower cost.
- Howard, A. G., et al. (2017). "MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications". arXiv:1704.04861 — Depthwise separable convolutions as building blocks for efficient on-device vision.
- Tan, M. & Le, Q. V. (2019). "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks". arXiv:1905.11946 — Compound scaling of depth, width and resolution.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Liu, Z., et al. (2022). "A ConvNet for the 2020s". arXiv:2201.03545 — ConvNeXt, a modernised pure CNN that matches Transformer baselines.
