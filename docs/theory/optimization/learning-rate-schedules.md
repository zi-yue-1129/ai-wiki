---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 學習率排程
  - 學習率預熱
  - Learning-rate schedule
  - Warm-up
related:
  - theory/math
tags:
  - optimization
  - learning rate
---

# Learning-Rate Schedules and Warm-up

The learning rate is the step size of gradient descent, and most training runs change it over time. A schedule specifies how it changes. The choice affects both how fast a network trains and how well it ends up, and a short warm-up at the start is often needed for Transformers and very large batches.

## Overview

Gradient descent takes steps \(\theta_t = \theta_{t-1} - \eta_t\, g_t\), where \(g_t\) is the gradient and \(\eta_t\) the learning rate. A constant \(\eta\) forces a compromise. A rate that is safe at the start can be too large near a minimum, where the loss surface is narrow and the iterates oscillate. A rate small enough for the end of training is slow at the start. A schedule lets the rate be large early and small late.

Warm-up addresses a different problem. At initialisation the gradients are unreliable, and a large rate can push the weights into a poor region before the network has settled. Starting from a small rate and ramping up avoids this, and it becomes more important as the batch size grows.

## Key concepts

- **Schedule**: a function from the step (or epoch) index to the learning rate.
- **Decay**: a rate that falls over training, in steps, linearly, or along a cosine curve.
- **Warm-up**: an initial period in which the rate rises from a small value to its target.
- **Restart**: the rate is raised again at fixed points, beginning a new decay.
- **Cycle**: one period of a schedule that repeats its rise and fall.

## How it works

Three shapes cover most practice:

| Shape | Form | Typical use |
|---|---|---|
| Step decay | \(\eta_t = \eta_0\,\gamma^{\lfloor t/s \rfloor}\), multiplied by \(\gamma\) every \(s\) steps | Classic image-classification recipes |
| Linear decay | \(\eta_t = \eta_0\,(1 - t/T)\) down to zero at step \(T\) | Fine-tuning and language models |
| Warm-up then decay | A linear ramp followed by any decay | Transformers and large-batch training |

Warm-up and decay are usually combined. The ramp is short, often a few epochs or a few thousand steps, and the decay runs for the rest of training.

## Key methods

Three landmark methods, each with its own page. They differ in the shape of the schedule and in the problem they solve.

| Method | Shape | What separates it |
|---|---|---|
| [Gradual warm-up and linear scaling](gradual-warm-up.md) (Goyal et al., 2017) | A linear ramp to \(k\eta\) over the first epochs | Scales the rate with batch size and ramps it up to avoid early instability. The Transformer schedule of Vaswani et al. (2017) is discussed on the same page |
| [Cosine annealing with warm restarts](cosine-annealing-warm-restarts.md) (Loshchilov & Hutter, 2017) | A cosine decay that restarts at fixed points, with each run longer than the last | Restarts the decay on a schedule, and lets snapshots be taken at the end of each run |
| [Cyclical learning rates](cyclical-learning-rates.md) (Smith, 2017) | The rate oscillates between two bounds | Has no fixed decay. The bounds are chosen by a short linear increase, so the rate need not be tuned by hand |

## Connections

- [Adaptive methods](adaptive/index.md) such as Adam still use a global learning rate, and a schedule multiplies the per-parameter step. Warm-up is common in Adam-based Transformer training for this reason.
- [SGD and momentum](sgd-and-momentum/index.md) is the setting where the stability bound on the learning rate, \(\eta \le 1/L\), is easiest to state, and where the schedule's effect on the final point is clearest.
- [Regularisation and weight decay](regularisation-and-weight-decay.md) interacts with the schedule, because the effective decay depends on the current rate.
- [Large-batch and distributed training](large-batch-and-distributed.md) is where warm-up and the linear scaling rule matter most.

## Applications

- Training ResNets on ImageNet with step or cosine schedules.
- Pre-training Transformer language models with a warm-up followed by decay.
- Fine-tuning pre-trained networks with a short, small-rate schedule.

## Open questions

- Why does warm-up help, and does it fix an optimisation problem or a problem with the normalisation layers?
- How should the warm-up length and the restart period be chosen for a fixed training budget?
- Do schedules that are tuned on one architecture transfer to another?

## References

### Seminal papers

- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Introduces the linear scaling rule and gradual warm-up for training with batch sizes up to 8192.
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — Cosine annealing with periodic warm restarts, and the snapshot ensembles it enables.
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — Varies the rate cyclically between bounds, removing the need for a hand-tuned schedule.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Uses a linear warm-up followed by inverse-square-root decay for training the Transformer.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including step-size schedules and their convergence theory.
