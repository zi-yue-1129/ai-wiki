---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/loss-functions-and-optimization
tags:
  - optimization
  - generalisation
  - noise
aliases:
  - SGD noise scale
  - Noise scale
  - 隨機梯度雜訊尺度
---

# SGD Noise Scale

The SGD noise scale is a quantity \(g = \epsilon\,(N/B - 1) \approx \epsilon N/B\), where \(\epsilon\) is the learning rate, \(N\) the training set size and \(B\) the batch size. Smith and Le (2018) argued that the optimal batch size scales with the learning rate and the training set size, and that the noise scale controls how much of the optimiser's path is driven by gradient noise. The parent overview is [Regularisation and Weight Decay in Optimisation](regularisation-and-weight-decay.md).

## Overview

Stochastic gradient descent replaces the full-data gradient with an average over a minibatch. The difference between the two is noise. Its size depends on the batch size, and the effect of that noise on the trajectory depends on the learning rate. Smith and Le treat the two together as a single quantity, which governs how far the optimiser wanders around the region it is converging to. Wandering helps generalisation up to a point, so the best batch size is one that makes the noise scale take a particular value.

## Problem

Practitioners choose a learning rate and a batch size, and the two interact. Smith and Le ask whether there is a relation between them that gives the best generalisation for a given training set, instead of tuning each separately.

## Core idea

Write the update as a stochastic step, and approximate the stochastic term by a Gaussian noise whose scale is governed by \(\epsilon N/B\). Use this to argue that the optimal batch size grows with the learning rate, and that it grows with the training set size. The authors also argue that, for a fixed noise scale, changing the batch size and the learning rate in proportion leaves the dynamics similar.

## Algorithm

The paper does not introduce an optimiser. The method is a rule for choosing the batch size:

1. Fix the learning rate \(\epsilon\) and the training set size \(N\).
2. Compute the noise scale \(g = \epsilon (N/B - 1)\) for candidate batch sizes \(B\).
3. Prefer a batch size at which \(g\) is in the range that the experiments identify as best.
4. When the learning rate changes, scale the batch size with it, so that \(g\) stays fixed.

## Results

- The abstract states that the optimal batch size scales with both the learning rate and the training set size, and that the authors verify this empirically.
- The abstract gives no numerical results, so the experiments in the paper should be consulted for the quantitative effects.

## Limitations

- The noise-scale argument uses a Gaussian approximation to the minibatch noise, which may not hold for heavy-tailed gradients.
- The rule is stated in terms of plain SGD. It is not directly a rule for adaptive optimisers such as Adam, where the effective step depends on the second moment.
- The optimal batch size depends on the regime, and the rule is an approximation that holds for the settings studied.

## Connections

- [Sharp minima and large-batch generalisation](sharp-minima.md) gives the empirical side of the same batch-size effect.
- [Gradual warm-up and linear scaling](gradual-warm-up.md) is the practical rule for scaling the learning rate with batch size, which the noise scale motivates.
- [SGD and momentum](sgd-and-momentum/index.md) is the setting where the argument is cleanest.
- [Learning-rate schedules](learning-rate-schedules.md) matter because a schedule changes the noise scale over training.

## Open questions

- How well does the noise-scale rule transfer to adaptive optimisers, and to momentum?
- Is there a noise scale for which generalisation is optimal independent of the architecture?

## References

### Seminal papers

- Smith, S. L. & Le, Q. V. (2018). *A Bayesian Perspective on Generalization and Stochastic Gradient Descent*. ICLR. https://arxiv.org/abs/1710.06451 — Introduces the SGD noise scale \(\epsilon N/B\) and argues that the optimal batch size scales with the learning rate and training set size.
- Keskar, N. S., et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR. https://arxiv.org/abs/1609.04836 — The empirical batch-size effect that the noise-scale account tries to explain.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Linear scaling of the learning rate with batch size, which keeps the noise scale roughly fixed.
- Loshchilov, I. & Hutter, F. (2017). *Decoupled Weight Decay Regularization*. ICLR. https://arxiv.org/abs/1711.05101 — Shows that adaptive optimisers change the effective learning rate, which the noise-scale rule does not account for.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, with discussion of gradient noise and step sizes.
