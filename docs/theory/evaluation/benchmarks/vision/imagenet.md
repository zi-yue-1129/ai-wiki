---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# ImageNet

ImageNet is a large image database organised by the nouns of WordNet. Its best-known benchmark is the ImageNet Large Scale Visual Recognition Challenge (ILSVRC), run annually from 2010 (Russakovsky et al., 2015). It is the reference benchmark for image classification, and it is also used for object detection and as a source of pre-training data.

## Task and data

Given an image, a model predicts one of a fixed set of categories. The challenge covers classification and object detection over hundreds of categories and millions of images (Russakovsky et al., 2015). The classification subset uses 1,000 categories.

## Protocol and metric

The challenge's primary metric is **top-5 error**: a prediction counts as correct if the true class is among the five highest scores. Top-1 accuracy is reported alongside it. Test labels are withheld, so the reported scores come from submitted predictions rather than local evaluation.

The metrics behind these numbers are described in [accuracy](../../metrics/classification/accuracy.md). Top-k accuracy is the same idea with a looser decision rule.

## What it shows

The benchmark made deep convolutional networks the standard approach to image recognition. Later architectures are routinely compared on it, including residual networks (He et al., 2015) and vision transformers (Dosovitskiy et al., 2020). The 2015 paper also compares the best systems with human accuracy, which shows where the task is still hard.

## Limitations

- **Generalisation to new data.** Recht et al. (2019) collected a new test set by following the original procedure. Accuracy dropped for many models, which suggests that part of the benchmark measures fit to its collection process.
- **Ambiguous labels.** Most images contain several objects but carry one label. Top-5 scoring softens this ambiguity without removing it.
- **Saturation.** Top systems now score well above the levels that first defined progress, so small gaps need intervals and an explicit test-set size before they can be interpreted.

## Variants

ImageNetV2, from the re-collection in Recht et al. (2019), is the best-known alternative test set. Robustness and out-of-distribution variants are used when a score on the original test set is not enough.

## Related

- [COCO](coco.md) covers detection and segmentation with per-instance masks.
- [Few-shot benchmarks](../few-shot/index.md) build on ImageNet images.
- [Vision family overview](index.md) compares the vision benchmarks.

## References

### Seminal papers

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR. https://doi.org/10.1109/cvpr.2009.5206848 — Introduces the image database from which the ILSVRC benchmark is sampled.
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — Describes the challenge, its metrics, and its comparison with human accuracy.

### Articles and documentation

- He, K. et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Residual networks, a standard architecture evaluated on ImageNet classification.
- Dosovitskiy, A. et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — Vision transformers trained and evaluated on ImageNet.

### Additional sources

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Re-collects a test set with the original procedure and measures the resulting accuracy drop.
