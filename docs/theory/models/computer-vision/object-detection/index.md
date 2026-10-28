---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/evaluation/metrics/segmentation/iou.md
tags:
  - computer vision
  - object detection
aliases:
  - Object detection
  - 物件偵測
  - 目標檢測
  - R-CNN
  - YOLO
  - DETR
---

# Object Detection

Object detection finds every instance of a set of object classes in an image and returns, for each one, a bounding box and a class label. It is harder than image classification, which gives one label for the whole image, and it is a precondition for most practical vision systems, from driver assistance to factory inspection.

## Overview

A detector must answer two questions at once: *what* is in the image, and *where* it is. The output is a variable-length list of boxes, each with a class and a confidence score. The number of objects is not known in advance, and the same object can be proposed many times by neighbouring predictions. Those two facts shaped most of the designs below.

Detection is evaluated with average precision (AP) per class and its mean over classes (mAP). A predicted box counts as correct when its overlap with a ground-truth box, measured by [intersection over union (IoU)](../../../evaluation/metrics/segmentation/iou.md), exceeds a threshold. The COCO benchmark averages AP over several IoU thresholds, which rewards precise localisation as well as correct classes (Lin et al., 2014).

## Key concepts

- **Bounding box**: a rectangle, usually given as centre, width and height, or as two corners.
- **Anchor or default box**: a set of reference boxes of fixed shapes placed at each feature-map location. The network predicts offsets from them.
- **Non-maximum suppression (NMS)**: a post-processing step that keeps the highest-scoring box among overlapping detections of the same class.
- **Feature pyramid**: features taken from several resolutions, so that small and large objects are both handled.
- **Assignment**: the rule that decides which predictions are trained to match which ground-truth objects.

## How it works

Most detectors share a pipeline. A convolutional or transformer backbone extracts features. A head predicts, at each candidate location, a class score and a box refinement. Training matches predictions to ground-truth objects, and inference removes duplicates. The families differ in how candidates are generated and how duplicates are removed.

**Two-stage detectors.** R-CNN (Girshick et al., 2013) ran a CNN on region proposals from a separate proposal method and reported a relative gain of more than 30% in mAP on PASCAL VOC 2012 over the previous best. Fast R-CNN (Girshick, 2015) computed the convolutional features once per image and pooled them for each proposal. It trained the VGG16 network nine times faster than R-CNN, according to the paper. Faster R-CNN (Ren et al., 2015) replaced the external proposal method with a region proposal network that shares its convolutional features with the detector, so the whole system trains end to end.

**One-stage detectors.** YOLO (Redmon et al., 2015) treats detection as a single regression from the image to boxes and classes. Its base model processed images at 45 frames per second, according to the paper. SSD (Liu et al., 2015) predicts scores and offsets for a fixed set of default boxes on several feature maps at once, and reports comparable accuracy to proposal-based methods at much higher speed. RetinaNet (Lin et al., 2017) addresses the extreme imbalance between foreground and background examples in dense detectors. It introduces the focal loss, which down-weights well-classified examples so that training is not dominated by easy background locations.

**Set prediction.** DETR (Carion et al., 2020) uses a transformer encoder and decoder to output a fixed set of object predictions directly. A bipartite matching between predictions and ground truth gives a one-to-one assignment during training. The paper reports that this removes the need for anchors and for non-maximum suppression.

## Key methods

Brief comparison. Each named detector is a candidate for its own method page; those pages are not yet written, so the detail is given in this section for now.

- **R-CNN family (two-stage)**: proposals first, then per-region classification and refinement. Accurate, historically slower at inference.
- **YOLO and SSD (one-stage)**: dense prediction in one pass. Faster, with a historical accuracy gap that focal loss and later designs narrowed.
- **RetinaNet (one-stage with focal loss)**: a dense detector whose loss is reweighted for class imbalance.
- **DETR (set prediction)**: transformer decoder with bipartite matching, no anchors and no NMS.

## Connections

Object detection builds on the convolutional features described in the [Convolutional Networks](../../cnn/index.md) and [U-Net](../../cnn/unet/index.md) pages. The DETR family connects to the [Transformer](../../transformer/index.md) architecture. The task overview is on the [Computer Vision](../index.md) page.

The brain connection is indirect. Detection benchmarks measure boxes and labels, not neural responses, so they do not show whether a detector matches how the brain localises objects. Comparisons between object-recognition networks and neural data are discussed in [NeuroAI](../../../../brain-mind/neuroai/index.md).

## Applications

- **Autonomous driving.** Detecting vehicles, pedestrians and traffic signs is one of the main perception tasks. See [Autonomous Driving](../../../../applications/autonomous-driving/index.md).
- **Medical imaging.** Localising lesions or organs in scans. See [Healthcare](../../../../applications/healthcare/index.md).
- **Industrial inspection.** Finding defects or parts on production lines. See [Manufacturing](../../../../applications/manufacturing/index.md).

## Open questions

- Small objects and crowded scenes still have lower accuracy than large, isolated objects.
- Long-tailed class distributions make rare classes hard to learn, which is the problem the focal loss was designed for.
- Open-vocabulary detection, which finds objects described in text rather than from a fixed label set, is an active area with different trade-offs from closed-set detectors.
- Speed and accuracy must be balanced on the hardware where a model is deployed, and benchmark results do not always transfer.

## References

### Seminal papers

- Girshick, R., Donahue, J., Darrell, T. & Malik, J. (2013). *Rich feature hierarchies for accurate object detection and semantic segmentation*. arXiv. https://arxiv.org/abs/1311.2524 — Introduces R-CNN: region proposals followed by CNN features, with the relative mAP gain on PASCAL VOC 2012 reported in the abstract.
- Girshick, R. (2015). *Fast R-CNN*. arXiv. https://arxiv.org/abs/1504.08083 — Shares convolutional computation across proposals with RoI pooling, and reports a nine-fold training speedup over R-CNN for VGG16.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — Adds a region proposal network that shares features with the detector, making proposal generation part of the trainable network.
- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2015). *You Only Look Once: Unified, Real-Time Object Detection*. arXiv. https://arxiv.org/abs/1506.02640 — Frames detection as one regression problem, reporting 45 frames per second for the base model.
- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — Predicts scores and offsets for default boxes on several feature maps in one pass.
- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection*. arXiv. https://arxiv.org/abs/1708.02002 — Introduces the focal loss for the class imbalance of dense one-stage detectors.
- Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A. & Zagoruyko, S. (2020). *End-to-End Object Detection with Transformers*. arXiv. https://arxiv.org/abs/2005.12872 — Introduces DETR, which predicts a set of objects with bipartite matching and no anchors or NMS.

### Surveys and benchmarks

- Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. & Zisserman, A. (2010). The Pascal Visual Object Classes (VOC) challenge. *International Journal of Computer Vision*, 88(2), 303–338. https://ora.ox.ac.uk/objects/uuid:8e9c1a89-e97d-4ca5-8581-a97a8cbb9f0a — The VOC benchmark and its evaluation protocol, used by the early detectors above. The Oxford repository record confirms the title, authors, journal and volume; its year field reads 2009, the online date.
- Lin, T.-Y., Maire, M., Belongie, S., Bourdev, L., Girshick, R., Hays, J., Perona, P., Ramanan, D., Zitnick, C. L. & Dollár, P. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — The COCO dataset and the AP metric averaged over IoU thresholds.
