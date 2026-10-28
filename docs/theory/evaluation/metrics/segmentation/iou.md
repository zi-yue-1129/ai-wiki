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
