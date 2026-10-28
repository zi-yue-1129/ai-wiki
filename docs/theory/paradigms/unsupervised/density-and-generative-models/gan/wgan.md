---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow
tags:
  - generative models
  - optimal transport
  - unsupervised learning
aliases:
  - WGAN
  - Wasserstein GAN
  - 瓦瑟斯坦生成對抗網路
---

# Wasserstein GAN (WGAN)

Wasserstein GAN replaces the Jensen–Shannon objective of the original GAN with the Wasserstein-1 (earth mover's) distance. The gradients it gives the generator stay useful even when the generated and real distributions do not overlap. It is one of the two main training-objective families in the [GAN overview](index.md).

## Overview

Arjovsky, Chintala and Bottou (2017) argue that the GAN objective fails when the model and data supports are disjoint, because the Jensen–Shannon divergence is then constant and gives no gradient to the generator. The Wasserstein distance is continuous in the model parameters, so it gives a usable signal throughout training. The paper also reports that the critic's loss tracks sample quality, which gives a training curve that can be read.

## Key concepts

- **Wasserstein-1 distance**: the minimum cost of transporting one distribution into another, with cost equal to distance moved.
- **Kantorovich–Rubinstein duality**: the distance equals the supremum of \(\mathbb E_{P_r}[f] - \mathbb E_{P_g}[f]\) over all 1-Lipschitz functions \(f\).
- **Critic**: the network \(f_w\) that approximates this supremum. It outputs an unbounded score, not a probability.
- **Lipschitz constraint**: the requirement that the critic's gradient norm is at most one. WGAN enforces it approximately.
- **Weight clipping**: the original enforcement method, clamping the critic's weights to a small interval after each update.

## How it works

With a critic constrained to be 1-Lipschitz, the Wasserstein distance is

\[
W(P_r, P_g) = \sup_{\|f\|_L \le 1} \mathbb E_{x\sim P_r}[f(x)] - \mathbb E_{x\sim P_g}[f(x)]
\]

The critic maximises the difference in expected score between real and generated samples. The generator minimises the same quantity from the other side. With a generator \(g_\theta(z)\), the two losses are

\[
L_{\text{critic}} = \mathbb E_{z}[f_w(g_\theta(z))] - \mathbb E_{x}[f_w(x)], \qquad L_{\text{gen}} = -\mathbb E_{z}[f_w(g_\theta(z))]
\]

In the paper's algorithm, the critic is updated several times (five in the paper) for each generator update, its weights are clipped after every step, and RMSProp is recommended over momentum-based optimisers, which the authors found less stable.

## Key methods

WGAN is one of the two Wasserstein-based GAN methods covered on the wiki. The two differ in how they enforce the Lipschitz constraint.

- **WGAN (Arjovsky et al., 2017)**: weight clipping on the critic. This page.
- **WGAN-GP (Gulrajani et al., 2017)**: a gradient penalty in place of clipping, see [WGAN-GP](wgan-gp.md).

### Wasserstein GAN (Arjovsky et al., 2017)

- **Problem:** GAN training is unstable, and the Jensen–Shannon objective gives no useful gradient when the model and data distributions are far apart.
- **Core idea:** replace the discriminator with a critic that approximates the Wasserstein-1 distance, and keep the critic approximately 1-Lipschitz by clipping its weights.
- **Equation or algorithm:** the critic and generator losses above. Each iteration: several critic updates on real and generated minibatches with clipping, then one generator update.
- **Results:** the paper compares training behaviour with the original GAN and reports that training is more stable, that the critic's loss correlates with sample quality, and that mode collapse is reduced in its experiments. Generated images are shown on several image datasets. The paper gives the numbers in its tables.
- **Limitations:** weight clipping limits the critic's capacity and can slow training, and the clipping range is a sensitive hyperparameter. Enforcing the constraint by a penalty instead, as in WGAN-GP, avoids these problems.

## Connections

- The Wasserstein distance is a form of optimal transport, and the critic is a dual potential of the transport problem. This makes it a natural bridge to the [flow](../flow/index.md) methods, which also learn a transport map from noise to data.
- Lipschitz-constrained networks and spectral normalisation are a related line of work, see [Spectral Normalization](https://arxiv.org/abs/1802.05957).
- The GAN framework and its value function are described on the [GAN overview](index.md).

## Applications

WGAN is used as a stable training objective for image synthesis experiments, and it is the base for the gradient-penalty variant that most later Wasserstein GAN work builds on.

## Open questions

- Whether weight clipping or other constraint methods give the best trade-off between capacity and stability.
- How well the critic's loss predicts sample quality across different datasets and architectures.
- Which constraint enforcement method scales best to very large models.

## References

### Seminal papers

- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. arXiv. https://arxiv.org/abs/1701.07875 — Introduces the Wasserstein objective and the weight-clipped critic for GAN training.
- Gulrajani, I., et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS (arXiv). https://arxiv.org/abs/1704.00028 — Replaces weight clipping with a gradient penalty, the successor method on this page.
- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. NeurIPS (arXiv). https://arxiv.org/abs/1406.2661 — Introduces the Jensen–Shannon GAN objective that WGAN replaces.
- Miyato, T., et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1802.05957 — Enforces a Lipschitz constraint on the discriminator by normalising its weight matrices.
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* arXiv. https://arxiv.org/abs/1801.04406 — Analyses when gradient-based GAN training converges, including the role of the discriminator's regularity.
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.04862 — Analyses why the original GAN gradients fail when the two distributions have disjoint supports, the argument behind the Wasserstein objective.
- Heusel, M., et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. arXiv. https://arxiv.org/abs/1706.08500 — Introduces the Fréchet Inception Distance, an evaluation measure commonly used to compare GAN training methods such as WGAN.

## Further learning

- Lilian Weng, *From GAN to WGAN*. https://lilianweng.github.io/posts/2017-08-20-gan/ — Derives the Wasserstein objective step by step, with diagrams.
