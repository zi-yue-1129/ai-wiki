---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# Dice Coefficient

The Dice coefficient measures the overlap between a predicted and a reference region, scaled so that identical regions give 1. It is widely used in medical image segmentation, where it is often called the Dice similarity coefficient.

## Definition

For a predicted region $A$ and a reference region $B$:

$$\text{Dice} = \frac{2\,|A \cap B|}{|A| + |B|}$$

On binary masks, with $TP$, $FP$ and $FN$ counted pixel by pixel, this equals $\frac{2\,TP}{2\,TP + FP + FN}$, which is the [F1 score](../classification/f1.md) for the positive class. That identity is why the two are often reported as the same measure.

## Interpretation

Dice is 1 for identical regions and 0 for no overlap. Since $\text{Dice} = 2\,\text{IoU} / (1 + \text{IoU})$, Dice is always at least as large as [IoU](iou.md) for the same masks, so a Dice of 0.8 corresponds to an IoU of about 0.67. Comparing a Dice value with an IoU value from another paper requires converting one of them.

## When to use it

Use Dice for binary or per-class segmentation where the region size varies, particularly in medical imaging, and where the score is reported per case and then averaged. Report whether the score is averaged per image or over pixels, because the two give different results when regions differ in size.

## Pitfalls

- **Empty masks.** If both masks are empty, the formula is 0/0. The convention for this case must be stated.
- **Mixed conventions.** Dice and IoU are both overlap measures on the same masks, but a comparison across papers requires knowing which one each uses.

## Related metrics

[IoU](iou.md) is the same overlap with a different denominator. [F1](../classification/f1.md) is the same formula applied to pixel labels. The family overview is [Segmentation Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API reference giving the formula $2TP / (2TP + FP + FN)$, which is the Dice coefficient on binary masks.
- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API reference for the overlap measure that Dice is related to.
