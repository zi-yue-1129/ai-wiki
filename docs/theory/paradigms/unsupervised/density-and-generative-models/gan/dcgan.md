---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - generative models
  - convolutional networks
  - unsupervised learning
aliases:
  - DCGAN
  - Deep convolutional GAN
  - 深度卷積生成對抗網路
---

# Deep Convolutional GAN (DCGAN)

DCGAN is a set of architectural rules for building a GAN from convolutional layers, so that training on images is stable. It is the standard starting point for image GANs, and the [GAN overview](index.md) lists it alongside the Wasserstein variants.

## Overview

GANs of the time were hard to train on images, and convolutional architectures were rarely used in them. Radford, Metz and Chintala (2016) found a combination of convolutional design choices that trained reliably across several image datasets, and they used the learned features for unsupervised representation learning.

## Key concepts

- **Strided convolution**: the discriminator downsamples with learned strided convolutions in place of pooling.
- **Fractional-strided (transposed) convolution**: the generator upsamples with learned layers instead of fixed interpolation.
- **Batch normalisation**: applied in both networks, except at the generator's output and the discriminator's input.
- **LeakyReLU and ReLU**: the discriminator uses LeakyReLU with slope 0.2, and the generator uses ReLU, with tanh at the output.

## How it works

The generator takes a noise vector \(z\) (sampled uniformly in the paper), projects it to a small spatial grid, and applies a stack of transposed convolutions to reach a 64 by 64 image. The discriminator mirrors this with strided convolutions and ends in a single sigmoid unit. The paper removes fully connected hidden layers and pooling layers in favour of strided and fractional-strided convolutions.

The training objective is the original minimax GAN loss from Goodfellow et al. (2014), with the non-saturating generator update. The paper uses Adam with a learning rate of 0.0002 and \(\beta_1 = 0.5\). The authors found the suggested learning rate of 0.001 too high, and the default momentum of 0.9 caused oscillation.

## Key methods

DCGAN is a recipe for the convolutional GAN, not a separate training objective. It is compared with the other GAN variants on the [GAN overview](index.md). Its neighbours in the family are [WGAN](wgan.md) and [WGAN-GP](wgan-gp.md), which change the objective rather than the architecture.

### Deep Convolutional GAN (Radford et al., 2016)

- **Problem:** the original GAN used fully connected networks and was unstable on images. Earlier convolutional attempts were unreliable.
- **Core idea:** a fixed set of convolutional design rules (strided and transposed convolutions, batch normalisation, LeakyReLU and ReLU activations, no hidden fully connected layers) that make the adversarial game trainable on natural images.
- **Equation or algorithm:** the GAN value function from the [GAN overview](index.md), optimised with the architecture above. Each step updates the discriminator on a real and a generated minibatch, then updates the generator.
- **Results:** the paper trains on LSUN, ImageNet-1k and a newly assembled faces dataset, and shows generated samples from these models. It also examines the structure of the latent space. The exact figures are in the paper.
- **Limitations:** the architecture alone does not remove the general GAN problems of mode coverage and the lack of a likelihood. The vector arithmetic shows some structure in the latent space, but not disentanglement. The main generator results are at 64 by 64 resolution.

## Connections

- DCGAN is a convolutional network for images in the sense of the [CNN family](../../../../models/cnn/index.md).
- The same training recipe carries over to the [VAE](../vae/index.md) and [flow](../flow/index.md) image models, which also use convolutional encoders or flows.
- Batch normalisation, which DCGAN relies on, was introduced by Ioffe and Szegedy (2015); see the references below.

## Applications

The paper's own experiments are small image synthesis tasks. DCGAN-style generators became the default baseline for image GAN research, and its discriminator features served as an unsupervised image representation.

## Open questions

- Whether the design rules transfer to much higher resolutions without changes.
- How much of the stability came from the architecture, and how much from the optimiser settings.
- Whether the latent arithmetic reflects meaningful semantic directions in general.

## References

### Seminal papers

- Radford, A., Metz, L. & Chintala, S. (2016). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR (arXiv). https://arxiv.org/abs/1511.06434 — Introduces DCGAN, with the architectural guidelines for stable convolutional GAN training on images.
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS (arXiv). https://arxiv.org/abs/1406.2661 — Introduces the adversarial framework and the value function that DCGAN trains.
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. arXiv. https://arxiv.org/abs/1502.03167 — Introduces batch normalisation, one of the layers DCGAN relies on for stable training.
- Salimans, T., et al. (2016). *Improved Techniques for Training GANs*. arXiv. https://arxiv.org/abs/1606.03498 — Collects training techniques for GANs, including feature matching and minibatch discrimination, that address the same stability problems.
- Zhu, J.-Y., et al. (2017). *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks*. arXiv. https://arxiv.org/abs/1703.10593 — Uses DCGAN-style convolutional generators in an image-to-image translation setting.
- Odena, A., Olah, C. & Shlens, J. (2017). *Conditional Image Synthesis With Auxiliary Classifier GANs*. arXiv. https://arxiv.org/abs/1610.09585 — Adds class conditioning to a DCGAN-style generator, a common extension of the architecture on this page.
- Karras, T., Laine, S. & Aila, T. (2019). *A Style-Based Generator Architecture for Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1812.04948 — A later generator design built on convolutional GAN generators of the DCGAN kind, with style-based control of features.

## Further learning

- Lilian Weng, *From GAN to WGAN*. https://lilianweng.github.io/posts/2017-08-20-gan/ — Derivations of GAN training and the Wasserstein variant, with diagrams, for readers new to the topic.
