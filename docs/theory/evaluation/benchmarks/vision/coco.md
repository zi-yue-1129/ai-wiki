---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - vision
---

# COCO

COCO (Common Objects in Context) is a benchmark for object detection and instance segmentation in everyday scenes. Its aim is to place object recognition in the broader setting of scene understanding (Lin et al., 2014).

## Task and data

The dataset contains photos of 91 object types, with 2.5 million labelled instances in 328,000 images. Each object has a per-instance segmentation mask, so a model must localise each instance and also delineate it (Lin et al., 2014).

## Protocol and metric

Detection and segmentation are scored with **average precision (AP)** computed over several intersection-over-union thresholds, from 0.5 to 0.95 in steps of 0.05. The overlap measure is [IoU](../../metrics/segmentation/iou.md). PASCAL VOC used a single threshold of 0.5 (Everingham et al., 2010), so COCO's averaged score is stricter about localisation quality. COCO also reports separate scores for small, medium and large objects.

## What it shows

Because AP is averaged over thresholds, a model cannot score well by finding objects roughly. Detection results on COCO became a common reference for detector design, for example Faster R-CNN (Ren et al., 2015).

## Limitations

- **Boundary quality.** At high thresholds, a few pixels of mask error can lower AP, so scores depend on the annotation protocol as well as the model.
- **Small objects.** Small instances have low AP in most systems, which makes the overall average sensitive to how many small objects the test set contains.
- **Hidden test labels.** Test results come from an evaluation server, which limits how often and how finely a team can probe the test set.

## Variants

Panoptic and long-tailed extensions of COCO change either the label set or the task. Compare scores only when the same annotation release, split and AP definition are used.

## Related

- [IoU](../../metrics/segmentation/iou.md) is the overlap measure behind AP.
- [ImageNet](imagenet.md) is the classification benchmark that most vision backbones are first evaluated on.
- [Vision family overview](index.md) compares the vision benchmarks.

## References

### Seminal papers

- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. ECCV. https://doi.org/10.1007/978-3-319-10602-1_48 — Introduces the dataset, its per-instance masks and its baseline analysis.
- Everingham, M. et al. (2010). *The PASCAL Visual Object Classes (VOC) Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-009-0275-4 — Defines the VOC evaluation, including the single 0.5 overlap threshold for detection.

### Articles and documentation

- Ren, S. et al. (2015). *Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks*. arXiv. https://arxiv.org/abs/1506.01497 — A detector whose results on COCO became a common reference point.
- Lin, T.-Y. et al. (2014). *Microsoft COCO: Common Objects in Context*. arXiv. https://arxiv.org/abs/1405.0312 — Preprint with the full statistical analysis of the dataset.

### Additional sources

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — Describes the earlier large-scale benchmark that COCO is often compared with.
