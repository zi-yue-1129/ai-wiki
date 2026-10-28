---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - segmentation
---

# Segmentation Metrics

Segmentation metrics compare a predicted mask with a reference mask, pixel by pixel or voxel by voxel. They measure overlap rather than whether the class is right on average, so they are the natural choice when the location and extent of a region matter.

## Problem

For one class, let \(A\) be the set of predicted foreground pixels and \(B\) the set of reference foreground pixels. A metric should be 1 when \(A = B\), fall as the two regions diverge, and not reward predicting everything as foreground. Pixel accuracy fails the last test on sparse classes, because a mask that is almost all background scores highly.

## Key concepts

- **Overlap:** the intersection \(|A \cap B|\), the pixels both masks mark as foreground.
- **Union:** \(|A \cup B|\), the pixels either mask marks as foreground.
- **Per-class and mean:** a metric is computed per class and then averaged, so rare classes weigh as much as common ones.

## Key methods

### Intersection over union (IoU)

\[
\mathrm{IoU} = \frac{|A \cap B|}{|A \cup B|} = \frac{\mathrm{TP}}{\mathrm{TP} + \mathrm{FP} + \mathrm{FN}}
\]

IoU is also known as the Jaccard index. The details are on the [IoU](iou.md) page. Its mean over classes is the usual headline number in semantic segmentation. The PASCAL VOC report (Everingham et al., 2010) is a standard reference for overlap-based evaluation, and the Cityscapes evaluation reports intersection over union per class (Cordts et al., 2016).

- **Limitations:** IoU says nothing about where errors lie on the boundary, and an empty predicted mask against an empty reference needs a convention.

### Dice coefficient

\[
\mathrm{Dice} = \frac{2\,\lvert A \cap B \rvert}{\lvert A \rvert + \lvert B \rvert} = \frac{2\,\mathrm{TP}}{2\,\mathrm{TP} + \mathrm{FP} + \mathrm{FN}}
\]

Dice (1945) introduced the coefficient as a measure of ecological association between species. On pixel labels it is the same ratio as the [F1 score](../classification/f1.md). If \(J\) is the IoU of the same masks, then \(\mathrm{Dice} = 2J / (1 + J)\), so Dice is at least as large as IoU, and the two rank models the same way on a single region. The details are on the [Dice](dice.md) page.

- **Limitations:** for highly unbalanced multi-class data, a plain Dice weights each class by its size, so a class-weighted variant is needed. Sudre et al. (2017) propose the generalised Dice overlap for this case.

## Connections

Overlap metrics do not say how far the predicted boundary is from the reference boundary, which is why segmentation evaluations often add a boundary-distance measure. The same overlap ratio is also used as a training loss in several segmentation methods, which is where Sudre et al. (2017) apply the generalised form.

## Open questions

- How to combine overlap with boundary accuracy in one reported number.
- How to define the metric when both the prediction and the reference are empty, which happens for small structures.

## References

### Seminal papers

- Dice, L. R. (1945). Measures of the amount of ecologic association between species. *Ecology* 26(3), 297–302. https://doi.org/10.2307/1932409 — Introduces the coefficient that is now called the Dice score.
- Everingham, M., et al. (2010). The Pascal Visual Object Classes (VOC) Challenge. *International Journal of Computer Vision* 88(2), 303–338. https://doi.org/10.1007/s11263-009-0275-4 — Standard benchmark report whose evaluation uses overlap-based measures.
- Sudre, C. H., Li, W., Vercauteren, T., Ourselin, S., et al. (2017). Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations. In *Deep Learning in Medical Image Analysis and Multimodal Learning for Clinical Decision Support* (DLMIA 2017), LNCS, pp. 240–248. https://doi.org/10.1007/978-3-319-67558-9_28 — Proposes a class-reweighted generalised Dice overlap for highly unbalanced segmentation.

### Articles and documentation

- scikit-learn contributors. *jaccard_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html — API reference describing the Jaccard index as the size of the intersection divided by the size of the union of two label sets.
- scikit-learn contributors. *f1_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html — API reference giving the formula \(2\mathrm{TP} / (2\mathrm{TP} + \mathrm{FP} + \mathrm{FN})\), the same overlap ratio that Dice uses on binary masks.
- Cordts, M., et al. (2016). The Cityscapes dataset for semantic urban scene understanding. CVPR 2016. https://openaccess.thecvf.com/content_cvpr_2016/html/Cordts_The_Cityscapes_Dataset_CVPR_2016_paper.html — Benchmark whose evaluation reports intersection over union per class.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the classification scorers that apply to pixel labels.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
