---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - normalising flows
  - generative models
  - density estimation
aliases:
  - 正規化流
  - 標準化流
  - Normalizing flows
  - Real NVP
  - Glow
---

# Normalising Flows

Normalising flows are generative models built from a chain of invertible, differentiable maps. Because each map can be inverted and its Jacobian determinant is cheap to compute, the exact log-likelihood of any data point and exact sampling are both available. This page covers the discrete flow family, with detailed sections on Real NVP and Glow. The family overview, with the continuous alternative, is on the [Flow-Based Models](../index.md) page, and the continuous method is on [Flow Matching](../flow-matching/index.md).

## Overview

Dinh et al. (2014) introduced the approach as NICE, which uses additive coupling layers so that the determinant is exactly one. Dinh et al. (2017) generalised the layer to affine coupling, which keeps the cheap determinant while allowing scaling, and applied it to images. Kingma and Dhariwal (2018) then added invertible 1×1 convolutions and activation normalisation to make the architecture deeper and more expressive. Rezende and Mohamed (2015) had earlier named the general framework and used flows for variational posteriors.

## Key concepts

- **Base distribution** \(p_z\): usually a standard Gaussian, from which sampling starts.
- **Invertible map** \(f\): a stack of layers whose inverse can be computed in the same cost as the forward pass.
- **Coupling layer**: splits the input into two parts, leaves one unchanged, and transforms the other with a scale and shift computed from the first.
- **Log-determinant**: the term that corrects for volume change under \(f\), added to the likelihood at every layer.
- **Multi-scale architecture**: squeezes and factors out parts of the representation at several resolutions, so that the deep layers see smaller inputs.

## How it works

For a flow \(x = f(z)\) with \(z\sim p_z\), the change of variables gives

\[
\log p_x(x) = \log p_z\big(f^{-1}(x)\big) + \log\left|\det \frac{\partial f^{-1}(x)}{\partial x}\right|
\]

Training maximises this log-likelihood averaged over the data. Sampling draws \(z\sim p_z\) and computes \(f(z)\) in one pass.

## Key methods

### Density estimation using Real NVP (Dinh, Sohl-Dickstein & Bengio, 2017)

- **Problem:** exact-likelihood generative models of images were limited to small or simple architectures, and the earlier NICE coupling did not scale to natural images.
- **Core idea:** affine coupling layers. Given an input split into \(x_A\) and \(x_B\), the output is \(y_A = x_A\) and \(y_B = x_B \odot \exp(s(x_A)) + t(x_A)\), where \(s\) and \(t\) are neural networks. The inverse is equally cheap, and the log-determinant is the sum of \(s\).
- **Equation or algorithm:** stack coupling layers, alternate which half is transformed, and apply batch normalisation and a multi-scale factoring of the representation. Train by maximum likelihood.
- **Results:** the paper reports log-likelihood results and generated images on several natural-image datasets. The abstract does not give figures, so quote the paper's own numbers when citing them.
- **Limitations:** the transformation of each dimension is constrained, and samples are less sharp than GAN samples at the time. Exact likelihood does not guarantee good samples, a point the Open questions below return to.

### Glow (Kingma & Dhariwal, 2018)

- **Problem:** flows of the time were hard to make deep and to control for high-resolution images.
- **Core idea:** use an invertible 1×1 convolution to mix channels, which replaces the fixed permutations of Real NVP and learns the mixing, and an actnorm layer for stable initialisation. Each step is actnorm, invertible 1×1 convolution, and affine coupling.
- **Equation or algorithm:** the log-determinant of the 1×1 convolution with weight matrix \(W\) over an \(h\times w\) feature map is \(h\,w\,\log\lvert\det W\rvert\). Glow stacks several such steps in a multi-scale architecture and trains by maximum likelihood.
- **Results:** the abstract reports a significant improvement in log-likelihood on standard benchmarks and realistic, efficient synthesis and manipulation of large images. It highlights latent-space manipulation, such as changing attributes by moving along learned directions. It gives no specific figures in the abstract.
- **Limitations:** the model stays expensive at high resolution, and exact likelihood does not always match perceived quality. Later architectures trade some of this exactness for expressiveness.

## Connections

- The flow formulation is one of the three generative algorithms on the [Generative Models](../../generative-models/index.md) page, next to the [VAE](../../vae/index.md) and the [GAN](../../gan/index.md).
- Flows are used as flexible posteriors in variational inference, see [probabilistic methods](../../../../probabilistic/index.md).
- Coupling layers use ordinary convolutional or dense subnetworks, see [Convolutional Networks](../../../../../models/cnn/index.md).

## Applications

Density estimation and anomaly detection, lossless and lossy compression with learned priors, and posterior approximation in Bayesian models.

## Open questions

- Matching the sample quality of diffusion and GAN models while keeping exact likelihoods.
- Whether invertibility is a real constraint on what the model can learn, or only a cost.
- Scaling to very high resolution at reasonable compute.

## References

### Seminal papers

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — Defines normalising flows as invertible transformations for flexible posteriors.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Introduces additive coupling layers with a unit Jacobian.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2017). *Density Estimation Using Real NVP*. ICLR. https://arxiv.org/abs/1605.08803 — Introduces affine coupling layers and a multi-scale architecture for images.
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS (arXiv). https://arxiv.org/abs/1807.03039 — Adds invertible 1×1 convolutions and actnorm, with latent-space manipulation of images.

### Surveys and textbooks

- Papamakarios, G., et al. (2019/2021). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Survey of flow architectures and their use in density estimation and inference.

## Further learning

- Eric Jang, *Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows*. Link: https://blog.evjang.com/2018/01/nf2.html — Accessible walkthrough of modern flow architectures and their Jacobians.
