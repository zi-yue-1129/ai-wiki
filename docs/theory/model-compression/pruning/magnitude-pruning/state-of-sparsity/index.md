---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- benchmarks
aliases:
  - The state of sparsity
  - Sparsity benchmark
  - 稀疏性現況
---

# The State of Sparsity in Deep Neural Networks

The state of sparsity is a 2019 benchmark that evaluates several pruning and sparsity methods under one protocol on large-scale tasks. Its main finding, that simple magnitude pruning matches or beats more complex methods, is the reason [magnitude pruning](../index.md) remains the baseline that newer methods must beat.

## Problem

Many sparsity methods were being proposed, each with its own setup, so their results could not be compared directly. It was unclear which gains were real and which came from differences in training.

## Core idea

Run several sparsity methods under a common protocol on large-scale image and language tasks. The methods share the same mask-and-retrain pattern and differ only in how the mask is chosen and updated, so the comparison isolates that choice.

## Equation or algorithm

The benchmark does not add a new algorithm. Each method chooses a mask at a target sparsity, the masked network is retrained, and the final accuracy is compared at matched sparsity. The paper reports the accuracy-sparsity trade-off for each method.

## Results

The abstract reports that on large-scale tasks, simple magnitude pruning matches or beats more complex sparsity techniques.

## Limitations

The benchmarks cover the image and language models of their time. The paper also shows that sparse networks obtained by pruning are harder to train from scratch than dense ones, a point that limits the sparse-training methods.

## Open issues and related variants

- **Newer models.** Whether the same ranking holds for large transformers, where pruning is often one-shot, is not covered by the original benchmark; see [one-shot pruning of large language models](../../one-shot-llm-pruning/index.md).
- **Related:** [gradual pruning](../gradual-pruning/index.md) is the schedule that the benchmark's magnitude baseline uses.

## Connections

The benchmark motivates the choice of magnitude as a default score across the [pruning](../../index.md) family. Its trade-offs between sparsity and speed depend on the hardware that runs the result, as discussed in [AI hardware](../../../../../engineering/hardware/index.md).

## References

### Seminal papers

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks sparsity methods under one protocol and finds magnitude pruning a strong baseline.
- Zhu, M., Gupta, S. (2017). *To prune, or not to prune: exploring the efficacy of pruning for model compression*. arXiv:1710.01878. https://arxiv.org/abs/1710.01878 — Gradual magnitude pruning that the benchmark evaluates.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — The prune-and-retrain method that defines the baseline.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — A survey placing the benchmark's methods in a wider context.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Frankle, J., Carbin, M. (2018). *The Lottery Ticket Hypothesis: Finding Sparse, Trainable Neural Networks*. arXiv:1803.03635. https://arxiv.org/abs/1803.03635 — A sparse-training result that the benchmark's trainability finding relates to.
