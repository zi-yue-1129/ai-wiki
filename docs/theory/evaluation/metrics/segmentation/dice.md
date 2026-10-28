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

## Worked example

Use the two regions from the [IoU](iou.md) example: 6 predicted pixels, 4 reference pixels and 3 shared. Dice is $2 \cdot 3 / (6 + 4) = 0.60$. As a check, $2 \cdot 0.43 / (1 + 0.43) \approx 0.60$. If both masks were empty, the formula would be $0/0$, which is the empty-mask case in the pitfalls below.

## Pitfalls

- **Empty masks.** If both masks are empty, the formula is 0/0. The convention for this case must be stated.
- **Mixed conventions.** Dice and IoU are both overlap measures on the same masks, but a comparison across papers requires knowing which one each uses.

## Related metrics

[IoU](iou.md) is the same overlap with a different denominator. [F1](../classification/f1.md) is the same formula applied to pixel labels. The family overview is [Segmentation Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API reference giving the formula $2TP / (2TP + FP + FN)$, which is the Dice coefficient on binary masks.
- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API reference for the overlap measure that Dice is related to.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- Dice, L. R. (1945). Measures of the amount of ecologic association between species. *Ecology* 26(3), 297–302. https://doi.org/10.2307/1932409 — Original paper defining the coefficient, first used to measure association between species.
- Milletari, F., Navab, N. & Ahmadi, S.-A. (2016). V-Net: fully convolutional neural networks for volumetric medical image segmentation. 3DV 2016. https://arxiv.org/abs/1606.04797 — Introduces a volumetric segmentation network trained with a Dice-based objective.
