---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- sparsity
- hardware
aliases:
  - Learning N:M from scratch
  - Fine-grained structured sparsity
  - 從頭學習 N:M 稀疏
---

# Learning N:M Sparse Networks from Scratch

Learning N:M sparse networks from scratch trains a network with the N:M constraint from the first step, rather than pruning a dense network to the pattern afterwards. Zhou et al. showed that the pattern can be kept throughout training without losing accuracy, and reported a 2 times speed-up for a 2:4 sparse network on NVIDIA A100 GPUs. It is a method within [N:M sparsity](../index.md).

## Problem

N:M sparsity is hardware friendly, but it was unclear whether networks can be trained with the pattern from scratch without losing accuracy. Pruning to the pattern after training is one option, but it discards the weights that the pattern removes before they can adapt.

## Core idea

Enforce the N:M constraint during training, so that the weights and their selection evolve together under the pattern. The network never has to recover from a one-off cut to the pattern.

## Equation or algorithm

Within each block of \(M\) weights, at most \(N\) may be non-zero. The method keeps this constraint throughout training, and the choice of which weights are non-zero is updated as the weights change. The exact update rule is in the paper.

## Results

The abstract states that a 2:4 sparse network could achieve a 2 times speed-up without performance drop on NVIDIA A100 GPUs.

## Limitations

The reported speed-up is for the matrix multiplications that the hardware accelerates, not for the whole model. The experiments are on the networks of the time.

## Open issues and related variants

- **Larger blocks.** Whether training from scratch works for patterns with larger blocks, such as 4:8, is less studied.
- **Related:** [sparse tensor cores](../sparse-tensor-cores/index.md) describe the hardware and the pruning workflow for the 2:4 pattern.

## Connections

The pattern is an example of a method shaped by hardware design, and its benefit depends on the [memory hierarchy](../../../../../engineering/hardware/index.md) and the matrix units of the target device.

## References

### Seminal papers

- Zhou, A., et al. (2021). *Learning N:M Fine-grained Structured Sparse Neural Networks From Scratch*. arXiv:2102.04010. https://arxiv.org/abs/2102.04010 — Trains networks with the 2:4 pattern from scratch, with a 2 times speed-up on A100 GPUs.
- Mishra, A., et al. (2021). *Accelerating Sparse Deep Neural Networks*. arXiv:2104.08378. https://arxiv.org/abs/2104.08378 — Describes the 2:4 pattern that sparse tensor cores execute.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Unstructured pruning, the pattern that N:M sparsity trades off against.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys sparsity patterns and their hardware implications.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks the accuracy cost of sparsity across methods.
