---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
tags:
- model compression
- sparsity
- hardware
aliases:
  - N:M sparsity
  - 2:4 sparsity
  - Structured sparsity
  - N:M 稀疏
  - 2:4 稀疏
---

# N:M Fine-Grained Structured Sparsity

N:M sparsity keeps at most \(N\) non-zero values in every block of \(M\) consecutive weights. The best-known pattern is 2:4, which keeps two values in every group of four. It is fine-grained enough to keep most of the accuracy of unstructured [pruning](../index.md), and regular enough that hardware can skip the zeros, which is why it has become a standard for accelerators.

## Overview

Unstructured sparsity can remove many weights, but the irregular positions of the zeros give little speed-up on dense hardware. Structured sparsity removes whole channels, which is fast but coarse. An N:M pattern sits between them: within each small block the positions of the non-zero values are fixed to a regular rule, so the hardware can store the compressed values together with a small index, and the computation skips the zeros.

## Key concepts

- **Pattern.** The rule \(N\):\(M\). The 2:4 pattern keeps half of the weights, and other patterns such as 1:4 or 4:8 are also studied.
- **Sparse tensor cores.** Recent NVIDIA GPUs implement the 2:4 pattern in hardware, storing the non-zero values and their positions in a compressed format.
- **Training with the pattern.** Pruning to N:M can be done after training or during training, and the pattern can be imposed from the start.
- **Trade-off with block size.** Larger blocks allow more freedom in choosing which weights to keep, but they make hardware support harder.

## Key methods

### Learning N:M Fine-grained Structured Sparse Neural Networks From Scratch (Zhou et al., 2021)

- **Problem:** N:M sparsity was known to be hardware friendly, but it was unclear whether networks can be trained with the pattern from scratch without losing accuracy.
- **Core idea:** Train the network with the N:M constraint from the start, using a training method that keeps the pattern while letting the weights and their selection evolve.
- **Equation or algorithm:** Within each block of \(M\) weights at most \(N\) may be non-zero. The method keeps this constraint throughout training, rather than pruning to the pattern once at the end. The exact update rule is in the paper.
- **Results:** The abstract states that a 2:4 sparse network could achieve a 2 times speed-up without performance drop on NVIDIA A100 GPUs.
- **Limitations:** The reported speed-up is for the matrix multiplications that the hardware accelerates, not for the whole model, and the paper's experiments are on the networks of its time.

### Accelerating Sparse Deep Neural Networks (Mishra et al., 2021)

- **Problem:** Sparse tensor cores need a documented hardware pattern and a software path that makes the sparse format usable in training and inference.
- **Core idea:** Describe the 2:4 pattern implemented by sparse tensor cores, the workflow for pruning a trained network to that pattern, and retraining to recover accuracy.
- **Equation or algorithm:** Pruning to 2:4 keeps the two largest values in each group of four, followed by fine-tuning, with the compressed representation handled by the hardware.
- **Results:** The abstract states that sparse tensor cores exploit the 2:4 (50%) sparsity pattern, giving twice the math throughput of dense matrix units.
- **Limitations:** The gain depends on the hardware pattern and on the operations that the hardware accelerates. Patterns other than 2:4 do not get the same support.

## Trade-offs

- **Speed versus flexibility.** The 2:4 pattern gives a fixed 50% sparsity with hardware support, but it is less flexible than unstructured sparsity at high sparsity levels.
- **Accuracy.** Fine-grained patterns keep more accuracy than channel pruning at the same speed on supporting hardware.
- **Hardware lock-in.** The pattern is only fast where it is supported, so the choice follows the [accelerator](../../../../engineering/hardware/index.md) available.

## More variants and open issues

- **Open issue:** whether N:M patterns with larger blocks or different \(N\) and \(M\) can be supported on future hardware without losing the speed-up.
- **Open issue:** how N:M sparsity combines with quantisation, since the compressed format must carry both sparsity and reduced precision; see [quantisation](../../quantisation/index.md).
- **Variant:** [structured pruning](../structured-pruning/index.md), which removes whole channels and needs no special hardware.

## Connections

N:M sparsity is the clearest example of a compression method shaped by hardware design. The [memory hierarchy](../../../../engineering/hardware/index.md) of a device determines how much the compressed format saves in bandwidth, and that determines whether the pattern pays off in practice.

## References

### Seminal papers

- Zhou, A., et al. (2021). *Learning N:M Fine-grained Structured Sparse Neural Networks From Scratch*. arXiv:2102.04010. https://arxiv.org/abs/2102.04010 — Trains networks with the 2:4 pattern from scratch, reporting a 2 times speed-up on A100 GPUs without accuracy loss.
- Mishra, A., et al. (2021). *Accelerating Sparse Deep Neural Networks*. arXiv:2104.08378. https://arxiv.org/abs/2104.08378 — Describes the 2:4 pattern that sparse tensor cores execute, with twice the math throughput.
- Han, S., Pool, J., Tran, J., Dally, W. J. (2015). *Learning both Weights and Connections for Efficient Neural Networks*. arXiv:1506.02626. https://arxiv.org/abs/1506.02626 — Unstructured pruning, the pattern that N:M sparsity trades off against.

### Surveys and textbooks

- Hoefler, T., et al. (2021). *Sparsity in Deep Learning: Pruning and Growth for Efficient Inference and Training in Neural Networks*. arXiv:2102.00554. https://arxiv.org/abs/2102.00554 — Surveys sparsity patterns and their hardware implications.
- Gale, T., Elsen, E., Hooker, S. (2019). *The State of Sparsity in Deep Neural Networks*. arXiv:1902.09574. https://arxiv.org/abs/1902.09574 — Benchmarks the accuracy cost of sparsity across methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
