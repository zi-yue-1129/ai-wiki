---
related:
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
  - theory/paradigms/unsupervised/density-and-generative-models/generative-models
tags:
  - diffusion models
  - score-based models
  - stochastic differential equations
aliases:
  - Score SDE
  - Score-based generative modeling through SDEs
  - 基於隨機微分方程的分數生成模型
  - 分數式生成模型
last_reviewed: 2026-11-01
---

# Score-Based Generative Modeling through SDEs

Song et al. (2021) showed that the two main score-based generative models are discretisations of stochastic differential equations (SDEs). One is the noise-conditioned score network (NCSN), which uses a sequence of noise levels. The other is DDPM. The paper builds a general framework on this view. A fixed forward SDE adds noise to data, a reverse-time SDE removes it using the score (the gradient of the log density), and a deterministic probability flow ODE has the same marginal densities. The framework unifies earlier models, allows exact likelihood computation, and opens new samplers. The family-level picture is on the [Diffusion Models](index.md) page.

## Problem

By 2020, diffusion-style and score-based models were built from discrete noise schedules. Each had its own training objective and sampler, and the relation between them was unclear. The paper asks whether one continuous-time description can cover both, and whether that description gives better tools for sampling and likelihood.

## Core idea

The framework has three parts.

- **Forward SDE.** A drift \(f(x,t)\) and a diffusion coefficient \(g(t)\) define how data is perturbed over time:
\[
dx = f(x,t)\,dt + g(t)\,dw
\]
This process is fixed and does not depend on the data or on any learned parameters.
- **Reverse-time SDE.** Reversing the process requires the score \(\nabla_x \log p_t(x)\) of each marginal distribution. Anderson (1982) gives the reverse SDE:
\[
dx = \big[f(x,t) - g(t)^2 \nabla_x \log p_t(x)\big]\,dt + g(t)\,d\bar w
\]
Here \(\bar w\) is a Wiener process running backward in time. A neural network is trained to approximate the score across noise levels, and then this equation is solved to generate samples.
- **Probability flow ODE.** The deterministic ODE
\[
dx = \big[f(x,t) - \tfrac{1}{2} g(t)^2 \nabla_x \log p_t(x)\big]\,dt
\]
has the same marginal densities \(p_t\) as the SDE. Because it is an ODE, it gives exact likelihoods when the score is a neural network, and it allows fast deterministic sampling.

### Two special cases

| SDE | Drift \(f\) | Diffusion \(g\) | Continuous limit of |
|---|---|---|---|
| Variance-preserving (VP) | \(-\tfrac{1}{2}\beta(t)\,x\) | \(\sqrt{\beta(t)}\) | DDPM |
| Variance-exploding (VE) | \(0\) | \(\sqrt{d[\sigma^2(t)]/dt}\) | SMLD, the noise-conditioned score network |

The paper says that the VP process keeps the variance at one when the data has unit variance. The VE process has a variance that grows without bound as \(t \to \infty\). Both are the continuous-time limits of the discrete processes they name.

## Results

Table 3 of the paper reports unconditional CIFAR-10 results, with FID (lower is better) and Inception score (higher is better). The rows below are a selection from that table.

| Model | FID ↓ | IS ↑ |
|---|---|---|
| NCSN (Song & Ermon, 2019) | 25.32 | 8.87 ± 0.12 |
| NCSNv2 (Song & Ermon, 2020) | 10.87 | 8.40 ± 0.07 |
| DDPM (Ho et al., 2020) | 3.17 | 9.46 ± 0.11 |
| NCSN++ | 2.45 | 9.73 |
| NCSN++ continuous (VE) | 2.38 | 9.83 |
| NCSN++ continuous, deep (VE) | 2.20 | 9.89 |

The best model in the table is the deep NCSN++ with a VE process, which the abstract reports as Inception score 9.89 and FID 2.20. These numbers use the best checkpoint by FID, sampled with predictor-corrector samplers. The paper's main contribution here is the framework. The gain over DDPM is a modest improvement on the same dataset, not a large jump.

## Limitations

- **Sampling speed.** The paper states that score-based models "remain slower at sampling than GANs" on the same datasets.
- **Combining methods.** The authors call for ways to combine the stable training of score-based models with the fast sampling of implicit models such as GANs, which they describe as "an important research direction."
- **Sampler hyperparameters.** The many sampler options add hyperparameters. The paper calls for methods that "automatically select and tune these hyperparameters."

## Connections

- The discrete-time special case with the variance-preserving process is [DDPM](ddpm.md). The same trained model can be sampled faster with [DDIM](ddim.md), which is non-Markovian.
- The continuous-time view gives the sampler family used later in [latent diffusion](latent-diffusion.md) and with [classifier-free guidance](classifier-free-guidance.md).
- The score-based and diffusion framing used here is one of several generative algorithms covered in [Generative Models](../generative-models/index.md).

## Open issues

- Can the sampler hyperparameters be chosen automatically for each model and dataset?
- How far can the number of function evaluations be reduced in the probability flow ODE without losing quality?
- Which parts of the framework are needed for good quality, and which are only needed for exact likelihood?

## References

### Seminal papers

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR (Oral). [arXiv:2011.13456](https://arxiv.org/abs/2011.13456) — Gives the forward and reverse SDEs, the probability flow ODE, and the VP and VE special cases.
- Song, Y. & Ermon, S. (2019). Generative Modeling by Estimating Gradients of the Data Distribution. [arXiv:1907.05600](https://arxiv.org/abs/1907.05600) — The noise-conditioned score network (NCSN), the discrete-noise model that the VE process generalises.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. [arXiv:2006.11239](https://arxiv.org/abs/2006.11239) — The discrete process that the VP SDE is the continuous limit of.
- Anderson, B. D. O. (1982). Reverse-time diffusion equation models. Stochastic Processes and their Applications, 12, 313–326. [DOI 10.1016/0304-4149(82)90051-5](https://doi.org/10.1016/0304-4149(82)90051-5) — Gives the reverse-time SDE that the paper uses for sampling.
- Vincent, P. (2011). A Connection Between Score Matching and Denoising Autoencoders. Neural Computation, 23, 1661–1674. [DOI 10.1162/NECO_a_00142](https://doi.org/10.1162/NECO_a_00142) — Links score matching to denoising, the basis of training a score network.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Song, Y. & Ermon, S. (2020). Improved Techniques for Training Score-Based Generative Models. [arXiv:2006.09011](https://arxiv.org/abs/2006.09011) — Practical techniques for score-based models that build on the NCSN line of work.
- Goodfellow, I. J. et al. (2014). Generative Adversarial Networks. [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) — The GAN baseline that the paper compares sampling speed against.
