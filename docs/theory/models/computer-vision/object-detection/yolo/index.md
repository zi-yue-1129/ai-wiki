---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/autonomous-driving
  - brain-mind/visual-perception
tags:
  - computer vision
  - efficient inference
  - benchmarks
aliases:
  - YOLO
  - You Only Look Once
  - 只看一次
---

# YOLO

YOLO (You Only Look Once) is a one-stage object detector that frames detection as a single regression problem. One convolutional network looks at the whole image once and predicts the bounding boxes, their confidences and the class probabilities together. Because there is no separate proposal stage, the system runs in real time. It is one of the methods named on the [Object Detection](../index.md) page.

## Overview

Earlier detectors built the task out of parts. Sliding-window systems scored many crops with a classifier, and the R-CNN family ran a classifier on proposals from a separate method. The YOLO paper argues that prior work repurposes classifiers for detection. Its alternative is one network that maps pixels straight to boxes and class probabilities, and that can be optimised end to end on detection performance.[^1] The base model runs at 45 frames per second on the paper's benchmark and Fast YOLO at 155; the price is lower accuracy on small objects and precise localisation.

## Key concepts

- **Grid.** The image is divided into an S×S grid, with S = 7 in the paper. The cell that contains an object's centre is responsible for detecting it.
- **Boxes and confidence.** Each cell predicts B = 2 boxes. Each has a centre relative to the cell, a width and height relative to the image, and a confidence: the probability of an object times the IoU between the predicted and true boxes.
- **Class probabilities.** Each cell predicts one set of conditional class probabilities for C = 20 PASCAL VOC classes, shared by its two boxes.
- **Output tensor.** S × S × (B·5 + C), which is 7 × 7 × 30 for VOC.

## How it works

The network has 24 convolutional layers, inspired by the GoogLeNet classifier, followed by fully connected layers. Training optimises one sum-squared error over the grid:

$$
\begin{aligned}
\mathcal{L} = &\; \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} \left[(x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2\right] \\
&+ \lambda_{\text{coord}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} \left[(\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2\right] \\
&+ \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{obj}}_{ij} (C_i - \hat{C}_i)^2 + \lambda_{\text{noobj}} \sum_{i=0}^{S^2} \sum_{j=0}^{B} \mathbb{1}^{\text{noobj}}_{ij} (C_i - \hat{C}_i)^2 \\
&+ \sum_{i=0}^{S^2} \mathbb{1}^{\text{obj}}_{i} \sum_{c \in \text{classes}} (p_i(c) - \hat{p}_i(c))^2
\end{aligned}
$$

Here \(\mathbb{1}^{\text{obj}}_{ij}\) is 1 when box \(j\) of cell \(i\) is responsible for an object, and \(\mathbb{1}^{\text{noobj}}_{ij}\) is its complement. The weights are \(\lambda_{\text{coord}} = 5\) and \(\lambda_{\text{noobj}} = 0.5\). The square roots in the size terms reduce the penalty on large boxes, so a given error matters more for a small box. The \(\lambda_{\text{noobj}}\) weight stops the many empty cells from overwhelming the confidence term.[^2]

At test time, each box's class-specific score is its class probability times its box confidence. Non-maximum suppression then removes duplicates, which the paper reports adds 2–3% to mAP.[^2]

## Results

On PASCAL VOC 2007, trained on the 2007 and 2012 trainval sets, YOLO reaches 63.4% mAP at 45 frames per second, and Fast YOLO reaches 52.7% at 155 frames per second. The paper's comparison table places these against other detectors.[^3]

| Detector (VOC 2007 test) | mAP | Speed |
|---|---|---|
| 30Hz DPM | 26.1 | 30 fps |
| Fast YOLO | 52.7 | 155 fps |
| YOLO | 63.4 | 45 fps |
| Fast R-CNN | 70.0 | 0.5 fps |
| Faster R-CNN, VGG-16 | 73.2 | 7 fps |

On VOC 2012 test, YOLO reaches 57.9% mAP, slightly below R-CNN with VGG-16 at 59.2% in the paper's table.[^3]

The error analysis is one of the paper's clearest results. YOLO makes more localisation errors than Fast R-CNN but far fewer background false positives, which are detections on regions with no object. Using YOLO to re-score Fast R-CNN's detections raises mAP from 71.8% to 75.0%. YOLO, trained on natural images, also generalises better than DPM and R-CNN to artwork in the Picasso and People-Art datasets.[^1]

## Limitations

- **Localisation.** Most of YOLO's mistakes are in localisation, not classification.[^3]
- **Spatial constraints.** Each cell predicts only two boxes and one set of class probabilities, so small or closely packed objects are hard to detect.[^1]
- **Small objects.** On VOC 2012, YOLO struggles with small objects compared with its closest competitors.[^3]

## Open questions

- **Design after the first version.** YOLO9000, the second version, improved the model and also learned from classification data. The later YOLOv4 and YOLOX papers re-examined the architecture and training recipe. The original paper does not address these changes.[^4]
- **Speed and accuracy.** Whether a single-pass model can match two-stage detectors on small objects without losing speed is the main question for this family.

## Connections

- **Generalisation.** The artwork experiment asks whether a detector trained on natural photographs still works on images with different statistics. [Geirhos et al. (2019)](../../../../../brain-mind/visual-perception/geirhos-2019/index.md) asks the same kind of question about how humans and CNNs weigh shape and texture.
- **Two-stage contrast.** The grid replaces the proposal step of [Faster R-CNN](../faster-rcnn/index.md), which also uses a CNN backbone but adds a learned proposal stage before classification.

## Applications

Real-time detection matters where a system must react to a moving scene: traffic and pedestrian monitoring in [autonomous driving](../../../../../applications/autonomous-driving/index.md), video surveillance, and robotics that must track objects while it moves.

[^1]: Redmon et al. (2015), abstract: the detector is a single network that can be optimised end to end, and its generalisation from natural images to artwork is compared with DPM and R-CNN.
[^2]: Redmon et al. (2015), Section 2: the grid, the confidence definition, and the sum-squared loss with λ_coord = 5 and λ_noobj = 0.5. The statement about NMS is in the same section.
[^3]: Redmon et al. (2015), Tables 1 and 3 and Section 4: the VOC 2007 and 2012 results, the speed comparison and the error analysis. The Faster R-CNN and Fast R-CNN figures are as tabulated in that paper.
[^4]: Redmon and Farhadi (2016), abstract; Bochkovskiy et al. (2020), abstract; Ge et al. (2021), abstract.

## References

### Seminal papers

- Redmon, J., Divvala, S., Girshick, R. & Farhadi, A. (2015). *You Only Look Once: Unified, Real-Time Object Detection*. arXiv. https://arxiv.org/abs/1506.02640 — The original YOLO paper, which frames detection as a single regression over a grid and reports results on VOC 2007 and 2012.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that YOLO's speed and accuracy are compared with in the paper.
- Liu, W., et al. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — A contemporary one-stage detector that predicts from multiple feature maps with default boxes.
- Redmon, J. & Farhadi, A. (2016). *YOLO9000: Better, Faster, Stronger*. arXiv. https://arxiv.org/abs/1612.08242 — The second version of YOLO, which adds improvements to the design and joint training on detection and classification data.

### Surveys and textbooks

- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — A survey that places the one-stage and two-stage families in the history of detection.

### Articles and documentation

- Bochkovskiy, A., Wang, C.-Y. & Liao, H.-Y. M. (2020). *YOLOv4: Optimal Speed and Accuracy of Object Detection*. arXiv. https://arxiv.org/abs/2004.10934 — Combines many published CNN techniques into a YOLO detector tuned for speed and accuracy on a single GPU.
- Ge, Z., Liu, S., Wang, F., Li, Z. & Sun, J. (2021). *YOLOX: Exceeding YOLO Series in 2021*. arXiv. https://arxiv.org/abs/2107.08430 — Moves the YOLO design to an anchor-free form with a decoupled head and a new label-assignment strategy.
