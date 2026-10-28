---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - diffusion models
aliases:
  - 去噪擴散機率模型
  - DDPM
  - Denoising diffusion probabilistic models
---

# DDPM: Denoising Diffusion Probabilistic Models

DDPM (Ho, Jain & Abbeel, 2020) is the method that made diffusion models practical for high-quality image generation. It trains a network to predict the noise added to a clean image at a random time step, then generates an image by removing noise one step at a time. Most later diffusion work builds on this objective. The family-level picture is on the [Diffusion Models](index.md) page.

## Overview

Diffusion models were first proposed by Sohl-Dickstein et al. (2015). They define a fixed forward process that adds noise to data and a learned reverse process that removes it. Ho et al. (2020) showed that a much simpler training recipe, with a fixed noise schedule and a plain noise-prediction loss, gives image samples of high quality. On unconditional CIFAR-10 the paper reports an FID of 3.17, which it describes as state of the art at the time.

## Problem

Image generators in 2020 faced a trade-off. GANs produced sharp images but trained unstably and had no tractable likelihood. Likelihood-based models trained stably, but the paper argues that they produced weaker samples. The earlier diffusion formulation was in principle stable, yet its variational objective was hard to tune for image quality. DDPM asks whether a simple objective can give high-quality samples from a diffusion model.

## Core idea

The forward process is a fixed chain that adds Gaussian noise over \(T\) steps, with no learned parameters. The reverse process is a network that predicts the noise \(\epsilon\) that was added to a noisy image \(x_t\). The paper shows that the variational bound on the likelihood can be written as a sum of denoising terms, and that a weighted version of the bound reduces to a simple mean-squared error on the noise. This simplified loss is what gives the best samples. The paper connects it to denoising score matching with Langevin dynamics over several noise levels.

## Algorithm

With \(\alpha_t = 1-\beta_t\) and \(\bar\alpha_t = \prod_{s\le t}\alpha_s\), the forward process can jump directly from \(x_0\) to any step:

\[
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal N(0, I)
\]

The simplified training loss is

\[
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

**Training (Algorithm 1):** repeat the following. Sample a clean image \(x_0\), a time step \(t\) uniformly from \(\{1,\dots,T\}\) and noise \(\epsilon\). Take a gradient step on \(\|\epsilon-\epsilon_\theta(\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\epsilon, t)\|^2\).

**Sampling (Algorithm 2):** start from \(x_T \sim \mathcal N(0, I)\). For \(t = T\) down to 1, draw \(z \sim \mathcal N(0, I)\) if \(t > 1\) (and \(z = 0\) otherwise), then compute

\[
x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\epsilon_\theta(x_t, t)\Big) + \sigma_t z
\]

The paper fixes \(\sigma_t^2\) to a constant, either \(\beta_t\) or \(\tilde\beta_t\), and reports similar results for both.

**Settings:** \(T = 1000\) steps, with a linear schedule of \(\beta_t\) from \(10^{-4}\) to \(0.02\). The denoiser is a U-Net with time-step conditioning, adapted from PixelCNN++.

## Results

The paper's Table 2 compares training objectives on unconditional CIFAR-10. FID is computed against the training set.

| Objective | Inception score ↑ | FID ↓ |
|---|---|---|
| \(\epsilon\)-prediction with \(L_{\text{simple}}\) (the paper's method) | 9.46 ± 0.11 | 3.17 |
| \(\epsilon\)-prediction with the full bound and a fixed isotropic covariance | 7.67 ± 0.13 | 13.51 |
| \(\tilde\mu\)-prediction with the full bound and a fixed isotropic covariance | 8.06 ± 0.09 | 13.22 |

On 256×256 LSUN, Table 3 reports FID 6.36 (Bedroom), 7.89 (Church) and 19.75 (Cat) for the small model, and 4.90 for the large Bedroom model. ProgressiveGAN reports 8.34, 6.42 and 37.52. DDPM is better on Bedroom and worse on Church and Cat, so the abstract's "similar to ProgressiveGAN" is an accurate summary.

## Limitations

- **Slow sampling.** Each sample needs \(T = 1000\) network evaluations. [DDIM](ddim.md) and [Latent Diffusion](latent-diffusion.md) reduce this cost.
- **Likelihood trade-off.** The simplified loss is not the bound that maximises likelihood. In Table 2 its likelihood bound is slightly worse (at most 3.75 bits/dim, against 3.70 for the full bound), so the sample-quality gain comes at a small cost in likelihood.
- **Objective sensitivity.** Table 2 shows that the choice of objective changes FID by a factor of about four. The gain depends on the particular weighting, and the paper does not sweep many alternatives.
- **Scope of results.** The main results are on CIFAR-10 and a few LSUN categories at 256×256. Later work extended DDPM to ImageNet and to text conditioning.

## Connections

- The faster sampler that reuses the same trained model is [DDIM](ddim.md).
- The latent-space version is [Latent Diffusion](latent-diffusion.md), and its Transformer denoiser is [DiT](../../../../models/transformer/dit/index.md).
- Conditioning on a class or a text prompt is done with [classifier-free guidance](classifier-free-guidance.md).
- The continuous-time view, in which DDPM is a discretised stochastic differential equation, is covered by Song et al. (2021), cited below.

## Open questions

- How much of the sample quality comes from the simplified loss, and how much from the U-Net and the noise schedule?
- How far can the number of steps be reduced, and at what cost in quality, without retraining?
- Why does reweighting the bound improve samples while lowering the likelihood?

## References

### Seminal papers

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — Introduces the \(L_{\text{simple}}\) noise-prediction objective, the linear schedule and the sampler, with results on CIFAR-10 and LSUN.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — Defines the forward noising chain and the learned reverse chain that DDPM builds on.
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — Shows that a DDPM-trained model can be sampled in far fewer steps.
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — Extends DDPM with architecture ablations and classifier guidance on ImageNet.

### Surveys and textbooks

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Shows that DDPM is a discretisation of a variance-preserving stochastic differential equation.

### Articles and documentation

- Ho, J. et al. *diffusion*, official code repository. https://github.com/hojonathanho/diffusion — The authors' TensorFlow implementation of the paper's experiments.

## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Code walk-through of DDPM training and sampling that matches the equations on this page.
