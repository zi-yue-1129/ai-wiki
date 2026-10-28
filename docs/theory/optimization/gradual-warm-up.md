---
status: complete
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

Gradual warm-up is a learning-rate schedule that starts small and rises over the first part of training. Goyal et al. (2017) combined it with the linear scaling rule, which multiplies the learning rate by the factor by which the minibatch grows. With this pair, ResNet-50 could be trained on ImageNet with minibatches of 8,192 images without a loss of accuracy. The parent overview is [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md).

## Overview

If the minibatch is multiplied by \(k\), each gradient is averaged over \(k\) times as many examples, so it is less noisy. The linear scaling rule says the learning rate should grow by the same factor \(k\), so that each pass over the data makes a similar amount of progress. A large rate applied from the first step, however, can push the weights into a poor region, because the gradients of a freshly initialised network are unreliable. Warm-up addresses that early instability.

## Problem

Large-batch training is attractive because many accelerators can work in parallel. Without a change to the schedule, accuracy falls as the minibatch grows. Goyal et al. ask whether a simple rule can keep accuracy at large minibatch sizes without tuning.

## Core idea

Two changes. First, the learning rate scales linearly with the minibatch size. Second, the rate starts at the small base value and rises to its scaled target over the first few epochs, rather than jumping there at once.

## Algorithm

Let \(\eta\) be the base rate for a minibatch of \(n\) images, and let the large minibatch be \(kn\) images. The paper uses a reference rate \(\eta = 0.1 \cdot kn/256\), so the base is a 256-image minibatch with a rate of 0.1.

1. **Linear scaling.** Set the target rate for the large minibatch to \(\hat\eta = k\eta\).
2. **Gradual warm-up.** Start at \(\eta\) and increase the rate by a constant amount at each iteration, so that it reaches \(\hat\eta\) after 5 epochs.
3. **Decay.** After warm-up, continue with the usual decay schedule.

For Transformers, Vaswani et al. (2017) use a related warm-up followed by an inverse-square-root decay:

\[
\mathrm{lrate} = d_{\mathrm{model}}^{-0.5}\cdot \min\!\left(\mathrm{step}^{-0.5},\ \mathrm{step}\cdot \mathrm{warmup\_steps}^{-1.5}\right)
\]

The paper sets \(\mathrm{warmup\_steps} = 4000\) and uses \(d_{\mathrm{model}} = 512\) for the base model. The rate rises linearly for the first 4,000 steps, then falls in proportion to the inverse square root of the step number.

## Results

- **Accuracy at large batches.** The abstract reports no loss of accuracy with minibatch sizes up to 8,192 images. In the paper's table, the 8k run with gradual warm-up has 23.74% top-1 error (±0.09), against 23.60% (±0.12) for the 256-image baseline.
- **Training time.** The authors train ResNet-50 with an 8,192-image minibatch on 256 GPUs in one hour.
- **Scaling efficiency.** Moving from 8 to 256 GPUs gives about 90% scaling efficiency, on the hardware the authors describe.

## Limitations

- **Breaking point.** The paper says the minibatch "cannot be scaled indefinitely". Accuracy degrades quickly beyond about 8k on ImageNet, with 24.79% error (±0.27) at 16k. Beyond 64k, training diverges with the linear rule.
- **Sensitivity.** Near the breaking point, the results are more sensitive to the learning rate, and the authors advise avoiding minibatch sizes close to it.
- **Warm-up form.** A constant warm-up "actually degrades results", and removing warm-up is worse than the baseline.
- **Duration.** The paper says the results are robust to the exact warm-up length, but it tests only 5 epochs. Other tasks may need a longer or shorter ramp.
- **Simulated runs.** Minibatches of 12k and larger were simulated on one server with gradient accumulation, not run across many machines.
- **Scope.** The authors' generalisation claim is for ImageNet, and they describe the linear rule's justification as a strong assumption.

## Variants and related schedules

- **Constant warm-up** holds the rate at a low value for the warm-up period. The paper reports that this degrades results.
- **Layer-wise rules** such as [LARS](lars.md) and [LAMB](lamb.md) scale the step per layer, which the linear rule does not do, and they are used with warm-up for very large batches.

## Connections

- [Learning-Rate Schedules and Warm-up](learning-rate-schedules.md) is the overview that compares this method with cosine restarts and cyclical rates.
- [Large-batch and distributed training](large-batch-and-distributed.md) is the setting where linear scaling and warm-up matter most.
- [Cosine annealing with warm restarts](cosine-annealing-warm-restarts.md) is a decay that is sometimes placed after a warm-up. The two are separate methods.
- [Transformers](../models/transformer/index.md) use warm-up in nearly every training recipe.

## Open questions

- Is warm-up mainly a fix for early optimisation, or does it stabilise normalisation statistics?
- Does the linear scaling rule hold beyond 8,192 images for other architectures?

## References

### Seminal papers

- Goyal, P., et al. (2017). *Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour*. arXiv. https://arxiv.org/abs/1706.02677 — The linear scaling rule and gradual warm-up, with ResNet-50 results at a minibatch of 8,192.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS 2017. https://arxiv.org/abs/1706.03762 — The Transformer schedule with linear warm-up and inverse-square-root decay.
- Loshchilov, I. & Hutter, F. (2017). *SGDR: Stochastic Gradient Descent with Warm Restarts*. ICLR 2017. https://arxiv.org/abs/1608.03983 — Cosine decay with restarts, a schedule that is often combined with a warm-up.
- Smith, L. N. (2017). *Cyclical Learning Rates for Training Neural Networks*. WACV 2017, pp. 464–472. doi:[10.1109/WACV.2017.58](https://doi.org/10.1109/WACV.2017.58) — Cycles the learning rate between bounds, a different approach to changing the rate over training.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. SIAM Review, 60(2), 223–311. doi:[10.1137/16M1080173](https://doi.org/10.1137/16M1080173) — Survey of stochastic gradient methods, including the step-size choices behind warm-up.
