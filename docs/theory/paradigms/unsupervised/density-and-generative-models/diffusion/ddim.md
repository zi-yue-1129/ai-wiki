---
status: draft
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

DDIM is a sampler for diffusion models that reuses a model trained with the DDPM objective but generates in far fewer steps. It changes the reverse process so that it is no longer a Markov chain, which allows steps to be skipped. The family-level picture is on the [Diffusion Models](index.md) page, and the training objective is in [DDPM](ddpm.md).

## Overview

DDPM generates samples by simulating a Markov chain of about a thousand steps. Song, Meng and Ermon (2021) observed that the same training objective is consistent with a family of non-Markovian forward processes. Each member of that family gives the same noise predictor and a different sampling rule. One member gives a deterministic sampler, and it can take any number of steps.

## Key concepts

- **Non-Markovian forward process**: each noisy sample \(x_t\) depends on the clean image \(x_0\), not only on \(x_{t-1}\). The training loss is unchanged.
- **Deterministic sampling**: with no fresh noise at each step, the same starting noise always gives the same image.
- **Step subsequence**: sampling can use an increasing subset \(\tau_1 < \dots < \tau_S\) of the training time steps, so the step count \(S\) is a free parameter.
- **Stochasticity \(\sigma\)**: a free parameter per step. Choosing the DDPM value recovers ancestral sampling, and \(\sigma = 0\) gives DDIM.

## How it works

Given the network's noise prediction \(\epsilon_\theta(x_t, t)\), the predicted clean image is

\[
\hat x_0 = \frac{x_t - \sqrt{1-\bar\alpha_t}\,\epsilon_\theta(x_t,t)}{\sqrt{\bar\alpha_t}}
\]

The next, less noisy sample is then

\[
x_{t_{\text{prev}}} = \sqrt{\bar\alpha_{t_{\text{prev}}}}\,\hat x_0 + \sqrt{1-\bar\alpha_{t_{\text{prev}}}-\sigma^2}\,\epsilon_\theta(x_t,t) + \sigma\,z
\]

where \(z\sim\mathcal N(0,I)\) is fresh noise and \(\sigma\) controls stochasticity. Setting \(\sigma = 0\) gives the deterministic sampler. With \(\sigma\) equal to the DDPM value, the update recovers ancestral sampling, so DDIM contains DDPM as a special case. The same trained model is reused with any choice of \(\sigma\).

## Key methods

### Denoising Diffusion Implicit Models (Song, Meng & Ermon, 2021)

- **Problem:** DDPM samples need many network evaluations, and its Markov reverse chain cannot skip steps.
- **Core idea:** keep the DDPM training objective but use a non-Markovian forward process whose reverse update can be applied with a shorter step subsequence.
- **Equation or algorithm:** the update above, with \(\sigma = 0\) for deterministic sampling. The paper's Eq. 12 is the same update written with \(\alpha_t\) for the cumulative product.
- **Results:** the abstract reports that DDIMs produce high-quality samples 10× to 50× faster in wall-clock time than DDPMs. On unconditional CIFAR-10 (Table 1), DDIM gives FID 4.67 with 50 steps, 4.16 with 100 steps and 4.04 with 1000 steps. DDPM gives 8.01 with 50 steps, 5.78 with 100 steps and 4.73 with 1000 steps. With 10 steps the gap is largest: DDIM 13.36 against DDPM 41.07.
- **Limitations:** quality still drops at very few steps, as the 10-step result shows. The speed-up is measured in wall-clock time on the paper's setup, and the paper itself quotes both 10× to 50× and 10× to 100× in different places. The deterministic sampler gives one output per starting noise, so it does not sample the stochastic variety of DDPM.

## Connections

- The training objective comes from [DDPM](ddpm.md).
- Other sampler and distillation ideas are summarised on the [Diffusion Models](index.md) page under faster sampling.
- Latent-space sampling in [Latent Diffusion](latent-diffusion.md) can use DDIM-style updates in the same way.
- The probability-flow ODE view of the deterministic sampler is in [Score-Based SDEs](https://arxiv.org/abs/2011.13456), cited below.

## Open questions

- How few steps can a deterministic sampler use before quality breaks down, and does this depend on the image domain?
- Which sampler is best for a given trade-off between diversity and speed?

## References

### Seminal papers

- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — Introduces the non-Markovian sampler, with FID and step counts on CIFAR-10 in Table 1.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The training objective and Markov sampler that DDIM accelerates.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Shows the deterministic sampler as a probability-flow ODE.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Compares sampling schedules and solvers across diffusion models.
- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — The original Markov-chain sampler that DDIM generalises to non-Markovian steps.

## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Walk-through of the DDPM sampler that DDIM generalises.
