---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
  - theory/models/cnn/backbones-and-scaling
tags:
  - transformers
  - computer vision
  - knowledge distillation
  - data efficiency
aliases:
  - DeiT
  - Data-efficient image Transformer
  - 資料高效影像 Transformer
---

# DeiT: Training data-efficient image transformers

DeiT, or Data-efficient image Transformer, trains a [Vision Transformer](../index.md) on ImageNet-1K alone. It adds a distillation token, which lets the Transformer learn from a convolutional teacher through attention. Touvron et al. (2021) show that a competitive ViT can be trained in under three days on a single machine, with no external pre-training data.

## Overview

The [original ViT](../index.md) reached its best results only after pre-training on hundreds of millions of images, on infrastructure that most groups do not have. DeiT asks whether the same architecture can be trained on ImageNet alone if the training recipe and the teacher make up for the missing data. The paper keeps the ViT architecture and changes two things: a heavy augmentation and regularisation recipe, and a distillation token.

## Key concepts

- **Distillation**: training a student network to match the outputs of a stronger teacher, here a labelled image classifier.
- **Distillation token**: a second learnable token, appended next to the class token, whose output is trained to predict the teacher's label.
- **Hard-label distillation**: the teacher's predicted class is used as a hard target, rather than its full probability vector.
- **Model variants**: DeiT-Ti (5M parameters), DeiT-S (22M) and DeiT-B (86M), at 224 resolution unless stated.

## How it works

The input to the encoder is the patch embeddings with two extra tokens, the class token and the distillation token. Each token has its own output head. The class head is trained against the true label \(y\). The distillation head is trained against the teacher's hard label \(y_t\), and the training loss is the equal-weight sum of the two cross-entropy terms:

\[
\mathcal{L} = \tfrac{1}{2}\,\mathrm{CE}\big(\psi(z^{\text{cls}}_L),\, y\big) + \tfrac{1}{2}\,\mathrm{CE}\big(\psi(z^{\text{dist}}_L),\, y_t\big)
\]

Here \(\psi\) is the linear classifier and \(y_t = \arg\max_c Z_t(c)\) is the teacher's predicted class. At test time the paper's main method fuses the two heads by adding their softmax outputs. The distillation token attends to the same patches as the class token, so the teacher's signal reaches the student through the attention layers.

## Key methods

### Training data-efficient image transformers & distillation through attention (Touvron et al., 2021)

- **Problem:** ViTs needed hundreds of millions of pre-training images and expensive infrastructure, which limited their adoption. The question was whether a convolution-free transformer could be competitive on ImageNet-1K alone.
- **Core idea:** Keep the ViT architecture, add a distillation token trained on a convnet teacher's labels, and use a strong augmentation and regularisation recipe to compensate for the smaller dataset.
- **Equation or algorithm:** The two-head cross-entropy loss above, with a teacher's hard label. The training recipe, in the paper's Table 9, uses AdamW with a learning rate of \(5\times10^{-4}\) scaled by batch size over 512, weight decay 0.05, cosine decay, a batch size of 1024 and 300 epochs.
- **Results:** The abstract states that the reference 86M-parameter model reaches 83.1% top-1 accuracy (single-crop) on ImageNet with no external data, and that the paper's teacher-student setup reaches up to 85.2%. Table 3 of the paper gives 72.2%, 79.8% and 81.8% for DeiT-Ti, DeiT-S and DeiT-B at 224 without distillation. With distillation, the same models reach 74.5%, 81.2% and 83.4%.
- **Limitations:** The distillation gain is largest when the teacher is a convnet, as the abstract notes. The distilled models depend on a strong teacher, which here is a RegNetY-16GF with 84M parameters. The recipe is heavy, with RandAugment, Mixup, CutMix, random erasing, stochastic depth and repeated augmentation, so the data-efficiency claim depends on that recipe.

## Components and variants

- **Augmentation and regularisation.** Table 9 of the paper lists RandAugment (9, 0.5), Mixup with probability 0.8, CutMix with probability 1.0, random erasing with probability 0.25, stochastic depth at 0.1 and label smoothing at 0.1. The authors also use repeated augmentation, and exclude dropout.
- **Teacher choice.** The paper compares teachers, and its convnet teacher gives the largest gains. A transformer teacher gives smaller gains.
- **Higher resolution.** Fine-tuning at 384 resolution lifts DeiT-B to 83.1% without distillation. With distillation and longer training the best reported result is 85.2%.

## Connections

- [Vision Transformer (ViT)](../index.md) is the architecture that DeiT keeps. DeiT changes the training recipe and adds the distillation token.
- [Transformers & Attention](../../index.md) gives the attention block that both models use.
- [ConvNeXt](../../../cnn/backbones-and-scaling/convnext/index.md) is a convnet that matches Transformer baselines, and is the kind of teacher that helps DeiT most.
- [Computer vision](../../../computer-vision/index.md) covers the image-classification models where DeiT is used as a backbone.

## Open questions

- **Teacher dependence.** Distillation adds a second network and a teacher training cost. Whether self-supervised pre-training on unlabelled ImageNet gives the same benefit without a teacher is a practical question.
- **Recipe versus architecture.** Much of the gain comes from augmentation and regularisation, so the contribution of the distillation token alone is hard to separate from the recipe.
- **Scaling beyond ImageNet.** The paper's claims are for ImageNet-1K, and transfer to other tasks is shown only briefly.

## References

### Seminal papers

- Touvron, H., et al. (2021). *Training data-efficient image transformers & distillation through attention*. ICML 2021, PMLR 139, pp. 10347–10357. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877) — Introduces DeiT, which trains a ViT on ImageNet alone with a distillation token.
- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) — The ViT architecture that DeiT keeps.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. [arXiv:1503.02531](https://arxiv.org/abs/1503.02531) — Introduces knowledge distillation, which the distillation token builds on.
- Steiner, A., et al. (2022). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. Transactions on Machine Learning Research. [arXiv:2106.10270](https://arxiv.org/abs/2106.10270) — Studies how augmentation and regularisation trade off against data for ViTs, the same recipe question that DeiT addresses.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

- Facebook Research, *DeiT*, GitHub. [facebookresearch/deit](https://github.com/facebookresearch/deit) — The official DeiT repository with evaluation and training code and pre-trained models. The repository is archived and also covers related papers.

## Further learning

(none added yet)
