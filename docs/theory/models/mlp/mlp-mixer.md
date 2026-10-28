---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
  - theory/models/computer-vision
tags:
  - multilayer perceptrons
  - vision
  - architecture
aliases:
  - MLP-Mixer
  - 全 MLP 架構
  - MLP 混合器
---

# MLP-Mixer

MLP-Mixer is an image classifier built only from multilayer perceptrons (MLPs). It uses no convolutions and no attention. Tolstikhin et al. (2021) showed that such a network can reach competitive accuracy on image benchmarks when trained on large data or with modern regularisation. The parent overview is [Multilayer perceptrons](index.md).

## Overview

Like the [Vision Transformer](../transformer/vision-transformer/index.md), MLP-Mixer cuts the image into non-overlapping patches and projects each one to a vector. It then alternates two kinds of MLP over this set of patch vectors. The difference from the Transformer is that the mixing across patches is done by a fixed MLP, not by attention.

## Problem

Convolutions and attention are both common in computer vision, and each carries an assumption about the input. The paper asks whether either is necessary: whether a network built only from MLPs can classify images well at a comparable cost.

## Core idea

Separate the two kinds of mixing that a vision model needs. A token-mixing MLP mixes information across patches, so it carries spatial information. A channel-mixing MLP mixes information across the features of each patch. Stacking these two kinds of layer gives the whole network.

## Algorithm

The image is split into \(S\) patches, each projected to \(C\) channels, giving a table \(X\) of size \(S \times C\). Each Mixer layer applies two residual MLP blocks with GELU nonlinearity \(\sigma\):

\[
U_{*,i} = X_{*,i} + W_2\, \sigma\!\big(W_1\, \mathrm{LayerNorm}(X)_{*,i}\big), \qquad i = 1, \ldots, C,
\]

\[
Y_{j,*} = U_{j,*} + W_4\, \sigma\!\big(W_3\, \mathrm{LayerNorm}(U)_{j,*}\big), \qquad j = 1, \ldots, S.
\]

The first equation is the token-mixing block: the MLP runs over the \(S\) patches of each channel. The second is the channel-mixing block: the MLP runs over the \(C\) channels of each patch. The paper states these equations in Section 2, using \(\sigma\) for the element-wise GELU.

## Key results

The paper reports ImageNet top-1 accuracy in two tables:

- **ImageNet-21k pre-training, with extra regularisation** (Table 3): Mixer-B/16 reaches 80.64% and Mixer-L/16 reaches 82.89%, both at 224 resolution.
- **ImageNet-21k pre-training, public checkpoint** (Table 2): Mixer-L/16 reaches 84.15% after fine-tuning at 448 resolution.

The text quotes 82.84% for Mixer-L/16 at 224 resolution, while Table 3 gives 82.89%. This page uses the table value. The paper describes these scores as competitive, with pre-training and inference cost comparable to state-of-the-art models.

## Limitations

- The abstract says the model reaches competitive scores when trained on large datasets or with modern regularisation schemes. Without either, the paper makes no claim of competitive accuracy.
- The token-mixing weights are sized to the number of patches, so changing the input resolution changes the layer shapes. The paper's higher-resolution results come from fine-tuning at the new resolution.
- Cost is described as comparable to state-of-the-art models, not lower. The architecture does not remove the compute cost of large pre-training.

## Connections

- [Vision Transformer](../transformer/vision-transformer/index.md) is the attention-based model with the same patch front end. The comparison isolates the effect of replacing attention with a fixed MLP.
- [Multilayer perceptrons](index.md) is the overview where MLP-Mixer sits beside [GELU](gelu/index.md) and [layer normalisation](layer-normalisation/index.md), the two components it uses.
- [Computer vision](../computer-vision/index.md) covers the tasks where patch-based classifiers are applied.

## Applications

- Image classification on ImageNet, the benchmark used in the paper.
- Transfer of large-scale pre-trained vision models to downstream image tasks.

## Open questions

- Is the gain from the two mixing operations themselves, or from the scale of pre-training data the paper uses?
- How well does a fixed token-mixing MLP handle inputs whose size varies, as in detection and segmentation?

## References

### Seminal papers

- Tolstikhin, I., Houlsby, N., Kolesnikov, A., et al. (2021). *MLP-Mixer: An all-MLP Architecture for Vision*. NeurIPS 2021. https://proceedings.neurips.cc/paper/2021/hash/cba0a4ee5ccd02fda0fe3f9a3e7b89fe-Abstract.html — Introduces MLP-Mixer and its token-mixing and channel-mixing blocks. Checked: NeurIPS proceedings entry; arXiv 2105.01601 matches the author list.
- Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — The Vision Transformer, which uses the same patch front end with attention in place of the mixing MLP. Checked: arXiv metadata.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS 2017. https://proceedings.neurips.cc/paper/7181-attention-is-all-you-need — The attention architecture that MLP-Mixer replaces in its mixing step. Checked: NeurIPS proceedings entry.
- Hendrycks, D. & Gimpel, K. (2016). *Gaussian Error Linear Units (GELUs)*. arXiv. https://arxiv.org/abs/1606.08415 — The GELU activation that the Mixer uses. Checked: arXiv metadata.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. arXiv. https://arxiv.org/abs/1607.06450 — The normalisation applied before each MLP block. Checked: arXiv metadata.

### Surveys and textbooks

- Liu, H., Dai, Z., So, D. R. & Le, Q. V. (2021). *Pay Attention to MLPs*. arXiv. https://arxiv.org/abs/2105.08050 — A contemporaneous MLP-only vision model with a spatial gating unit, for comparison. Checked: arXiv metadata.
