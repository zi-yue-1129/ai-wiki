---
status: draft
last_reviewed: 2026-10-28
tags:
  - adversarial training
  - security
  - calibration
aliases:
  - 隨機平滑
  - 可證明穩健性
  - Randomized Smoothing
  - certified robustness
---

# Randomized Smoothing

Randomized smoothing turns any classifier into a smoothed classifier that comes with a provable guarantee. For each input it certifies a radius within which no \(\ell_2\) perturbation can change the prediction. Cohen et al. (2019) gave a tight guarantee for Gaussian noise and scaled it to ImageNet. It is one of the methods on the [adversarial examples and robustness](../index.md) overview.

## Overview

Earlier certified defences worked on small networks or needed special training. Raghunathan et al. (2018) used a semidefinite relaxation for networks with one hidden layer. Randomized smoothing works with any base network, because the guarantee comes from averaging over random noise rather than from the network's internals. Cohen et al. (2019) state that they turn any classifier that performs well under Gaussian noise into a classifier certifiably robust under the \(\ell_2\) norm, and they report that no certified defence had then been shown feasible on ImageNet except smoothing.

## Key concepts

- **Smoothed classifier.** The prediction is the class that the base classifier outputs most often when the input is corrupted by Gaussian noise.
- **Certified radius.** The largest \(\ell_2\) distance from the input within which the smoothed prediction is guaranteed not to change.
- **Base classifier.** The network that is averaged over noise. It must be trained with noise, so that it still predicts well on noisy inputs.
- **Abstention.** When the noisy votes are not decisive enough to certify any radius, the method declines to predict.
- **Probabilistic certificate.** Vote fractions are estimated by sampling, so the guarantee holds with a chosen confidence level.

## How it works

The smoothed classifier is

\[
g(x) = \arg\max_c \; \mathbb{P}_{\eta \sim \mathcal{N}(0, \sigma^2 I)}\big[f(x+\eta) = c\big].
\]

Let \(p_A\) be the probability of the top class and \(p_B\) that of the runner-up. Cohen et al. (2019) show that \(g\) keeps its prediction within an \(\ell_2\) ball of radius

\[
R = \frac{\sigma}{2}\big(\Phi^{-1}(p_A) - \Phi^{-1}(p_B)\big),
\]

where \(\Phi^{-1}\) is the inverse of the standard normal distribution function. Since \(p_B \le 1 - p_A\), the simpler value \(\sigma\,\Phi^{-1}(p_A)\) is a valid, slightly conservative radius.

Certification proceeds in four steps.

1. Train the base classifier on inputs with Gaussian noise of scale \(\sigma\) added.
2. Draw many noisy copies of the input and count the votes for each class.
3. Replace the observed fraction of the top class with a lower confidence bound \(\underline{p}_A\).
4. If \(\underline{p}_A\) is above one half, certify the radius \(\sigma\,\Phi^{-1}(\underline{p}_A)\); otherwise abstain.

## Results

Cohen et al. (2019) report, in their abstract, an ImageNet classifier with a certified top-1 accuracy of 49% under \(\ell_2\) perturbations of norm less than 0.5. On smaller datasets, where competing certified approaches are feasible, they report that smoothing gives higher certified accuracies.

## Limitations

- **Guarantee in \(\ell_2\) only.** Gaussian smoothing gives guarantees for \(\ell_2\) perturbations; it does not directly give the \(\ell_\infty\) guarantees that most attack benchmarks use.
- **Clean accuracy falls.** Training on noise reduces accuracy on unperturbed inputs, and the trade-off grows with the noise scale.
- **Radius and accuracy trade off.** A larger \(\sigma\) gives a larger radius but a noisier base classifier, so the choice of \(\sigma\) is a design decision.
- **Cost.** Certifying one input needs many noisy forward passes.
- **Narrow threat model.** The certificate covers only the \(\ell_2\) ball. It does not cover semantic or physical changes such as prompt injection, covered in [LLM security](../../../../engineering/llm-security/index.md).

## Open questions

- Can certificates be extended to other norms or to larger perturbations without losing much clean accuracy?
- The certified radii are smaller than the radii that empirical attacks find, so how large is the remaining gap?
- How should abstention be handled in deployed systems, where a refusal may have its own cost?

## Connections

Smoothing is an average over perturbed inputs, a close relative of the averaging used in [MC dropout](../../uncertainty-and-calibration/mc-dropout/index.md) and of the abstention that [uncertainty and calibration](../../uncertainty-and-calibration/index.md) studies. The probabilistic certificate relies on confidence intervals, described in [probabilistic methods](../../../probabilistic/index.md). Lécuyer et al. (2018) connected the same kind of noise-based guarantee to differential privacy, a link to the [privacy](../../../../society/privacy/index.md) literature.

## Applications

- **Certified image classifiers.** Smoothed networks give ImageNet-scale certificates, which serve as a reference point for certified robustness.

## References

### Seminal papers

- Cohen, J. M., Rosenfeld, E. & Kolter, J. Z. (2019). *Certified Adversarial Robustness via Randomized Smoothing*. arXiv. https://arxiv.org/abs/1902.02918 — Proves a tight \(\ell_2\) guarantee for Gaussian smoothing and reports certified accuracy on ImageNet.
- Raghunathan, A., Steinhardt, J. & Liang, P. (2018). *Certified Defenses against Adversarial Examples*. arXiv. https://arxiv.org/abs/1801.09344 — A semidefinite relaxation gives certificates for one-hidden-layer networks, a model class where certified training was feasible.
- Wong, E. & Kolter, J. Z. (2017). *Provable defenses against adversarial examples via the convex outer adversarial polytope*. arXiv. https://arxiv.org/abs/1711.00851 — Learns ReLU classifiers with provable robustness, using a convex outer approximation of reachable activations.
- Lécuyer, M. et al. (2018). *Certified Robustness to Adversarial Examples with Differential Privacy*. arXiv. https://arxiv.org/abs/1802.03471 — Proposes PixelDP, a certified defence that scales to ImageNet-sized networks and applies to arbitrary models.

### Surveys and textbooks

- Akhtar, N. & Mian, A. (2018). *Threat of Adversarial Attacks on Deep Learning in Computer Vision: A Survey*. arXiv. https://arxiv.org/abs/1801.00553 — Surveys attacks and defences in computer vision, providing background for certified methods.

### Articles and documentation

- Carlini, N. et al. (2019). *On Evaluating Adversarial Robustness*. arXiv. https://arxiv.org/abs/1902.06705 — Gives methodological guidance for evaluating defences, noting that many are broken by adaptive attacks.
- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — Shows why empirical robustness can mislead, the motivation for certified guarantees.
