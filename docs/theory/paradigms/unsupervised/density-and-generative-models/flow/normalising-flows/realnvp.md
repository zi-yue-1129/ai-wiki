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
  - Real NVP
  - Real-valued non-volume preserving
  - 實值非體積守恆
---

# Real NVP

Real NVP is a normalising flow built from affine coupling layers. It makes exact-likelihood training and sampling practical for natural images. It belongs to the [Normalising Flows](index.md) family, and its predecessor, the additive coupling model NICE, is described in the references.

## Overview

Dinh, Sohl-Dickstein and Bengio (2017) extend the coupling idea of NICE. Instead of adding a function of half the input, they scale and shift the other half with networks of the first half. The layer stays invertible with a cheap Jacobian, and a multi-scale architecture lets the model work on natural images at several resolutions.

## Key concepts

- **Affine coupling layer**: keeps one part of the input unchanged and transforms the other part with a learned scale and shift that depend only on the unchanged part.
- **Masks**: a checkerboard mask splits an image by spatial position, and a channel mask splits it by channel. Alternating the masks lets every dimension be transformed.
- **Squeezing**: trades spatial size for channels, turning an \(s \times s \times c\) tensor into \(\frac{s}{2} \times \frac{s}{2} \times 4c\).
- **Factoring out**: removes half of the dimensions at regular intervals, so that later layers work on smaller inputs.

## How it works

Split the input \(x\) into \(x_{1:d}\) and \(x_{d+1:D}\). The layer computes

\[
y_{1:d} = x_{1:d}, \qquad y_{d+1:D} = x_{d+1:D} \odot \exp\big(s(x_{1:d})\big) + t(x_{1:d})
\]

The inverse is \(x_{d+1:D} = (y_{d+1:D} - t(y_{1:d})) \odot \exp(-s(y_{1:d}))\). Because the first part is copied unchanged, \(s\) and \(t\) can be arbitrary neural networks, and they need not be invertible themselves. The Jacobian is triangular, so its log-determinant is the sum \(\sum_j s(x_{1:d})_j\).

Each scale applies three coupling layers with alternating checkerboard masks, squeezes, applies three more with channel masks, and factors out half of the dimensions. The final scale applies four checkerboard coupling layers. Training maximises the change-of-variables log-likelihood on the data.

### Visual walkthrough: one affine coupling layer

![Four-stage Real NVP affine coupling animation: split input, condition on the unchanged channel, transform the other channel and invert the mapping.](../../../../../../assets/concept-animations/realnvp-affine-coupling-motion.svg)

[Static Real NVP coupling overview for GitHub](../../../../../../assets/concept-animations/realnvp-affine-coupling-still.svg)

The four stages are **Split → Condition → Transform → Invert**. In this one-dimensional-per-part **worked example**, \(x_A=0.5\), \(x_B=1\), and the conditioning network is *assumed* to output \(s(x_A)=\ln 2\) and \(t(x_A)=-0.5\). The layer copies \(y_A=x_A=0.5\) and produces \(y_B=\exp(\ln 2)\cdot 1-0.5=1.5\). Its inverse recovers \(x_B=(1.5+0.5)/2=1\). The triangular Jacobian gives \(\log|\det J|=\ln 2\) for this example; it does **not** require differentiating through the conditioning network to compute that determinant. Later coupling layers alternate the unchanged and transformed subsets.

These numbers are **chosen for teaching, not trained-network outputs or empirical likelihood results**. On MkDocs, use the keyboard-accessible **Play/Pause** control; the linked static overview remains readable in GitHub Markdown. Original illustration, **CC BY-SA 4.0**. The layer follows Dinh, Sohl-Dickstein and Bengio (2017), cited below.

## Key methods

### Density estimation using Real NVP (Dinh et al., 2017)

- **Problem:** exact-likelihood generative models of images had been limited to small or simple architectures, and the additive coupling of NICE did not scale to natural images.
- **Core idea:** make the coupling layer affine, with a learned scale and shift, and stack it in a multi-scale architecture so the transform is expressive yet keeps a cheap log-determinant.
- **Equation or algorithm:** the forward and inverse equations above, with the log-determinant \(\sum_j s(x_{1:d})_j\). Masks alternate across layers, and the multi-scale squeeze and factor-out steps are applied as described under How it works.
- **Results:** the paper's Table 1 reports test or validation bits per dimension, for example 3.49 on CIFAR-10 (test) and 3.02 on CelebA (validation). The text says the model is competitive but does not improve on the PixelRNN baseline in bits per dimension. Check the paper's Table 1 for the full set.
- **Limitations:** the model does not beat the autoregressive PixelRNN baseline on likelihood, and the paper's comparisons are on likelihood, not sample quality. Each layer leaves half of the dimensions unchanged, so fine-grained transforms need many layers.

## Connections

- [Glow](glow.md) builds on this design, replacing the fixed channel masks with learned invertible 1×1 convolutions.
- The scale and shift networks are ordinary neural networks, usually convolutional for images, see [Convolutional Networks](../../../../../models/cnn/index.md).
- The likelihood is the same change-of-variables formula used in the [flow overview](../index.md).

## Applications

Density estimation on natural images, anomaly detection using the exact likelihood, and learned priors for compression.

## Open questions

- Whether exact likelihood on images tracks perceptual quality, and how much sample quality is lost to the architecture.
- How to make coupling layers more expressive without increasing the cost of the Jacobian.

## References

### Seminal papers

- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR (arXiv). https://arxiv.org/abs/1605.08803 — Introduces affine coupling layers and the multi-scale architecture for images, the method on this page.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Introduces additive coupling layers with a unit Jacobian, the predecessor of this method.
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS (arXiv). https://arxiv.org/abs/1807.03039 — Replaces the fixed channel masks with learned invertible 1×1 convolutions.
- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — Defines normalising flows as a general class of invertible transformations.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — A survey of flow architectures, including coupling layers, and their use in density estimation.

## Further learning

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*. Link: https://blog.evjang.com/2018/01/nf2.html — An accessible walkthrough of coupling layers and their Jacobians.
