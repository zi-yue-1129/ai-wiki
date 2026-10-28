---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning
  - theory/paradigms/supervised
tags:
  - adversarial examples
  - robustness
  - security
aliases:
  - 對抗樣本
  - 對抗穩健性
  - Adversarial examples
  - Adversarial robustness
  - Certified robustness
---

# Adversarial Examples and Robustness

An adversarial example is an input changed by a small, often imperceptible, perturbation that makes a model produce a wrong output. Robustness is the study of how to make models resist such perturbations, and how to measure whether they do. Part of [Machine learning](../index.md). LLM-specific attacks are covered in [LLM security](../../../engineering/llm-security/index.md).

## Overview

Szegedy et al. (2014) showed that state-of-the-art image classifiers can be fooled by changes too small for a person to notice. Goodfellow et al. (2015) argued that the effect comes from the linear behaviour of high-dimensional models rather than from rare failures. Since then, attacks have become stronger, defences have been tested and broken, and the field has developed certified methods that give guarantees for some perturbation sizes.

## Key concepts

- **Threat model**: the perturbation norm and budget \(\epsilon\), and what the attacker knows (white-box or black-box access).
- **Attack**: a procedure that searches for a perturbation within the budget that increases the loss or changes the label.
- **Adversarial training**: training on adversarial examples, so that the model learns to resist the attack family it was trained on.
- **Certified robustness**: a guarantee that no perturbation within the budget changes the prediction, for every input.

## How it works

Most attacks take a gradient of the loss with respect to the input and move the input in the direction that increases the loss, subject to the budget. The simplest is a single step (FGSM) (Goodfellow et al., 2015). Stronger attacks repeat smaller steps and project back onto the budget, which is projected gradient descent (Madry et al., 2018). Defences usually train on attacked inputs, or they provide a probabilistic certificate for a smoothed classifier (Cohen et al., 2019).

## Key methods

- [Fast gradient sign method](fgsm.md): a one-step attack that is the basis of much adversarial-training work.
- [Projected gradient descent and adversarial training](pgd-adversarial-training.md): the strong iterative attack and the training method built on it.
- [Randomized smoothing](randomized-smoothing.md): a certified-robustness method that gives an \(\ell_2\) radius for a smoothed classifier.

## Connections

- [Generalization theory](../../paradigms/supervised/generalization-theory/index.md) explains why standard training does not produce robust margins.
- [LLM security](../../../engineering/llm-security/index.md) covers prompt-level attacks on language models, which differ from the pixel-level setting here.
- [Out-of-distribution detection](../ood-detection/index.md) addresses inputs that are not adversarial but are unfamiliar, which often need similar tools.

## Applications

- **Safety-critical vision**: checking that traffic-sign or medical classifiers do not flip under small noise.
- **Security**: detecting or resisting evasion attacks on spam or malware classifiers.
- **Benchmarking**: robust accuracy is reported alongside clean accuracy to compare models fairly.

## Open questions

- Robustness and clean accuracy can trade off. Tsipras et al. (2019) show that the trade-off is inherent in some learning settings, not only an artefact of current methods.
- Empirical defences have often been broken by stronger adaptive attacks, so claims need evaluation against adaptive attacks.
- Certified radii are small for most practical models, and scaling certification to large networks is hard.

## References

### Seminal papers

- Szegedy, C. et al. (2014). Intriguing properties of neural networks. arXiv:1312.6199. https://arxiv.org/abs/1312.6199 — Shows that deep networks can be fooled by small perturbations of their inputs.
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — Introduces the fast gradient sign method and a linearity explanation of adversarial examples.
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — Introduces stronger attacks that break several defences, setting an evaluation standard.
- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — Introduces projected gradient descent attacks and adversarial training.
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — Gives a certified \(\ell_2\) radius for a randomly smoothed classifier.

### Surveys and textbooks

- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — Shows a fundamental trade-off between standard accuracy and robustness in a simple setting.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers adversarial examples and robustness in its chapter on adversarial methods.
