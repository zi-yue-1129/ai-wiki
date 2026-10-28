---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/paradigms/federated
tags:
  - optimization
  - large batch
  - distributed training
aliases:
  - Large-batch training
  - Distributed optimisation
  - 大批次訓練
  - 分散式最佳化
---

# Large-Batch and Distributed Optimisation

Batch size and parallelism change the optimiser. A larger batch gives a less noisy gradient and lets more hardware work at once, but past a point the extra examples stop reducing the number of steps needed. This subchapter covers when that happens, and why very large batches need layer-wise scaling and longer warm-up.

## Overview

Part of the [Optimisation](index.md) folder. Each method has its own page, and this one compares them and says when each applies. The learning-rate side of the same problem is in [Learning-rate schedules](learning-rate-schedules.md).

## Key concepts

- **Batch size \(B\):** the number of examples used for one gradient estimate. A larger \(B\) lowers gradient noise and gives more work per step that can run in parallel.
- **Data parallelism:** each device computes gradients on a shard of the batch, and the gradients are then averaged. The effective batch size is the total over all devices.
- **Gradient noise scale:** a statistic of how noisy the gradient is relative to its true value. McCandlish et al. (2018) show that it predicts the largest batch size that still reduces the number of steps. Its definition is on the [SGD noise scale](sgd-noise-scale.md) page.
- **Generalisation gap:** the drop in test accuracy when a model is trained with a large batch on the same schedule as a small batch.

## How it works

With batch size \(B\), each step uses \(B\) examples. Below a critical batch size, doubling \(B\) roughly halves the number of steps needed, so the extra hardware is used well. Above it, extra examples help less and the step count stops falling. McCandlish et al. relate this threshold to the gradient noise scale.

Two problems appear in practice. The first is one of optimisation. With a fixed learning rate, a very large batch can make early training unstable, which is why linear learning-rate scaling and warm-up are used. The second concerns generalisation. Hoffer et al. (2017) attribute much of the gap to the smaller number of updates rather than to the batch itself, and show that the gap can be removed by adapting the training regime.

Shallue et al. (2019) measure the number of steps needed to reach a target error across several batch sizes and workloads. They report that many disagreements in the literature about batch size can be explained, and find no evidence that larger batches degrade out-of-sample performance.

## Key methods

Each method below has its own page. This table compares them.

| Method | Problem it addresses | Page |
|---|---|---|
| Linear scaling with warm-up (Goyal et al., 2017) | Keeping early training stable as \(B\) grows | [Gradual warm-up](gradual-warm-up.md) |
| Gradient noise scale (McCandlish et al., 2018) | Predicting the useful batch size | [SGD noise scale](sgd-noise-scale.md) |
| LARS (You et al., 2017) | A per-layer step size when \(B\) is very large, for SGD-type updates | [LARS](lars.md) |
| LAMB (You et al., 2019) | Layer-wise scaling for Adam-type updates | [LAMB](lamb.md) |

## Connections

- [Gradient clipping and normalisation](gradient-clipping-and-normalisation.md) is the overview where LARS and LAMB sit beside norm clipping.
- [Learning-rate schedules](learning-rate-schedules.md) cover the warm-up and decay that large-batch training relies on.
- [Sharp minima](sharp-minima.md) is one explanation given for the generalisation gap.
- [Adam](adaptive/adam.md) provides the per-coordinate update that LAMB rescales layer by layer.
- [Federated learning](../paradigms/federated/index.md) is another setting in which computation is spread across many devices, though with different constraints on communication and data.

## Applications

- Pre-training large language and vision models across many accelerators, using LAMB or LARS with warm-up.
- Training ResNet-50 on ImageNet with large batches in about an hour, as in Goyal et al. (2017).
- Training BERT with very large batches, as reported in You et al. (2019).

## Open questions

- What sets the critical batch size beyond the gradient noise scale, and can it be estimated before training starts?
- Does the generalisation gap disappear once the number of updates is matched across architectures, or do some models need more?

## References

### Seminal papers

- McCandlish, S., Kaplan, J., Amodei, D. & OpenAI Dota Team (2018). *An Empirical Model of Large-Batch Training*. arXiv. https://arxiv.org/abs/1812.06162 — Shows that the gradient noise scale predicts the largest useful batch size across many domains.
- Shallue, C. J., et al. (2019). *Measuring the Effects of Data Parallelism on Neural Network Training*. arXiv. https://arxiv.org/abs/1811.03600 — Measures steps to reach a target error across batch sizes and workloads, and finds no evidence that larger batches degrade out-of-sample performance.
- Hoffer, E., Hubara, I. & Soudry, D. (2017). *Train longer, generalize better: closing the generalization gap in large batch training of neural networks*. arXiv. https://arxiv.org/abs/1705.08741 — Attributes the large-batch generalisation gap to the smaller number of updates, and shows that adapting the training regime removes it.
- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — Linear learning-rate scaling with warm-up, which keeps large-batch training stable.
- You, Y., Gitman, I. & Ginsburg, B. (2017). *Large Batch Training of Convolutional Networks*. arXiv. https://arxiv.org/abs/1708.03888 — Introduces LARS, a per-layer step size for SGD-type updates at large batch sizes.
- You, Y., et al. (2019). *Large Batch Optimization for Deep Learning: Training BERT in 76 Minutes*. ICLR. https://arxiv.org/abs/1904.00962 — Introduces LAMB, which extends the layer-wise trust ratio to Adam.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, with discussion of batch-size and step-size choices.
