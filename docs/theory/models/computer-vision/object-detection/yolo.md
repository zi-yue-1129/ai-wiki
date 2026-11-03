---
status: draft
last_reviewed: 2026-11-03
tags:
  - computer vision
  - object detection
aliases:
  - YOLO
  - You Only Look Once
  - 你只看一次
---

# YOLO (You Only Look Once)

YOLO is a one-stage object detector that predicts boxes and class probabilities for the whole image in a single pass of one network. It treats detection as one regression problem rather than as a classification run over many proposals (Redmon et al., 2015). Its speed made real-time detection practical, and the family has continued through later versions.

This page is part of [Object Detection](index.md).

## Overview

Earlier detectors ran a classifier many times, once per proposal, and then combined the results. Those pipelines were accurate but slow, and their stages were trained separately. YOLO removes the proposal stage: one convolutional network looks at the image once and outputs all the boxes and classes together.

The price is a coarser view of the image. Each prediction must cover a fixed grid cell, which limits how well the model handles crowds of small objects.

## Key concepts

- **Grid cell**: the image is split into an S × S grid. The cell that contains an object's centre is responsible for predicting that object.
- **Box predictor**: each cell predicts B boxes. Each box has five numbers: the centre x and y, the width and height, and a confidence score.
- **Class probabilities**: each cell also predicts C class probabilities, shared by its B boxes.
- **Responsible predictor**: within a cell, the box with the highest overlap with the ground-truth object.

## How it works

For PASCAL VOC the paper uses S = 7, B = 2 and C = 20, so the network outputs a 7 × 7 × 30 tensor (7 × 7 × (B × 5 + C)). Training uses a sum-squared error with several parts. The error on box centres and on the square roots of box sizes is weighted by λcoord = 5, so that localisation matters. The confidence error for empty cells is down-weighted by λnoobj = 0.5, because most cells contain no object. Class errors are counted only in cells that do contain an object.

The paper takes square roots of the width and height so that an error on a small box costs more than the same error on a large one.

## Key methods

This page is the detail for one of the landmark methods in the [Object Detection](index.md) overview. Its closest relatives are:

- **Faster R-CNN**: the two-stage alternative that generates proposals first ([Faster R-CNN](faster-r-cnn.md)).
- **DETR**: a one-stage design that predicts a fixed set of objects with transformers ([DETR](detr.md)).
- **RetinaNet**: a one-stage detector that addresses class imbalance with a new loss ([RetinaNet](retinanet.md)).

## Results

On PASCAL VOC 2007, the paper reports **63.4%** mAP at **45 frames per second** for YOLO, and **52.7%** mAP at **155 fps** for a smaller version, Fast YOLO. In the same table Fast R-CNN reaches 70.0% mAP but runs at about 0.5 fps. The paper's error analysis reports that 19.0% of YOLO's errors are localisation errors, against 8.6% for Fast R-CNN, while YOLO makes fewer background false positives (4.75% against 13.6%).

The later YOLOv3 report (Redmon and Farhadi, 2018) gives 28.2 mAP for its 320-pixel model, which it says runs in 22 ms. The authors state that this matches SSD's accuracy at about three times the speed.

## Limitations

The paper lists its own weaknesses:

- Each cell predicts only two boxes and one class, which limits how many nearby objects can be found. The paper gives groups of small objects, such as a flock of birds, as an example.
- The model generalises poorly to objects with unusual shapes or aspect ratios.
- Several downsampling layers leave the features used for box prediction coarse.
- The main source of error is incorrect localisation.

The YOLOv3 report describes a series of smaller design changes made to the family, which improved accuracy while keeping it fast.

## Connections

YOLO is the one-stage counterpart of the two-stage line in the [Object Detection](index.md) overview. Its backbone is a convolutional network, as described on the [Convolutional Networks](../../cnn/index.md) page. The brain connection is indirect: like the rest of the detection literature, YOLO is judged on boxes and labels, not on neural responses.

## References

### Seminal papers

- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2015). *You Only Look Once: Unified, Real-Time Object Detection*. arXiv. https://arxiv.org/abs/1506.02640 — The original YOLO paper, with the grid design, the loss and the PASCAL VOC speed and accuracy results used above.
- Redmon, J. & Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv. https://arxiv.org/abs/1804.02767 — The third version, with its speed and AP50 comparison against SSD and RetinaNet.
- Liu, W., Anguelov, D., Erhan, D., Szegedy, C., Reed, S., Fu, C.-Y. & Berg, A. C. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — Another one-stage detector that predicts boxes on several feature maps, the comparison point for YOLOv3.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage system that YOLO's speed is measured against.

### Surveys and benchmarks

- Everingham, M., Van Gool, L., Williams, C. K. I., Winn, J. & Zisserman, A. (2010). The Pascal Visual Object Classes (VOC) challenge. *International Journal of Computer Vision*, 88(2), 303–338. https://ora.ox.ac.uk/objects/uuid:8e9c1a89-e97d-4ca5-8581-a97a8cbb9f0a — The VOC benchmark and evaluation protocol on which the YOLO results are reported. The Oxford repository record confirms the title, authors, journal and volume.
