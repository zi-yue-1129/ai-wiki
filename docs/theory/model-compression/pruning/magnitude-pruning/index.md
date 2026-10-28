---
status: complete
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- magnitude pruning
aliases:
  - Magnitude pruning
  - Gradual pruning
  - 量值剪枝
---

# Magnitude Pruning

Magnitude pruning removes the weights with the smallest absolute values and keeps the rest. It is the oldest and simplest [pruning](../index.md) criterion, and it is still the baseline that newer methods must beat. Its appeal is that it needs no extra statistics, no second-order information and no special hardware to compute the scores.

## Overview

Given a weight tensor \(W\) and a sparsity target \(s\), magnitude pruning builds a mask \(M\) that keeps the weights whose absolute values are above the \(s\)-quantile of \(|W|\), and sets the rest to zero. Done once, this is one-shot pruning. Done repeatedly with retraining in between, or with a gradual schedule that raises the sparsity over the course of training, it recovers much more accuracy. The choice of schedule, and whether the threshold is global or per layer, matters as much as the scoring rule.

## Key concepts

- **Score.** The absolute value of a weight. It ignores how the weight interacts with the inputs, which is the weakness that later scores such as [Wanda](../one-shot-llm-pruning/wanda/index.md) address.
- **Global versus layer-wise thresholds.** A global threshold lets some layers prune more than others. Layer-wise thresholds keep every layer at the same sparsity.
- **Gradual schedule.** Sparsity increases from zero to the target over training, so that the network can adapt while it is being pruned.
- **Retraining.** The weights that remain are trained further to recover accuracy after each pruning step.

## Comparison of key methods

| Method | What it adds to magnitude pruning | Page |
| --- | --- | --- |
| Gradual pruning | A smooth sparsity schedule over training, large sparse models beat small dense ones at the same memory footprint | [Gradual pruning](gradual-pruning/index.md) |
| Benchmark study | Head-to-head comparison showing magnitude pruning is a strong baseline | [The state of sparsity](state-of-sparsity/index.md) |

Gradual pruning changes when the mask is cut. The benchmark asks whether more complex pruning methods are worth their cost, and finds that simple magnitude pruning matches or beats them on the tasks it tests.

## Trade-offs

- **Simplicity versus accuracy at high sparsity.** Magnitude pruning is cheap and strong at moderate sparsity. At very high sparsity, methods that correct the remaining weights do better.
- **Unstructured versus structured.** Magnitude scores can prune whole structures too, but the usual result is an irregular mask, which needs sparse kernels to run faster.
- **Schedule cost.** Gradual pruning needs training time, and the saving in compute depends on the hardware.

## More variants and open issues

- **Open issue:** why the magnitude of a weight is a good proxy for its importance in trained networks. This is the question the [lottery ticket](../lottery-ticket/index.md) line of work approaches from another side.
- **Variant:** magnitude times input norm, the basis of [Wanda](../one-shot-llm-pruning/wanda/index.md).
- **Open issue:** whether gradual schedules transfer across architectures without tuning.

## Connections

Magnitude pruning gives an unstructured mask, so its speed-up depends on the sparse kernels discussed under [AI hardware](../../../../engineering/hardware/index.md). The idea that the brain eliminates weak connections during development, which magnitude pruning mimics, is discussed in [neuroscience](../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — Finds that large sparse models beat small dense models at the same memory footprint, with up to 10 times fewer non-zero parameters and minimal loss in accuracy.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Magnitude pruning followed by retraining, reducing AlexNet parameters by a factor of 9.
- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — Magnitude-based pruning finds subnetworks that train well from their initial weights.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A broad survey of sparsity methods across training and inference.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods and finds magnitude pruning a strong baseline.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
