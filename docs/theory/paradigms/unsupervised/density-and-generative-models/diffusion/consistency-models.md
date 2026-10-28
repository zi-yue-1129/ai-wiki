---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/flow/flow-matching/conditional-flow-matching.md
tags:
  - diffusion models
  - fast sampling
  - consistency models
aliases:
  - Consistency models
  - 一致性模型
  - 快速採樣
  - progressive distillation
  - DPM-Solver
---

# Consistency Models and Fast Samplers

Diffusion models generate by running a denoising process many times, often for hundreds of steps. Consistency models and the fast samplers around them aim to produce comparable samples in one to a few steps. The question they answer is how much of the many-step process can be compressed without losing sample quality, and what the compressed model learns in the process.

## Overview

A diffusion sampler integrates a learned reverse process from noise to data. Each step is a neural network evaluation, so the cost of sampling is the number of steps times the cost of one evaluation. Reducing that number is the goal of most work in this area, and it can be pursued in three ways: change the sampler so that fewer steps are accurate, distil a many-step sampler into a few-step student, or train a model that is designed to act in one step.

Consistency models take the third route. Song et al. (2023) describe them as supporting "fast one-step generation by design", and they also allow several steps to refine a sample. The samplers described below take the first route, and progressive distillation takes the second.

## Key concepts

- **Sampling steps**: the number of network evaluations needed to produce one sample. This is the main cost of diffusion sampling.
- **Deterministic sampler**: a sampler that maps a noise sample to a data sample by a fixed rule, so the same noise gives the same output.
- **Ordinary differential equation (ODE) sampler**: a sampler that integrates a deterministic flow from noise to data, which can use standard numerical solvers.
- **Distillation**: training a student model to reproduce the output of a teacher that needs more steps.
- **Self-consistency**: the property that points on the same sampling trajectory map to the same output. A consistency model is trained to have it.

## How it works

**Deterministic sampling.** Song, Meng and Ermon (2021) introduce denoising diffusion implicit models (DDIM), which use a non-Markovian process with the same training objective as DDPM. The abstract reports that DDIMs "can produce high quality samples 10× to 50× faster in terms of wall-clock time" than the original sampler. The method is deterministic, so it can trade sample diversity for speed and allows interpolation between samples. See [DDIM](ddim.md).

**Higher-order ODE solvers.** Lu et al. (2022) treat sampling as solving an ODE and build a solver tailored to the diffusion process. The abstract reports that DPM-Solver "can generate high-quality samples in only 10 to 20 function evaluations", without retraining the model.

**Progressive distillation.** Salimans and Ho (2022) train a student that takes half as many sampling steps as its teacher, and repeat the process to halve the steps again. The abstract describes the new model as one that "takes half as many sampling steps". Each round requires training, but the final sampler needs few steps.

**Consistency models.** Song et al. (2023) train a network $f_\theta(x_t, t)$ so that all points on one trajectory of the diffusion process map to the same output, which is the trajectory's clean data point. A consistency model can then produce a sample in one step by evaluating $f_\theta(x_T, T)$ at the noise level $T$. Two training routes are described in the paper: distilling a pre-trained diffusion model, and training the consistency model directly from data. Refining the sample with additional steps, which trades a little time for quality, is also supported.

## Key methods

Brief comparison. Each named method is a candidate for its own method page; those pages are not yet written, so the detail is given in this section for now.

- **DDIM (deterministic, non-Markovian)**: a change of sampler with the same trained model. Large speed-ups with modest loss in quality, and a clean path for interpolation.
- **DPM-Solver (high-order ODE)**: a numerical solver for the same model, with 10 to 20 evaluations for good samples.
- **Progressive distillation (teacher–student halving)**: repeated halving of the steps, each round training a new student.
- **Consistency models (self-consistent mapping)**: trained to map any point of a trajectory to its origin, supporting one-step and multi-step sampling.

## Connections

The base process and the training objective are on the [DDPM](ddpm.md) page, and the deterministic sampler on the [DDIM](ddim.md) page. The [Latent diffusion](latent-diffusion.md) and [Classifier-free guidance](classifier-free-guidance.md) pages describe other ways in which the cost and quality of diffusion sampling are traded off. Flow-based models give a related route to few-step sampling, through straighter paths, see [Conditional flow matching](../flow/flow-matching/conditional-flow-matching.md).

These models are built for generation rather than as accounts of neural processing, so any link to the brain is a question for [NeuroAI](../../../../../brain-mind/neuroai/index.md), not a property of the methods.

## Applications

- **Interactive image generation.** One- or few-step samplers make generation fast enough for interactive tools.
- **Editing and inpainting.** The same samplers are used with conditioning to fill in or change parts of an image.
- **Video and audio.** Fast sampling matters more for longer outputs, where each step is more costly.

## Open questions

- Few-step samples often lag behind many-step samples in fine detail, and the gap depends on the model, the data and the distillation method.
- Distillation needs a teacher, and the cost of training the student can be large.
- Consistency models trained directly from data are less well understood than distilled ones, and their theory is still developing.
- Comparisons across samplers depend on which evaluation metric is used, and metrics for generation quality remain debated.

## References

### Seminal papers

- Song, Y., Dhariwal, P., Chen, M. & Sutskever, I. (2023). *Consistency Models*. In *Proceedings of the 40th International Conference on Machine Learning (ICML 2023)*, PMLR 202. https://arxiv.org/abs/2303.01469 — Introduces consistency models, which map points on a diffusion trajectory to its output and support one-step generation.
- Salimans, T. & Ho, J. (2022). *Progressive Distillation for Fast Sampling of Diffusion Models*. In *ICLR 2022*. https://arxiv.org/abs/2202.00512 — Halves the sampling steps of a diffusion model by repeated distillation into students that take half as many steps.
- Song, J., Meng, C. & Ermon, S. (2021). *Denoising Diffusion Implicit Models*. In *ICLR 2021*. https://arxiv.org/abs/2010.02502 — Deterministic, non-Markovian sampler that gives much faster sampling with the same trained model.
- Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C. & Zhu, J. (2022). *DPM-Solver: A Fast ODE Solver for Diffusion Probabilistic Model Sampling in Around 10 Steps*. In *NeurIPS 2022*. https://arxiv.org/abs/2206.00927 — A high-order ODE solver for diffusion sampling, with high-quality samples in about 10 to 20 function evaluations.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. In *NeurIPS 2020*. https://arxiv.org/abs/2006.11239 — The base model and sampler that the methods on this page accelerate.
