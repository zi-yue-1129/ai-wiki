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

![Animated 2:4 structured sparsity: four weights per group are evaluated, two are retained, and their values and positions are packed for supported sparse hardware.](../../../../assets/concept-animations/nm-sparsity-packing.gif)

*Original animated schematic, CC BY-SA 4.0.* In each **four-element group**, this example retains the **two largest-magnitude weights** and zeroes the others, then packs the retained values with position metadata. The 2:4 pattern enables compatible sparse matrix-multiplication hardware to skip the zeros; **a 50% nonzero reduction does not guarantee a 2× end-to-end speed-up**. All values and hardware pulses are illustrative, not benchmark results. [Mishra et al. (2021)](https://arxiv.org/abs/2104.08378).

## Key concepts

- **Pattern.** The rule \(N\):\(M\). The 2:4 pattern keeps half of the weights, and other patterns such as 1:4 or 4:8 are also studied.
- **Sparse tensor cores.** Recent NVIDIA GPUs implement the 2:4 pattern in hardware, storing the non-zero values and their positions in a compressed format.
- **Training with the pattern.** Pruning to N:M can be done after training or during training, and the pattern can be imposed from the start.
- **Trade-off with block size.** Larger blocks allow more freedom in choosing which weights to keep, but they make hardware support harder.

## Comparison of key methods

| Method | When the pattern is imposed | Page |
| --- | --- | --- |
| Learning N:M from scratch | During training, from the first step | [Learning N:M from scratch](learning-n-m-from-scratch/index.md) |
| Sparse tensor cores | After training, then fine-tuning to the 2:4 pattern | [Sparse tensor cores](sparse-tensor-cores/index.md) |

The first method asks whether the pattern costs accuracy if it is present from the start. The second describes the hardware and the workflow that make the pattern fast in practice.

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
