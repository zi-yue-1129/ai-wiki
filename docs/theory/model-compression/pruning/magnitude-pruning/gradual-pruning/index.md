---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- magnitude pruning
aliases:
  - Gradual pruning
  - Sparsity schedule
  - 漸進式剪枝
---

# Gradual Pruning

Gradual pruning raises the sparsity of a network smoothly during training, rather than cutting it in one step. Zhu and Gupta used it to compare large sparse networks with small dense networks at the same parameter count, and found that the sparse networks were consistently better. It is a schedule layered on top of [magnitude pruning](../index.md).

## Problem

Pruning papers compared pruned networks with the dense networks they came from. It was unclear whether pruning was a better use of a fixed parameter budget than training a smaller dense network from the start.

## Core idea

Compare large sparse models with small dense models at the same number of parameters, and prune the large model gradually during training. The network can adapt to each small cut, so a gradual schedule recovers more accuracy than a single cut to the same sparsity.

## Equation or algorithm

Sparsity rises from zero to the target over the training steps according to a smooth cubic schedule. At each step the lowest-magnitude weights are masked until the current sparsity is reached, and training continues on the remaining weights. The schedule replaces one large cut with many small ones.

## Results

The authors find that large sparse models consistently outperform small dense models across the architectures they tested, at the same parameter count.

## Limitations

The gradual schedule adds training steps. The comparison is at fixed parameter count, which is not the same as fixed compute, because sparse layers may not run faster on dense hardware.

## Open issues and related variants

- **Schedule transfer.** Whether a schedule tuned for one architecture transfers to another without retuning is not settled.
- **Related:** the [lottery ticket](../../lottery-ticket/lottery-ticket-hypothesis/index.md) procedure also prunes gradually, but it resets the surviving weights to an early point in training.

## Connections

A gradual schedule is a form of the iterative pruning in [learning both weights and connections](../../learning-weights-and-connections/index.md). The benchmark that places magnitude pruning among other methods is in [the state of sparsity](../state-of-sparsity/index.md).

## References

### Seminal papers

- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — Introduces the gradual schedule and shows that large sparse models beat small dense ones.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The iterative prune-and-retrain pipeline that gradual schedules refine.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks gradual magnitude pruning against other sparsity methods.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys schedules for sparsity during training.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — The rewind-and-retrain alternative to a gradual schedule.
