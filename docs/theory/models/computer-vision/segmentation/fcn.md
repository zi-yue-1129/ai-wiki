---
status: draft
last_reviewed: 2026-11-04
related:
  - theory/models/cnn
tags:
  - computer vision
  - image segmentation
  - semantic segmentation
aliases:
  - FCN
  - Fully Convolutional Network
  - Fully Convolutional Networks
  - 全卷積網路
---

# Fully convolutional networks (FCN)

Fully convolutional networks, or FCN, are the method that made deep networks practical for semantic segmentation. Long, Shelhamer and Darrell (2015) showed that a classification network with its fully connected layers replaced by convolutions can take an image of any size and output a dense map of class scores, trained end to end from pixels to pixels.

This page is part of [Image segmentation](index.md).

## Problem

Image classification networks of the time, such as AlexNet, VGG and GoogLeNet, ended in fully connected layers. Those layers fix the input size and discard the spatial layout of the final features, so the output is a single label for the whole image. Semantic segmentation needs one label per pixel. Earlier approaches fed image patches to a classifier one at a time, which was slow and gave each pixel only a small window of context.

## Core idea

The authors observed that a fully connected layer is a convolution whose kernel covers the whole input. Rewriting it as a convolution lets the network run on images of arbitrary size, and yields a coarse grid of class scores whose spatial layout matches the input. The paper calls this the *fully convolutional* form. Starting from pretrained classifiers and fine-tuning them on segmentation data is far cheaper than training a segmentation network from scratch, which the authors describe as infeasible given the time needed to learn the base classification networks.

The coarse output has a stride of 32 pixels in the basic version, so it must be upsampled. Upsampling is done inside the network with learned deconvolution (backward strided convolution). The final deconvolution filters are fixed to bilinear interpolation, while intermediate ones are initialised to bilinear upsampling and then learned. The paper also adds *skip* connections: predictions from shallower layers, which have finer resolution, are fused with the deep prediction before the final upsampling. This gives three variants:

- **FCN-32s**: prediction from the last layer only, upsampled by a factor of 32.
- **FCN-16s**: the last-layer prediction is upsampled by 2 and fused with a prediction from the pool4 layer, then upsampled by 16.
- **FCN-8s**: the same fusion is repeated with the pool3 layer, then upsampled by 8.

Fusing shallow features restores boundary detail that the coarse final layer has lost.

## Equation and procedure

Training minimises a per-pixel multinomial logistic loss, summed over the spatial dimensions of the final output. Let $y_{ij}\in\{1,\dots,K\}$ be the ground-truth class at output location $(i,j)$, and $f_{ij}(\mathbf{x};\theta)\in\mathbb{R}^K$ the class scores there. The objective has the form

$$
\mathcal{L}(\theta) = \sum_{i,j} \ell\big(f_{ij}(\mathbf{x};\theta),\, y_{ij}\big),
\qquad
\ell(\mathbf{s}, y) = -\log \frac{\exp(s_y)}{\sum_{k=1}^{K}\exp(s_k)}.
$$

Pixels marked as ambiguous or difficult in the ground truth are excluded from the sum. The paper describes the procedure as standard backpropagation of this loss through the whole network, so the segmentation output and the upsampling filters are trained jointly.

Inference is a single forward pass over the image. The paper's abstract reports that inference takes about one third of a second for a typical image.

## Results

- **PASCAL VOC 2012.** The abstract reports 62.2% mean intersection over union (mean IU) on the VOC 2012 segmentation test set, which it describes as a 20% relative improvement.
- **Variant comparison.** On a validation subset of VOC 2011, the paper's Table 2 reports 59.4 mean IU for FCN-32s, 62.4 for FCN-16s and 62.7 for FCN-8s, so the skip fusion adds about three points in mean IU.
- **Other benchmarks.** The abstract also reports state-of-the-art results on NYUDv2 and SIFT Flow.

The paper's appendix notes that mean IU is not a good measure of fine-scale accuracy, which is one reason later work reports boundary-sensitive metrics as well (see [Segmentation metrics](../../../evaluation/metrics/segmentation/index.md)).

## Limitations

- **Coarse boundaries.** The authors note that the 32-pixel stride at the final prediction layer limits the scale of detail in the output. Skip fusion reduces this but does not remove it.
- **No instance separation.** Each pixel receives a class, so two objects of the same class merge into one region. Instance methods such as [Mask R-CNN](mask-r-cnn.md) address this.
- **Context at a fixed scale.** The receptive field of the network is fixed by its architecture, so very large or very small structures are hard to label consistently.
- **Dependence on pretraining.** The paper relies on fine-tuning classifiers pretrained on ImageNet. Training the same architecture from scratch on segmentation data alone was not feasible in the authors' setting.

Later encoder–decoder designs such as [U-Net](../../cnn/unet/index.md) use a symmetric decoder with skip connections to recover finer detail. The FCN paper introduced the fully convolutional view of dense prediction that these designs build on.

## Connections

- The classification networks that FCN adapts are covered in the [convolutional networks](../../cnn/index.md) section.
- The encoder–decoder family that followed FCN is described on the [U-Net](../../cnn/unet/index.md) page.
- Among the segmentation methods compared on the [overview](index.md), FCN is the simplest route from a classifier to a dense map.

## References

### Seminal papers

- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR, pp. 3431–3440. doi:[10.1109/CVPR.2015.7298965](https://doi.org/10.1109/CVPR.2015.7298965). Also available as [arXiv:1411.4038](https://arxiv.org/abs/1411.4038). — Converts classification networks into fully convolutional networks with learned upsampling and skip fusion, trained end to end for dense prediction.
- Shelhamer, E., Long, J. & Darrell, T. (2017). *Fully Convolutional Networks for Semantic Segmentation*. IEEE Transactions on Pattern Analysis and Machine Intelligence, pp. 640–651. doi:[10.1109/TPAMI.2016.2572683](https://doi.org/10.1109/TPAMI.2016.2572683). — Journal version of the same work, which the conference paper above introduced.
- Simonyan, K. & Zisserman, A. (2014). *Very Deep Convolutional Networks for Large-Scale Image Recognition*. arXiv. https://arxiv.org/abs/1409.1556 — The VGG classification network, one of the three networks (with AlexNet and GoogLeNet) that the FCN paper converts.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. Lecture Notes in Computer Science, pp. 234–241. doi:[10.1007/978-3-319-24574-4_28](https://doi.org/10.1007/978-3-319-24574-4_28). Also available as [arXiv:1505.04597](https://arxiv.org/abs/1505.04597). — The encoder–decoder with skip connections that built on the fully convolutional approach, covered on the U-Net page.

### Surveys and textbooks

- Minaee, S., Boykov, Y., Porikli, F. et al. (2021). Image Segmentation Using Deep Learning: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. doi:[10.1109/TPAMI.2021.3059968](https://doi.org/10.1109/TPAMI.2021.3059968). — Survey of deep-learning methods for image segmentation, for readers who want the wider landscape.
