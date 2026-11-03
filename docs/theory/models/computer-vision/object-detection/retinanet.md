---
status: draft
last_reviewed: 2026-11-03
tags:
  - computer vision
  - object detection
aliases:
  - RetinaNet
  - Focal loss
  - 焦點損失
  - 視網膜網路
---

# RetinaNet and the Focal Loss

RetinaNet is a one-stage object detector that reaches the accuracy of two-stage detectors. Its main contribution is the **focal loss**, a change to the classification loss that stops the many easy background examples from dominating training (Lin et al., 2017).

This page is part of [Object Detection](index.md).

## Overview

One-stage detectors such as YOLO and SSD are fast, but for several years they trailed the two-stage detectors in accuracy. The paper identifies the cause as extreme class imbalance. A dense one-stage detector evaluates tens of thousands of candidate locations per image, and nearly all of them are easy background. Their many small losses add up and overwhelm the few informative examples that contain objects.

Earlier fixes, such as hard example mining and class-balanced cross-entropy, either discarded examples or did not separate easy from hard ones. The focal loss reweights every example by how confident the model already is.

## Key concepts

- **Cross-entropy loss**: the standard classification loss, which penalises a wrong prediction in proportion to its size.
- **Modulating factor**: the term (1 − p_t)^γ, which is small when the model already predicts the true class with high confidence.
- **Focusing parameter γ**: controls how strongly easy examples are down-weighted.
- **Class weight α**: balances the two classes, positive and negative.

## How it works

The focal loss is

FL(p_t) = −α_t (1 − p_t)^γ log(p_t),

where p_t is the model's probability for the true class. When γ = 0 it reduces to the weighted cross-entropy. The paper reports that **γ = 2 with α = 0.25** works best in its ablation, giving 34.0 AP on the minival split with a ResNet-50-FPN backbone at 600 pixels. Compared with the α-balanced cross-entropy baseline, which reaches 31.1 AP in the same ablation, the focal loss adds 2.9 AP. The authors note that α and γ must be chosen together.

The architecture is a ResNet backbone with a Feature Pyramid Network (FPN; Lin et al., 2017a) that produces features at five levels, P3 to P7. At each location there are **nine anchors**: three aspect ratios (1:2, 1:1 and 2:1) and three scales. Two small subnetworks sit on every level. One predicts a class score for each anchor and class. The other predicts four box offsets for each anchor. The two subnetworks do not share parameters. Its classification output starts from a prior that gives a foreground probability of 0.01. The paper reports that training diverged without this initialisation.

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **YOLO and SSD**: one-stage detectors that use the ordinary cross-entropy loss ([YOLO](yolo.md)).
- **Faster R-CNN**: the two-stage approach that RetinaNet matches in accuracy ([Faster R-CNN](faster-r-cnn.md)).
- **DETR**: a one-stage design without anchors or non-maximum suppression ([DETR](detr.md)).

## Results

On COCO test-dev, the paper reports **34.4 AP** for RetinaNet-101 at a 500-pixel scale and about 90 ms per image. At an 800-pixel scale it reports **37.8 AP** at about 198 ms. Its headline model, which uses scale jitter and trains for 1.5 times longer, reaches **39.1 AP**. That is 2.3 points above the best two-stage entry in its comparison table, a Faster R-CNN variant with 36.8 AP. The authors state that the 800-pixel model is above all two-stage approaches in their comparison, while the 500-pixel model is below the strongest two-stage entry.

## Limitations

The paper states these limits itself:

- The authors say that improving the high frame-rate regime "will likely require special network design", and treat it as beyond the scope of the work.
- The focal loss is tested only in its binary form. The authors describe the multi-class extension as straightforward but do not test it.
- The two hyperparameters, α and γ, are coupled and must be tuned together.
- The paper reports that an alternative hinge-style loss was unstable in early experiments.
- The authors note that a later variant of Faster R-CNN produced faster and more accurate results than RetinaNet's comparison models.

## Connections

RetinaNet reuses the feature pyramid design (Lin et al., 2016) and the anchor scheme used by the one-stage detectors in the [Object Detection](index.md) overview. The focal loss is a classification loss, so it is a more general idea than the detector: it applies wherever the training data is dominated by easy negatives.

## References

### Seminal papers

- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection*. arXiv. https://arxiv.org/abs/1708.02002 — Introduces the focal loss and the RetinaNet detector, with the γ and α ablation and the COCO results used above.
- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — The feature pyramid that RetinaNet uses for its P3 to P7 levels.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that the paper's accuracy comparison is made against.
- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — A one-stage detector that uses the ordinary classification loss, the contrast point for the focal loss.

### Surveys and benchmarks

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO benchmark and the AP metric in which all the RetinaNet results are reported.
