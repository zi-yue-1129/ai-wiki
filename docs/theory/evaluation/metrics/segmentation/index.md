---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# Segmentation Metrics

Segmentation metrics compare a predicted mask with a reference mask, pixel by pixel or voxel by voxel. They measure overlap rather than whether the class is right on average, so they are the natural choice when the location and extent of a region matter.

## Key metrics

| Metric | What it measures | Range |
|---|---|---|
| [IoU](iou.md) | Overlap divided by union of the predicted and reference regions | 0 to 1 |
| [Dice](dice.md) | Twice the overlap divided by the sum of the two region sizes | 0 to 1 |

IoU and Dice are both overlap measures and rank models in the same order for a single region, but their values are not interchangeable. Dice is always at least as large as IoU for the same masks, so report which one you use.

## Connections

On binary masks, the Dice coefficient is the same formula as the [F1 score](../classification/f1.md) on the pixel labels, so the two families describe the same overlap. Overlap metrics do not say how far the boundary is from the reference, which is why segmentation evaluations often add a boundary-distance measure.

## References

### Articles and documentation

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API reference describing the Jaccard index as the size of the intersection divided by the size of the union of two label sets.
- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API reference giving the formula $2TP / (2TP + FP + FN)$, the same overlap ratio that Dice uses on binary masks.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the classification scorers that apply to pixel labels.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- Sudre, C. H. et al. (2017). Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations. DLMIA 2017. https://arxiv.org/abs/1707.03237 — Proposes generalised Dice overlap, which weights classes by their size, for highly unbalanced segmentation.
- Cordts, M. et al. (2016). The Cityscapes dataset for semantic urban scene understanding. CVPR 2016. https://arxiv.org/abs/1604.01685 — Benchmark whose evaluation reports intersection over union per class.
