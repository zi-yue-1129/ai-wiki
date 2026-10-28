---
related:
- theory/models/cnn/convolution-variants
- theory/models/cnn
aliases:
  - Deformable Convolution
  - DCN
  - 可變形卷積
tags:
  - convolution
  - object detection
  - spatial adaptation
last_reviewed: 2026-10-28
---

# Deformable Convolution

Deformable convolution lets the sampling positions of a convolution move. Dai et al. (2017), in "Deformable Convolutional Networks", learn an offset for each sampling point, so that the kernel can follow the shape of an object. The paper reports gains for object detection and semantic segmentation.

## Problem

A regular convolution samples a fixed grid around each output position, so its receptive field has the same shape everywhere. Objects differ in shape, scale and pose, and one fixed grid cannot match all of them. Dai et al. make the sampling grid itself learnable, so that each output can sample from a region adapted to the object.

## Core idea

Each sampling point of the regular grid receives an extra learned offset, predicted by a separate offset layer that reads the same input feature map. The offset layers start with zero weights, so the operation begins as a regular convolution. Because offsets are generally fractional, the input is sampled by bilinear interpolation, which keeps the operation differentiable. The same offset idea is applied to RoI pooling, so that the pooling bins can move with the object.

## Equation or algorithm

For a standard convolution over a regular grid \(\mathcal{R}\), the paper writes

\[
\mathbf{y}(\mathbf{p}_0) = \sum_{\mathbf{p}_n \in \mathcal{R}} \mathbf{w}(\mathbf{p}_n)\, \mathbf{x}(\mathbf{p}_0 + \mathbf{p}_n).
\]

Deformable convolution adds a learned offset \(\Delta\mathbf{p}_n\) to each of the \(N = |\mathcal{R}|\) sampling points:

\[
\mathbf{y}(\mathbf{p}_0) = \sum_{\mathbf{p}_n \in \mathcal{R}} \mathbf{w}(\mathbf{p}_n)\, \mathbf{x}(\mathbf{p}_0 + \mathbf{p}_n + \Delta\mathbf{p}_n).
\]

Fractional positions are sampled by bilinear interpolation, with a per-axis weight \(g(a,b) = \max(0, 1 - |a - b|)\). For deformable RoI pooling, the paper gives \(\mathbf{y}(i,j) = \sum_{\mathbf{p} \in \text{bin}(i,j)} \mathbf{x}(\mathbf{p}_0 + \mathbf{p} + \Delta\mathbf{p}_{ij}) / n_{ij}\), where \(n_{ij}\) is the number of pixels in the bin and the offsets are scaled by \(\gamma = 0.1\).

## Results

The paper's results use ResNet-101 unless noted. On COCO test-dev, mAP@[0.5:0.95] rises from 29.4 to 33.1 for Faster R-CNN and from 30.8 to 34.5 for R-FCN. R-FCN with multi-scale testing and iterative bounding-box averaging rises from 35.5 to 37.5. The paper describes these as "11%, 13%, and 12% relatively higher" for its three main comparisons. For segmentation with DeepLab, mIoU rises from 69.7 to 75.3 on PASCAL VOC and from 70.4 to 75.2 on Cityscapes. On PASCAL VOC 2007, R-FCN's mAP@0.5 rises from 80.0 to 82.6. The overhead is small: Faster R-CNN's parameters grow from 58.3M to 59.9M, and its forward time from 0.147 s to 0.192 s, measured on an Intel E5-2650 v2 CPU with an Nvidia K40 GPU.

## Limitations

The paper has no dedicated limitations section, but its text states several caveats. Deformable convolution is applied to the last few convolutional layers, and three deformable layers are chosen as "a good trade-off." The gains saturate with depth: they saturate at 3 deformable layers for DeepLab and 6 for the other models. Deformable RoI pooling currently uses bins of the same size, and it ignores spatial relations between parts, which the paper describes as simpler than deformable part models (DPM). The ablations use fixed, pre-computed RPN proposals without feature sharing. The overhead figures are wall-clock times on one CPU and GPU setup, so they do not measure the irregular memory access that the approach text names as the main cost on some hardware.

## Connections

The [convolution variants](../index.md) page lists deformable convolution as the form that learns its sampling positions, and the [CNN family](../../index.md) page places it among the components of a CNN. The [dilated convolution](../dilated-convolution/index.md) page fixes the sampling pattern with gaps rather than learning it, and the [depthwise separable convolution](../depthwise-separable-convolution/index.md) page changes how channels are mixed rather than where samples are taken. The detection and segmentation tasks in which the paper reports its gains are covered on the [computer vision](../../../computer-vision/index.md) page. The [attention variants](../../../transformer/attention-variants/index.md) page covers related ideas about where a layer looks.

## Open issues and further variants

- **Cost of irregular access.** The paper's measured overhead is small on its own hardware, but the approach text identifies irregular memory access as the main cost on some accelerators. Hardware-friendly learned sampling remains open.
- **Depth saturation.** The paper reports that gains saturate after 3 layers for DeepLab and 6 for the other models. Whether a different design of the offset layers would delay this saturation is an open question.
- **Relations between parts.** Deformable RoI pooling ignores spatial relations between parts, which the paper presents as a simplification relative to DPM. Whether adding those relations would help is not tested in the paper.

## References

### Seminal papers

- Dai, J., et al. (2017). "Deformable Convolutional Networks". [arXiv:1703.06211](https://arxiv.org/abs/1703.06211) — Learns sampling offsets so the convolution adapts to object shape.
- Yu, F. & Koltun, V. (2015). "Multi-Scale Context Aggregation by Dilated Convolutions". [arXiv:1511.07122](https://arxiv.org/abs/1511.07122) — Dilated convolutions for dense prediction with exponentially growing receptive fields.
- Chen, L.-C., et al. (2016). "DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs". [arXiv:1606.00915](https://arxiv.org/abs/1606.00915) — Atrous convolution with fully connected CRFs for dense segmentation.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — Residual connections that allow very deep CNNs to train.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 9 covers convolutional networks, with the standard account of the convolution operation.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
