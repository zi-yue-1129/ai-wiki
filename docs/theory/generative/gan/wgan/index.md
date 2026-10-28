---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
tags:
  - adversarial training
  - optimization
aliases:
  - Wasserstein 生成對抗網路
  - WGAN
  - Wasserstein GAN
  - 瓦瑟斯坦 GAN
---

# Wasserstein GAN

Wasserstein GAN (WGAN), introduced by Arjovsky, Chintala and Bottou (2017), replaces the Jensen–Shannon-based objective of the original GAN with the Earth Mover distance, also called the Wasserstein-1 distance. The discriminator becomes a *critic* that outputs a real number rather than a probability, and its loss tracks how far the generator's samples are from the data. WGAN is one of the landmark methods of the [Generative Adversarial Networks](../index.md) topic.

## Overview

The original GAN criterion is closely related to the Jensen–Shannon divergence (see the [Original GAN](../original-gan/index.md) page). The paper argues that this divergence is a poor training signal when the data and generator distributions lie on low-dimensional manifolds that do not overlap. In that case the divergence stays constant, so the gradient for the generator is zero, even though the samples are far from the data. The Earth Mover distance, by contrast, still changes smoothly as the generator moves, so it gives a usable gradient. The paper turns this observation into a training algorithm.

## Key concepts

- **Earth Mover (Wasserstein-1) distance**: the least cost of moving probability mass from one distribution to another, with cost given by distance.
- **Kantorovich–Rubinstein duality**: the distance equals the supremum, over all 1-Lipschitz functions \(f\), of the difference between the expected value of \(f\) on real data and on generated data.
- **Critic**: the network \(f_w\) that approximates that supremum. It has no sigmoid output, so its score is not a probability.
- **Lipschitz constraint**: the critic must be 1-Lipschitz, meaning its output cannot change faster than its input. The paper enforces this approximately by clipping the weights to a small box.

## How it works

The critic maximises an estimate of the distance, and the generator minimises it:

\[
\max_{w \in \mathcal{W}} \; \mathbb{E}_{x \sim P_r}\big[f_w(x)\big] - \mathbb{E}_{z \sim p(z)}\big[f_w(g_\theta(z))\big], \qquad \min_\theta \; -\mathbb{E}_{z \sim p(z)}\big[f_w(g_\theta(z))\big]
\]

Here \(P_r\) is the data distribution, \(g_\theta\) is the generator and \(\mathcal{W}\) is the set of critic weights. The paper's Algorithm 1 proceeds as follows:

1. Repeat \(n_{\text{critic}}\) times: sample \(m\) real examples and \(m\) noise vectors, update the critic weights with RMSProp on the gradient of the estimate above, then clip each weight to \([-c, c]\).
2. Sample \(m\) noise vectors and update the generator parameters with RMSProp on the gradient of \(-\frac{1}{m}\sum_i f_w(g_\theta(z^{(i)}))\).

All experiments in the paper use learning rate \(\alpha = 0.00005\), clipping parameter \(c = 0.01\), batch size \(m = 64\) and \(n_{\text{critic}} = 5\). The authors chose RMSProp over Adam because they found that momentum-based optimisers made the critic's non-stationary loss unstable.

## Results

The paper reports three kinds of evidence. Its image experiments use the LSUN-Bedrooms dataset, with DCGAN as the baseline.

- **Loss and quality.** Unlike the standard GAN's discriminator-based estimate, the critic's estimate of the distance falls as sample quality improves. The paper reports that it correlates with visual quality, which makes it useful for debugging and for comparing hyperparameter settings.
- **Architectural robustness.** The paper trains a convolutional generator, a DCGAN generator without batch normalisation and with constant filter counts, and a four-layer ReLU MLP generator with 512 hidden units. The authors note that these two generators are known to perform very poorly with standard GANs, and report that WGAN remains robust across all three.
- **Mode collapse.** The paper states that in no experiment did it see evidence of mode collapse for the WGAN algorithm.

## Limitations

- **Weight clipping.** The paper calls clipping "a clearly terrible way" to enforce the Lipschitz constraint. If the clipping limit is large, weights take a long time to reach it. If it is small, gradients can vanish in deep critics.
- **Slow critic training.** Each generator update needs several critic updates, so training is more expensive.
- **Optimiser sensitivity.** Training becomes unstable with high learning rates or with momentum-based optimisers, as noted above.
- **Scores across models.** The estimate depends on the critic's architecture by a constant factor, so scores are hard to compare between models with different critics.

## Open questions

- Which enforcement of the Lipschitz constraint works best at scale? Gulrajani et al. (2017) replace clipping with a gradient penalty, and Miyato et al. (2018) constrain each layer's spectral norm.
- How should GAN samples be scored across architectures? The critic's value alone is not a fair comparison, which later motivated sample-based metrics such as the Fréchet Inception Distance.

## References

### Seminal papers

- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — The paper itself: the Wasserstein objective, Algorithm 1, the training analysis and the image experiments described here.
- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — The original GAN objective, whose Jensen–Shannon criterion WGAN replaces.
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1701.04862 — Analyses the saturation and instability of the original objective, the problem WGAN addresses.
- Gulrajani, I. et al. (2017). *Improved Training of Wasserstein GANs*. NeurIPS. https://arxiv.org/abs/1704.00028 — Replaces weight clipping in the critic with a gradient penalty and reports more reliable training.
- Miyato, T. et al. (2018). *Spectral Normalization for Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1802.05957 — Enforces the Lipschitz constraint on the discriminator by normalising the spectral norm of each weight matrix.

### Surveys and textbooks

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — A review of GAN objectives and training methods, written for signal-processing readers.

### Lectures and videos

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — The author's tutorial on GAN objectives and training methods, including the variants that changed the loss, with exercises.
