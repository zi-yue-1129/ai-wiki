---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/models/cnn/backbones-and-scaling
tags:
  - computer vision
  - loss functions
  - benchmarks
aliases:
  - RetinaNet
  - Focal Loss
  - 焦點損失
  - Focal loss for dense object detection
---

# RetinaNet and Focal Loss

RetinaNet is a one-stage object detector with a feature pyramid backbone and dense predictions at every location. It was built to test one idea: that one-stage detectors had lagged behind two-stage detectors because of class imbalance during training, not because of the one-stage design itself. The fix is the focal loss, a reshaped cross-entropy that down-weights the many easy background examples. It is one of the methods named on the [Object Detection](../index.md) page.

## Overview

A one-stage detector evaluates a large number of candidate locations in one pass, and nearly all of them are background. The paper puts the number at between 10^4 and 10^5 candidate locations per image, of which only a few contain an object.[^1] Standard training treats all of these examples alike, so the easy background examples dominate the total loss and the gradient is spent on examples the detector already gets right. Two-stage detectors avoid this with a proposal stage and with minibatch sampling at a fixed ratio. The RetinaNet paper keeps the single-stage design and changes the loss.

## Key concepts

- **Cross-entropy.** The standard classification loss, \(-\log(p_t)\), where \(p_t\) is the predicted probability of the true class.
- **α-balancing.** A weight \(\alpha_t\) favouring the rare foreground class. It corrects the imbalance in counts, but not the imbalance in ease: easy examples still dominate.
- **Focal loss.** Cross-entropy multiplied by \((1 - p_t)^\gamma\), with a focusing parameter \(\gamma \geq 0\). Well-classified examples lose most of their loss, so training concentrates on hard examples.
- **Feature pyramid.** A [ResNet](../../../cnn/backbones-and-scaling/resnet/index.md) backbone with a feature pyramid network on top, giving maps from P3 to P7 (strides 8 to 128) for different object sizes.
- **Dense heads.** A classification subnet and a box regression subnet, small fully convolutional networks applied to every pyramid level. Each location has nine anchors: three scales and three aspect ratios.

## How it works

The focal loss for a single example is

$$
\text{FL}(p_t) = -\alpha_t (1 - p_t)^\gamma \log(p_t)
$$

With \(\gamma = 0\) and \(\alpha_t = 1\) it reduces to cross-entropy. At \(\gamma = 2\), an example with \(p_t = 0.9\) is down-weighted by a factor of 100, while one with \(p_t = 0.1\) keeps 81% of its loss. The default is \(\gamma = 2\) with \(\alpha = 0.25\). The paper reports that \(\alpha = 0.5\) is nearly as good, and that the best \(\alpha\) falls as \(\gamma\) rises.[^2]

The classification layer's bias is set so that the initial foreground probability is about 0.01. This keeps the many background examples from producing a large loss at the start of training. The paper calls it a change of initialisation, not of the loss.[^2]

At inference, the network keeps at most 1,000 top-scoring predictions per level, above a confidence of 0.05. The predictions from all levels are merged, and non-maximum suppression with a threshold of 0.5 gives the final detections.[^4]

## Results

The COCO ablations use models trained on the trainval35k split and tested on minival. With a ResNet-50 backbone, focal loss with \(\gamma = 2\) improves on the best α-balanced cross-entropy by 2.9 AP, which reaches at most 31.1 AP. The paper reports that the detector is relatively robust to \(\gamma\) between 0.5 and 5.[^2]

Against online hard example mining (OHEM), which selects the hardest examples in each minibatch, focal loss with a ResNet-101 backbone at 600 pixels reaches 36.0 AP, against 32.8 AP for the best OHEM variant.[^2]

On COCO test-dev, RetinaNet-101 at 800 pixels, trained with scale jitter for 1.5 times longer, reaches 39.1 AP. This is 5.9 AP above DSSD, the closest one-stage competitor in the paper's table, and 2.3 AP above the top Faster R-CNN model listed.[^3] The speed comparison puts the 800-pixel model at 198 ms per image on an M40 GPU. The paper states that larger input scales let RetinaNet surpass all two-stage approaches while still running faster than them.[^4]

## Limitations

- **Speed at high accuracy.** The strongest models are slower than the fastest one-stage detectors. High frame rates need a different network design, which the paper leaves to future work.[^4]
- **Interacting hyperparameters.** The focusing parameter and the balancing weight must be chosen together. The paper shows a stable range for α, not a universal setting.[^2]
- **Evidence base.** The results are on COCO with ResNet backbones, and the claim that focal loss explains the gap to two-stage detectors rests on these ablations.

## Open questions

- **Is the imbalance the whole story?** The paper attributes the gap mainly to class imbalance. Whether anchors or feature design account for the rest is not settled.
- **Other fixes for the same problem.** YOLOX uses a different label-assignment strategy, SimOTA, rather than reshaping the loss.[^5]
- **Beyond detection.** Whether focal loss transfers without tuning to other dense prediction problems is an open question.

## Connections

- **Loss functions.** Focal loss is a reshaped cross-entropy. The general treatment of [loss functions and optimisation](../../../../paradigms/supervised/loss-functions-and-optimization/index.md) gives the background.
- **Two-stage detectors.** [Faster R-CNN](../faster-rcnn/index.md) handles the same imbalance with a proposal stage and minibatch sampling. For one-stage detectors, focal loss is an alternative to that machinery.
- **Parent.** The [Object Detection](../index.md) page compares the dense one-stage family with the other families.

## Applications

Dense one-stage detectors suit settings where latency matters, such as video analysis and embedded systems. The choice between one-stage and two-stage designs depends on latency, data and hardware, and the applications listed on the [Object Detection](../index.md) page apply here too.

## References

### Seminal papers

- Lin, T.-Y., Goyal, P., Girshick, R., He, K. & Dollár, P. (2017). *Focal Loss for Dense Object Detection*. arXiv. https://arxiv.org/abs/1708.02002 — Introduces focal loss and the RetinaNet detector, which closes the accuracy gap between one-stage and two-stage detectors on COCO.
- Lin, T.-Y., Dollár, P., Girshick, R., He, K., Hariharan, B. & Belongie, S. (2016). *Feature Pyramid Networks for Object Detection*. arXiv. https://arxiv.org/abs/1612.03144 — The feature pyramid used as the RetinaNet backbone, with top-down connections for multi-scale features.
- Shrivastava, A., Gupta, A. & Girshick, R. (2016). *Training Region-based Object Detectors with Online Hard Example Mining*. arXiv. https://arxiv.org/abs/1604.03540 — Online hard example mining, the main alternative that the paper compares the focal loss against.
- Ren, S., He, K., Girshick, R. & Sun, J. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — The two-stage detector that the paper's RetinaNet is compared with, and the source of the anchor design.
- Liu, W., et al. (2015). *SSD: Single Shot MultiBox Detector*. arXiv. https://arxiv.org/abs/1512.02325 — The one-stage detector whose hard example mining the paper discusses.

### Surveys and textbooks

- Zou, Z., et al. (2019). *Object Detection in 20 Years: A Survey*. arXiv. https://arxiv.org/abs/1905.05055 — A survey that places one-stage and two-stage detectors, and their training methods, in the history of the field.

### Articles and documentation

- Ge, Z., Liu, S., Wang, F., Li, Z. & Sun, J. (2021). *YOLOX: Exceeding YOLO Series in 2021*. arXiv. https://arxiv.org/abs/2107.08430 — A later one-stage detector that uses a different label-assignment strategy, SimOTA.

[^1]: Lin et al. (2017), Introduction: dense detectors evaluate 10^4 to 10^5 candidate locations per image, of which only a few contain objects; the paper argues that class imbalance is the central cause of the accuracy gap.
[^2]: Lin et al. (2017), Sections 3 and 5 and Table 1: the focal loss definition, the α and γ ablations (Tables 1a and 1b), the OHEM comparison (Table 1d), and the default setting γ = 2 with α = 0.25.
[^3]: Lin et al. (2017), Section 5 and Table 2, including the Inception-ResNet-v2-TDM comparison.
[^4]: Lin et al. (2017), Section 4 (inference), Section 5.2 and Figure 2: the inference procedure, the speed-accuracy comparison on an M40 GPU, and the paper's statement that high frame rates need a different network design.
[^5]: Ge et al. (2021), abstract: YOLOX uses an anchor-free form with a decoupled head and the SimOTA label-assignment strategy.
