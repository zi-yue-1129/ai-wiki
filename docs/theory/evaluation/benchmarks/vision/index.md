---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# Vision Benchmarks

Vision benchmarks measure recognition at two levels: whole-image classification and instance-level detection and segmentation. The two tasks use different metrics, so their scores are not comparable with each other.

| Benchmark | Task | Main metric |
|---|---|---|
| [ImageNet](imagenet.md) | Image classification | Top-5 error and top-1 accuracy |
| [COCO](coco.md) | Detection and instance segmentation | Average precision over IoU thresholds from 0.5 to 0.95 |

## Comparing scores

Compare models on the same test set, with the same metric and the same training data. Pre-training on a larger image collection changes what a fine-tuned score means, so the training data must be stated along with the score.

## Common issues

- **Test-set fit.** A test set can be fitted by repeated use, and a fresh collection can show lower accuracy (Recht et al., 2019).
- **Ambiguous labels.** Images can contain several valid labels or objects, which limits what any score can show.
- **Saturation.** Top systems leave little room, so differences need intervals.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Few-shot](../few-shot/index.md) tests recognition from few examples.
- [Accuracy](../../metrics/classification/accuracy.md) and [IoU](../../metrics/segmentation/iou.md) are the metrics behind these benchmarks.

## References

### Seminal papers

- Deng, J. et al. (2009). *ImageNet: A large-scale hierarchical image database*. CVPR. https://doi.org/10.1109/cvpr.2009.5206848 — Introduces the image database behind the classification benchmark.
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — Describes the challenge, its metrics and human comparison.
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://doi.org/10.1007/978-3-319-10602-1_48 — Introduces the detection and segmentation benchmark with per-instance masks.

### Articles and documentation

- Everingham, M. et al. (2010). *The PASCAL Visual Object Classes (VOC) Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-009-0275-4 — Defines the earlier VOC evaluation with a single overlap threshold.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Re-collects an ImageNet test set and measures the accuracy drop.
