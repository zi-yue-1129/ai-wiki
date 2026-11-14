---
status: complete
last_reviewed: 2026-11-14
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

MLP-Mixer classifies images by alternating two multilayer perceptrons (MLPs). One exchanges information across image patches and the other across feature channels. The architecture also includes patch projection, normalisation, residual connections and a classifier. [Multilayer perceptrons](index.md).[^mixer]

## Overview

An image of height $H$ and width $W$ is split into non-overlapping square patches of side $P$, assuming both dimensions are divisible by $P$. A shared linear projection maps each flattened patch to $C$ features. The resulting table $X\in\mathbb{R}^{S\times C}$ has $S=HW/P^2$ rows. Each row is a patch token. This representation is also used by the Vision Transformer. [Vision Transformer](../transformer/vision-transformer/index.md).[^mixer][^vit]

## Problem

A patch representation needs a way for distant locations to exchange information. The Mixer paper tests whether dense transformations over patch positions, paired with per-patch feature transformations, can support image classification at scale.[^mixer]

## Core idea

**Token mixing** applies the same MLP to each column of $X$. Its weights are shared across channels and indexed by patch position. The learned position weights are fixed at inference, while the activations depend on the image. The architecture therefore uses the ordering of the patches directly.[^mixer]

**Channel mixing** applies the same MLP to each row. It combines features within one patch and shares its weights across patch positions. After the final Mixer layer and normalisation, the head averages the patch representations and applies a linear classifier.[^mixer]

## Algorithm

Let $D_S$ and $D_C$ be the hidden widths of the token and channel MLPs. Layer normalisation $\mathrm{LN}$ acts across the $C$ channels of each patch before each MLP. With biases omitted, $\sigma$ denoting GELU, and the channel vectors written as columns, the updates are as follows. [GELU](gelu/index.md), [Layer normalisation](layer-normalisation/index.md).[^mixer][^gelu][^ln]

$$
\begin{aligned}
U_{:,i} &= X_{:,i}+W_2\,\sigma\!\left(W_1\,\mathrm{LN}(X)_{:,i}\right),\\
Y_{j,:}^{\top} &= U_{j,:}^{\top}+W_4\,\sigma\!\left(W_3\,\mathrm{LN}(U)_{j,:}^{\top}\right).
\end{aligned}
$$

The first equation applies for $i=1,\ldots,C$ and the second for $j=1,\ldots,S$. Both residual outputs have shape $S\times C$. The four weight matrices have the following dimensions.[^mixer]

$$
W_1\in\mathbb{R}^{D_S\times S},\quad
W_2\in\mathbb{R}^{S\times D_S},\quad
W_3\in\mathbb{R}^{D_C\times C},\quad
W_4\in\mathbb{R}^{C\times D_C}.
$$

For a small shape example, set $S=4$, $C=3$, $D_S=2$ and $D_C=5$. The token MLP maps $4\to2\to4$ three times, once per channel. The channel MLP maps $3\to5\to3$ four times, once per patch. The same matrix pair is reused each time within its respective MLP.

The dense multiplications cost $2CSD_S$ and $2SCD_C$ multiply-accumulates per layer per image, excluding bias, normalisation and activation. The cost is linear in $S$ when $C$, $D_S$ and $D_C$ stay fixed. With $P=16$, increasing a square input from $224\times224$ to $448\times448$ takes the patch count from $196$ to $784$. Both token-mixing matrices must accommodate the new count. The paper's higher-resolution recipe also widens $D_S$ in proportion to $S$, copies the pre-trained matrices into diagonal blocks of the larger matrices, and fine-tunes the result.[^mixer]

## Key results

The paper reports top-1 accuracy on the original ImageNet validation labels. The rows below specify the pre-training data and fine-tuning input size.[^mixer]

| Model | Pre-training data | Input size | Top-1 | Source |
| --- | --- | --- | --- | --- |
| Mixer-B/16 | ImageNet with extra regularisation | 224 | 76.44% | Table 3 |
| Mixer-B/16 | ImageNet-21k with extra regularisation | 224 | 80.64% | Table 3 |
| Mixer-L/16 | ImageNet-21k with extra regularisation | 224 | 82.89% | Table 3 |
| Mixer-L/16 | ImageNet-21k with extra regularisation | 448 | 83.91% | Table 3 |
| Mixer-L/16 | ImageNet-21k | 448 | 84.15% | Table 2 |
| Mixer-H/14 | JFT-300M | 448 | 87.94% | Table 2 |

Table 3 averages three fine-tuning runs. Section 3.1 separately quotes 82.84% for the 224-pixel Mixer-L/16 result. The table above retains the value from Table 3 for that row. The 84.15% figure comes from the separate Table 2 comparison.[^mixer]

## Limitations

- Token mixing is tied to the number and ordering of patches. Changing the resolution at fixed patch size requires adjusting that sublayer's dimensions.[^mixer]
- Accuracy and throughput depend on the training data, regularisation, model size and input resolution. The original experiments report overfitting when training Mixer from scratch on ImageNet, and stronger accuracy with larger pre-training datasets.[^mixer]

## Connections

ResMLP uses a linear cross-patch layer and a channel MLP. gMLP mixes positions through a spatial gating unit. Both explore how to combine spatial interaction with per-token feature transformations. [ResMLP paper](https://arxiv.org/abs/2105.03404), [gMLP paper](https://arxiv.org/abs/2105.08050).[^resmlp][^gmlp]

## Applications

The paper evaluates image classification and transfer to other classification datasets, including CIFAR and the VTAB-1k tasks. [Computer vision](../computer-vision/index.md).[^mixer]

[^mixer]: Tolstikhin et al., [*MLP-Mixer*](https://arxiv.org/html/2105.01601), §§2–3 and Appendix C.
[^vit]: Dosovitskiy et al., [*An Image is Worth 16x16 Words*](https://arxiv.org/abs/2010.11929), §3.1.
[^gelu]: Hendrycks and Gimpel, [*Gaussian Error Linear Units*](https://arxiv.org/abs/1606.08415), §2.
[^ln]: Ba et al., [*Layer Normalization*](https://arxiv.org/abs/1607.06450), §3.
[^resmlp]: Touvron et al., [*ResMLP*](https://arxiv.org/abs/2105.03404), §2.
[^gmlp]: Liu et al., [*Pay Attention to MLPs*](https://arxiv.org/abs/2105.08050), §2.

## References

### Seminal papers

- Tolstikhin, I., Houlsby, N., Kolesnikov, A., et al. (2021). *MLP-Mixer: An all-MLP Architecture for Vision*. NeurIPS. https://arxiv.org/abs/2105.01601 — Defines the two mixing operations and reports the ImageNet experiments.
- Dosovitskiy, A., Beyer, L., Kolesnikov, A., et al. (2021). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. ICLR. https://arxiv.org/abs/2010.11929 — Introduces a vision Transformer built on image patch embeddings.
- Hendrycks, D. & Gimpel, K. (2016). *Gaussian Error Linear Units (GELUs)*. https://arxiv.org/abs/1606.08415 — Defines the elementwise activation used inside the Mixer MLPs.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). *Layer Normalization*. https://arxiv.org/abs/1607.06450 — Derives normalisation from the features of a single example.
- Touvron, H., Bojanowski, P., Caron, M., et al. (2021). *ResMLP: Feedforward Networks for Image Classification with Data-Efficient Training*. https://arxiv.org/abs/2105.03404 — Uses a linear cross-patch layer alongside a channel MLP.
- Liu, H., Dai, Z., So, D. R. & Le, Q. V. (2021). *Pay Attention to MLPs*. https://arxiv.org/abs/2105.08050 — Introduces gMLP and its spatial gating unit for token interaction.
