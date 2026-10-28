---
status: draft
last_reviewed: 2026-10-28
tags:
  - adversarial training
  - security
  - optimization
aliases:
  - 投影梯度下降
  - 對抗訓練
  - Projected Gradient Descent
  - PGD
  - Madry adversarial training
---

# Projected Gradient Descent and Adversarial Training

Projected gradient descent (PGD) is an iterated, constrained version of FGSM that became the standard strong attack on neural networks. Madry et al. (2017) placed PGD inside a min–max training objective, and this combination, usually called adversarial training, became a common baseline for [adversarial robustness](../index.md).

## Overview

[FGSM](../fgsm/index.md) takes a single linear step, which is a crude guess at the worst perturbation. PGD instead takes many small steps, each followed by a projection back into the allowed region around the input. Madry et al. (2017) framed the whole problem as robust optimisation: a model is robust if its loss stays low under the worst perturbation an adversary can choose. Their abstract describes this as a security guarantee against any first-order adversary, meaning one that uses gradient information.

## Key concepts

- **Projection.** After each step, the perturbed input is mapped back into the set of allowed inputs, usually the \(\ell_\infty\) ball of radius \(\varepsilon\) around the original and the valid pixel range.
- **Random start.** The attack can begin from a random point in the ball rather than from the clean input, which helps it explore the region.
- **Min–max objective.** Training minimises the loss of the worst-case perturbation, so the model learns on its hardest examples at every step.
- **First-order adversary.** An attacker that uses gradients of the model, which covers most practical white-box attacks.

## How it works

The robust objective is

\[
\min_\theta \; \mathbb{E}_{(x,y)\sim\mathcal{D}} \Big[ \max_{\|\delta\|_\infty \le \varepsilon} L(\theta, x+\delta, y) \Big].
\]

The inner maximisation is approximated by PGD, with step size \(\alpha\) and \(K\) iterations:

\[
x^{t+1} = \Pi_{\mathcal{B}_\varepsilon(x)}\Big(x^{t} + \alpha\, \operatorname{sign}\big(\nabla_x L(\theta, x^{t}, y)\big)\Big),
\]

where \(\Pi\) is the projection onto the ball \(\mathcal{B}_\varepsilon(x)\).

1. Choose a random point in the ball around each training input.
2. Repeat \(K\) times: take a signed gradient step and project back.
3. Use the resulting adversarial examples in place of, or alongside, the clean ones.
4. Take a standard gradient step on the model parameters \(\theta\).

Each training step therefore costs roughly \(K\) extra forward and backward passes, which is the main practical price of the method.

## Results

Madry et al. (2017) report that networks trained with this objective show significantly improved resistance to a wide range of attacks. The abstract gives no accuracy figures, so none are quoted here.

Independent evaluation has been critical. Croce and Hein (2020) combined improved PGD variants with other attacks into AutoAttack. Their abstract reports that, for all but one of more than 50 published defences they tested, the robust accuracy they measured was lower than the paper reported, often by more than 10%. Croce et al. (2020) then built RobustBench, a leaderboard that uses AutoAttack as its standard evaluation.

## Limitations

- **Cost.** Training scales with the number of PGD steps, so robust training is much more expensive than standard training.
- **Lower clean accuracy.** Robust models often trade some accuracy on unperturbed inputs, a trade-off that Tsipras et al. (2018) show exists in a simple setting. See the [topic overview](../index.md).
- **Attack-specific robustness.** A model tuned against one attack can be weaker against another. Adaptive evaluation is needed, which is the point of AutoAttack.
- **Data hunger.** Schmidt et al. (2018) show that robust learning can need substantially more samples than standard learning.

## Open questions

- Is the accuracy cost inherent to robustness, or can better training remove it?
- Can the inner attack be made cheaper without losing its strength?
- Does robustness to an \(\ell_\infty\) ball transfer to other perturbation types?

## Connections

PGD is FGSM repeated with projection, built on [gradient descent](../../../math/calculus/gradient-descent/index.md). The generalisation questions it raises connect to [generalisation theory](../../../paradigms/supervised/generalization-theory/index.md). The min–max idea reappears when language models are attacked and hardened through red teaming, covered in [jailbreaks and red teaming](../../../../engineering/llm-security/jailbreaks-and-red-teaming.md). For a certified alternative, see [randomized smoothing](../randomized-smoothing/index.md).

## Applications

- **Benchmarking.** Standardised PGD-based and AutoAttack evaluations, as used in RobustBench, let image classifiers be compared under fixed threat models.

## References

### Seminal papers

- Madry, A. et al. (2017). *Towards Deep Learning Models Resistant to Adversarial Attacks*. arXiv. https://arxiv.org/abs/1706.06083 — Frames robustness as min–max optimisation, uses PGD as the training attack, and releases MNIST and CIFAR-10 challenges.
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2014). *Explaining and Harnessing Adversarial Examples*. arXiv. https://arxiv.org/abs/1412.6572 — The single-step FGSM attack that PGD extends, and the first adversarial-training objective.
- Carlini, N. & Wagner, D. (2016). *Towards Evaluating the Robustness of Neural Networks*. arXiv. https://arxiv.org/abs/1608.04644 — Optimisation-based attacks that defeat defensive distillation.
- Tsipras, D. et al. (2018). *Robustness May Be at Odds with Accuracy*. arXiv. https://arxiv.org/abs/1805.12152 — Shows a provable tension between standard accuracy and adversarial robustness in a simple setting.
- Athalye, A., Carlini, N. & Wagner, D. (2018). *Obfuscated Gradients Give a False Sense of Security*. arXiv. https://arxiv.org/abs/1802.00420 — Shows that several defences with obfuscated gradients were broken by adaptive attacks.

### Surveys and textbooks

- Bai, T. et al. (2021). *Recent Advances in Adversarial Training for Adversarial Robustness*. arXiv. https://arxiv.org/abs/2102.01356 — Surveys variants of adversarial training and the generalisation problems they raise.

### Articles and documentation

- Croce, F. & Hein, M. (2020). *Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks*. arXiv. https://arxiv.org/abs/2003.01690 — Introduces AutoAttack, a parameter-free ensemble that finds lower robust accuracy than many published defences report.
- Croce, F. et al. (2020). *RobustBench: a standardized adversarial robustness benchmark*. arXiv. https://arxiv.org/abs/2010.09670 — Describes the leaderboard and library for standardised robustness evaluation under AutoAttack.
- Schmidt, L. et al. (2018). *Adversarially Robust Generalization Requires More Data*. arXiv. https://arxiv.org/abs/1804.11285 — Proves a sample-complexity gap between robust and standard learning, with image experiments.
