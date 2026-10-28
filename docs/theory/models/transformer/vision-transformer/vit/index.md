---
status: draft
last_reviewed: 2026-10-28
tags:
  - computer vision
  - architecture
  - transfer learning
aliases:
  - An Image is Worth 16x16 Words
  - ViT-L/16
  - 16x16 Words
  - 視覺 Transformer 原始論文
---

# ViT: an image is worth 16x16 words (Dosovitskiy et al., 2020)

ViT is a Transformer encoder applied to a sequence of image patches, trained with a supervised classification loss. It is the landmark method of the [Vision Transformer](../index.md) topic, and it shows that convolution is not needed for state-of-the-art image classification when pre-training data is large.

## Overview

Before ViT, Transformers in vision were mostly used alongside convolutions. The paper asks whether a plain Transformer, with almost no image-specific structure, can classify images. Its answer is yes, provided the model is pre-trained on enough data. The paper describes the model as close to the NLP Transformer of [Attention Is All You Need](../../attention-is-all-you-need/index.md), so that existing large-scale implementations can be used.

## Key concepts

- **Patch sequence**: the image is cut into N = HW/P² non-overlapping patches. Each one is flattened and linearly projected to width D.
- **Class token**: a learned vector prepended to the sequence, borrowed from BERT. Its final state gives the image representation.
- **Learned 1D position embeddings**: the paper uses standard learned embeddings, not 2D-aware ones, because the 2D variants gave no clear gain.
- **Inductive bias**: locality and translation equivariance appear only in the patch cut and in the MLP blocks. Self-attention is global in every layer, so the model must learn spatial structure from data.

## How it works

The model takes an H × W × C image and a patch size P, and runs the following steps:

1. Form the sequence [x_class; x_p¹E; …; x_pᴺE] + E_pos, where E projects each patch to width D.
2. For each of L layers, apply multi-head self-attention to LN(z), add a residual connection, then apply an MLP with a GELU, again with layer normalisation and a residual.
3. Take LN(z_L⁰), the class token after the last layer, as the image representation y.
4. Pre-train with a classification head, which has one hidden layer. Fine-tune by replacing the head with a single zero-initialised linear layer.

The paper defines three sizes that follow BERT: Base with 12 layers, width 768 and 86M parameters; Large with 24 layers, width 1024 and 307M parameters; and Huge with 32 layers, width 1280 and 632M parameters. Models are named by size and patch size, so ViT-L/16 is Large with 16 × 16 patches. Fine-tuning at higher resolution keeps the patch size, and the position embeddings are interpolated in 2D to the new grid.

## Results

The main comparison in Table 2 of the paper uses top-1 accuracy on ImageNet, CIFAR-100 and the 19-task VTAB suite. The figures below are the paper's reported means.

| Model (pre-training data) | ImageNet | CIFAR-100 | VTAB (19 tasks) | TPUv3-core-days |
|---|---|---|---|---|
| ViT-H/14 (JFT-300M) | 88.55 | 94.55 | 77.63 | 2.5k |
| ViT-L/16 (JFT-300M) | 87.76 | 93.90 | 76.28 | 0.68k |
| BiT-L, ResNet152x4 (JFT-300M) | 87.54 | 93.51 | 76.29 | 9.9k |
| ViT-L/16 (ImageNet-21K) | 85.30 | 93.25 | 72.72 | 0.23k |

The ViT-L/16 model pre-trained on JFT-300M matches or exceeds the ResNet baseline on these benchmarks at a fraction of the pre-training compute. On ImageNet alone, the ViT models trail comparable ResNets, and the gap closes only as the pre-training set grows. On average over five datasets, ViT reaches the same performance with about two to four times less compute than ResNets. The paper also reports that some attention heads cover much of the image already in the lowest layers, which the authors take as evidence that the model uses global context early.

## Limitations

- **Data demand.** Without large pre-training, ViT overfits more than a ResNet of similar cost. The strongest results rely on JFT-300M, which is not publicly available (Steiner et al., 2021).
- **Single-resolution features.** The paper's conclusion names detection and segmentation as open challenges for plain ViT. The later [Swin](../swin/index.md) design addresses this.
- **Self-supervision gap.** The authors' masked-patch experiments improve on training from scratch, but the paper reports a large gap to supervised pre-training.
- **Cost of smaller patches.** The token count grows with the inverse square of patch size, so accuracy gains from smaller patches come with a compute cost.

## Open questions

- Whether the gap at small data sizes closes with better training recipes, a question the [DeiT](../deit/index.md) results later address.
- Whether ViT's global attention is an advantage in general or only at scale, given that hybrid models do better at small budgets.
- How far the attention patterns learned by ViT match those learned by CNNs.

## References

### Seminal papers

- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv; ICLR 2021. https://arxiv.org/abs/2010.11929 — The original paper, defining ViT and its pre-training and transfer experiments.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — The Transformer encoder that ViT follows almost exactly.
- Sun, C., et al. (2017). *Revisiting Unreasonable Effectiveness of Data in Deep Learning Era*. arXiv. https://arxiv.org/abs/1707.02968 — Measures vision performance across training set sizes up to JFT-300M, the dataset ViT relies on.
- Kolesnikov, A., et al. (2019). *Big Transfer (BiT): General Visual Representation Learning*. arXiv; ECCV 2020. https://arxiv.org/abs/1912.11370 — The large ResNet transfer recipe that ViT is compared against in Table 2.

### Articles and documentation

- Cordonnier, J.-B., et al. (2020). *On the Relationship between Self-Attention and Convolutional Layers*. arXiv. https://arxiv.org/abs/1911.03584 — A closely related model with 2×2 patches and full self-attention, which the ViT paper discusses.
- Steiner, A., et al. (2021). *How to train your ViT? Data, Augmentation, and Regularization in Vision Transformers*. arXiv. https://arxiv.org/abs/2106.10270 — Shows that augmentation and regularisation can partly replace the data that ViT was first trained on.
- Zhai, X., et al. (2021). *Scaling Vision Transformers*. arXiv. https://arxiv.org/abs/2106.04560 — Characterises how ViT error relates to data, compute and model size.
