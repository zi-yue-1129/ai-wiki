---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/paradigms/imitation
tags:
  - generative models
  - adversarial training
  - unsupervised learning
aliases:
  - 生成對抗網路
  - GAN
  - Generative adversarial network
---

# Generative Adversarial Networks (GAN)

A generative adversarial network trains two networks against each other. A generator turns random noise into samples, and a discriminator tries to tell those samples from real data. The generator improves by fooling the discriminator, so the model learns to generate data without ever writing down a likelihood. GANs were the leading method for sharp image synthesis for several years. The family-level comparison is on the [Generative Models](../generative-models/index.md) page, and the alternatives are the [VAE](../vae/index.md) and [flow](../flow/index.md) methods.

## Overview

Goodfellow et al. (2014) introduced the framework as a minimax game between a generator \(G\) and a discriminator \(D\). The paper shows that, under idealised assumptions, the game has a unique solution in which the generator recovers the data distribution and the discriminator outputs one half everywhere. Training with multilayer perceptrons and backpropagation was practical from the start, and the approach needs no Markov chains.

## Key concepts

- **Generator** \(G(z)\): maps noise \(z\sim p_z\) to a sample.
- **Discriminator** \(D(x)\): outputs the probability that \(x\) came from the data rather than the generator.
- **Minimax game**: \(D\) maximises its classification accuracy, and \(G\) minimises it.
- **Mode collapse**: the generator produces only a few kinds of sample.
- **Critic**: a discriminator whose output is an unbounded score rather than a probability, as used in the Wasserstein formulation.

## How it works

The value function is

\[
\min_G \max_D \; V(D, G) = \mathbb E_{x\sim p_{\text{data}}}[\log D(x)] + \mathbb E_{z\sim p_z}[\log(1 - D(G(z)))]
\]

For a fixed generator, the best discriminator is \(D^*(x) = p_{\text{data}}(x)/(p_{\text{data}}(x)+p_g(x))\). Substituting it into the value function gives \(-\log 4 + 2\,\mathrm{JSD}(p_{\text{data}}\,\|\,p_g)\), so the generator minimises the Jensen–Shannon divergence between the data and the model. In practice the generator uses the non-saturating loss \(-\log D(G(z))\), because the original loss gives vanishing gradients when the discriminator is confident.

Training alternates a few discriminator updates on minibatches of real and generated samples with one generator update. Sampling draws \(z\sim p_z\) and applies \(G\) once, which is fast compared with autoregressive or diffusion sampling.

## Key methods

Each named variant addresses training stability or architecture. The brief comparison below links to each method's own page.

- **Generative Adversarial Networks (Goodfellow et al., 2014)**: the original minimax framework, described in full below.
- **[DCGAN (Radford et al., 2015)](dcgan.md)**: convolutional generator and discriminator with architectural rules that make training stable on images.
- **[WGAN (Arjovsky et al., 2017)](wgan.md)**: replaces the Jensen–Shannon objective with a Wasserstein distance, with weight clipping to enforce the Lipschitz constraint.
- **[WGAN-GP (Gulrajani et al., 2017)](wgan-gp.md)**: replaces weight clipping with a gradient penalty on interpolated samples.

### Generative Adversarial Networks (Goodfellow et al., 2014)

- **Problem:** learning a generative model without the intractable likelihood computations of earlier methods, and without Markov chains.
- **Core idea:** train a generator and a discriminator together in a minimax game, so that the generator is pushed toward the data distribution through the discriminator's signal.
- **Equation or algorithm:** the value function above. Each iteration: sample a minibatch of noise and of real data, update \(D\) by gradient ascent on \(V\), sample new noise, and update \(G\) to minimise \(-\log D(G(z))\).
- **Results:** the abstract reports qualitative and quantitative evaluation of the generated samples, and says the approach shows potential, without giving specific figures. The paper's experiments use MNIST, the Toronto Face Database and CIFAR-10 for sample quality.
- **Limitations:** training is unstable and sensitive to architecture and learning rates. Mode collapse can drop parts of the data distribution. There is no likelihood, so models are hard to compare, and evaluation relies on proxies.

## Connections

- The adversarial idea reappears in adversarial imitation learning, where a discriminator scores demonstrations against a policy, see [Adversarial Imitation](../../../imitation/adversarial-imitation/index.md).
- GAN generators are typically convolutional, so their architecture overlaps with [Convolutional Networks](../../../../models/cnn/index.md).
- The divergence view links the method to [information theory](../../../../information-theory/index.md) through the Jensen–Shannon divergence.
- Image GANs are the basis of many image-to-image systems, see [Multimodal Models](../../../../models/multimodal/index.md).

## Applications

Image synthesis and editing, super-resolution, data augmentation, domain translation between image styles, and realistic speech and face generation. Many of these uses have shifted toward diffusion models in recent years.

## Open questions

- Stable training without careful tuning, and whether the gradient-penalty and spectral-normalisation fixes generalise across tasks.
- Evaluating sample quality and diversity without relying on a single proxy.
- Whether adversarial objectives remain competitive with likelihood-based and diffusion models at very large scale.

## References

### Seminal papers

- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS (arXiv). https://arxiv.org/abs/1406.2661 — Introduces the adversarial framework, the value function and the non-saturating training recipe.
- Radford, A., Metz, L. & Chintala, S. (2016). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR (arXiv). https://arxiv.org/abs/1511.06434 — Introduces DCGAN, with architectural guidelines for stable convolutional GAN training on images.
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — Proposes the Wasserstein objective for more stable GAN training.
- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS (arXiv). https://arxiv.org/abs/1704.00028 — Replaces weight clipping with a gradient penalty.

### Surveys and textbooks

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — A tutorial-length overview of the framework and its training problems.

## Further learning

- Lilian Weng, *From GAN to WGAN*. https://lilianweng.github.io/posts/2017-08-20-gan/ — Derivations of the GAN and Wasserstein objectives, with diagrams.
