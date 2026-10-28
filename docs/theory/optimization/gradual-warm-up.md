---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - optimization
  - learning rate
  - large batch
aliases:
  - Gradual warm-up
  - Linear scaling rule
  - 漸進式預熱
  - 線性縮放規則
---

# Gradual Warm-up and Linear Scaling

Gradual warm-up is a learning-rate schedule that starts small and rises over the first part of training. Goyal et al. (2017) combined it with the linear scaling rule, which multiplies the learning rate by the batch-size factor, so that very large minibatches could train ResNets without losing accuracy. The parent overview is [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md).

## Overview

If the batch size is multiplied by \(k\), the gradient is averaged over \(k\) times as many examples, so it is less noisy. The linear scaling rule says the learning rate should grow by the same factor \(k\) to keep the progress per epoch roughly constant. In practice a large rate applied from the first step can push the weights into a poor region, because the early gradients of a randomly initialised network are unreliable. The warm-up is the remedy.

## Problem

Large-batch training is attractive because it uses many accelerators in parallel. Without a change in the schedule, however, accuracy falls as the batch grows. Goyal et al. ask whether a simple rule can keep accuracy at large batch sizes without tuning.

## Core idea

Two changes. First, the learning rate scales linearly with the minibatch size. Second, the rate starts from the small base value and rises to its scaled target over the first few epochs, instead of jumping there at once.

## Algorithm

Let \(\eta\) be the base rate for a batch of size \(n\), and let the batch be \(kn\).

1. Set the rate for the large batch to \(k\eta\) (linear scaling rule).
2. For the first warm-up period, start at \(\eta\) and increase the rate by a constant amount at each iteration. The paper's schedule reaches \(\hat\eta = k\eta\) after 5 epochs.
3. After warm-up, use the usual decay schedule.

The paper reports that the results are robust to the exact duration of warm-up.

For Transformers, Vaswani et al. (2017) use a related warm-up with an inverse-square-root decay afterwards:

\[
\mathrm{lrate} = d_{\mathrm{model}}^{-0.5}\cdot \min\!\left(\mathrm{step}^{-0.5},\ \mathrm{step}\cdot \mathrm{warmup\_steps}^{-1.5}\right)
\]

With \(\mathrm{warmup\_steps} = 4000\), the rate rises linearly for the first 4000 steps, then declines in proportion to the reciprocal of the square root of the step number.

## Results

- Goyal et al. (2017) report "no loss of accuracy when training with large minibatch sizes up to 8192 images" on ImageNet.
- They report training ResNet-50 with a minibatch of 8192 on 256 GPUs in one hour, and about 90% scaling efficiency when moving from 8 to 256 GPUs, on the hardware they describe.
- The Transformer schedule in Vaswani et al. (2017) uses warmup_steps = 4000, as stated in the paper.

## Limitations

- The linear scaling rule is hyperparameter-free, but it is only tested in the large-batch regime that the paper studies. Other settings may need a different scaling.
- The 5-epoch warm-up is shown to be robust for ResNet-50 on ImageNet. It is not a general prescription, and other tasks may need a longer or shorter ramp.
- The Transformer schedule ties the rate to the model width through \(d_{\mathrm{model}}\), so the same numbers do not carry over to a different width without rechecking.

## Connections

- [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md) is the overview that compares this method with cosine restarts and cyclical rates.
- [Large-batch and distributed training](large-batch-and-distributed.md) is the setting where linear scaling and warm-up matter.
- [Cosine annealing with warm restarts](cosine-annealing-warm-restarts.md) is the decay that often follows a warm-up.
- [Transformers](../models/transformer/index.md) use warm-up in nearly every training recipe.

## Open questions

- Is warm-up a fix for optimisation at the start of training, or does it mainly stabilise normalisation statistics?
- Does the linear scaling rule hold at batch sizes far beyond 8192 for other architectures?

## References

### Seminal papers

- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — The linear scaling rule and gradual warm-up, with the ResNet-50 results at batch size 8192.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — The Transformer schedule with linear warm-up and inverse-square-root decay.
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR. https://arxiv.org/abs/1608.03983 — A later schedule that also begins each run with a high rate, after a restart.
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV. https://arxiv.org/abs/1506.01186 — Another schedule that varies the rate between bounds, for comparison.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review. https://arxiv.org/abs/1606.04838 — Survey of stochastic gradient methods, including the step-size choices behind warm-up.
