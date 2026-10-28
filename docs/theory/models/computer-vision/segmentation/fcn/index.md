---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn/backbones-and-scaling
tags:
  - computer vision
  - convolutional networks
  - architecture
aliases:
  - FCN
  - 全卷積網路
  - Fully Convolutional Networks
---

# Fully Convolutional Networks

A fully convolutional network (FCN) turns an image classifier into a dense pixel labeller. It removes the fully connected layers, so that the network accepts an image of any size and produces a grid of class scores, which learned upsampling layers then bring back to full resolution. It is the method that made end-to-end semantic segmentation with deep networks standard. It is one of the four landmark methods on the [Image Segmentation](../index.md) page.

## Overview

Before this work, many deep segmentation systems classified image patches one at a time, which repeated much of the computation for overlapping patches. Long, Shelhamer and Darrell observed that a network built only from convolution, pooling and activation layers can be run once over a whole image. Its output is then a spatial map of class scores, not a single label. They adapted several contemporary classification networks into this form and fine-tuned them on segmentation data.[^1]

## Key concepts

- **Convolutionalisation**: replacing the fully connected layers of a classifier with convolutions over the final feature map. The same learned weights then act as a classifier at every location.
- **Stride**: pooling reduces resolution. In the main network the output has a stride of 32, so the raw prediction is 32 times smaller than the image in each direction.
- **Learned upsampling**: a backwards strided convolution, sometimes called deconvolution. It is initialised to bilinear interpolation and then learned from the pixel loss.
- **Skip architecture**: predictions from earlier, finer layers are added to the upsampled coarse prediction, so that edges are recovered.

## How it works

The pipeline starts with a classification network whose layers are convolutional throughout. Its last layer gives a coarse map. The FCN-32s model upsamples this map straight to the image size. FCN-16s first doubles the coarse map and adds the prediction from a layer at stride 16, and FCN-8s repeats the step with a layer at stride 8. Each fused map is then upsampled to the input size.

Training minimises a per-pixel multinomial logistic loss, summed over the labelled pixels:

$$
\mathcal{L} = -\sum_{x \in \Omega} \log p_{\ell(x)}(x)
$$

Here \(\Omega\) is the set of labelled pixels, \(\ell(x)\) is the true class of pixel \(x\), and \(p_k(x)\) is the softmax probability of class \(k\) at that pixel. Pixels marked as ambiguous are ignored.

## Results

The paper evaluates on the PASCAL VOC segmentation benchmark, with mean intersection over union (mean IU) as the metric. On a subset of the VOC 2011 validation set, the variants reach:

| Variant | Mean IU |
|---|---|
| FCN-32s with only the last layer fine-tuned | 45.4 |
| FCN-32s | 59.4 |
| FCN-16s | 62.4 |
| FCN-8s | 62.7 |

The abstract reports 62.2% mean IU on the PASCAL VOC 2012 test set, a 20% relative improvement, and states that inference on a typical image takes about one third of a second.[^2] The same network was also evaluated on NYUDv2 and SIFT Flow.

## Limitations

- **Coarse output.** Even with skip fusion, the prediction is produced at a coarse grid, which limits the detail of thin structures. The authors report diminishing returns after fusing the stride-8 layer.
- **No instances.** The loss labels pixels by class, so two touching objects of the same class merge into one region. [Mask R-CNN](../mask-rcnn/index.md) addresses this.
- **Limited context.** A fixed receptive field restricts how much global context each prediction sees. The pyramid pooling network PSPNet was proposed to aggregate global context.[^3]
- **Training cost.** The paper reports that fine-tuning takes three days on one GPU for FCN-32s, and about a day for each upgrade to FCN-16s and FCN-8s.

## Open questions

- Can a network keep both fine detail and wide context without a separate skip path? Dilated convolution, pyramid pooling and encoder–decoder designs answer this in different ways.
- How much do the gains come from the architecture, and how much from pre-training on classification data? The paper's results depend on that initialisation.

[^1]: Long et al. (2015), abstract: several classification networks are adapted into fully convolutional networks and fine-tuned for segmentation.
[^2]: Long et al. (2015), abstract and Table 2 of the paper. The VOC 2011 subset figures are on the paper's validation split, not the test server.
[^3]: Zhao et al. (2017), abstract: the pyramid pooling module aggregates context from different regions to improve scene parsing.

## References

### Seminal papers

- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR. https://arxiv.org/abs/1411.4038 — The paper itself: adapts classification networks into fully convolutional segmenters with skip fusion.
- Shelhamer, E., Long, J. & Darrell, T. (2017). *Fully Convolutional Networks for Semantic Segmentation*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2016.2572683 — The journal version of the FCN paper, with the same method and experiments.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. MICCAI. https://doi.org/10.1007/978-3-319-24574-4_28 — A symmetric encoder–decoder that replaces the FCN skip fusion with concatenation.
- Chen, L.-C., Papandreou, G., Kokkinos, I., Murphy, K. & Yuille, A. L. (2018). *DeepLab: Semantic Image Segmentation with Deep Convolutional Nets, Atrous Convolution, and Fully Connected CRFs*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2017.2699184 — Keeps resolution high with atrous convolution, an alternative to upsampling the coarse map.
- Zhao, H., Shi, J., Qi, X., Wang, X. & Jia, J. (2017). *Pyramid Scene Parsing Network*. CVPR. https://arxiv.org/abs/1612.01105 — Adds a pyramid pooling module to aggregate global context for scene parsing.

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV. https://arxiv.org/abs/1703.06870 — Adds a mask branch to a detector, the instance-level step that follows this method.

### Surveys and textbooks

- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — Reviews FCN-style pixel-labelling networks alongside later encoder–decoder and attention designs.
