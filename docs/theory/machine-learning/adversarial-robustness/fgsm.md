---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning/adversarial-robustness
tags:
  - adversarial examples
  - attack
  - gradient methods
aliases:
  - FGSM
  - 快速梯度符號法
  - Fast gradient sign method
---

# Fast Gradient Sign Method

The fast gradient sign method (FGSM) is a one-step attack that perturbs an input in the direction of the sign of the loss gradient with respect to the input, by a fixed size \(\epsilon\). Part of [Adversarial examples and robustness](index.md).

## Overview

FGSM is the simplest effective attack on a differentiable classifier. It needs one gradient computation and no search, so it is fast enough to use inside training. Goodfellow et al. (2015) introduced it and used it to argue that adversarial examples arise from the linear behaviour of high-dimensional models.

## Key concepts

- **Perturbation budget \(\epsilon\)**: the largest allowed change to each input component, measured in the \(\ell_\infty\) norm.
- **Loss gradient**: the derivative of the training loss with respect to the input, not the parameters.
- **Sign operation**: keeping only the direction of each gradient component makes every pixel move by the full budget.

## How it works

Given an input \(x\), label \(y\), loss \(J(\theta,x,y)\) and parameters \(\theta\), the adversarial input is

\[
\tilde{x} = x + \epsilon\,\mathrm{sign}\big(\nabla_x J(\theta, x, y)\big).
\]

Clipping \(\tilde{x}\) to the valid input range, such as \([0,1]\) for images, keeps the example a valid input. Goodfellow et al. (2015) show that a linear model is especially vulnerable, because the perturbation adds up across many input dimensions and changes the output by \(\epsilon\|w\|_1\).

## Variants

- **Targeted FGSM** moves the input toward a chosen wrong label rather than away from the true label.
- **Iterative FGSM** repeats smaller steps, which gives a stronger attack and is the basis of PGD (see [PGD and adversarial training](pgd-adversarial-training.md)).
- **Single-step adversarial training** trains on FGSM examples. It is cheap but can suffer from catastrophic overfitting to the single-step attack.

## Results and limits

- FGSM reduces the accuracy of undefended image classifiers sharply at small budgets, which is the result that drew attention to the problem (Goodfellow et al., 2015).
- It is a weak attack for defended models, because one linear step can miss the adversarial region. Carlini and Wagner (2017) show that stronger attacks break many defences that resist FGSM.
- The sign operation is a heuristic for \(\ell_\infty\) attacks, and it does not directly give the smallest perturbation that changes the label.

## Applications

- **Robustness evaluation**: a fast baseline for reporting accuracy under attack.
- **Adversarial training**: generating training examples cheaply inside the training loop.
- **Teaching**: the standard first example of a gradient-based attack.

## Open questions

- Why single-step attacks sometimes lose effectiveness on adversarially trained models, and how to avoid catastrophic overfitting, remain under study.
- Whether linear explanations describe the behaviour of very deep networks well is still debated.

## References

### Seminal papers

- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — Introduces FGSM and the linearity explanation.
- Szegedy, C. et al. (2014). Intriguing properties of neural networks. arXiv:1312.6199. https://arxiv.org/abs/1312.6199 — The earlier demonstration that small perturbations change network outputs.
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — Shows that stronger attacks defeat defences that resist FGSM.

### Surveys and textbooks

- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — Uses iterated FGSM-style attacks to train robust models.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on gradient-based adversarial attacks.
