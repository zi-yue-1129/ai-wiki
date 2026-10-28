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

GANs of the time were hard to train on images, and convolutional architectures were rarely used in them. Radford, Metz and Chintala (2016) found a combination of convolutional design choices that trained reliably across several image datasets, and they showed that the discriminator's features could be reused for other tasks.

## Key concepts

- **Strided convolution**: the discriminator downsamples with learned strided convolutions in place of pooling.
- **Fractional-strided (transposed) convolution**: the generator upsamples with learned layers instead of fixed interpolation.
- **Batch normalisation**: applied in both networks, except at the generator's output and the discriminator's input.
- **LeakyReLU and ReLU**: the discriminator uses LeakyReLU, and the generator uses ReLU, with tanh at the output.

## How it works

The generator takes a noise vector \(z\) (sampled uniformly in the paper), projects it to a small spatial grid, and applies a stack of transposed convolutions to reach a 64 by 64 image. The discriminator mirrors this with strided convolutions and ends in a single sigmoid unit. The paper removes fully connected hidden layers in favour of convolutional stacks, and it uses global average pooling where a dense layer would normally sit.

The training objective is the original minimax GAN loss from [Goodfellow et al. (2014)](index.md#generative-adversarial-networks-goodfellow-et-al-2014), with the non-saturating generator update. The paper trains with Adam using a learning rate of 0.0002 and \(\beta_1 = 0.5\).

## Key methods

DCGAN is a recipe for the convolutional GAN, not a separate training objective. It is compared with the other GAN variants on the [GAN overview](index.md). Its neighbours in the family are [WGAN](wgan.md) and [WGAN-GP](wgan-gp.md), which change the objective rather than the architecture.

### Deep Convolutional GAN (Radford et al., 2016)

- **Problem:** the original GAN used fully connected networks and was unstable on images. Earlier convolutional attempts were unreliable.
- **Core idea:** a fixed set of convolutional design rules (strided and transposed convolutions, batch normalisation, LeakyReLU and ReLU activations, no hidden fully connected layers) that make the adversarial game trainable on natural images.
- **Equation or algorithm:** the GAN value function from the [GAN overview](index.md), optimised with the architecture above. Each step updates the discriminator on a real and a generated minibatch, then updates the generator.
- **Results:** the paper shows generated images of bedrooms and faces, latent-space interpolations, and simple vector arithmetic on face attributes. It also evaluates the discriminator's learned features on image classification. The exact figures are in the paper.
- **Limitations:** the architecture alone does not remove the general GAN problems of mode coverage and the lack of a likelihood. The vector arithmetic shows some structure in the latent space, but not disentanglement. The work targets 64 by 64 images.

## Connections

- DCGAN is a convolutional network for images in the sense of the [CNN family](../../../../models/cnn/index.md).
- The same training recipe carries over to the [VAE](../vae/index.md) and [flow](../flow/index.md) image models, which also use convolutional encoders or flows.
- Batch normalisation, which DCGAN relies on, is a regularisation technique that the wiki covers under [Normalisation layers](../../../../models/cnn/index.md).

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

## Further learning

- Lilian Weng, *From GAN to WGAN*. https://lilianweng.github.io/posts/2017-08-20-gan/ — Derivations of GAN training and the Wasserstein variant, with diagrams, for readers new to the topic.
