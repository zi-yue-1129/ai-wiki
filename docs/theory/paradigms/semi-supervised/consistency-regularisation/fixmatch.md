---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/semi-supervised/consistency-regularisation
  - theory/paradigms/semi-supervised/pseudo-labelling-and-self-training
  - theory/models/computer-vision
tags:
  - semi-supervised learning
  - consistency regularisation
  - pseudo-labelling
aliases:
  - 以一致性與信心簡化半監督學習
  - FixMatch
  - Simplifying semi-supervised learning with consistency and confidence
---

# FixMatch

FixMatch is a semi-supervised method. It takes the model's confident prediction on a weakly augmented unlabelled image as a hard pseudo-label, then trains the model to predict that label from a strongly augmented version of the same image. Predictions below a confidence threshold are ignored. The family-level picture is on the [Consistency Regularisation](index.md) page.

## Overview

Sohn et al. (2020) presented FixMatch at NeurIPS 2020. The paper combines two ideas that are common in semi-supervised learning: consistency between perturbed views of the same input, and confident pseudo-labels. Its aim is simplicity. It keeps these two parts and drops the mixing and sharpening steps that MixMatch uses. The abstract reports 94.93% accuracy on CIFAR-10 with 250 labels, and 88.61% accuracy with 40 labels (four per class). The paper evaluates on CIFAR-10, CIFAR-100, SVHN, STL-10 and ImageNet, all for image classification.

## Key concepts

- **Weak augmentation** \(\alpha(\cdot)\): a random horizontal flip (not used on SVHN) and a random translation of up to 12.5% vertically and horizontally.
- **Strong augmentation** \(A(\cdot)\): RandAugment or CTAugment, followed by Cutout.
- **Hard pseudo-label** \(\hat q_b\): the class with the highest probability under the weak view.
- **Confidence threshold** \(\tau\): 0.95 for CIFAR-10, CIFAR-100, SVHN and STL-10, and 0.7 for ImageNet in the paper's Table 4.
- **Distribution alignment (DA)**: an optional adjustment of the pseudo-label distribution. The paper uses it in some experiments, and reports that CIFAR-100 and ImageNet with 1% of labels need it.

## How it works

Each training step takes a labelled batch of size \(B\) and an unlabelled batch of size \(\mu B\). The supervised loss is the cross-entropy on weakly augmented labelled examples:

\[
\ell_s = \frac{1}{B}\sum_{b=1}^{B} H\big(p_b,\; p_m(y \mid \alpha(x_b))\big)
\]

For each unlabelled example, the weak view gives \(q_b = p_m(y \mid \alpha(u_b))\) and the hard pseudo-label \(\hat q_b = \arg\max q_b\). The unsupervised loss keeps the pseudo-label only when its confidence reaches \(\tau\), and trains the strong view to predict it:

\[
\ell_u = \frac{1}{\mu B}\sum_{b=1}^{\mu B} \mathbb 1\big(\max q_b \ge \tau\big)\, H\big(\hat q_b,\; p_m(y \mid A(u_b))\big)
\]

Here \(H\) is cross-entropy and \(p_m\) is the model's predicted distribution. The total loss is \(\ell_s + \lambda_u \ell_u\). The paper writes the threshold test as \(\ge \tau\) in its equation and as \(> \tau\) in its algorithm box. This page follows the equation.

The paper's main hyperparameters are \(B = 64\), \(\mu = 7\) and \(\lambda_u = 1\) for the CIFAR, SVHN and STL-10 experiments, with SGD, Nesterov momentum 0.9, learning rate 0.03 and a cosine learning-rate decay. Weight decay is 0.0005 for CIFAR-10, SVHN and STL-10, and 0.001 for CIFAR-100.

## Key methods

### FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence (Sohn et al., 2020)

- **Problem:** many semi-supervised methods combine several losses and extra components. Their results vary a lot when only a few labels are available, and the gains are hard to attribute to any one part.
- **Core idea:** use a confident prediction on a weakly augmented view as the target for a strongly augmented view of the same image. Confidence thresholding keeps the noisy targets out.
- **Equation or algorithm:** the supervised loss, the thresholded unsupervised loss and their weighted sum, as above.
- **Results:** the error rates below are means over five folds, with RA and CTA the two strong augmentations (Table 2).
  - CIFAR-10, 250 labels: 5.07 ± 0.65% (RA) and 5.07 ± 0.33% (CTA).
  - CIFAR-10, 4000 labels: 4.26 ± 0.05% (RA) and 4.31 ± 0.15% (CTA).
  - SVHN, 1000 labels: 2.28 ± 0.11% (RA) and 2.36 ± 0.19% (CTA).
  - STL-10, 1000 labels: 7.98 ± 1.50% (RA) and 5.17 ± 0.63% (CTA).
  - ImageNet with 10% of the labels: top-1 error 28.54 ± 0.52%, with τ = 0.7.
  - The abstract gives the matching accuracies of 94.93% and 88.61% for CIFAR-10 with 250 and 40 labels.
  - In the threshold study (Section 5.1), τ = 0.95 gives the lowest error of the values the paper compares.
  - At 40 labels on CIFAR-10, the error across five seeds ranges from 5.46% to 13.32% (Table 8).
- **Limitations:** the authors describe results with few labels as "particularly high-variance", and say that the choice of seed matters. A low threshold admits noisy pseudo-labels and can cause confirmation bias. Weight decay and learning rate strongly affect the results, and the paper notes that the same technique "can not always be directly compared across different implementations". On ImageNet with 1% of labels, training "does not train well" without distribution alignment. The experiments cover images only. The paper has no dedicated limitations section, so these come from its text and appendix.

## Connections

- FixMatch sits in the [Consistency Regularisation](index.md) family. Its pseudo-labels are a thresholded form of the ideas in [pseudo-labelling and self-training](../pseudo-labelling-and-self-training/index.md).
- [Mean Teacher](mean-teacher.md) is another consistency method. It uses a weight-averaged teacher instead of thresholded pseudo-labels.
- The smoothness assumption that consistency methods rely on is made explicit by [graph-based methods](../graph-based-methods/index.md).
- For images, the augmentations are the main design choice. See [computer vision](../../../models/computer-vision/index.md). Strong augmentation strategies also appear in [self-supervised learning](../../self-supervised/index.md).

## Open questions

- Is a threshold of 0.95 the right choice beyond images, and how should it be set when labels are scarce and the model is weak?
- Why does distribution alignment matter on some datasets, such as CIFAR-100 and ImageNet with 1% of labels, but not on others?
- Can the method be made less sensitive to the seed in the one-label-per-class regime?

## References

### Seminal papers

- Sohn, K. et al. (2020). FixMatch: Simplifying Semi-Supervised Learning with Consistency and Confidence. NeurIPS 2020. https://arxiv.org/abs/2001.07685 — Introduces FixMatch and the results used on this page.
- Berthelot, D. et al. (2019). MixMatch: A Holistic Approach to Semi-Supervised Learning. arXiv:1905.02249. https://arxiv.org/abs/1905.02249 — Combines consistency, sharpening and MixUp into one objective. FixMatch simplifies this design.
- Laine, S. & Aila, T. (2017). Temporal Ensembling for Semi-Supervised Learning. arXiv:1610.02242. https://arxiv.org/abs/1610.02242 — Uses averages of predictions from earlier epochs as consistency targets.
- Tarvainen, A. & Valpola, H. (2017). Mean teachers are better role models. NeurIPS 2017. https://arxiv.org/abs/1703.01780 — Uses a teacher built from weight averages of the student. See also [Mean Teacher](mean-teacher.md).

### Surveys and textbooks

- Oliver, A. et al. (2018). Realistic Evaluation of Deep Semi-Supervised Learning Algorithms. arXiv:1804.09170. https://arxiv.org/abs/1804.09170 — Shows that many reported gains shrink when baselines are tuned fairly, which is a caution when comparing methods such as FixMatch.
