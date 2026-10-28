---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/generative/diffusion
tags:
  - generative models
  - uncertainty
aliases:
  - 朗之萬動力學
  - 朗之萬演算法
  - 朗之萬取樣
  - Langevin dynamics
  - Langevin algorithm
  - ULA
  - MALA
---

# Langevin Dynamics

Langevin dynamics is a sampling method that moves a state along the gradient of the log density and adds random noise at each step. As an [MCMC](../index.md) method it draws from a target distribution. With a learned score, it generates samples in score-based generative models, which are closely related to modern diffusion models.

## Overview

The Langevin diffusion is a stochastic differential equation whose stationary distribution is a given target $\pi$. It moves the state up the gradient of $\log\pi$ and adds Gaussian noise, so the state does not collapse onto the mode. A computer can take only discrete steps, and the resulting chain is biased unless corrected. Roberts and Tweedie (1996) gave conditions under which the continuous process and its discrete approximations converge to the target.

The method serves two purposes. In MCMC, it yields proposals that an accept–reject step can correct, which improve on random walks in [Metropolis–Hastings](../metropolis-hastings/index.md). In generative modelling, a score is learned from data and Langevin steps draw samples from it. Song and Ermon (2019) introduced this with annealing over noise levels.

## Key concepts

- **Score**: the gradient $\nabla_x \log p(x)$. It points toward higher probability and needs no normalising constant.
- **Unadjusted Langevin algorithm (ULA)**: the discretised chain without an accept–reject step. It is simple but biased, by an amount that depends on the step size.
- **MALA**: ULA with a Metropolis–Hastings correction, which removes the bias.
- **Denoising score matching**: learning the score by predicting the noise added to data (Vincent, 2011).

## How it works

The continuous process is

$$
dX_t = \nabla_x \log \pi(X_t)\,dt + \sqrt{2}\,dW_t,
$$

where $W_t$ is a Brownian motion. The ULA discretisation with step size $\eta$ is

$$
x_{k+1} = x_k + \eta\,\nabla_x \log\pi(x_k) + \sqrt{2\eta}\,\xi_k, \qquad \xi_k \sim \mathcal{N}(0, I).
$$

MALA uses this expression as a proposal and accepts it with the Metropolis–Hastings probability. Roberts and Rosenthal (1998) show how the step size must scale with dimension, with an optimal acceptance rate of about 0.574.

Song and Ermon (2019) apply annealed Langevin dynamics to a learned score $s_\theta(x, \sigma)$. For noise levels $\sigma_1 > \dots > \sigma_L$, they run $T$ steps at each level of

$$
x \leftarrow x + \alpha_i\, s_\theta(x, \sigma_i) + \sqrt{2\alpha_i}\,z, \qquad z \sim \mathcal{N}(0, I),
$$

with $\alpha_i = \varepsilon\,\sigma_i^2/\sigma_L^2$, moving from the largest noise level to the smallest.

Song et al. (2020) write the reverse of a noising process as a stochastic differential equation whose drift is the score,

$$
dX_t = \big[f(X_t, t) - g(t)^2\,\nabla_x \log p_t(X_t)\big]\,dt + g(t)\,d\bar W_t,
$$

and Langevin steps can serve as a corrector. Ho et al. (2020) relate the training of denoising diffusion models to denoising score matching with Langevin dynamics.

## Results

Roberts and Rosenthal (1998) show that for Metropolis-type proposals derived from Langevin diffusions, efficiency is governed by the acceptance rate rather than by the target. The asymptotically optimal rate is about 0.574, and the cost grows as the cube root of the dimension, compared with linear growth for random-walk proposals.

Song and Ermon (2019) report samples comparable to GANs on MNIST, CelebA and CIFAR-10.[^1] Song et al. (2020) report record unconditional image generation on CIFAR-10 for their score-based model.[^2] These results measure generated sample quality, not the mixing of the sampler as an MCMC method.

[^1]: The Inception score of 8.87 on CIFAR-10 is from the abstract of Song and Ermon (2019).
[^2]: The Inception score of 9.89 and FID of 2.20 on CIFAR-10 are from the abstract of Song et al. (2020), for a particular architecture and training setup.

## Limitations

- **Discretisation bias.** ULA is biased for any fixed step size. MALA removes the bias but rejects some moves and costs more per step.
- **Multimodal targets.** A local gradient method can stay in one mode, which is why annealing is used in generative settings.
- **Score errors.** Generated samples depend on how accurately the score is learned.
- **Many steps.** Annealed sampling needs many steps per noise level, so generation is slow.

## Open questions

- How does the discretisation error of a Langevin-type sampler relate to that of a diffusion model's sampler?
- Why does annealing help, and how many noise levels does a given data distribution need?

## References

### Seminal papers

- Roberts, G. O. & Tweedie, R. L. (1996). Exponential Convergence of Langevin Distributions and Their Discrete Approximations. *Bernoulli*. https://doi.org/10.2307/3318418 — Gives conditions for convergence of Langevin diffusions and their discrete approximations.
- Song, Y. & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. arXiv. https://arxiv.org/abs/1907.05600 — Generates samples with annealed Langevin dynamics driven by estimated scores.
- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2020). Score-Based Generative Modeling through Stochastic Differential Equations. arXiv. https://arxiv.org/abs/2011.13456 — Writes score-based and diffusion models as reverse-time SDEs with a Langevin corrector.
- Vincent, P. (2011). A Connection Between Score Matching and Denoising Autoencoders. *Neural Computation*. https://doi.org/10.1162/NECO_a_00142 — Shows that denoising autoencoders match the score of a density estimate.

### Surveys and textbooks

- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. arXiv. https://arxiv.org/abs/2006.11239 — Trains diffusion models with an objective related to denoising score matching.

### Articles and documentation

- Roberts, G. O. & Rosenthal, J. S. (1998). Optimal Scaling of Discrete Approximations to Langevin Diffusions. *JRSS B*. https://doi.org/10.1111/1467-9868.00123 — Gives the optimal acceptance rate and dimension scaling for Langevin-based proposals.
