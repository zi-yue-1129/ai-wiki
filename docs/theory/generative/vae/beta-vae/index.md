---
status: draft
last_reviewed: 2026-10-28
related:
  - brain-mind/computational-neuroscience/sparse-coding
tags:
  - representation learning
  - generative models
aliases:
  - β-VAE
  - Beta-VAE
  - Disentangled VAE
  - 解耦變分自編碼器
---

# β-VAE

The β-VAE is a variational autoencoder whose training objective multiplies the KL term by a factor β. Setting β above one encourages the latent code to separate the independent factors of variation in the data, at a cost in reconstruction quality. It is one of the landmark variants described in [Variational Autoencoders](../index.md).

## Overview

A VAE's objective contains a cost on information: the KL term measures how far each code departs from the prior, and therefore how much the code tells the decoder about the input. The β-VAE scales that cost. The motivation is disentanglement. Suppose a dataset shows one object moving, shrinking and rotating. A good representation would have one latent dimension for position, one for scale and one for rotation, so that changing one dimension changes one property of the image. In a standard VAE the latent axes need not match the factors, so several factors can share one dimension. The β-VAE makes it more likely that each factor lines up with one axis. Burgess et al. (2018) call it a state-of-the-art model for unsupervised visual disentanglement and analyse why it works.

The method sits within the [Generative Models](../../index.md) overview. The [VQ-VAE](../vq-vae/index.md) also modifies the VAE, but it changes the form of the code rather than its weighting.

## Key concepts

- **Disentangled representation**: a representation in which each latent dimension corresponds to a single generative factor, and changing it leaves the other factors unchanged. Higgins et al. (2018) propose a formal definition based on the transformations of the world.
- **The β weight**: a scalar multiplying the KL term. At β = 1 the objective is the standard ELBO of the [VAE](../../../probabilistic/variational-inference/variational-autoencoder/index.md).
- **Information bottleneck**: the code can carry only a limited amount of information about the input. Larger β makes the bottleneck tighter.
- **Reconstruction–disentanglement trade-off**: a stronger bottleneck discards some detail, so reconstructions are less faithful, which is the cost of the method.
- **Capacity**: the KL divergence of the posterior from the prior, in nats, which Burgess et al. (2018) control during training.

## How it works

The β-VAE maximises, for each data point,

\[
\mathcal{L}_\beta(\theta,\phi;x) = \mathbb{E}_{q_\phi(z\mid x)}\big[\log p_\theta(x\mid z)\big] - \beta\,\mathrm{KL}\big(q_\phi(z\mid x)\,\|\,p(z)\big)
\]

The encoder, decoder and reparameterisation trick are the same as in the VAE. Only the weight on the KL term changes, so the training procedure is the standard one:

1. Draw a minibatch of data points \(x\).
2. Encode each \(x\) to the mean and variance of \(q_\phi(z\mid x)\), and sample \(z\) with the reparameterisation trick.
3. Compute the reconstruction log-likelihood and the KL term to the prior, and combine them with the weight \(\beta\).
4. Take a stochastic gradient step on \(\theta\) and \(\phi\), and repeat.

Burgess et al. (2018) analyse the case in which the KL term acts as a capacity limit. They propose a controlled variant that replaces the fixed weight with a penalty on the deviation from a target capacity \(C\), written \(\gamma\,|\mathrm{KL} - C|\). The target starts at zero and increases during training. The motivation is that a model with a small capacity first encodes the factor whose information improves the reconstruction most, and then adds further factors as the capacity grows. In a simplified generative model conditioned on the ground-truth factors of dSprites, the authors show this ordering: position first, then scale, shape and rotation.

## Results

Burgess et al. (2018) evaluate on dSprites, a synthetic dataset of 2D sprites whose position, scale, orientation and shape are known, a coloured variant, and 3D chairs. Their main evidence is qualitative: latent traversal plots, in which one latent dimension is varied while the others are held fixed. For the coloured dSprites dataset, the authors report robust disentangling of all factors together with high-quality reconstructions when the capacity is increased during training. The capacity analysis uses the simplified model described above, not the full VAE.

## Limitations

- **Reconstruction cost.** The original formulation trades reconstruction fidelity for disentanglement, and the controlled-capacity variant is proposed to reduce this cost (Burgess et al., 2018).
- **No guarantee.** Locatello et al. (2019) show that unsupervised learning of disentangled representations is impossible without inductive biases on the model or the data. Any given β-VAE run may therefore give a mixed or non-aligned code.
- **Evaluation needs known factors.** The usual way to check disentanglement uses datasets with known factors. Results on synthetic data may not carry over to natural images.
- **Hyperparameter choice.** β, or the capacity schedule, must be chosen, and the papers give no rule that works across datasets.

## Open questions

- Why do the learned axes align with the true factors of variation? Burgess et al. (2018) give a rate-distortion explanation, but a complete account is not yet available.
- Does the controlled-capacity schedule transfer from synthetic sprites to natural images at scale?
- How should disentanglement be defined and measured when the true factors are unknown? Higgins et al. (2018) propose one definition, but its practical use remains open.

## References

### Seminal papers

- Burgess, C. P. et al. (2018). *Understanding disentangling in β-VAE*. arXiv. https://arxiv.org/abs/1804.03599 — Explains β-VAE disentangling through a rate-distortion view and proposes a controlled capacity schedule.
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — The VAE objective that β-VAE modifies.
- Higgins, I. et al. (2018). *Towards a Definition of Disentangled Representations*. arXiv. https://arxiv.org/abs/1812.02230 — Proposes a formal definition of disentangled representations based on the transformations of the world.
- Locatello, F. et al. (2019). *Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations*. ICML. https://arxiv.org/abs/1811.12359 — Argues that unsupervised disentanglement needs inductive biases and tests many methods.

### Surveys and textbooks

- Doersch, C. (2016). *Tutorial on Variational Autoencoders*. arXiv. https://arxiv.org/abs/1606.05908 — A tutorial that explains the VAE objective from first principles.
