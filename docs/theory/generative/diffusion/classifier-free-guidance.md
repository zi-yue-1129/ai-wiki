---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - diffusion models
  - guidance
aliases:
  - 無分類器引導
  - Classifier-free guidance
  - CFG
---

# Classifier-Free Guidance

Classifier-free guidance is a way to make a conditional diffusion model follow its condition more closely, such as a text prompt, at the cost of diversity. It needs no separate classifier. A single network is trained both with and without the condition, and at sampling time the two predictions are combined. It is the standard conditioning control in text-to-image diffusion models. The family-level picture is on the [Diffusion Models](index.md) page.

## Overview

Dhariwal and Nichol (2021) showed that guiding diffusion models with the gradient of a separately trained classifier improves sample quality. This is called classifier guidance. It needs an extra classifier trained on noisy images, which is an awkward extra component. Ho and Salimans (2022) removed the classifier by training the diffusion model itself to make unconditional predictions as well as conditional ones.

## Key concepts

- **Conditional model** \(\epsilon_\theta(x_t, t, c)\): predicts noise given the condition \(c\).
- **Unconditional model** \(\epsilon_\theta(x_t, t, \varnothing)\): the same network with the condition dropped.
- **Guidance scale** \(w\): how strongly the condition is emphasised at sampling time. Larger values give closer prompt matching and less diversity.
- **Condition dropout**: during training, the condition is replaced by a null token with some probability, typically around 10%.

## How it works

At each sampling step the network is run twice, and the predictions are combined as

\[
\tilde\epsilon = \epsilon_\theta(x_t, t, \varnothing) + w\,\big(\epsilon_\theta(x_t, t, c) - \epsilon_\theta(x_t, t, \varnothing)\big)
\]

With \(w = 1\) this is the plain conditional model. Larger \(w\) pushes the sample further in the direction that the condition adds. This doubles the cost per step, because two network evaluations are needed.

## Key methods

### Classifier-Free Diffusion Guidance (Ho & Salimans, 2022)

- **Problem:** classifier guidance trades diversity for quality, but needs a separate classifier trained on noisy images, which is costly and awkward.
- **Core idea:** train one diffusion model with the condition randomly dropped, then blend its conditional and unconditional score estimates at sampling time.
- **Equation or algorithm:** the combination rule above, with the guidance scale \(w\) chosen at sampling time.
- **Results:** the abstract says guidance can be performed by a pure generative model without a classifier, and that the blended approach achieves a quality–diversity trade-off comparable to classifier guidance. It gives no numbers in the abstract.
- **Limitations:** the doubled cost per step, and the loss of diversity at high guidance scales, both remain. The abstract does not quantify either.

## Connections

- The condition is usually encoded by a cross-attention path described in [Latent Diffusion](latent-diffusion.md).
- The denoiser is often a [DiT](dit.md) or U-Net; guidance is independent of the backbone.
- The faster samplers in [DDIM](ddim.md) can be combined with guidance.

## Open questions

- How should the guidance scale change over the sampling trajectory?
- Can guidance be made cheaper than two network evaluations per step?

## References

### Seminal papers

- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — Introduces guidance without an external classifier by blending conditional and unconditional predictions.
- Dhariwal, P. & Nichol, A. (2021). Diffusion Models Beat GANs on Image Synthesis. NeurIPS. https://arxiv.org/abs/2105.05233 — Introduces classifier guidance, the method classifier-free guidance replaces.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The base diffusion model that guidance is applied to.

### Surveys and textbooks

- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Discusses guidance and sampling choices in a unified design framework.
- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Shows how conditional sampling can steer the score, the view that classifier-free guidance builds on.

### Articles and documentation

