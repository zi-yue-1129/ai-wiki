---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning/adversarial-robustness
tags:
  - adversarial examples
  - adversarial training
  - robustness
aliases:
  - PGD
  - 投影梯度下降
  - Projected gradient descent
  - Adversarial training
---

# Projected Gradient Descent and Adversarial Training

Projected gradient descent (PGD) is an iterative attack that repeats small gradient steps and projects the perturbed input back into the allowed budget after each step. Adversarial training uses PGD examples as training data, which Madry et al. (2018) showed to be a strong defence. Part of [Adversarial examples and robustness](index.md).

## Overview

A single FGSM step can miss the region of highest loss. PGD takes many steps and restarts from random points in the budget, so it finds stronger adversarial examples. Madry et al. (2018) framed robust training as a min–max problem: minimise over the parameters the worst-case loss over perturbations within the budget.

## Key concepts

- **Projection**: after each step, the perturbation is clipped back into the \(\epsilon\)-ball around the clean input.
- **Random start**: the attack begins at a random point in the ball, which helps it escape flat regions of the loss.
- **Min–max objective**: \(\min_\theta \mathbb{E}\big[\max_{\|\delta\|\le\epsilon} J(\theta,x+\delta,y)\big]\).

## How it works

Starting from \(x^{(0)}=x+\eta\) with a random \(\eta\) in the ball, PGD updates

\[
x^{(t+1)}=\Pi_{\mathcal{B}_\epsilon(x)}\!\Big(x^{(t)}+\alpha\,\mathrm{sign}\big(\nabla_x J(\theta,x^{(t)},y)\big)\Big),
\]

where \(\Pi\) is the projection onto the ball and \(\alpha\) is the step size. Adversarial training computes this inner maximisation for each minibatch and updates the parameters on the resulting examples. The approach is expensive, because each training step needs several gradient computations.

## Variants

- **TRADES** trains with a loss that balances clean accuracy against the change in output under attack, which gives a different accuracy–robustness trade-off.
- **Free adversarial training** reuses the gradient from one pass to make the attack cheaper.
- **Fast adversarial training** uses a single FGSM step with random initialisation to save compute, with the risk of catastrophic overfitting noted in [FGSM](fgsm.md).

## Results and limits

- PGD adversarial training produced models with much higher robust accuracy on image benchmarks than standard training (Madry et al., 2018).
- Clean accuracy usually falls as robustness rises, which Tsipras et al. (2019) explain as an inherent trade-off in some settings.
- Robust accuracy depends on the attack used for evaluation. Carlini and Wagner (2017) show that defences trained against one attack can fail against a stronger one.
- Training cost is several times that of standard training, and the gains need to be weighed against that cost.

## Applications

- **Robust image classifiers** for settings where small noise can change decisions.
- **Benchmarking**: PGD with many steps and random restarts is a standard evaluation attack.
- **Transfer to other domains**: adversarial training ideas are applied to speech, text embeddings and graphs, with the same cost issues.

## Open questions

- The right budget and attack for training in each domain is not settled, and robustness does not always transfer to new attack types.
- Reducing the cost of adversarial training without losing robustness remains a research goal.

## References

### Seminal papers

- Madry, A., Makelov, A., Schmidt, L., Tsipras, D. & Vladu, A. (2018). Towards deep learning models resistant to adversarial attacks. In *International Conference on Learning Representations*. arXiv:1706.06083. https://arxiv.org/abs/1706.06083 — Introduces PGD attacks and min–max adversarial training.
- Goodfellow, I. J., Shlens, J. & Szegedy, C. (2015). Explaining and harnessing adversarial examples. In *International Conference on Learning Representations*. arXiv:1412.6572. https://arxiv.org/abs/1412.6572 — Introduces the gradient-based attack and the first adversarial training experiments.
- Carlini, N. & Wagner, D. (2017). Towards evaluating the robustness of neural networks. In *2017 IEEE Symposium on Security and Privacy*, 39–57. https://doi.org/10.1109/SP.2017.49 — Shows that stronger attacks break defences evaluated only against weaker ones.

### Surveys and textbooks

- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — Explains the accuracy–robustness trade-off that adversarial training exhibits.
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — Compares empirical adversarial training with certified guarantees.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers adversarial training as a min–max problem.
