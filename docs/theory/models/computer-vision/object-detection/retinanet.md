---
status: draft
last_reviewed: 2026-11-14
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

RetinaNet is a one-stage object detector that reaches the accuracy of two-stage detectors. Its main contribution is the **focal loss**, a change to the classification loss that stops the many easy background examples from dominating training (Lin et al., 2017).[^focal]

This page is part of [Object Detection](index.md).

## Overview

One-stage detectors such as YOLO and SSD are fast, but for several years they trailed the two-stage detectors in accuracy. The paper identifies extreme foreground–background imbalance as a central obstacle. A dense one-stage detector evaluates tens of thousands of candidate locations per image, and nearly all of them are easy background. Their many small losses can overwhelm the informative examples.[^focal]

Earlier fixes, such as hard example mining and class-balanced cross-entropy, either discarded examples or did not separate easy from hard ones. The focal loss reweights every example by how confident the model already is.

## Key concepts

- **Cross-entropy loss**: the classification loss $-\log(p_t)$, where $p_t$ is the probability assigned to the true class.
- **Modulating factor**: the term $(1-p_t)^\gamma$, which is small when the model already predicts the true class with high confidence.
- **Focusing parameter $\gamma$**: controls how strongly easy examples are down-weighted.
- **Class weight $\alpha$**: balances the two classes, positive and negative.

## How it works

The focal loss is

$$
\operatorname{FL}(p_t)=-\alpha_t(1-p_t)^\gamma\log(p_t),
$$

where $p_t$ is the model's probability for the true binary label and $\alpha_t$ is $\alpha$ for a positive label or $1-\alpha$ for a negative label. When $\gamma=0$ it reduces to the weighted cross-entropy. The paper reports that **γ = 2 with α = 0.25** works best in its ablation, giving 34.0 AP on the minival split with a ResNet-50-FPN backbone at 600 pixels. Compared with the α-balanced cross-entropy baseline, which reaches 31.1 AP in the same ablation, the focal loss adds 2.9 AP. The authors tune $\alpha$ for each $\gamma$ in this comparison.[^focal]

The architecture is a ResNet backbone with a Feature Pyramid Network (FPN; Lin et al., 2017a) that produces features at five levels, P3 to P7. At each location there are **nine anchors**: three aspect ratios (1:2, 1:1 and 2:1) and three scales. Two small subnetworks sit on every level. One predicts a class score for each anchor and class. The other predicts four box offsets for each anchor. The two subnetworks do not share parameters with each other; each shares its own weights across pyramid levels. Classification uses independent sigmoid predictions with binary focal loss for each class. Its classification output starts from a foreground prior probability of 0.01. In the authors' standard-cross-entropy baseline, training diverged before this initialisation was added.[^focal]

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **YOLO and SSD**: earlier one-stage designs. Original [YOLO](yolo.md) uses sum-squared error; SSD uses a softmax confidence loss with hard-negative mining.
- **Faster R-CNN**: the two-stage approach that RetinaNet matches in accuracy ([Faster R-CNN](faster-r-cnn.md)).
- **DETR**: a one-stage design without anchors or non-maximum suppression ([DETR](detr.md)).

## Results

On COCO test-dev, the paper reports **34.4 AP** for RetinaNet-101 at a 500-pixel scale and about 90 ms per image. At an 800-pixel scale it reports **37.8 AP** at about 198 ms. Its ResNet-101-FPN model with scale jitter and 1.5 times longer training reaches **39.1 AP**. That is 2.3 points above the best two-stage entry in its comparison table, a Faster R-CNN variant with 36.8 AP. The authors state that the 800-pixel model is above all two-stage approaches in their comparison, while the 500-pixel model is below the strongest two-stage entry. Table 2 also reports 40.8 AP with a different, ResNeXt-101-FPN backbone. These comparisons use the paper's particular models and training schedules; they do not establish that one-stage detectors are always more accurate.[^focal]

## Limitations

The paper states these limits itself:[^focal]

- The authors say that improving the high frame-rate regime "will likely require special network design", and treat it as beyond the scope of the work.
- The two hyperparameters, $\alpha$ and $\gamma$, interact; the ablation selects $\alpha$ separately for each $\gamma$.
- The paper reports that an alternative hinge-style loss was unstable in early experiments.
- The authors note that a later variant of Faster R-CNN produced faster and more accurate results than RetinaNet's comparison models.

## Connections

RetinaNet reuses the feature pyramid design (Lin et al., 2016) and the anchor scheme used by the one-stage detectors in the [Object Detection](index.md) overview. The focal loss is a classification loss, so it is a more general idea than the detector: it can be useful in other settings dominated by easy negatives, but benefits must be evaluated for the task.

## References

### Seminal papers

[^focal]: Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection*. arXiv. https://arxiv.org/abs/1708.02002 — Introduces the focal loss and the RetinaNet detector, with the γ and α ablation and the COCO results used above.

- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — The feature pyramid that RetinaNet uses for its P3 to P7 levels.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that the paper's accuracy comparison is made against.
- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — A one-stage detector that uses the ordinary classification loss, the contrast point for the focal loss.

### Surveys and benchmarks

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO benchmark and the AP metric in which all the RetinaNet results are reported.
