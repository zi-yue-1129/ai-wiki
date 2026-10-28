---
tags:
  - semi-supervised learning
  - consistency regularisation
---

# Consistency Regularisation

Consistency regularisation trains a model to give the same prediction for an unlabelled input and for a perturbed version of it. The unlabelled data then shape the decision boundary without any labels, and this is the family of methods behind most recent semi-supervised image results.

## Overview

The loss has two parts: ordinary cross-entropy on the few labelled examples, plus a penalty on the difference between predictions for two perturbed views of each unlabelled example. The perturbation can be noise, augmentation or dropout. The assumption is that a good classifier should not change its answer under small, label-preserving changes.

## Main methods

- **Π-model and temporal ensembling** (Laine & Aila, 2017) apply two random augmentations to each example and penalise disagreement. Temporal ensembling averages predictions across epochs to get smoother targets.
- **Mean Teacher** (Tarvainen & Valpola, 2017) keeps a teacher whose weights are an exponential moving average of the student's, and uses the teacher's prediction as the target. This is more stable than using the student alone.
- **MixMatch** combines consistency with mixup, guessing labels for unlabelled data by averaging predictions over augmentations and sharpening them.
- **FixMatch** uses a weak augmentation to produce a confident pseudo-label, and a strong augmentation to predict it, keeping only predictions above a confidence threshold.

## Why it helps, and when it does not

Consistency methods help when the classes are separated by low-density regions, so that the decision boundary should pass through gaps in the data. They can hurt when the augmentations change the class (a rotated "6" is a "9"), and when the labelled set is so small that the teacher's predictions are poor from the start.

## Connections

The consistency idea is closely linked to [pseudo-labelling](../pseudo-labelling-and-self-training/index.md), since FixMatch-style methods use confident predictions as targets. The smoothness assumption is the one that [graph-based methods](../graph-based-methods/index.md) make explicit. For images, the augmentations themselves are the main design choice, see [computer vision](../../../../models/computer-vision/index.md). Strong augmentation strategies also appear in [self-supervised learning](../../self-supervised/index.md).

## Applications

Image classification with a few hundred labels per class, medical imaging where expert labels are scarce, speech recognition with partly transcribed audio, and text classification with consistency under word dropout.

## Open questions

Results depend heavily on the augmentations and on how many labels there are, and reported gains often shrink under fair evaluation (Oliver et al., 2018). It is unclear how to choose augmentations for non-image data, and how to guard against confirmation bias when the teacher's errors reinforce themselves.

## References

### Seminal papers

- Laine & Aila (2017), "Temporal ensembling for semi-supervised learning", ICLR, arXiv:1610.02242 — Introduces the Π-model and temporal ensembling, consistency losses with averaged targets.
- Tarvainen & Valpola (2017), "Mean teachers are better role models", NeurIPS, arXiv:1703.01780 — Mean Teacher, a teacher built from weight averages of the student.
- Berthelot et al. (2019), "MixMatch: a holistic approach to semi-supervised learning", NeurIPS, arXiv:1905.02249 — Combines consistency, sharpening and mixup into one semi-supervised objective.
- Sohn et al. (2020), "FixMatch: simplifying semi-supervised learning with consistency and confidence", NeurIPS, arXiv:2001.07685 — Uses confident pseudo-labels from weak augmentations as targets for strong ones.
- Oliver, Odena, Raffel, Cubuk & Goodfellow (2018), "Realistic evaluation of deep semi-supervised learning algorithms", NeurIPS, arXiv:1804.09170 — Shows that many reported gains disappear under a fair, consistent evaluation protocol. https://proceedings.neurips.cc/paper/2018/hash/c1fea270c48e8079d8ddf7d06d26ab52-Abstract.html

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

- Chapelle, Schölkopf & Zien (eds.), *Semi-Supervised Learning*, MIT Press (2006). No free link checked.
