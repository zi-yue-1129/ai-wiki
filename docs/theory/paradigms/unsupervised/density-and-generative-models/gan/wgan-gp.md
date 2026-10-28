---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - generative models
  - optimal transport
  - unsupervised learning
aliases:
  - WGAN-GP
  - Improved WGAN
  - 梯度懲罰瓦瑟斯坦生成對抗網路
---

# WGAN with Gradient Penalty (WGAN-GP)

WGAN-GP keeps the Wasserstein objective of [WGAN](wgan.md) but enforces the Lipschitz constraint with a gradient penalty instead of weight clipping. The critic is then free to use its full capacity, and training works across a much wider range of architectures. It is the most widely used Wasserstein GAN variant, and it sits beside [WGAN](wgan.md) in the [GAN overview](index.md).

## Overview

Gulrajani, Ahmed, Arjovsky, Dumoulin and Courville (2017) show that weight clipping pushes the critic's weights toward a few extreme values, which limits what the critic can represent and makes training sensitive to the clipping range. They replace the clipping with a penalty on the norm of the critic's gradient, applied at points between real and generated samples.

## Key concepts

- **Gradient penalty**: a term added to the critic loss that is zero when the critic's gradient norm is one, and positive otherwise.
- **Interpolated samples**: points on straight lines between a real sample and a generated sample, where the penalty is applied.
- **Penalty weight \(\lambda\)**: how strongly the penalty is enforced. The paper uses \(\lambda = 10\).

## How it works

Let \(\tilde x = g_\theta(z)\) and \(\hat x = \epsilon x + (1-\epsilon)\tilde x\), where \(\epsilon \sim U[0,1]\). The critic loss is

\[
L_{\text{critic}} = \mathbb E_{\tilde x}[f_w(\tilde x)] - \mathbb E_{x}[f_w(x)] + \lambda\,\mathbb E_{\hat x}\big[(\|\nabla_{\hat x} f_w(\hat x)\|_2 - 1)^2\big]
\]

The generator loss is unchanged from WGAN, \(-\mathbb E_z[f_w(g_\theta(z))]\). Because the penalty needs the critic's gradient, each critic step computes a gradient of a gradient. The paper also advises against batch normalisation in the critic, since batch statistics mix samples and break the per-sample penalty.

## Key methods

WGAN-GP differs from [WGAN](wgan.md) only in how the Lipschitz constraint is enforced. Both belong to the Wasserstein family in the [GAN overview](index.md).

- **WGAN (Arjovsky et al., 2017)**: weight clipping, see [WGAN](wgan.md).
- **WGAN-GP (Gulrajani et al., 2017)**: gradient penalty on interpolated samples. This page.

### Improved Training of Wasserstein GANs (Gulrajani et al., 2017)

- **Problem:** weight clipping in [WGAN](wgan.md) limits the critic and makes training sensitive to the clipping threshold.
- **Core idea:** constrain the critic by penalising deviations of its gradient norm from one on random interpolations between real and generated samples.
- **Equation or algorithm:** the critic loss above, with \(\lambda = 10\) and the generator loss from WGAN. The paper trains the critic several times per generator step.
- **Results:** the abstract reports stable training of a wide variety of GAN architectures with almost no hyperparameter tuning, including deep residual networks and language models over discrete data. Image results are in the paper's experiments.
- **Limitations:** the penalty is enforced only on interpolated points, so the constraint holds approximately everywhere. Each critic step costs an extra gradient computation. The method still needs a suitable critic architecture, and the paper's guidance on normalisation is specific to it.

## Connections

- The penalty is one way to enforce the Lipschitz constraint that the Wasserstein distance requires, and it is compared with spectral normalisation in the [WGAN](wgan.md) references.
- The Wasserstein objective links the method to optimal transport, which also underlies the [flow](../flow/index.md) models.
- Convolutional critics for image data follow the [CNN family](../../../../models/cnn/index.md).

## Applications

WGAN-GP is used as a stable training objective for image and sequence GANs, and as a baseline in GAN comparisons.

## Open questions

- Whether the interpolation-based penalty gives a good constraint away from the interpolation points.
- The cost of the double gradient at very large model sizes.
- Whether the penalty can be replaced by a cheaper constraint without losing stability.

## References

### Seminal papers

- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS (arXiv). https://arxiv.org/abs/1704.00028 — Introduces the gradient penalty for the critic, the method on this page.
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — Introduces the Wasserstein objective that WGAN-GP keeps, with weight clipping.
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS (arXiv). https://arxiv.org/abs/1406.2661 — Introduces the adversarial framework that the Wasserstein variants modify.
- Miyato, T., et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1802.05957 — Enforces the Lipschitz constraint by normalising the discriminator's weights, an alternative to the gradient penalty.
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* arXiv. https://arxiv.org/abs/1801.04406 — Analyses GAN training convergence, including gradient penalties on the discriminator.
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.04862 — Analyses why the original GAN gradients fail when the two distributions have disjoint supports, the motivation for the critic penalty.
- Heusel, M., et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. arXiv. https://arxiv.org/abs/1706.08500 — Introduces the Fréchet Inception Distance, an evaluation measure commonly used to compare GAN training methods such as WGAN-GP.

## Further learning

- Lilian Weng, *From GAN to WGAN*. https://lilianweng.github.io/posts/2017-08-20-gan/ — Explains the Wasserstein and gradient-penalty variants with diagrams.
