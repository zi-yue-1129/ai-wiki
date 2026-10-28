---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/models/cnn
tags:
  - generative models
  - variational inference
  - unsupervised learning
aliases:
  - 變分自編碼器
  - VAE
  - Variational autoencoder
---

# Variational Autoencoders (VAE)

A variational autoencoder is a latent-variable generative model trained by maximising a lower bound on the data likelihood. An encoder maps each input to a distribution over a latent code, and a decoder maps codes back to data. Because the latent space is continuous and has a simple prior, the model can generate new samples by drawing codes from the prior and decoding them. It is one of the three classic generative algorithms, next to [GANs](../gan/index.md) and [flows](../flow/index.md). The family-level comparison is on the [Generative Models](../generative-models/index.md) page.

## Overview

Kingma and Welling (2013) and Rezende, Mohamed and Wierstra (2014) introduced the same model at about the same time. Both combine a neural-network recognition model, which approximates the posterior over latent variables, with a generative model trained through a reparameterised bound. The result is a single objective that can be optimised with stochastic gradient descent on large datasets.

## Key concepts

- **Latent variable** \(z\): an unobserved code with prior \(p(z) = \mathcal N(0, I)\).
- **Encoder (recognition model)** \(q_\phi(z\mid x)\): a network that outputs the mean and variance of a Gaussian over \(z\) for each input \(x\).
- **Decoder** \(p_\theta(x\mid z)\): a network that defines the likelihood of the data given a code.
- **Evidence lower bound (ELBO)**: the training objective, a lower bound on \(\log p_\theta(x)\).
- **Reparameterisation trick**: writing \(z = \mu + \sigma \odot \epsilon\) with \(\epsilon \sim \mathcal N(0, I)\), so gradients flow through the sampling step.

## How it works

The ELBO for one data point is

\[
\mathcal L(\theta,\phi; x) = \mathbb E_{q_\phi(z\mid x)}\big[\log p_\theta(x\mid z)\big] - D_{\mathrm{KL}}\big(q_\phi(z\mid x)\,\|\,p(z)\big) \le \log p_\theta(x)
\]

The first term rewards reconstructions. The second keeps the approximate posterior close to the prior, which makes the latent space smooth enough to sample from. The gap between the bound and \(\log p_\theta(x)\) is exactly the KL divergence between the approximate and the true posterior, so a better encoder tightens the bound.

Training draws \(\epsilon\) for each data point, computes \(z = \mu_\phi(x) + \sigma_\phi(x)\odot\epsilon\), evaluates the decoder, and takes a gradient step on \(-\mathcal L\). When the prior and posterior are Gaussian, the KL term has a closed form. Generation draws \(z\sim\mathcal N(0,I)\) and returns the decoder's mean or a sample.

## Key methods

Several variants change the latent prior, the decoder, or the bound itself. Each one would get its own page; the brief comparison here is enough for the family overview.

- **Stochastic backpropagation and approximate inference (Rezende et al., 2014)**: the same model and the same reparameterised estimator, developed from the deep latent Gaussian model viewpoint.
- **Vector-quantised VAE (VQ-VAE)**: a discrete latent code learned with a codebook. It is common in image and audio tokenisation. A method page is still to be written.
- **Conditional VAE (CVAE)**: conditions both encoder and decoder on a label or other input. A method page is still to be written.

### Auto-Encoding Variational Bayes (Kingma & Welling, 2013)

- **Problem:** exact posterior inference is intractable in directed latent-variable models with continuous latents, and mean-field or sampling-based methods scale poorly to large datasets.
- **Core idea:** optimise the ELBO with a reparameterised Monte Carlo estimator, and amortise the inference by training one encoder shared across all data points.
- **Equation or algorithm:** the ELBO above, with the Gaussian reparameterisation \(z = \mu_\phi(x) + \sigma_\phi(x)\odot\epsilon\). Each step uses a minibatch, one sample of \(\epsilon\) per point, and one gradient update of \(\theta\) and \(\phi\) together.
- **Results:** the paper reports experiments on MNIST and the Frey Face dataset, including generated samples and marginal likelihood estimates. The abstract describes the approach as efficient on large datasets and reflects its theoretical advantages in experiments, without quoting figures.
- **Limitations:** the Gaussian posterior and decoder can produce blurry samples, because the likelihood term averages over plausible outputs. The bound is also loose when the encoder is weak. Later work addresses the posterior family, the prior, and the bound itself.

### Stochastic backpropagation and approximate inference (Rezende et al., 2014)

- **Problem:** the same as above, for deep directed generative models with continuous latent variables.
- **Core idea:** a recognition model acts as a stochastic encoder, and gradients are propagated through the sampling step with a reparameterisation.
- **Equation or algorithm:** the reparameterised estimator of the variational bound, optimised jointly for the generative and recognition models.
- **Results:** the abstract reports that the model generates realistic samples, imputes missing data accurately, and helps visualise high-dimensional data on several real-world datasets. It gives no specific numbers.
- **Limitations:** as for the VAE above. The paper emphasises the estimator and the model class rather than a single benchmark.

## Connections

- The reparameterisation trick is the same device used by Monte Carlo gradient estimators in [reinforcement learning](../../../reinforcement-learning/policy-gradient-and-actor-critic/index.md).
- Diffusion models can be read as hierarchical VAEs with a fixed encoder, see [DDPM](../diffusion/ddpm.md).
- VAE encoders are convolutional for images, see [Convolutional Networks](../../../../models/cnn/index.md), and the [U-Net](../../../../models/cnn/unet/index.md) is the usual decoder in diffusion latents.
- The ELBO is an instance of variational inference, which links to [probabilistic methods](../../../probabilistic/index.md).
- For how brain-inspired generative models relate to these objectives, see [NeuroAI](../../../../../brain-mind/neuroai/index.md).

## Applications

Representation learning for images, audio and molecules, anomaly detection by reconstruction error, semi-supervised classification, and tokenisation of images for large generative models.

## Open questions

- Blurry samples: whether richer posteriors or discrete latents close the gap to GAN and diffusion sample quality.
- Posterior collapse: decoders that are too powerful can ignore the latent code.
- The gap between the ELBO and log-likelihood, and how much it limits model comparison.

## References

### Seminal papers

- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — Introduces the VAE, the ELBO and the reparameterisation estimator for amortised inference.
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. ICML. https://arxiv.org/abs/1401.4082 — Develops the same model class with stochastic backpropagation and a recognition model.

### Surveys and textbooks

- Kingma, D. P. & Welling, M. (2019). *An Introduction to Variational Autoencoders*. arXiv. https://arxiv.org/abs/1906.02691 — Tutorial-length survey of the VAE framework and its extensions.

### Articles and documentation

- Doersch, C. (2016). *Tutorial on Variational Autoencoders*. arXiv. https://arxiv.org/abs/1606.05908 — Step-by-step derivation of the VAE objective and its training.

## Further learning

- Lilian Weng, *From Autoencoder to Beta-VAE*. Link: https://lilianweng.github.io/posts/2018-08-12-vae/ — A visual walkthrough of autoencoders, VAEs and their variants.
