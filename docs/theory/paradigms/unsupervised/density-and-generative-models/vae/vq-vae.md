---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/autoencoders-and-representations
tags:
  - generative models
  - discrete latents
  - representation learning
aliases:
  - VQ-VAE
  - Vector-quantised VAE
  - 向量量化 VAE
---

# Vector-Quantised VAE (VQ-VAE)

VQ-VAE replaces the continuous latent of a [variational autoencoder](index.md) with a discrete code, chosen from a learned codebook, and then trains a separate autoregressive prior over those codes. The discrete code makes the latent space easier to model with strong priors. The method sits within the [VAE](index.md) family.

## Overview

van den Oord, Vinyals and Kavukcuoglu (2017) show that a VAE whose latent is a set of discrete codes can be trained end to end, with the codebook learned alongside the encoder and decoder. Once training is done, a PixelCNN prior is fitted over the discrete latents for images, and a WaveNet is used for raw audio. Sampling then draws codes from the prior and decodes them.

## Key concepts

- **Codebook**: a set of embedding vectors \(e_1, \dots, e_K\). Each encoder output is mapped to the nearest one.
- **Nearest-neighbour quantisation**: the code index is \(k = \arg\min_j \lVert z_e(x) - e_j \rVert_2\), and the decoder receives \(e_k\).
- **Straight-through gradient**: quantisation has no gradient, so the gradient at the decoder input is copied to the encoder output.
- **Commitment loss**: keeps encoder outputs close to their chosen codes, weighted by \(\beta\).
- **Two-stage training**: the autoencoder is trained first, and the prior is fitted afterwards on the discrete codes.

## How it works

The encoder produces \(z_e(x)\), which is quantised to the nearest codebook vector \(e_k\), and the decoder reconstructs \(x\) from \(e_k\). The loss is

\[
L = \log p(x \mid z_q(x)) + \lVert \operatorname{sg}[z_e(x)] - e \rVert_2^2 + \beta\,\lVert z_e(x) - \operatorname{sg}[e] \rVert_2^2
\]

where \(\operatorname{sg}\) is the stop-gradient operator. The first term is reconstruction, the second moves codebook vectors toward encoder outputs, and the third keeps encoder outputs from drifting. The paper uses \(\beta = 0.25\) in all its experiments.

For ImageNet at 128 by 128 by 3, the paper compresses each image into a 32 by 32 by 1 discrete latent with \(K = 512\) codes. A PixelCNN then models that latent grid autoregressively, so sampling produces latents that are decoded to images.

## Key methods

### Neural Discrete Representation Learning (van den Oord et al., 2017)

- **Problem:** VAEs with continuous latents and strong decoders tend to ignore part of the latent code or give blurry samples. Discrete latents are easier to model with autoregressive priors, but standard training cannot back-propagate through a discrete choice.
- **Core idea:** a discrete bottleneck chosen by nearest-neighbour lookup in a learned codebook, trained with the straight-through estimator and the codebook and commitment losses above, followed by an autoregressive prior fitted on the codes.
- **Equation or algorithm:** the loss and the nearest-neighbour rule above. Training updates the encoder, decoder and codebook together. After training, the prior is fitted on the code grid.
- **Results:** the paper's CIFAR-10 comparison reports 4.67 bits per dimension for VQ-VAE, 4.51 for the continuous VAE, and 5.14 for VIMCO. All three are lower bounds on likelihood. The paper also reports images and audio generated from the discrete latents with the PixelCNN and WaveNet priors.
- **Limitations:** the prior is fitted after the autoencoder rather than jointly with it, which the paper leaves as future work. On the CIFAR-10 comparison VQ-VAE's bound is slightly weaker than the continuous VAE's. The discrete bottleneck also limits how much detail one code can carry.

## Connections

- The continuous VAE that VQ-VAE modifies is defined on the [VAE overview](index.md), and its ELBO is the same as before.
- Discrete codes from VQ-VAE act as image tokens for later hierarchical models, such as [VQ-VAE-2](https://arxiv.org/abs/1906.00446) by Razavi et al. (2019).
- The idea of learning compact representations of data sits within [Autoencoders and Representations](../../autoencoders-and-representations/index.md).

## Applications

Image and audio compression into discrete codes, and token-based image generation, where a learned codebook turns images into sequences that an autoregressive model can predict.

## Open questions

- Keeping every codebook vector in use, so that the discrete bottleneck does not collapse onto a few codes.
- Training the prior and the autoencoder jointly, which the paper leaves as future work.
- How large a discrete code must be to match the detail of continuous latents.

## References

### Seminal papers

- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. NeurIPS (arXiv). https://arxiv.org/abs/1711.00937 — Introduces VQ-VAE, the discrete codebook bottleneck with the straight-through estimator, the method on this page.
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — Introduces the VAE and the reparameterisation estimator that VQ-VAE modifies.
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. ICML. https://arxiv.org/abs/1401.4082 — Develops the same model class with stochastic backpropagation and a recognition model.
- Burda, Y., Grosse, R. & Salakhutdinov, R. (2016). *Importance Weighted Autoencoders*. ICLR. https://arxiv.org/abs/1509.00519 — Tightens the ELBO with importance-weighted samples for the same model class.
- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. arXiv. https://arxiv.org/abs/1601.06759 — Introduces the autoregressive pixel models whose PixelCNN form is used as the prior for VQ-VAE images.
- Razavi, A., van den Oord, A. & Vinyals, O. (2019). *Generating Diverse High-Fidelity Images with VQ-VAE-2*. arXiv. https://arxiv.org/abs/1906.00446 — Extends VQ-VAE to a hierarchy of discrete codes for high-fidelity image generation.

## Further learning

- Lilian Weng, *From Autoencoder to Beta-VAE*. Link: https://lilianweng.github.io/posts/2018-08-12-vae/ — A visual walkthrough of autoencoders, VAEs and their variants, including discrete latents.
