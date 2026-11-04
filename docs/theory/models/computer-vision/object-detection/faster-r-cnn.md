---
status: draft
last_reviewed: 2026-11-03
tags:
  - computer vision
  - object detection
aliases:
  - Faster R-CNN
  - Region Proposal Network
  - RPN
  - 更快的 R-CNN
  - 區域提議網路
---

# Faster R-CNN

Faster R-CNN is a two-stage object detector that generates its own region proposals with a small network trained together with the detector. It was the first design in which the whole pipeline, from proposals to final boxes, could be trained end to end on shared convolutional features (Ren et al., 2015).

This page is part of [Object Detection](index.md).

## Overview

The R-CNN line of detectors (R-CNN, and Fast R-CNN that followed it) first produced candidate regions with a separate, hand-designed proposal method, and then classified each region with a network. Fast R-CNN (Girshick, 2015) computed convolutional features once per image and pooled them for each proposal, which made training and testing much faster. The proposal step, however, still ran outside the network, so it could not be trained together with the detector and remained a bottleneck.

Faster R-CNN replaces that external step with a **Region Proposal Network (RPN)** that reads the same convolutional feature map as the detector.

## Key concepts

- **Anchor**: a reference box of a fixed scale and aspect ratio, placed at each position of the feature map. The network predicts how to shift and resize each anchor.
- **Objectness**: the score that an anchor contains an object, as opposed to background.
- **Proposal**: a box that the RPN suggests as a likely object, passed on to the detector.
- **Shared features**: convolutional layers used by both the RPN and the detector, so that the second stage adds little cost.

## How it works

The RPN slides a small 3×3 window over the shared feature map. At each position, two sibling 1×1 convolutions predict an objectness score and box offsets for each of **k = 9** anchors. The anchors combine three scales (box areas of 128², 256² and 512² pixels) with three aspect ratios (1:1, 1:2 and 2:1). The RPN keeps the highest-scoring proposals, and the Fast R-CNN head classifies each one and refines its box.

Training is the hard part, because the two networks must agree on the shared layers. The paper trains them in alternating steps: the RPN first, then the detector using those proposals, then each network again with the shared convolutional layers held fixed. The paper also describes an approximate joint scheme that trains both at once, and reports that it cuts training time by about 25 to 50 percent compared with alternating training, while ignoring the gradient with respect to the proposal coordinates.

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **Fast R-CNN**: the same detector head with an external proposal method.
- **YOLO**: a one-stage design that skips proposals altogether ([YOLO](yolo.md)).
- **DETR**: a set-prediction design with no proposal stage ([DETR](detr.md)).

## Results

The paper reports PASCAL VOC mAP with a VGG-16 backbone. Trained on VOC 2007 and 2012 trainval, Faster R-CNN reaches **73.2%** mAP on the VOC 2007 test set and **70.4%** on the VOC 2012 test set. Adding COCO to the training data raises VOC 2007 test mAP to **78.8%**. Its timing table lists about **198 ms** per image on a K40 GPU, of which the RPN accounts for about 10 ms because it shares the convolutional features. The paper gives a frame rate of 5 fps (including all steps) for the VGG-16 system, and 17 fps for the smaller ZF backbone.

## Limitations

The paper itself lists several limits:

- The exact joint training that would propagate gradients through the proposal coordinates is left unsolved. The approximate version ignores them.
- Testing uses one image scale. The authors note that multi-scale testing may improve accuracy at a poor speed trade-off.
- The total stride of 16 pixels is coarse, and the authors expect a smaller stride to help.
- The anchor settings were not tuned for a particular dataset.

Later work addressed some of these. Feature pyramids build multi-scale features on top of this design (Lin et al., 2016), and set-prediction detectors remove the proposal and post-processing steps altogether ([DETR](detr.md)).

## Connections

Faster R-CNN is the standard two-stage baseline in the [Object Detection](index.md) overview. Its shared convolutional features come from the networks on the [Convolutional Networks](../../cnn/index.md) page. The regions it proposes are scored with the overlap measure described in [intersection over union](../../../evaluation/metrics/segmentation/iou.md).

## References

### Seminal papers

- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — Introduces the Region Proposal Network, its anchor design, and the shared-feature training scheme described above.
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — The detector head that Faster R-CNN keeps. The abstract reports 9× faster training and 213× faster testing than R-CNN for VGG16.
- Girshick, R., Donahue, J., Darrell, T. & Malik, J. (2013). *Rich feature hierarchies for accurate object detection and semantic segmentation*. arXiv. https://arxiv.org/abs/1311.2524 — The R-CNN pipeline that the two-stage line starts from, with an external proposal method.
- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — Builds multi-scale feature maps on top of a Faster R-CNN system, reporting state-of-the-art single-model COCO results at the time.

### Surveys and benchmarks

- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO dataset and the AP metric averaged over IoU thresholds, used for the COCO results above.
