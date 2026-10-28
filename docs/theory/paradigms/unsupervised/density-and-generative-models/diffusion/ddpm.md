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

DDPM is the method that made diffusion models practical for high-quality image generation. It trains a network to predict the noise added to an image at a random time step, and generates by removing noise step by step. It is the reference point for almost all later diffusion work. The family-level picture is on the [Diffusion Models](index.md) page.

## Overview

Ho, Jain and Abbeel (2020) showed that a simple, fixed noise schedule and a plain noise-prediction loss were enough to produce samples whose quality the paper reports as competitive with GANs, without adversarial training. Earlier diffusion work by Sohl-Dickstein et al. (2015) had the same forward and reverse processes but used a more complicated objective.

## Key concepts

- **Forward process**: a fixed Markov chain that adds Gaussian noise over \(T\) steps, with variances \(\beta_t\). It has no learned parameters.
- **Forward posterior** \(q(x_{t-1}\mid x_t, x_0)\): the exact Gaussian posterior of the forward chain, with mean \(\tilde\mu_t\) and variance \(\tilde\beta_t\). It is tractable, and the training objective is built from it.
- **Reverse process**: a learned Gaussian \(p_\theta(x_{t-1}\mid x_t)\) whose mean is computed from the network's noise prediction.
- **Noise schedule** \(\beta_t\): the paper uses a linear schedule from \(10^{-4}\) to \(0.02\) over \(T = 1000\) steps.

## How it works

With \(\alpha_t = 1-\beta_t\) and \(\bar\alpha_t = \prod_{s\le t}\alpha_s\), noise can be added in one jump:

\[
x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon, \qquad \epsilon \sim \mathcal N(0, I)
\]

The forward posterior has mean \(\tilde\mu_t(x_t, x_0)\) and variance \(\tilde\beta_t = \frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t\). The paper parameterises the reverse mean through a noise predictor,

\[
\mu_\theta(x_t, t) = \frac{1}{\sqrt{\alpha_t}}\Big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\,\epsilon_\theta(x_t, t)\Big)
\]

Substituting this into the variational bound gives a sum of denoising terms that resemble denoising score matching over multiple noise scales. Dropping the per-step weights gives the simplified loss

\[
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

Training (Algorithm 1 in the paper) repeats: sample a clean image \(x_0\), a uniform time step \(t\in\{1,\dots,T\}\) and noise \(\epsilon\), then take a gradient step on \(\|\epsilon-\epsilon_\theta(\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon, t)\|^2\). Sampling (Algorithm 2) starts from \(x_T\sim\mathcal N(0,I)\). For \(t=T\) down to 1 it draws \(z\sim\mathcal N(0,I)\) if \(t>1\) (and \(z=0\) otherwise), then computes \(x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\big(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\big) + \sigma_t z\). The paper sets \(\sigma_t^2\) to a fixed constant, either \(\beta_t\) or \(\tilde\beta_t\), and reports similar results for both. The network is a U-Net with time-step conditioning.

## Key methods

### Denoising Diffusion Probabilistic Models (Ho, Jain & Abbeel, 2020)

- **Problem:** GANs produce sharp images but train unstably, and likelihood-based models of the time produced weaker samples.
- **Core idea:** train a network to predict the noise added at random time steps, using a weighted variational bound that simplifies to noise prediction.
- **Equation or algorithm:** the \(L_{\text{simple}}\) loss, a linear \(\beta\) schedule, and ancestral sampling over \(T\) steps, as in Algorithms 1 and 2 above.
- **Results:** the abstract reports an Inception score of 9.46 and an FID of 3.17 on unconditional CIFAR-10, described as state of the art at the time. For 256×256 LSUN the abstract says sample quality is similar to ProgressiveGAN, with no number given there. The paper's Table 2 ablation on unconditional CIFAR-10 shows that the simplified loss matters. Predicting \(\epsilon\) with the unweighted \(L_{\text{simple}}\) gives FID 3.17 and IS 9.46. Predicting \(\epsilon\) with the full variational bound and a fixed isotropic covariance gives FID 13.51 and IS 7.67. The \(\tilde\mu\)-prediction baseline with the full bound gives FID 13.22 and IS 8.06.
- **Limitations:** sampling uses \(T=1000\) steps, so generation needs about a thousand network evaluations and is slow. The abstract does not report training or sampling cost. [DDIM](ddim.md) and latent diffusion address this.

## Connections

- Its faster sampler is [DDIM](ddim.md), which reuses the same trained model.
- Its latent-space successor is [Latent Diffusion](latent-diffusion.md), and its Transformer successor is [DiT](../../../../models/transformer/dit/index.md).
- Its conditioning method is [classifier-free guidance](classifier-free-guidance.md).
- The variational framing links to the probabilistic background in [Probabilistic Methods](../../../probabilistic/index.md).
- The continuous-time and flow view of the same objective is in [Flow Matching](../flow/flow-matching/index.md).

## Open questions

- How much of the sample quality comes from the simple loss, and how much from the U-Net and the noise schedule?
- Can the number of steps be reduced without retraining?

## References

### Seminal papers

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — Introduces the noise-prediction objective and reports high-quality CIFAR-10 and LSUN samples.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML (PMLR 37). https://arxiv.org/abs/1503.03585 — The earlier diffusion model whose forward and reverse processes DDPM builds on.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Shows that DDPM is a discretisation of a stochastic differential equation.

### Articles and documentation

- Ho, J., DDPM official code repository, *diffusion* project. https://github.com/hojonathanho/diffusion — The authors' original TensorFlow implementation of the paper's experiments.
- Song, J., Meng, C. & Ermon, S. (2020). Denoising Diffusion Implicit Models. arXiv. https://arxiv.org/abs/2010.02502 — Shows that a DDPM-trained model can be sampled in far fewer steps.

## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Code walk-through of DDPM training and sampling that matches the equations on this page.
