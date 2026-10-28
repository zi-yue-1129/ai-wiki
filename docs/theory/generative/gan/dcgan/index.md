---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - adversarial training
  - representation learning
aliases:
  - 深度卷積生成對抗網路
  - DCGAN
  - Deep convolutional GAN
---

# DCGAN: Deep Convolutional Generative Adversarial Networks

DCGAN, introduced by Radford, Metz and Chintala (2015), is a set of architectural rules that lets convolutional GANs train stably on natural images. It keeps the adversarial objective of the [Original GAN](../original-gan/index.md) and changes only the networks, which makes it one of the landmark methods of the [Generative Adversarial Networks](../index.md) topic.

## Overview

Before this work, GANs built from convolutional networks had been hard to scale. Training often failed, and the images were noisy and hard to read. The authors searched over many architectures and identified a family that trained stably across several datasets, and that allowed higher resolution and deeper models. The paper contributes three things: the architectural guidelines, the use of the trained discriminator as a feature extractor, and an analysis of the latent space, including simple vector arithmetic on the input noise.

## Key concepts

- **Strided convolution**: the discriminator downsamples with learned strided convolutions instead of pooling. The generator upsamples with fractionally-strided convolutions.
- **Batch normalisation**: the paper found it critical for deep generators to start learning, because it prevents collapse of all samples to a single point.
- **Activation functions**: ReLU in every generator layer except the output, which uses Tanh. LeakyReLU in every discriminator layer.
- **Latent input**: a 100-dimensional noise vector, projected to a small spatial tensor that starts the convolutional stack.
- **Latent arithmetic**: the paper reports that simple vector operations on the input allow easy manipulation of semantic qualities of generated samples.

## How it works

The paper summarises the architecture as four guidelines:

1. Replace pooling layers with strided convolutions in the discriminator and fractionally-strided convolutions in the generator.
2. Use batch normalisation in both networks. Applying it to every layer caused oscillation and instability, so it is omitted from the generator output and the discriminator input.
3. Remove fully connected hidden layers for deeper architectures. Only the first generator layer, which reshapes the noise, acts as a dense projection.
4. Use the activations listed under Key concepts.

Training details matter as much as the architecture. Images are scaled to \([-1, 1]\). Weights start from a zero-centred normal distribution with standard deviation 0.02. The optimiser is Adam (Kingma & Ba, 2014) with learning rate 0.0002, which the authors found necessary because the suggested 0.001 was too high, and with \(\beta_1 = 0.5\), because the default 0.9 caused oscillation. The minibatch size is 128, and the leak slope of LeakyReLU is 0.2.

## Results

The paper evaluates the learned representations and the generated images in three ways.

- **CIFAR-10 classification.** Features from a discriminator trained on ImageNet-1k were pooled into a 28,672-dimensional vector and classified with a linear L2-SVM. The paper reports 82.8% accuracy. This beats the single-layer K-means baseline at 80.6% but not the Exemplar CNN at 84.3% (Table 1 of the paper).
- **SVHN classification.** With 1,000 labelled examples, the same pipeline reached a 22.48% test error. The paper describes this as state of the art for that label budget at the time.
- **Image generation.** Samples of LSUN bedrooms are shown after one pass through the data and after five epochs. The authors use them to argue that the model does not simply memorise its training images.

## Limitations

- **Mostly visual evaluation.** The generated images are judged by eye. The quantitative results measure the features, not the samples.
- **Empirical guidelines.** The rules were found by search. The paper gives no theory for why they stabilise training.
- **Sensitivity.** Several settings, including the momentum term and the batch normalisation placement, were needed to avoid oscillation.
- **Not a complete fix.** Architecture alone does not guarantee stability. Arjovsky et al. (2017) show that DCGAN-style generators without batch normalisation and with constant filter counts perform poorly under the standard GAN objective.

## Open questions

- What is the theoretical reason that batch normalisation and these convolutional constraints help the adversarial game?
- How well do features from a GAN discriminator compare with features from self-supervised methods at larger scale?

## References

### Seminal papers

- Radford, A., Metz, L. & Chintala, S. (2015). *Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1511.06434 — The paper itself: the architectural guidelines, training details and the CIFAR-10 and SVHN feature experiments described here.
- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — The original framework, whose objective DCGAN keeps unchanged while changing the networks.
- Kingma, D. P. & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. ICLR. https://arxiv.org/abs/1412.6980 — Introduces the Adam optimiser, whose momentum settings DCGAN training depends on.
- Ioffe, S. & Szegedy, C. (2015). *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift*. ICML. https://arxiv.org/abs/1502.03167 — Introduces batch normalisation, one of the three architectural ingredients that DCGAN adopts.
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — Tests DCGAN-style generators with and without batch normalisation and shows that GAN training can fail without it.

### Surveys and textbooks

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — A review of GAN architectures and applications, including the convolutional designs that followed DCGAN.

### Lectures and videos

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — The author's tutorial on GAN training practice and architecture choices, including convolutional generators and discriminators, with exercises.
