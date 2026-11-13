---
status: draft
last_reviewed: 2026-11-04
related:
  - theory/models/computer-vision/object-detection
tags:
  - computer vision
  - image segmentation
  - instance segmentation
  - object detection
aliases:
  - Mask R-CNN
  - Mask RCNN
  - 遮罩 R-CNN
  - 實例分割網路
---

# Mask R-CNN

Mask R-CNN is a framework for instance segmentation: it detects each object in an image and predicts a separate pixel mask for each one. He, Gkioxari, Dollár and Girshick (2017) extended the detector Faster R-CNN with a third output branch that predicts a mask in parallel with the class and box outputs. It became a standard baseline for instance segmentation and was extended to keypoint estimation in the same framework.

This page is part of [Image segmentation](index.md).

## Problem

Semantic segmentation methods such as [FCN](fcn.md) label every pixel by class, so two adjacent people of the same class merge into one region. Instance segmentation has to separate the objects as well as outline them. Two-stage detectors already find each object as a box, and the open question was how to add a precise mask to each detection without a large cost and without giving up the accuracy of the box output.

## Core idea

Mask R-CNN keeps the two-stage structure of Faster R-CNN. A region proposal network proposes candidate regions, and for each region the network extracts features and predicts a class and a refined box. The new step is a small fully convolutional branch that predicts a binary mask for each region of interest (RoI). The mask branch runs in parallel with the box branch, so the mask prediction does not change how the boxes are found. The paper reports that the method adds only a small overhead to Faster R-CNN and runs at 5 frames per second.

Two design choices matter most.

- **Per-class binary masks.** The mask head outputs one binary mask for each class, and the loss uses only the mask of the RoI's ground-truth class. Each class has its own sigmoid, so masks do not compete with one another as they do under the per-pixel softmax of FCN. Classification is handled by the separate class branch.
- **RoIAlign.** Faster R-CNN extracts the features of each RoI with RoIPool, which rounds the RoI boundaries and bins to the feature-map grid. The paper argues that this misalignment has a large negative effect on pixel-accurate masks. RoIAlign removes the quantisation: it samples the feature map at regularly spaced points inside each bin and combines them by bilinear interpolation.

## Animated walkthrough: rounded versus aligned sampling

<div style="max-width:100%;overflow-x:auto" role="region" tabindex="0" aria-label="Scrollable RoI sampling comparison">
<div style="width:800px">
<img src="../../../../assets/concept-animations/roi-align-sampling-still.svg" data-motion-src="../../../../assets/concept-animations/roi-align-sampling-motion.svg" data-still-src="../../../../assets/concept-animations/roi-align-sampling-still.svg" width="800" height="460" alt="Two matching feature grids: an orange target moves continuously, while rounded RoIPool-style sampling jumps and RoIAlign-style bilinear sampling varies smoothly.">
</div>
</div>

**What changes?** The orange marker moves through the same invented feature grid in both panels. The teal sample on the left snaps between positions, producing an abrupt output-bar change; on the right the sample follows the continuous coordinate and the output bar changes smoothly. The illustration deliberately reduces RoIPool-style coordinate quantisation to a **single nearest-grid read**, not the full RoIPool max-pooling algorithm. Real RoIAlign evaluates **bilinearly interpolated feature values at locations inside every RoI bin**, then aggregates them. This is a schematic one-dimensional slice, not a measured feature map or the numerical result of [Mask R-CNN](https://arxiv.org/abs/1703.06870).

GitHub shows the reviewed **static fallback** directly. On MkDocs, the same asset gains an accessible **Play/Pause** button (Tab, Enter or Space), plus reduced-motion fallback. On a narrow screen, focus the diagram region and scroll horizontally to retain readable labels.

*Original concept animation and static fallback, CC BY-SA 4.0.*

## Equation and procedure

Each sampled RoI carries a multi-task loss

$$
\mathcal{L} = \mathcal{L}_{\text{cls}} + \mathcal{L}_{\text{box}} + \mathcal{L}_{\text{mask}},
$$

where $\mathcal{L}_{\text{cls}}$ and $\mathcal{L}_{\text{box}}$ are the classification and box-regression losses of Fast R-CNN. The mask loss is the average binary cross-entropy over the $m \times m$ mask of the ground-truth class $k$, after a per-pixel sigmoid:

$$
\mathcal{L}_{\text{mask}} = -\frac{1}{m^2}\sum_{i,j}\Big[\,y_{ij}\log \hat{y}^{k}_{ij} + (1-y_{ij})\log\big(1-\hat{y}^{k}_{ij}\big)\Big],
$$

where $y_{ij}$ is the ground-truth mask value and $\hat{y}^{k}_{ij}$ the predicted probability for class $k$.

The procedure for one image is:

1. The backbone network computes a feature map.
2. The region proposal network proposes candidate boxes.
3. RoIAlign extracts a fixed-size feature grid for each proposal.
4. The class and box branches predict a label and a refined box. The mask branch predicts a per-class mask for the same RoI.
5. At inference, the mask for the predicted class is kept and resized to the box.

## Results

The results below are those reported in the paper, on the COCO benchmark.

- **Instance segmentation.** With a ResNet-101 backbone and feature pyramid network, the paper reports 35.7 mask average precision (AP) on the COCO test-dev split, with AP50 of 58.0 and AP75 of 37.8.
- **Box detection.** The same model reaches 38.2 box AP on test-dev, so the mask branch does not reduce detection accuracy.
- **RoIAlign effect.** In the paper's ablation with a ResNet-50 C4 backbone, mask AP rises from 26.9 with RoIPool to 30.3 with RoIAlign.
- **Speed.** The abstract reports running at 5 frames per second with the main configuration.

The abstract also states that the same framework produces top results in the COCO bounding-box and person-keypoint tracks, which the authors used to show that the design generalises beyond masks.

## Limitations

- **Not optimised for speed.** The authors state that the design is not optimised for speed and that better speed–accuracy trade-offs may exist. Two-stage detection is slower than single-stage designs.
- **Expensive variants.** The paper does not recommend its ResNet-101 C4 variant in practice, because it takes about 400 ms per image.
- **Failure cases.** The authors identify the scarcity of training data for some classes, such as truck, bus and train on the Cityscapes dataset, as a main challenge, and show a failure prediction in the paper's figures.
- **Mask resolution.** The mask is predicted at a small fixed resolution per RoI and then resized to the box. Fine structures and thin parts of objects are therefore represented coarsely.

## Connections

- The detection stage that Mask R-CNN extends is covered on [Object detection](../object-detection/index.md), where Faster R-CNN is one of the two-stage families.
- Semantic segmentation by a fully convolutional network, the contrast point for instance methods, is on the [FCN](fcn.md) page.
- Promptable segmentation, which does not need a detector, is on the [Segment Anything](segment-anything.md) page.

## References

### Seminal papers

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV, pp. 2980–2988. doi:[10.1109/ICCV.2017.322](https://doi.org/10.1109/ICCV.2017.322). Also available as [arXiv:1703.06870](https://arxiv.org/abs/1703.06870). — Adds a mask branch to Faster R-CNN, predicting a binary mask per class for each RoI, and introduces RoIAlign.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that Mask R-CNN extends with a mask branch.
- Lin, T.-Y., Maire, M., Belongie, S. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV, pp. 740–755. doi:[10.1007/978-3-319-10602-1_48](https://doi.org/10.1007/978-3-319-10602-1_48). Also available as [arXiv:1405.0312](https://arxiv.org/abs/1405.0312). — The benchmark with instance masks on which the paper's results are reported.
- Lin, T.-Y. et al. (2017). *Feature Pyramid Networks for Object Detection*. CVPR, pp. 936–944. doi:[10.1109/CVPR.2017.106](https://doi.org/10.1109/CVPR.2017.106). — The feature pyramid used in the paper's main ResNet-101-FPN configuration.
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). *Deep Residual Learning for Image Recognition*. CVPR, pp. 770–778. doi:[10.1109/CVPR.2016.90](https://doi.org/10.1109/CVPR.2016.90). — The residual networks (ResNet-50 and ResNet-101) whose backbones the paper evaluates.

### Surveys and textbooks

- Minaee, S., Boykov, Y., Porikli, F. et al. (2021). Image Segmentation Using Deep Learning: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. doi:[10.1109/TPAMI.2021.3059968](https://doi.org/10.1109/TPAMI.2021.3059968). — Survey of deep-learning methods for image segmentation, for readers who want the wider landscape.
