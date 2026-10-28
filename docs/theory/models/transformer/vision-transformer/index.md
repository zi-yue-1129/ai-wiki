---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/models/cnn/backbones-and-scaling
  - theory/models/computer-vision
tags:
  - transformers
  - computer vision
  - image classification
aliases:
  - ViT
  - Vision Transformer
  - 視覺 Transformer
  - An Image is Worth 16x16 Words
---

# Vision Transformer (ViT)

The Vision Transformer, or ViT, applies a standard Transformer encoder to an image by cutting the image into fixed-size patches and treating each patch as a token. Dosovitskiy et al. (2021) showed that this pure Transformer, with no convolutional layers in the image path, can match or beat strong convolutional networks on image classification when pre-trained on enough data.

## Overview

Before ViT, attention was used in computer vision only alongside convolutions, or to replace some of their components. Convolution builds in locality and translation equivariance, which helps when data is small. ViT asks whether those built-in priors are needed if the model sees enough data. The answer, under the paper's setting, is that they are not: the model learns its own spatial structure from the position embeddings and the data.

The trade-off is that ViT has a weaker inductive bias than a CNN. It does better with more data, and when data is scarce it depends on regularisation and augmentation.

## Key concepts

- **Patch**: a \(P \times P\) square of pixels. A \(224 \times 224\) image cut into \(16 \times 16\) patches gives \(N = 196\) tokens.
- **Patch embedding**: each flattened patch is linearly projected to the model width \(D\).
- **Class token**: a learnable vector prepended to the token sequence. Its output is used as the image representation.
- **Position embedding**: a learnable 1D embedding added to each token, so the encoder knows where each patch sits.
- **Backbone variants**: named sizes such as ViT-Base (86M parameters), ViT-Large (307M) and ViT-Huge (632M), combined with a patch size, for example ViT-L/16.

## How it works

Given an image \(x \in \mathbb{R}^{H \times W \times C}\) and patch size \(P\), the image is reshaped into \(N = HW / P^2\) flattened patches \(x_p^i\). The encoder input is

\[
z_0 = \big[\, x_{\text{class}};\ x_p^1 E;\ x_p^2 E;\ \dots;\ x_p^N E \,\big] + E_{\text{pos}}
\]

where \(E\) is the patch projection and \(E_{\text{pos}}\) the position embeddings. Each of the \(L\) layers is a standard pre-norm Transformer block:

\[
z'_\ell = \mathrm{MSA}\big(\mathrm{LN}(z_{\ell-1})\big) + z_{\ell-1}, \qquad
z_\ell = \mathrm{MLP}\big(\mathrm{LN}(z'_\ell)\big) + z'_\ell
\]

The image representation is the final layer-normalised class token, \(y = \mathrm{LN}(z_L^0)\), which feeds a linear classifier. Apart from the patch projection and the position embeddings, the encoder is the same as the language Transformer.

## Key methods

### An Image is Worth 16x16 Words (Dosovitskiy et al., 2021)

- **Problem:** Transformers dominated language, but in vision attention was still used mostly alongside CNNs. The question was whether a pure Transformer could classify images well without convolutional structure.
- **Core idea:** Split the image into patches, embed each one as a token, and feed the sequence to an unmodified Transformer encoder. Scale the model and the pre-training data together.
- **Equation or algorithm:** The patch embedding, class token and layer equations above. Training is supervised classification with a linear head on the class token.
- **Results:** The abstract states that a pure Transformer "applied directly to sequences of image patches can perform very well on image classification tasks", and that when pre-trained on large data ViT "attains excellent results compared to state-of-the-art convolutional networks while requiring substantially fewer computational resources to train." In the paper's Table 2, models pre-trained on the internal JFT-300M dataset reach 88.55% top-1 on ImageNet for ViT-H/14 and 87.76% for ViT-L/16, both fine-tuned at higher resolution.
- **Limitations:** The advantage appears only with large pre-training, as the abstract's wording makes clear. The best results rely on JFT-300M, which is not public. The paper's main evidence is classification; detection and segmentation came later.

### Variants and related models

These are named methods that build on ViT, each with its own page.

- **[DeiT](deit/index.md)** (Touvron et al., 2021) trains a ViT on ImageNet alone. Its 86M-parameter reference model reaches 83.1% top-1 on ImageNet with no external data, and it adds a distillation token that learns from a teacher through attention. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877)
- **[Swin Transformer](swin/index.md)** (Liu et al., 2021) builds a hierarchical ViT that computes self-attention inside shifted local windows. Its cost is linear in image size, and it serves as a general backbone for detection and segmentation. [DOI 10.1109/ICCV48922.2021.00986](https://doi.org/10.1109/ICCV48922.2021.00986)
- **ConvNeXt** (Liu et al., 2022) goes the other way: it modernises a ResNet with Transformer-style design choices and stays a pure convolutional network. [CNN backbones and scaling](../../cnn/backbones-and-scaling/convnext/index.md)

## Components and variants

- **Pre-training data and regularisation.** The inductive bias of ViT is weak, so its results depend on data and training recipe. Steiner et al. (2022) show that more compute combined with data augmentation and regularisation ("AugReg") can match models trained on about ten times more data, and that models trained on the public ImageNet-21k can match or beat counterparts trained on JFT-300M.
- **Hierarchical and windowed attention.** [Swin](swin/index.md) and similar models trade global attention for local windows, which suits dense prediction.
- **Distillation and data-efficient training.** [DeiT](deit/index.md) shows that a convnet teacher can help a ViT learn on ImageNet alone.

## Connections

- [Transformers & Attention](../index.md) gives the attention and Transformer block that ViT reuses. The original paper is covered in [Attention Is All You Need](../attention-is-all-you-need/index.md).
- [Backbones and scaling](../../cnn/backbones-and-scaling/index.md) is the convolutional alternative that ViT is compared against, with ResNet and EfficientNet as the main references.
- [Computer vision](../../computer-vision/index.md) lists ViT among the image-classification models and covers the tasks where ViT-style backbones are used.
- [Diffusion Transformer](../dit/index.md) applies the same patch-as-token idea to latent images inside a diffusion model.
- The brain connection is indirect: the strong role of locality in convolutional models is one of the inductive biases that ViT drops, and the comparison is a way to ask which priors vision needs.

## Applications

- Image classification at scale, with pre-trained ViT models used as backbones for transfer to smaller benchmarks, as in the original paper's evaluation on ImageNet and CIFAR-100.
- Object detection and semantic segmentation with ViT-style backbones. Steiner et al. (2022) cite these tasks as places where ViTs achieve strong results.
- Official code and pre-trained checkpoints are published by Google Research. [google-research/vision_transformer](https://github.com/google-research/vision_transformer)

## Open questions

- **How much inductive bias is needed.** Models trained with more data or stronger augmentation close the gap with CNNs, but how much locality or translation equivariance a model should build in is still debated.
- **What ViTs learn.** Raghu et al. (2021) find that ViT representations are more uniform across layers than CNN representations, and that self-attention aggregates global information early. Whether that structure explains ViT's transfer behaviour is not settled.
- **Cost of global attention.** Global attention over all patches grows quadratically with the number of patches, which limits resolution. Windowed and hierarchical designs address this, but at a cost in simplicity.

## References

### Seminal papers

- Dosovitskiy, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR 2021. [arXiv:2010.11929](https://arxiv.org/abs/2010.11929) — The original ViT, showing that a pure Transformer on image patches competes with CNNs when pre-trained on large data.
- Touvron, H., et al. (2021). *Training data-efficient image transformers & distillation through attention*. ICML 2021, PMLR 139, pp. 10347–10357. [arXiv:2012.12877](https://arxiv.org/abs/2012.12877) — DeiT, which trains a ViT on ImageNet alone and adds a distillation token.
- Liu, Z., et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. ICCV 2021. [DOI 10.1109/ICCV48922.2021.00986](https://doi.org/10.1109/ICCV48922.2021.00986) — A hierarchical ViT with shifted local windows, usable as a general vision backbone.
- Steiner, A., et al. (2022). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. Transactions on Machine Learning Research. [arXiv:2106.10270](https://arxiv.org/abs/2106.10270) — A systematic study of how data, augmentation, compute and model size interact for ViT.
- Raghu, M., et al. (2021). *Do Vision Transformers See Like Convolutional Neural Networks?* [arXiv:2108.08810](https://arxiv.org/abs/2108.08810) — Compares the internal representations of ViTs and CNNs, and the role of self-attention and residual connections.
- Liu, Z., et al. (2022). *A ConvNet for the 2020s*. CVPR 2022. [DOI 10.1109/CVPR52688.2022.01167](https://doi.org/10.1109/CVPR52688.2022.01167) — ConvNeXt, a pure ConvNet that matches Transformer baselines, and the reference point for the ViT versus CNN comparison.

### Surveys and textbooks

(none checked for this page)

### Lectures

(none checked for this page)

### Articles and documentation

- Google Research, *vision_transformer*, GitHub. [google-research/vision_transformer](https://github.com/google-research/vision_transformer) — Official fine-tuning code and pre-trained ViT models, linked from the arXiv listing of the original paper.

## Further learning

(none added yet)
