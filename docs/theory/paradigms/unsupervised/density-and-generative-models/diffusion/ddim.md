---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - diffusion models
  - sampling
aliases:
  - 去噪擴散隱式模型
  - DDIM
  - Denoising diffusion implicit models
---

# DDIM: Denoising Diffusion Implicit Models

DDIM (Song, Meng & Ermon, 2021) is a sampler for diffusion models. It reuses a model trained with the DDPM objective, but generates in far fewer steps by making the reverse process non-Markovian, so that steps can be skipped. The family-level picture is on the [Diffusion Models](index.md) page, and the training objective is in [DDPM](ddpm.md).

## Overview

DDPM generates an image by simulating a Markov chain of about a thousand denoising steps. Song, Meng & Ermon observed that the DDPM objective depends only on the marginal distributions \(q(x_t \mid x_0)\), not on the joint distribution of the whole chain. Many different forward processes share those marginals, and each one gives a different sampler. One choice gives a deterministic sampler, and it can use any number of steps.

## Problem

Sampling from a DDPM takes one network evaluation per training step, so a typical sample needs about 1000 evaluations. The reverse process is a Markov chain, so it cannot skip steps without changing the model's assumptions. The question is whether a model trained with the DDPM objective can be sampled with far fewer steps, without retraining.

## Core idea

The paper defines a family of inference processes \(q_\sigma(x_{1:T} \mid x_0)\) indexed by a stochasticity parameter \(\sigma\). Each member has the same marginals as DDPM, so the same trained network is valid for every \(\sigma\). The generative process is then run over an increasing subsequence of \(S\) training steps, which can be much shorter than \(T\). Setting \(\sigma = 0\) gives a deterministic sampler, in which the same starting noise always produces the same image. Choosing the DDPM value of \(\sigma\) recovers ancestral sampling, so DDPM is a special case.

## Algorithm

Given the network's noise prediction \(\epsilon_\theta(x_t, t)\), the predicted clean image is

\[
\hat x_0 = \frac{x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta(x_t,t)}{\sqrt{\bar\alpha_t}}
\]

The next, less noisy sample is then

\[
x_{t_{\text{prev}}} = \sqrt{\bar\alpha_{t_{\text{prev}}}}\,\hat x_0 + \sqrt{1-\bar\alpha_{t_{\text{prev}}}-\sigma^2}\,\epsilon_\theta(x_t,t) + \sigma\,z, \qquad z \sim \mathcal N(0, I)
\]

Here \(t_{\text{prev}}\) is the previous step in the subsequence. In the paper's notation \(\alpha_t\) denotes the cumulative product, so \(\alpha_t\) here is the \(\bar\alpha_t\) used above. With \(\sigma = 0\) the update is deterministic. The paper notes that this update resembles an Euler integration step of an ordinary differential equation, which is the basis of its connection to neural ODEs.

## Results

The paper's Table 1 reports FID on unconditional CIFAR-10 as the number of steps \(S\) varies. Here \(\eta\) is the paper's name for \(\sigma\): \(\eta = 0\) is DDIM and \(\eta = 1\) is DDPM.

| Steps \(S\) | 10 | 20 | 50 | 100 | 1000 |
|---|---|---|---|---|---|
| DDIM (\(\eta = 0\)) | 13.36 | 6.84 | 4.67 | 4.16 | 4.04 |
| DDPM (\(\eta = 1\)) | 41.07 | 18.36 | 8.01 | 5.78 | 4.73 |

On CelebA (64×64), DDIM with 20 steps (FID 13.73) is about as good as DDPM with 100 steps (FID 13.93). The paper reports that DDIM reaches quality comparable to the 1000-step model within 20 to 100 steps, a 10× to 50× speed-up. Its introduction also quotes 10× to 100×. The speed-up was measured as sampling time, which the paper shows scales linearly with the number of steps.

## Limitations

- **Quality still falls at very few steps.** At 10 steps the FID is 13.36, against 4.04 at 1000 steps, so the speed-up has a quality cost.
- **Results come from one setting.** The paper's experiments are on CIFAR-10 and CelebA, with the models it trained itself.
- **Less diversity per noise.** Because the deterministic sampler maps each starting noise to one image, it does not explore the stochastic variety of ancestral sampling in the same way.
- **Speed depends on design choices.** Karras et al. (2022) show that the time schedule and the solver have a large effect on quality, so the sampler needs tuning.

## Connections

- The training objective comes from [DDPM](ddpm.md), and DDIM uses the same network without retraining.
- [Latent Diffusion](latent-diffusion.md) samples with DDIM steps in its experiments, so the method applies to latent models too.
- The continuous-time view of the deterministic sampler, as a probability-flow ordinary differential equation, is in Song et al. (2021), cited below.
- Other sampler and distillation ideas are summarised on the [Diffusion Models](index.md) page under faster sampling.

## Open questions

- How few steps can a deterministic sampler use before quality breaks down, and does this depend on the image domain?
- Which sampler suits a given trade-off between diversity and speed?
- How much does the deterministic sampler's loss of diversity matter for tasks such as image editing?

## References

### Seminal papers

- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — Introduces the non-Markovian sampler, with FID against the number of steps in Table 1.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The training objective and Markov sampler that DDIM accelerates.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — The original Markov-chain diffusion model that DDIM generalises.
- Rombach, R. et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — Uses DDIM sampling with 100 to 200 steps in its experiments.

### Surveys and textbooks

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Defines the probability-flow ordinary differential equation that matches the deterministic sampler.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Separates the design choices of diffusion samplers, including the step schedule and solver.


