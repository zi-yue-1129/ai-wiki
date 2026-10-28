---
status: draft
last_reviewed: 2026-10-28
tags:
  - adversarial training
  - security
aliases:
  - 快速梯度符號法
  - Fast Gradient Sign Method
  - FGSM
---

# Fast Gradient Sign Method (FGSM)

The Fast Gradient Sign Method is the simplest gradient-based attack on a neural network. It takes one step of fixed size in the direction that increases the loss most. Goodfellow et al. (2014) introduced it to generate [adversarial examples](../index.md) quickly and to explain why they exist.

## Overview

Szegedy et al. (2013) showed that small, imperceptible changes to an image could flip a deep network's output, but their attack needed an iterative search. Goodfellow et al. (2014) argued that the main cause of this vulnerability is the nearly linear behaviour of networks in high-dimensional input spaces, rather than the nonlinearity or overfitting that earlier explanations blamed. If the loss changes roughly linearly with the input, the best small change is aligned with the sign of the gradient, and one backward pass computes it.

## Key concepts

- **Perturbation budget \(\varepsilon\).** The largest change allowed to each input coordinate, measured in the \(\ell_\infty\) norm.
- **Gradient sign.** Only the direction of each gradient component is kept, so every input coordinate moves by the same amount.
- **Single-step attack.** One gradient evaluation produces the adversarial example, which makes FGSM cheap compared with the iterative attacks on the [PGD page](../pgd-adversarial-training/index.md).
- **Linearity hypothesis.** The explanation that many small changes, each aligned with a weight, add up along the direction to which the model is most sensitive.

## How it works

Let \(J(\theta, x, y)\) be the loss of a model with parameters \(\theta\) on input \(x\) with label \(y\). The adversarial example is

\[
x^{\text{adv}} = x + \varepsilon \,\operatorname{sign}\big(\nabla_x J(\theta, x, y)\big).
\]

1. Compute the loss on the clean input \(x\) against its true label \(y\).
2. Backpropagate to the input, so the gradient is taken with respect to \(x\) and the weights stay fixed.
3. Keep only the sign of each gradient component.
4. Add \(\varepsilon\) times that sign to \(x\), then clip to the valid input range, such as \([0, 1]\) for normalised pixels.

The same paper proposes training on these examples. The objective mixes the clean loss with the loss on the perturbed input, with a weight \(\alpha\) set by the practitioner. This is the earliest form of [adversarial training](../pgd-adversarial-training/index.md).

## Results

Goodfellow et al. (2014) support the linear explanation with quantitative results, and they show that examples generated for one model transfer across architectures and training sets. They also report that training on adversarial examples reduced the test error of a maxout network on MNIST. The abstract gives no figures, so consult the paper for them.

Later work adds context. Kurakin et al. (2016) found that adversarial images captured by a cell-phone camera were still often misclassified. Tramèr et al. (2017) found that adversarial training with single-step examples can converge to a degenerate solution that resists FGSM but not stronger attacks.

## Limitations

- **The linear model is an approximation.** Where the loss surface is strongly curved, one step may not increase the loss much, so FGSM can be much weaker than an optimised attack.
- **A failed attack is not evidence of robustness.** Defences that obscure gradients can defeat FGSM while stronger attacks still succeed (Athalye et al., 2018). Defences need [adaptive evaluation](../../../../engineering/evaluation/index.md).
- **Single-step training is fragile.** Models trained only on FGSM-style examples can give a false sense of security (Tramèr et al., 2017).

## Open questions

- Is linearity the whole explanation? Ilyas et al. (2019) attribute adversarial examples to predictive but brittle features, a different account.
- Can single-step adversarial training be made stable without collapsing into weak perturbations?
- Whether a small \(\ell_\infty\) change matches what people perceive as small is not settled. Elsayed et al. (2018) found that transferred examples can also affect time-limited human observers.

## Connections

FGSM is the one-step case of the projected gradient method, and the [gradient descent](../../../math/calculus/gradient-descent/index.md) page explains the update rule that it shares with training. It is usually run on [convolutional networks](../../../models/cnn/index.md) for images. Text inputs to language models are discrete, so the gradient step does not transfer directly; that case is covered in [LLM security](../../../../engineering/llm-security/index.md). For the brain side, see [visual perception](../../../../brain-mind/visual-perception/index.md).

## Applications

- **Robustness testing.** FGSM is a fast baseline for checking sensitivity to small perturbations.
- **Physical-world risk.** Kurakin et al. (2016) show that adversarial images can remain effective after camera capture, relevant to systems such as [autonomous driving](../../../../applications/autonomous-driving/index.md) perception.

## References

### Seminal papers

- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples*. arXiv. https://arxiv.org/abs/1412.6572 — Introduces FGSM, argues that linearity explains adversarial vulnerability, and proposes training on such examples.
- Szegedy, C. et al. (2013). *Intriguing properties of neural networks*. arXiv. https://arxiv.org/abs/1312.6199 — First shows that imperceptible input perturbations can change the output of deep image classifiers.
- Kurakin, A., Goodfellow, I. J. & Bengio, S. (2016). *Adversarial examples in the physical world*. arXiv. https://arxiv.org/abs/1607.02533 — Shows that adversarial images captured by a cell-phone camera are still often misclassified.
- Tramèr, F. et al. (2017). *Ensemble Adversarial Training: Attacks and Defenses*. arXiv. https://arxiv.org/abs/1705.07204 — Shows that single-step adversarial training can converge to a degenerate minimum that resists FGSM but not stronger attacks.

### Articles and documentation

- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — Explains why gradient-based attacks can fail against defences that do not truly improve robustness.
- Ilyas, A. et al. (2019). *Adversarial Examples Are Not Bugs, They Are Features*. arXiv. https://arxiv.org/abs/1905.02175 — Attributes adversarial vulnerability to non-robust but predictive features, a competing account to linearity.
- Elsayed, G. F. et al. (2018). *Adversarial Examples that Fool both Computer Vision and Time-Limited Humans*. arXiv. https://arxiv.org/abs/1802.08195 — Shows that examples transferred from vision models also change the decisions of time-limited human observers.
