---
status: draft
last_reviewed: 2026-10-28
tags:
  - regularisation
  - data augmentation
  - deep learning
aliases:
  - mixup
  - CutMix
  - 混合增強
  - 切割混合
---

# Mixup and CutMix

Mixup and CutMix are data augmentation methods that train a classifier on blends of two training examples, with their labels blended in the same proportion. Mixup blends whole images by a weighted average. CutMix pastes a rectangular patch from one image into another. Both are described on the parent [dropout and stochastic regularisation](../index.md) page as randomness applied to the training data rather than to the network.

## Overview

Data augmentation enlarges a training set by transforming its examples, for instance by cropping or flipping images. Most transformations leave the label unchanged. Zhang et al. (2017) changed this by combining two examples and their labels. Their abstract describes mixup as training on convex combinations of pairs of examples and their labels, which encourages the network to behave linearly between training examples.

CutMix (Yun et al., 2019) addresses a drawback of an earlier family of regional methods. Those methods erase a region of an image, usually by overlaying black pixels or noise, which discards information and wastes training pixels. CutMix replaces the erased region with a patch cut from another image, and mixes the labels according to the area of the patch.

## Key concepts

- **Convex combination.** A weighted average whose weights are between 0 and 1 and sum to 1.
- **Soft label.** A target that is a distribution over classes, for example 70% of one class and 30% of another. Both methods train on soft labels.
- **Regional dropout.** Removing a rectangular region from an input image. Cutout is the best-known example. CutMix is an alternative to it.
- **Localisation.** The ability to find where an object is in an image. The CutMix paper argues that patch-based training encourages the network to attend to less discriminative parts of objects.

## How it works

### Mixup

Draw a mixing weight \(\lambda\) from a Beta distribution with parameter \(\alpha\). For two examples \((x_i, y_i)\) and \((x_j, y_j)\), form

\[
\tilde x = \lambda x_i + (1-\lambda)\,x_j, \qquad \tilde y = \lambda y_i + (1-\lambda)\,y_j.
\]

The loss is computed on the mixed input against the mixed label. The parameter \(\alpha\) controls how strongly examples are mixed: values near 0 leave the examples almost unchanged, while larger values give more even mixtures.

### CutMix

Draw a rectangle \(B\) in the image of \(x_j\), with its area chosen from a Beta-distributed fraction, and place it at a random position. Write \(M\) for the binary mask that is 1 outside the rectangle and 0 inside it. Then

\[
\tilde x = M \odot x_i + (1-M) \odot x_j, \qquad \tilde y = \lambda\, y_i + (1-\lambda)\, y_j,
\]

where \(\lambda\) is the fraction of the image that still comes from \(x_i\), namely one minus the area of the rectangle divided by the area of the image.

### Procedure

1. Take a mini-batch and pair each example with another from the same batch, usually by a random permutation.
2. Draw a mixing weight for each pair.
3. Build the mixed inputs and their mixed labels.
4. Train with the loss computed on the mixed examples.

## Results

The mixup abstract reports that the method improves the generalisation of state-of-the-art architectures on ImageNet-2012, CIFAR-10, CIFAR-100, Google commands and UCI datasets. It also reports that mixup reduces the memorisation of corrupt labels, increases robustness to adversarial examples, and stabilises the training of generative adversarial networks.

The CutMix abstract reports that the method consistently outperforms other augmentation strategies on CIFAR and ImageNet classification. When used to pretrain a model, the CutMix-trained classifier improves detection on Pascal and captioning on MS-COCO. The abstract also reports better robustness to input corruption and better out-of-distribution detection.

## Limitations

- **Mixed images are not natural images.** Training on blends shifts the input distribution away from the one seen at test time, and the network must learn to handle both.
- **Labels depend on a mixing rule.** CutMix uses area as a proxy for how much of the label each image should contribute. The proxy is approximate when the object is small or the patch misses it.
- **Choice of \(\alpha\).** The strength of mixing is a hyperparameter, and its best value depends on the task.
- **Requires a meaningful blend.** The method assumes that combining two inputs has a sensible meaning. This holds for images and for some hidden representations, but is less clear for discrete inputs such as tokens or for structured outputs.

## Open questions

- **Why does interpolation help?** Mixup is motivated by a preference for simple, linear behaviour between examples. Verma et al. (2018) apply the same interpolation to hidden states, an approach called Manifold Mixup, and report flatter representations of each class. A complete explanation is missing.
- **What should the label be?** Whether CutMix's area-based labels should follow the content of the patch, for instance through saliency, is an open design question.
- **Beyond images.** The extension of mixing to text, audio and graphs requires choices of what to blend, and the best choices are not established.

## Connections

Mixup produces soft targets from hard labels, which links it to [label smoothing](../label-smoothing/index.md). Both reduce the confidence the network is pushed towards on training examples. Mixup and CutMix are data augmentation methods, so they sit alongside the [parent topic's](../index.md) other random perturbations, such as dropout. A survey of image augmentation is given by Shorten and Khoshgoftaar (2019). The brain has no established counterpart to blending two stimuli during learning, so the method is best understood as an engineering device. The wider links are on the [dropout](../index.md) page and in [NeuroAI](../../../../brain-mind/neuroai/index.md).

## Applications

- **Image classification.** Mixup and CutMix are used to train classifiers on CIFAR and ImageNet, the benchmarks in their papers.
- **Pretraining for detection and captioning.** The CutMix paper reports gains when a CutMix-trained classifier is used as the pretrained model for detection and captioning.
- **Robustness and generative models.** Mixup's paper reports robustness to adversarial examples and stabilisation of GAN training.

## References

### Seminal papers

- Zhang, H. et al. (2017). *mixup: Beyond Empirical Risk Minimization*. arXiv. https://arxiv.org/abs/1710.09412 — The paper itself: trains on convex combinations of pairs of examples and their labels, improving generalisation and robustness.
- Yun, S. et al. (2019). *CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features*. arXiv. https://arxiv.org/abs/1905.04899 — Pastes patches between training images and mixes the labels by patch area, as an alternative to erasing regions.
- Verma, V. et al. (2018). *Manifold Mixup: Better Representations by Interpolating Hidden States*. arXiv. https://arxiv.org/abs/1806.05236 — Applies the interpolation idea to hidden representations and reports smoother decision boundaries.

### Surveys and textbooks

- Shorten, C. & Khoshgoftaar, T. M. (2019). *A survey on Image Data Augmentation for Deep Learning*. Journal of Big Data. https://doi.org/10.1186/s40537-019-0197-0 — Surveys augmentation methods for image data, the setting in which mixup and CutMix are used.

### Articles and documentation

- Zhang, C. et al. (2016). *Understanding deep learning requires rethinking generalization*. arXiv. https://arxiv.org/abs/1611.03530 — Shows that large networks can fit random labels, which motivates the study of regularisers such as mixup.
