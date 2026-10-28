---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - normalising flows
  - generative models
  - density estimation
aliases:
  - Glow
  - Generative flow with invertible 1x1 convolutions
  - Glow 生成流
---

# Glow

Glow is a normalising flow that replaces the fixed channel permutations of [Real NVP](realnvp.md) with learned invertible 1×1 convolutions. It adds actnorm for stable initialisation, and it shows that flows can generate and manipulate large face images. It belongs to the [Normalising Flows](index.md) family.

## Overview

Kingma and Dhariwal (2018) build a deeper flow out of the Real NVP coupling layer. Their two additions are a learned channel mixing step and a data-dependent normalisation layer. They report better likelihood than Real NVP on several natural-image datasets and show that the learned latent space supports smooth interpolation and attribute editing.

## Key concepts

- **Actnorm**: a per-channel scale and bias, initialised from the first minibatch so that each channel has zero mean and unit variance. After initialisation it is trained like any other parameter.
- **Invertible 1×1 convolution**: a learned channel-mixing matrix \(W\). It replaces the fixed permutation of Real NVP, and it is initialised as a random rotation, so its log-determinant starts at zero.
- **LU decomposition**: writing \(W\) in LU form reduces the cost of its log-determinant from cubic to linear in the number of channels.
- **Zero-initialised coupling**: the last convolution of each coupling network starts at zero, so every coupling layer begins as the identity.

## How it works

One flow step is actnorm, then an invertible 1×1 convolution, then an affine coupling layer. For an \(h \times w\) feature map, the 1×1 convolution contributes \(h\,w\,\log\lvert\det W\rvert\) to the log-determinant. Steps are stacked in the same multi-scale design as Real NVP, with squeezing and factoring out at each scale. Training maximises the exact log-likelihood.

## Key methods

### Glow (Kingma & Dhariwal, 2018)

- **Problem:** flows of the time were hard to make deep, and they were difficult to control for high-resolution images.
- **Core idea:** learn the channel mixing with an invertible 1×1 convolution, and normalise activations with actnorm, so that deep stacks train reliably. Each step keeps the cheap log-determinant of a coupling flow.
- **Equation or algorithm:** the step structure and the 1×1 log-determinant above, with the multi-scale architecture of Real NVP. Each step is actnorm, invertible 1×1 convolution, and affine coupling.
- **Results:** in the paper's Table 2, bits per dimension is lower than Real NVP on every dataset shown. For example, CIFAR-10 is 3.35 against 3.49, LSUN bedroom is 2.38 against 2.72, and ImageNet 32×32 is 4.09 against 4.28. Table 3 in the appendix reports 5-bit results, including 1.03 bits per dimension on CelebA-HQ at 256×256, which is on a different bit depth and is not directly comparable with the 8-bit tables. The paper also shows interpolation and attribute editing in the latent space, with attribute directions computed from labelled images after training.
- **Limitations:** the model is expensive at high resolution. Likelihood does not guarantee perceptual quality. The 5-bit results cannot be compared with the 8-bit results without care.

## Connections

- [Real NVP](realnvp.md) is the coupling-layer design that Glow extends.
- The likelihood and the normalising-flow framework are on the [Normalising Flows](index.md) overview.
- Flows for continuous time are a different approach, see [Flow Matching](../flow-matching/index.md).
- The coupling networks are convolutional for images, see [Convolutional Networks](../../../../../models/cnn/index.md).

## Applications

High-resolution image synthesis with exact likelihood, and latent-space editing of faces through learned attribute directions.

## Open questions

- Whether learned channel mixing gives a real advantage over fixed permutations at larger scales.
- How to reduce the cost of deep flows at high resolution.
- Whether latent-space editing with flows is as reliable as with GAN or diffusion editing.

## References

### Seminal papers

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS (arXiv). https://arxiv.org/abs/1807.03039 — Introduces actnorm and invertible 1×1 convolutions in a multi-scale flow, the method on this page.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR (arXiv). https://arxiv.org/abs/1605.08803 — Introduces affine coupling layers and the multi-scale architecture that Glow builds on.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Introduces the additive coupling layer, the origin of this family.
- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — Defines normalising flows as a general class of invertible transformations.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — A survey of flow architectures, including the Glow design, and their use in density estimation.

## Further learning

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*. Link: https://blog.evjang.com/2018/01/nf2.html — An accessible walkthrough of modern flow architectures.
