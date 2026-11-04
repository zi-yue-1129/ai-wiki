---
status: complete
last_reviewed: 2026-11-02
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

## Threat model and feasible set

The norm and radius are part of the security claim, not interchangeable hyperparameters. In the usual image-classification setting an attacker observes the model and label, then chooses an input perturbation constrained by a norm ball and the valid pixel domain. An \(\ell_\infty\) budget bounds each coordinate independently; an \(\ell_2\) budget bounds the total Euclidean displacement. A robustness score at one radius does not establish robustness at a different radius, under spatial transformations, or against changes to the underlying task semantics.

For \(\ell_\infty\) PGD, projection can be implemented by clipping each coordinate to \([x_i-\epsilon,x_i+\epsilon]\) and then to the valid input range. This is a projection onto the intersection of two axis-aligned boxes. For \(\ell_2\) PGD, the update direction and projection change: the gradient can be normalized by its Euclidean norm, and a perturbation beyond the radius is rescaled to length \(\epsilon\). A sign-gradient step is specifically natural for the \(\ell_\infty\) threat model, not a generic formula for all norms.

The distinction between *untargeted* and *targeted* attacks also matters. Untargeted PGD increases the loss of the true label. Targeted PGD instead attempts to make a chosen target class more likely, so the sign of the optimization direction changes when minimizing target-label loss. The attacker may additionally be constrained by query access or by the ability to differentiate through preprocessing; these assumptions must be recorded with any reported result.

## Implementation and reproducibility

A practical white-box evaluation should explicitly fix the model in evaluation mode and avoid inadvertently changing its weights while differentiating the input. The following pseudocode shows the untargeted \(\ell_\infty\) variant; it is an algorithm sketch rather than a framework-specific implementation.

```text
for each input (x, y):
    best_loss = -infinity
    for restart in 1..R:
        delta = uniform(-epsilon, epsilon) elementwise
        delta = clamp(x + delta, valid_range) - x
        for step in 1..K:
            g = gradient_x(loss(model(x + delta), y))
            delta = delta + alpha * sign(g)
            delta = clamp(delta, -epsilon, epsilon)
            delta = clamp(x + delta, valid_range) - x
        retain the feasible candidate with the highest loss
    evaluate model(x + best_delta)
```

The inner maximization is only *approximately* solved. Larger \(K\), additional random restarts, and a suitable step size can expose failures missed by a weak configuration, but they do not prove global optimality. Report \(\epsilon\), norm, \(\alpha\), steps, restarts, initialization, preprocessing, pixel scaling, and whether the attack selected the highest-loss candidate per example. Comparing a budget expressed in \([0,1]\) pixels with one expressed in \([0,255]\) without conversion invalidates the comparison.

For training, the optimizer should update \(\theta\) against the final adversarial batch, while the inner loop changes the input perturbation. The common implementation treats the selected perturbation as fixed when differentiating the outer objective; it does not ordinarily backpropagate through every attack iteration. This distinction is important when estimating memory requirements and reproducing the robust-optimization baseline of Madry et al. (2018).

## Evaluation protocol and failure modes

**Clean accuracy** and **robust accuracy** must be reported separately, on the same held-out examples. Robust accuracy is the fraction classified correctly after an allowed attack; it is conditional on the chosen threat model and attack implementation. A strong empirical evaluation checks multiple step sizes, budgets, and restarts, rather than presenting a single PGD run as a certificate.

Gradient masking is a particularly dangerous failure mode: nondifferentiable preprocessing, saturated activations, or stochastic components can make naive gradients uninformative without making the classifier genuinely robust. Unexpectedly high adversarial accuracy should trigger checks for attack loss increasing across iterations, gradient magnitudes, stochasticity, and stronger or alternative attacks. A randomized-smoothing certificate addresses a different question: it can provide a formal guarantee under a specified \(\ell_2\) radius, whereas PGD testing gives empirical evidence for the chosen attack (Cohen et al., 2019).

**Compute accounting** should include attack steps per training minibatch, restarts at evaluation, and actual hardware throughput. A nominally stronger defence trained with a smaller batch, a different data pipeline, or fewer total optimization updates is not a controlled comparison. Also distinguish robustness against bounded perturbations from robustness to distribution shift, corruption, and adaptive adversaries; success on one does not imply success on the others.

## Connections

PGD is a first-order optimization procedure used as an inner adversary in robust empirical risk minimization. Its training objective is connected to [machine learning](../index.md), while its single-step predecessor is [FGSM](fgsm.md). The central methodological question is whether an evaluation attack is strong enough to approximate the inner maximum, not whether a classifier survives one arbitrarily chosen perturbation.

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

- Croce, F. & Hein, M. (2020). Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks. In *Proceedings of the 37th International Conference on Machine Learning*, PMLR 119. https://proceedings.mlr.press/v119/croce20b.html — Introduces AutoAttack, a parameter-free ensemble that strengthens robustness evaluation.
- Tsipras, D., Santurkar, S., Engstrom, L., Turner, A. & Madry, A. (2019). Robustness may be at odds with accuracy. In *International Conference on Learning Representations*. arXiv:1805.12152. https://arxiv.org/abs/1805.12152 — Explains the accuracy–robustness trade-off that adversarial training exhibits.
- Cohen, J., Rosenfeld, E. & Kolter, Z. (2019). Certified adversarial robustness via randomized smoothing. In *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97. https://proceedings.mlr.press/v97/cohen19c.html — Compares empirical adversarial training with certified guarantees.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Repository for Murphy's textbook series; general background on the learning objectives used here.
