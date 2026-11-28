---
status: draft
last_reviewed: 2026-11-28
tags:
  - computer vision
  - object detection
aliases:
  - YOLO
  - You Only Look Once
  - 你只看一次
---

# YOLO (You Only Look Once)

YOLO is a one-stage object detector that predicts boxes and class probabilities for the whole image in a single pass of one network. It treats detection as one regression problem rather than as a classification run over many proposals (Redmon et al., 2016).[^yolo] Its speed made real-time detection practical, and the family has continued through later versions.

This page is part of [Object Detection](index.md).

## Overview

Earlier detectors ran a classifier many times, once per proposal, and then combined the results. Those pipelines were accurate but slow, and their stages were trained separately. YOLO removes the proposal stage: one convolutional network looks at the image once and outputs all the boxes and classes together.

The price is a coarser view of the image. Each object is assigned by its centre to one grid cell, although its predicted box can extend beyond that cell. The limited predictions per cell make crowds of small objects difficult.[^yolo]

## Key concepts

- **Grid cell**: the image is split into an S × S grid. The cell that contains an object's centre is responsible for predicting that object.
- **Box predictor**: each cell predicts B boxes. Each box has five numbers: the centre x and y, the width and height, and a confidence score.
- **Class probabilities**: each cell also predicts C class probabilities, shared by its B boxes.
- **Responsible predictor**: within a cell, the box with the highest overlap with the ground-truth object.

## How it works

For PASCAL VOC the paper uses S = 7, B = 2 and C = 20, so the network outputs a 7 × 7 × 30 tensor (7 × 7 × (B × 5 + C)). Training uses a sum-squared error with several parts. The error on box centres and on the square roots of box sizes is weighted by λcoord = 5, so that localisation matters. The confidence error for box predictors not responsible for an object is down-weighted by λnoobj = 0.5, because most cells contain no object. Class errors are counted only in cells that do contain an object.[^yolo]

The paper takes square roots of the width and height so that an error on a small box costs more than the same error on a large one.[^yolo]

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **Faster R-CNN**: the two-stage alternative that generates proposals first ([Faster R-CNN](faster-r-cnn.md)).
- **DETR**: a one-stage design that predicts a fixed set of objects with transformers ([DETR](detr.md)).
- **RetinaNet**: a one-stage detector that addresses class imbalance with a new loss ([RetinaNet](retinanet.md)).

## Results

On PASCAL VOC 2007 test, with training on VOC 2007+2012 trainval, the paper reports **63.4%** mAP at **45 frames per second** for YOLO, and **52.7%** mAP at **155 fps** for a smaller version, Fast YOLO. In the same table Fast R-CNN reaches 70.0% mAP but runs at about 0.5 fps. YOLO's speed was measured on a Titan X GPU without batching; the table is a comparison of published systems rather than a controlled same-hardware benchmark.[^yolo]

The error analysis examines the top N detections per class, where N is the number of ground-truth objects of that class, then averages across the 20 classes. Localisation errors account for 19.0% of those detections for YOLO, against 8.6% for Fast R-CNN; background false positives account for 4.75% against 13.6%. These percentages use all top-N detections as the denominator, including correct ones, rather than only errors.[^yolo]

The later YOLOv3 report (Redmon and Farhadi, 2018) gives **28.2 COCO AP** (averaged over IoU thresholds 0.50–0.95) for its 320-pixel model, which it says runs in 22 ms. This is a different benchmark and metric from the VOC scores above. Its Figure 1 compares that result with SSD321 at 28.0 AP and 61 ms; the authors describe this as about three times faster, using timings from M40 or Titan X GPUs rather than a single matched hardware setup.[^yolov3]

## Limitations

The original YOLO paper lists its own weaknesses; these apply to the original model described here, not automatically to later versions:[^yolo]

- Each cell predicts only two boxes and one class, which limits how many nearby objects can be found. The paper gives groups of small objects, such as a flock of birds, as an example.
- The model generalises poorly to objects with unusual shapes or aspect ratios.
- Several downsampling layers leave the features used for box prediction coarse.
- The main source of error is incorrect localisation.

The YOLOv3 report describes a series of smaller design changes made to the family, which improved accuracy while keeping it fast. YOLO9000 (Redmon and Farhadi, 2017) extends the same line with joint training on detection and classification data.[^yolo9000]

## Connections

YOLO is the one-stage counterpart of the two-stage line in the [Object Detection](index.md) overview. Its backbone is a convolutional network, as described on the [Convolutional Networks](../../cnn/index.md) page. The brain connection is indirect: like the rest of the detection literature, YOLO is judged on boxes and labels, not on neural responses.

## References

### Seminal papers

[^yolo]: Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. CVPR, pp. 779–788. doi:[10.1109/CVPR.2016.91](https://doi.org/10.1109/CVPR.2016.91) (preprint: https://arxiv.org/abs/1506.02640) — The original YOLO paper, with the grid design, the loss and the PASCAL VOC speed and accuracy results used above.

[^yolo9000]: Redmon, J. & Farhadi, A. (2017). *YOLO9000: Better, Faster, Stronger*. CVPR, pp. 6517–6525. doi:[10.1109/CVPR.2017.690](https://doi.org/10.1109/CVPR.2017.690) (preprint: https://arxiv.org/abs/1612.08242) — The second version, with batch normalisation, anchor boxes and joint training on detection and classification data.

[^yolov3]: Redmon, J. & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv. https://arxiv.org/abs/1804.02767 — The third version, with COCO AP, AP50, and speed comparisons against SSD and RetinaNet.

- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — Another one-stage detector that predicts boxes on several feature maps, the comparison point for YOLOv3.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage system that YOLO's speed is measured against.

### Surveys and benchmarks

- Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. & Zisserman, A. (2010). The Pascal Visual Object Classes (VOC) challenge. *International Journal of Computer Vision*, 88, 303–338. doi:[10.1007/s11263-009-0275-4](https://doi.org/10.1007/s11263-009-0275-4) — The VOC benchmark and evaluation protocol on which the YOLO results are reported.
