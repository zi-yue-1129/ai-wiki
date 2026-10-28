---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
tags:
- AI hardware
- accelerators
- TPU
- systolic arrays
aliases:
  - Tensor Processing Unit
  - TPU
  - 張量處理單元
---

# Tensor Processing Unit

The Tensor Processing Unit (TPU) is Google's application-specific chip for neural network inference, built around a large systolic array of multiply-accumulate units. Jouppi et al. describe the first generation and report that it ran production workloads about 15 to 30 times faster than contemporary CPUs and GPUs, with roughly 30 to 80 times higher performance per watt. It is an [AI accelerator](../index.md) whose design principle is a fixed dataflow for dense matrix multiplication.

## Problem

Neural network inference at datacentre scale is dominated by matrix multiplication with a small number of operand types. A general-purpose processor spends most of its energy on instruction fetch, control and memory movement rather than on arithmetic, and the cost per inference is set by that overhead.

## Core idea

Build a chip around a large matrix unit in which data flows through a grid of multiply-accumulate cells. Each weight is loaded once and reused across many inputs, and each activation passes from cell to cell, so most values are read from memory once. The control logic is small, and the chip does the same operation on every cycle.

## Equation or algorithm

The core operation is a matrix product \(Y = XW\). In a systolic array of size \(n \times n\), each cell multiplies its stored weight by the incoming activation and adds the result to a partial sum passed to its neighbour. A layer of size \(m \times k\) by \(k \times n\) therefore keeps the array busy with little traffic to memory. The first-generation TPU used 8-bit integer arithmetic, which trades precision for throughput.

## Results

The abstract reports that the TPU is about 15 to 30 times faster than contemporary GPUs and CPUs, with performance per watt roughly 30 to 80 times higher. The paper also estimates that giving the TPU the memory bandwidth of a GPU would roughly triple its achieved throughput. The comparison covers the workloads of the period, and the figures are specific to them.

## Limitations

A fixed dataflow suits dense matrix work and handles irregular or sparse operations poorly. The first-generation chip was an inference accelerator, and later generations added training and inter-chip interconnects. Comparisons of this kind depend on the workloads and the software stack used.

## Open issues and related variants

- **Sparse workloads.** Whether a systolic design can exploit sparsity without losing its efficiency is an open design question, which the [Eyeriss v2](../eyeriss-v2/index.md) design approaches differently.
- **Memory bandwidth.** The paper's own estimate suggests that memory, rather than the matrix unit, limits the chip. The same point is made by Gholami et al. in the memory-wall analysis cited below.
- **Related:** the matrix units inside GPUs, the tensor cores, play a similar role with a more flexible control structure.

## Connections

The TPU's pods are connected by an inter-chip network, which the scaling discussion on the [AI hardware](../../index.md) overview depends on. Its dense-matrix design is also why the [transformer](../../../../theory/models/transformer/index.md) layer is a natural fit for it.

## References

### Seminal papers

- Jouppi, N. P., et al. (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — Describes the first TPU and reports 15 to 30 times the speed and 30 to 80 times the performance per watt of contemporary CPUs and GPUs.
- Chen, Y.-H., et al. (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — A contrasting design that exploits sparsity with a reconfigurable on-chip network.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the architectures that make dense matrix work efficient.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Explains why memory bandwidth limits accelerators such as the TPU.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — Shows how reducing memory traffic speeds up attention on accelerators.
