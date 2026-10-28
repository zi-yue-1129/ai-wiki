---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
tags:
  - optimization
  - learning rate
aliases:
  - Cyclical learning rates
  - CLR
  - Learning-rate range test
  - 循環學習率
---

# Cyclical Learning Rates

Cyclical learning rates vary the learning rate between a lower and an upper bound, repeatedly, instead of decaying it monotonically. Smith (2017) proposed the method, with the bounds found by a short test in which the rate is increased linearly. It removes the need for a hand-tuned global schedule. The parent overview is [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md).

## Overview

Most schedules assume the rate should fall over time. Smith's observation is that a higher rate can help the optimiser cross saddle points and flat regions, while a lower rate helps it settle into a minimum. Oscillating between the two lets the network benefit from both, without an external decision about when to lower the rate.

## Problem

The best constant learning rate, and the best decay schedule, are expensive to find by grid search. Smith asks whether there is a simple rule that finds a useful range of rates automatically and then keeps the rate cycling within it.

## Core idea

Estimate a reasonable pair of bounds \(\eta_{\min}\) and \(\eta_{\max}\) with a learning-rate range test: increase the rate linearly for a few epochs and watch where the loss falls fastest and where it starts to rise. Then cycle the rate between those bounds for the rest of training.

## Algorithm

1. Run a short test in which the learning rate increases linearly over a few epochs.
2. Take \(\eta_{\min}\) and \(\eta_{\max}\) from the range over which the loss decreases.
3. Cycle the rate between the bounds. In the simplest form, it rises linearly from \(\eta_{\min}\) to \(\eta_{\max}\) and falls back over each cycle.

The abstract does not name the cycle policies, and it does not state how to choose the cycle length.

## Results

- The abstract says that cycling the rate between bounds improves classification accuracy without manual tuning, often in fewer iterations.
- It says the approach "practically eliminates the need to experimentally find the best values and schedule for the global learning rates".
- The benchmarks are CIFAR-10, CIFAR-100 and ImageNet, with ResNets, Stochastic Depth networks, DenseNets, AlexNet and GoogLeNet. The abstract gives no quantitative results.

## Limitations

- The abstract gives no numbers, so the size of the gain must be taken from the paper's experiments.
- The cycle length, which controls how often the rate returns to its maximum, is a choice the abstract does not settle.
- The bounds come from a range test on one architecture and dataset. How well they transfer to a different architecture is not stated in the abstract.

## Connections

- [Cosine annealing with warm restarts](cosine-annealing-warm-restarts.md) restarts the rate as well, with a smooth decay inside each run.
- [Gradual warm-up](gradual-warm-up.md) uses a linear rise at the start, which is also what the range test does.
- [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md) is the overview that places this method among the others.
- [Loss landscape](theory-and-landscapes.md) explains why a larger rate can help escape flat regions and saddle points.

## Open questions

- When does a cyclical schedule beat a well-tuned decay, and when does it not?
- How should the cycle length be chosen for a given budget?

## References

### Seminal papers

- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — Proposes cycling the learning rate between bounds, with the bounds found by a linear range test.
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — A periodic schedule with a cosine decay inside each run, for comparison.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — A warm-up schedule that shows why the starting rate matters.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — A monotone decay after a warm-up, the baseline that cyclical schedules are compared with in practice.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of step-size choices for stochastic methods, which the range test is a practical version of.
