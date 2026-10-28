---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - learning rate
aliases:
  - SGDR
  - Cosine annealing
  - Warm restarts
  - 餘弦退火
  - 暖重啟
---

# Cosine Annealing with Warm Restarts

Cosine annealing with warm restarts (SGDR) decays the learning rate along a half cosine curve, then raises it back to its maximum at fixed points and begins again, with each run longer than the one before. Loshchilov and Hutter (2017) introduced it. The parent overview is [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md).

## Overview

A plain cosine decay falls smoothly from a high rate to a low one, and it is a common choice. Its weakness is that the search can settle into one region and the rate stays small until the end of training. Restarting the rate periodically gives the optimiser a chance to leave a region and to converge to a new one, and each restart produces a point that can be saved as a snapshot.

## Problem

Training budgets are finite, and the usual decay is chosen before training starts. Loshchilov and Hutter ask whether a schedule that restarts can reach good solutions faster, measured by the performance at any time during training, not only at its end.

## Core idea

Within each run \(i\), decay the rate with a cosine curve from \(\eta^i_{\max}\) to \(\eta^i_{\min}\). At the end of the run, restart by setting the rate back to \(\eta^i_{\max}\). Make each run longer than the last by a factor \(T_{\mathrm{mult}}\), so the schedule has longer phases at the end of training.

## Algorithm

For run \(i\) with length \(T_i\) epochs, let \(T_{\mathrm{cur}}\) be the epochs elapsed since the last restart, updated after every batch. The learning rate is

\[
\eta_t = \eta^i_{\min} + \frac{1}{2}\left(\eta^i_{\max} - \eta^i_{\min}\right)\left(1 + \cos\!\left(\frac{T_{\mathrm{cur}}}{T_i}\,\pi\right)\right)
\]

Each restart sets \(T_{i+1} = T_{\mathrm{mult}}\, T_i\). The paper suggests increasing the run length this way to improve performance at any point in training. Snapshots of the model at the end of each run can be averaged into an ensemble.

## Results

- The abstract reports that the method improves the anytime performance of stochastic gradient descent when training deep networks, and it gives new state-of-the-art results on CIFAR-10 and CIFAR-100. The stated error rates are 3.14% and 16.21%, which the paper attributes to an ensemble of snapshots.
- The abstract also mentions experiments on EEG recordings and on a downsampled version of ImageNet, without numbers.

## Limitations

- The restart points and the run lengths \(T_0\) and \(T_{\mathrm{mult}}\) are chosen by hand, so the schedule still needs a budget decision.
- Restarts can waste compute if the run ends before the rate is small enough for the model to settle.
- The headline error rates come from a snapshot ensemble, so they are not the error of a single model trained with the same schedule.

## Connections

- [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md) compares this decay with step decay and with cyclical rates.
- [Gradual warm-up](gradual-warm-up.md) is often combined with a cosine decay, using the warm-up for the first phase.
- [Cyclical learning rates](cyclical-learning-rates.md) also restart the rate, but with a fixed bound and no cosine decay.
- [Regularisation and weight decay](regularisation-and-weight-decay.md) interacts with the rate, since the effective decay depends on it.

## Open questions

- Does the restart schedule help more on large datasets with long training than on short training runs?
- Is there a principled rule for choosing \(T_{\mathrm{mult}}\) for a given compute budget?

## References

### Seminal papers

- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — Proposes cosine annealing with warm restarts, and reports error rates on CIFAR-10 and CIFAR-100.
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — Another periodic schedule, with bounds chosen by a learning-rate range test.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Warm-up at the start of training, which the cosine schedule often follows.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — A linear warm-up followed by a different decay, for comparison with cosine decay.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of step-size schedules for stochastic gradient methods and their convergence theory.
