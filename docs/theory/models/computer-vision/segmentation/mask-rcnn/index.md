---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/autonomous-driving
  - theory/models/cnn/backbones-and-scaling
tags:
  - computer vision
  - benchmarks
  - architecture
aliases:
  - Mask R-CNN
  - 遮罩 R-CNN
  - Mask RCNN
---

# Mask R-CNN

Mask R-CNN is an instance segmentation method. It extends the [Faster R-CNN](../../object-detection/faster-rcnn/index.md) detector with a branch that predicts a binary mask for each detected object, in parallel with the box and class predictions. A new operation, RoIAlign, keeps the features aligned with the pixels they describe. It is one of the four landmark methods on the [Image Segmentation](../index.md) page.

## Overview

Instance segmentation asks for each object's class, its box and its exact pixels. Earlier instance methods usually started from per-pixel classification and then cut same-class pixels into separate instances. Mask R-CNN takes the opposite route. It first detects each object, then predicts a mask inside each detection. The paper describes a simple, flexible framework that adds little overhead to Faster R-CNN, running at 5 frames per second.[^1]

Faster R-CNN was not built for pixel-accurate alignment: its RoIPool operation quantises region coordinates. RoIAlign removes this quantisation.

## Key concepts

- **Instance-first strategy**: detect the object, then segment it within its box.
- **RoIAlign**: pools each region by bilinear interpolation at exact, fractional sample points, without rounding the region's coordinates.
- **Decoupled masks**: the mask head predicts one binary mask per class, with a per-pixel sigmoid. The class is chosen by the classification branch, so masks do not compete with one another.
- **Multi-task training**: the box, class and mask losses are optimised jointly on sampled regions of interest (RoIs).

## How it works

The first stage is the region proposal network of Faster R-CNN, which proposes candidate boxes from shared convolutional features. For each proposal, RoIAlign extracts a fixed-size feature map. Two heads then run in parallel: a fully connected head predicts the class and refines the box, and a small fully convolutional mask head predicts a \(28\times28\) mask for each of the \(K\) classes.

During training, each sampled RoI contributes the loss

$$
\mathcal{L} = \mathcal{L}_{cls} + \mathcal{L}_{box} + \mathcal{L}_{mask}
$$

where the classification and box losses are those of Fast R-CNN. The mask loss is the average binary cross-entropy of the per-pixel sigmoids, and it is computed only on the mask of the ground-truth class \(k\). At inference, the mask of the predicted class is resized to the box and binarised at a threshold of 0.5.

## Results

On the COCO benchmark, the paper reports a mask average precision (AP) of 35.7 on the test-development split with a 101-layer residual backbone and a feature pyramid, and 37.1 with a stronger backbone of the same family. These single-model results surpass the winners of the COCO 2015 and 2016 segmentation challenges.[^2]

The ablations on the validation split show the effect of each design choice:

- **RoIAlign** instead of RoIPool improves mask AP by 7.3 points and mask AP at IoU 0.75 by 10.5 points, in the 50-layer residual setting with a stride-32 backbone.
- **Independent per-pixel sigmoids** instead of a per-pixel softmax, as used in FCN, improve mask AP by 5.5 points, a gap the paper attributes to decoupling mask and class prediction.
- **Class-agnostic masks**, one mask shared across classes, reach 29.7 mask AP against 30.3 for class-specific masks, which fits the division of labour in which the box branch does the classification.

## Limitations

- **Two stages.** The mask branch runs on top of a detector, so the method is slower than a single-stage design, and it depends on detection quality. A missed or misplaced box cannot be recovered by the mask.
- **Coarse masks.** A 28×28 mask is stretched over the box, which limits the sharpness of the boundary, especially for large objects.
- **Annotation cost.** Training needs a label and a polygon or mask for every object in the training set.

## Open questions

- Can a one-stage or query-based design match the accuracy of the two-stage pipeline at lower cost? Mask2Former, described on the [Image Segmentation](../index.md) page, is one answer in the broader panoptic setting.
- How far can mask resolution rise without losing speed?

[^1]: He et al. (2017), abstract: Mask R-CNN extends Faster R-CNN with a mask branch and runs at 5 fps.
[^2]: He et al. (2017), Table 1: mask AP is reported on COCO test-dev, while the ablations in Table 2 are on the minival split of the validation set.

## References

### Seminal papers

- He, K., Gkioxari, G., Dollár, P. & Girshick, R. (2017). *Mask R-CNN*. ICCV. https://arxiv.org/abs/1703.06870 — The paper itself: adds a mask branch and RoIAlign to Faster R-CNN for instance segmentation.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The detector that Mask R-CNN extends, with a region proposal network that shares features.
- Lin, T.-Y., et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://arxiv.org/abs/1405.0312 — The COCO dataset and benchmark on which the instance segmentation results are reported.
- Kirillov, A., He, K., Girshick, R., Rother, C. & Dollár, P. (2019). *Panoptic Segmentation*. CVPR. https://arxiv.org/abs/1801.00868 — Combines instance masks with stuff classes in a single panoptic task.
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — Shares convolutional computation across region proposals, and defines the box and class losses used here.
- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR. https://arxiv.org/abs/1411.4038 — The fully convolutional segmenter that the per-pixel softmax of this comparison comes from.
- Cheng, B., Misra, I., Schwing, A. G., Kirillov, A. & Girdhar, R. (2022). *Masked-attention Mask Transformer for Universal Image Segmentation*. CVPR. https://arxiv.org/abs/2112.01527 — A later query-based architecture that handles instance, panoptic and semantic segmentation.

### Surveys and textbooks

- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — Covers instance segmentation methods of the Mask R-CNN family within a broader review.
