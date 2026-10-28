---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# Intersection over Union

Intersection over union (IoU), also called the Jaccard index, is the area where the predicted and reference regions overlap, divided by the area they cover together. It is the standard overlap measure in object detection and segmentation.

## Definition

For a predicted region $A$ and a reference region $B$:

$$\text{IoU} = \frac{|A \cap B|}{|A \cup B|}$$

IoU is 1 when the regions are identical and 0 when they do not overlap. scikit-learn's `jaccard_score` computes the same quantity for label sets, so for a binary mask it gives the IoU of the positive class (see References).

## Interpretation

Because the union appears in the denominator, IoU penalises both missing pixels and extra pixels. A prediction that covers the right region but is twice its size scores 0.5, not 1.0. For small objects, a few pixels of boundary error can change IoU a lot, so results on small objects can look worse than the model's visual quality suggests.

## When to use it

Use IoU when the question is how well a predicted region matches the reference, for example in detection with a threshold such as IoU ≥ 0.5 to count a detection as correct. Report the threshold and whether scores are averaged per image, per class or over the dataset.

## Worked example

Take a strip of 10 pixels. The predicted region covers pixels 1 to 6 (6 pixels) and the reference covers pixels 4 to 7 (4 pixels), so they share 3 pixels. The union is $6 + 4 - 3 = 7$, so IoU $= 3 / 7 \approx 0.43$. For the same masks, [Dice](dice.md) gives 0.60, which shows how far the two measures can differ.

## Properties and variants

- **Pixel form.** For a binary mask, $|A \cap B| = \mathrm{TP}$ and $|A \cup B| = \mathrm{TP} + \mathrm{FP} + \mathrm{FN}$, so $\mathrm{IoU} = \mathrm{TP} / (\mathrm{TP} + \mathrm{FP} + \mathrm{FN})$. This is the Jaccard index of the two sets.
- **Relation to Dice.** $\mathrm{Dice} = 2\,\mathrm{IoU} / (1 + \mathrm{IoU})$. The two are monotone functions of each other, so they rank models identically on a single region.
- **Mean IoU.** The mean over classes (mIoU) is the usual summary for multi-class segmentation. Per-class values show whether rare classes are failing.
- **Box variant.** Generalised IoU subtracts a penalty based on the smallest enclosing box. It still gives a useful signal when boxes do not overlap, where plain IoU is zero for every such pair.
- **Limit.** Small or thin objects have small areas, so a few boundary pixels can change IoU a lot.

## Pitfalls

- **Averaging.** Mean IoU over classes or images can hide poor performance on rare or small objects. Report per-class values.
- **Threshold choice.** A detection counted correct at IoU 0.5 may be wrong at 0.75. Give the threshold used.

## Related metrics

[Dice](dice.md) is a related overlap measure with a different denominator. The family overview is [Segmentation Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API reference giving the intersection-over-union definition for label sets, with binary and multilabel examples.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers available for classification-style comparisons.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- Rezatofighi, H. et al. (2019). Generalized intersection over union: a metric and a loss for bounding box regression. CVPR 2019. https://arxiv.org/abs/1902.09630 — Extends IoU so that it stays informative for boxes that do not overlap.
- Cordts, M. et al. (2016). The Cityscapes dataset for semantic urban scene understanding. CVPR 2016. https://arxiv.org/abs/1604.01685 — Benchmark whose evaluation reports intersection over union per class.
