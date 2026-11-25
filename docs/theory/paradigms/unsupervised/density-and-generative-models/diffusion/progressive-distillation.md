---
status: draft
last_reviewed: 2026-11-25
tags:
  - diffusion models
  - distillation
  - fast sampling
aliases:
  - Progressive distillation
  - 漸進式蒸餾
  - 逐步蒸餾
  - 漸進蒸餾
---

# Progressive distillation

Progressive distillation (Salimans & Ho, 2022) is a method that makes a deterministic diffusion sampler take half as many steps, and then repeats the process to halve the steps again. Each round trains a student network to reproduce, in one step, what two steps of its teacher produce. The family-level picture is on the [Diffusion Models](index.md) page. The sampler it distils is [DDIM](ddim.md).

## Overview

A deterministic sampler such as DDIM can be run with fewer steps, but its quality falls as the steps are reduced. Progressive distillation changes the model instead of the sampler. The student is trained to act like the teacher with twice the step size, so the student needs half the evaluations. Because the student becomes the next teacher, the process can be repeated until only a few steps remain.

## Problem

The aim is a sampler that takes a few network evaluations, while keeping the quality of a sampler that takes hundreds or thousands. Salimans and Ho (2022) start from a diffusion model with a deterministic sampler, and ask whether it can be distilled into a model that needs only four steps without losing much perceptual quality.

## Core idea

Let the teacher be a model that samples with DDIM in \(N\) steps. The student is trained to take \(N/2\) steps that match two teacher DDIM steps. For a time \(t\), the teacher takes two steps to \(t'\) and then \(t''\). The student is trained so that one step from \(z_t\) lands where the teacher's two steps land. The student's input is the noisy sample \(z_t\), and its target is the clean sample that the teacher's two-step result implies. After training, the student becomes the teacher for the next round, with half as many steps.

The paper also makes two changes that the distillation needs. The first is the parameterisation of the network output. Ho et al. (2020) predict the noise \(\epsilon\). The paper finds that predicting \(\epsilon\) combined with the truncated-SNR loss weighting diverges, and proposes predicting the clean sample \(x\) directly, or predicting a velocity \(v = \alpha_t \epsilon - \sigma_t x\), which gives \(\hat x = \alpha_t z_t - \sigma_t \hat v\). The second is the loss weighting. The weighting used by Ho et al. (2020), based on signal-to-noise ratio, gives zero weight to data with zero signal, which the paper says makes it unsuitable for distillation, so it uses a truncated or "SNR+1" weighting instead.

## Algorithm

The paper's Algorithm 2 has four parts. For \(K\) rounds:

1. **Initialise the student from the teacher**, so the student starts from a good model rather than from scratch.
2. **Sample a time** \(t = i/N\) for a random integer \(i\) between 1 and \(N\), and noise \(\epsilon\), and form \(z_t = \alpha_t x + \sigma_t \epsilon\) from a training example \(x\).
3. **Compute the teacher's target.** Take two DDIM steps with the teacher, from \(t\) to \(t' = t - 0.5/N\) and then to \(t'' = t - 1/N\). The target combines the two steps into a single clean-sample estimate:

\[
\tilde x = \frac{z_{t''} - \frac{\sigma_{t''}}{\sigma_t}\,z_t}{\alpha_{t''} - \frac{\sigma_{t''}}{\sigma_t}\,\alpha_t}.
\]

4. **Train the student** on the weighted loss \(w(\lambda_t)\,\lVert \tilde x - \hat x_\theta(z_t)\rVert_2^2\), where \(\lambda_t = \log(\alpha_t^2/\sigma_t^2)\) is the log signal-to-noise ratio. Then make the student the teacher and halve \(N\).

Each round is a full training run. The paper trains each student for a fixed number of updates, and the number of updates per round matters for quality, which is discussed below.

## Results

On unconditional CIFAR-10, the paper reports the FID of the distilled model for several step counts, next to DDIM with a standard schedule:

| Method | Model evaluations | FID |
|---|---|---|
| Progressive distillation | 1 | 9.12 |
| Progressive distillation | 2 | 4.51 |
| Progressive distillation | 4 | 3.00 |
| Progressive distillation | 8 | 2.57 |
| [DDIM](ddim.md) (Song et al., 2021) | 10 | 13.36 |
| DDIM | 50 | 4.67 |
| DDIM | 100 | 4.16 |

The abstract reports a FID of 3.0 on CIFAR-10 in 4 steps, and says the distillation can start from samplers that take as many as 8192 steps. It also reports that the full procedure takes no more time than training the original model. In the ablation study, predicting \(x\) or \(v\) with the paper's loss weightings gives results close to each other on CIFAR-10. The noise prediction with truncated-SNR weighting is the one combination the paper reports as unstable.

## Limitations

- **One training run per halving.** Each halving needs a new student, so the cost of distillation grows with the number of rounds, even if the total stays near the cost of training the original model.
- **Same architecture.** The paper limits itself to students with the same architecture and number of parameters as the teacher, and lists relaxing this as future work.
- **Quality at one step.** The one-step result has an FID of 9.12, well behind the four-step result. The paper also reports that when the sampler takes very few steps, the loss in quality is larger if each student is trained for only a short time.
- **Deterministic samplers.** The method is built on a deterministic sampler, and the paper's discussion frames it that way.

## Connections

- The sampler being distilled is [DDIM](ddim.md), and the teacher's two steps are DDIM steps.
- [DPM-Solver](dpm-solver.md) reaches a similar step count without any training, by changing the sampler rather than the model.
- [Consistency models](consistency-models.md) also reach one or few steps, and can be trained by distilling a diffusion model. They use a different training target.
- The [Diffusion Models](index.md) page summarises distillation together with the other faster-sampling families.

## Open questions

- Can the student differ in architecture from the teacher, as the paper's future-work note suggests, without losing quality?
- How much of the quality at one or two steps depends on the number of updates per round?
- Does the same procedure work for stochastic samplers, or does it depend on the deterministic mapping?

## References

### Seminal papers

- Salimans, T. & Ho, J. (2022). *Progressive Distillation for Fast Sampling of Diffusion Models*. In *ICLR 2022*. https://arxiv.org/abs/2202.00512 — Introduces progressive distillation, the velocity and clean-sample parameterisations, and the repeated halving of sampling steps.
- Song, J., Meng, C. & Ermon, S. (2021). *Denoising Diffusion Implicit Models*. In *ICLR 2021*. https://arxiv.org/abs/2010.02502 — The deterministic sampler that the teacher uses, and the source of the 10-step DDIM baseline.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. In *NeurIPS 2020*. https://arxiv.org/abs/2006.11239 — The noise-prediction training objective that the distilled models replace with other parameterisations.
- Song, Y., Dhariwal, P., Chen, M. & Sutskever, I. (2023). *Consistency Models*. In *ICML 2023*. https://arxiv.org/abs/2303.01469 — A later few-step method that can also be obtained by distilling a diffusion model.

### Surveys and textbooks

- Yang, L., Zhang, Z., Song, Y., Hong, S., Xu, R., Zhao, Y., Zhang, W., Cui, B. & Yang, M.-H. (2022). *Diffusion Models: A Comprehensive Survey of Methods and Applications*. arXiv. https://arxiv.org/abs/2209.00796 — Survey of diffusion models that covers distillation and fast samplers.
