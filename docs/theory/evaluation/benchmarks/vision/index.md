---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
aliases:
  - Vision benchmarks
  - 視覺基準
---

# Vision Benchmarks

Vision benchmarks measure recognition at two levels: whole-image classification and instance-level detection and segmentation. The two tasks use different metrics and different annotations, so their scores are not comparable with each other.

## Overview

The field's reference point is ImageNet, a large hierarchical image database, described by Deng et al. (2009). The annual ImageNet Large Scale Visual Recognition Challenge built a classification and detection benchmark on hundreds of object categories and millions of images, and it compared the best systems with human accuracy. Its organisers also described the lessons from five years of running the challenge (Russakovsky et al., 2015).

Detection and segmentation needed a different kind of data. Microsoft COCO gathers everyday scenes and labels objects with per-instance segmentation masks. It contains 2.5 million labelled instances in 328k images across 91 object types, and it is designed to place recognition in the context of scene understanding (Lin et al., 2014).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [ImageNet](imagenet.md) | Image classification | Top-1 and top-5 accuracy |
| [COCO](coco.md) | Detection and instance segmentation | Average precision over several overlap thresholds |

Image classification asks what is in the picture, so one label per image is enough. Detection and segmentation ask where each object is and what its shape is, so the metric must account for localisation quality as well as the label. This is why the same model can rank differently on the two.

## Comparing scores

Compare models on the same test set, with the same metric and the same training data. Pre-training on a larger image collection changes what a fine-tuned score means, so the training data must be stated along with the score. Results from different input resolutions or crop policies also differ, and a comparison should hold those fixed.

## Key concepts

- **Top-1 and top-5 accuracy**: the share of images whose correct label is the top prediction, or among the five highest predictions.
- **Instance segmentation**: labelling each object separately, not just each pixel by class.
- **Overlap threshold**: the minimum overlap between a predicted and a true region for a detection to count as correct.

## Common issues

- **Test-set fit.** A test set can be fitted by repeated use. When Recht et al. (2019) collected a new test set by following the original process, they found accuracy drops of 3% to 15% on CIFAR-10 and 11% to 14% on ImageNet, and they attributed the drop to models failing on slightly harder images rather than to adaptivity.
- **Robustness.** A high clean-data score can hide weakness to blur, noise and weather. ImageNet-C tests this with common corruptions (Hendrycks & Dietterich, 2019).
- **Ambiguous labels.** Images can contain several valid labels or objects, which limits what any score can show.
- **Saturation.** Top systems leave little room on the older sets, so differences need confidence intervals.

## Connections

- [Visual perception](../../../../brain-mind/visual-perception/index.md) describes how the brain recognises objects, the comparison that Brain-Score makes concrete for models.
- [Few-shot](../few-shot/index.md) tests recognition from few examples.
- [Accuracy](../../metrics/classification/accuracy.md) and [IoU](../../metrics/segmentation/iou.md) are the metrics behind these benchmarks.

## Open questions

- How much of the progress on ImageNet transfers to new image collections, and how to build test sets that stay fresh.
- Whether detection benchmarks with many small objects measure the same skill as classification benchmarks with one dominant object.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Neuroscience](../neuroscience/index.md) compares model representations with neural responses to the same kind of images.
- [Multimodal](../multimodal/index.md) combines images with language.

## References

### Seminal papers

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR 2009. https://doi.org/10.1109/CVPR.2009.5206848 — Introduces the image database behind the classification benchmark.
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision, 115, 211–252. https://doi.org/10.1007/s11263-015-0816-y — Describes the challenge, its data, and the comparison of the best systems with human accuracy.
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — Introduces 2.5 million per-instance labels in 328k images, the detection and segmentation benchmark.

### Articles and documentation

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Re-collects test sets for CIFAR-10 and ImageNet and measures the accuracy drops.
- Hendrycks, D. & Dietterich, T. (2019). *Benchmarking Neural Network Robustness to Common Corruptions and Perturbations*. arXiv. https://arxiv.org/abs/1903.12261 — Introduces ImageNet-C and ImageNet-P, which measure robustness to common corruptions rather than worst-case perturbations.
