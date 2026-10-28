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

The Tensor Processing Unit (TPU) is Google's application-specific chip for neural network inference, built around a large systolic array of multiply-accumulate units. Jouppi et al. describe the first generation and report that it ran neural network inference about 15 to 30 times faster than contemporary CPUs and GPUs, with roughly 30 to 80 times higher performance per watt. It is an [AI accelerator](../index.md) whose design principle is a fixed dataflow for dense matrix multiplication.

## Problem

Neural network inference at datacentre scale is dominated by matrix multiplication with a small number of operand types. A general-purpose processor spends much of its energy on instruction fetch, control and memory movement rather than on arithmetic, so the cost per inference is set largely by that overhead.

## Core idea

Build a chip around a large matrix unit in which data flows through a grid of multiply-accumulate cells. Each weight is loaded once and reused across many inputs, and each activation passes from cell to cell, so most values are read from memory once. The control logic is small, and the chip performs the same operation on every cycle.

## Equation or algorithm

The core operation is a matrix product \(Y = XW\). In a systolic array of size \(n \times n\), each cell multiplies its stored weight by the incoming activation and adds the result to a partial sum passed to its neighbour. The first-generation chip contains a 256 × 256 array of multiply-accumulate units that perform 8-bit multiply-and-adds on signed or unsigned integers, as the paper's architecture section describes. A layer of size \(m \times k\) by \(k \times n\) therefore keeps the array busy with little traffic to memory. The chip trades numerical precision for throughput.

## Key methods

Two landmark designs show the trade-off between a fixed dense dataflow and a more flexible one.

- **First-generation TPU (Jouppi et al., 2017):** described on this page. A fixed systolic dataflow for dense matrix products, with 8-bit integer arithmetic and inference only.
- [Eyeriss v2 (Chen et al., 2018)](../eyeriss-v2/index.md): a flexible on-chip network that processes compressed and sparse models, aimed at mobile devices.

## Results

The abstract reports that the TPU is about 15 to 30 times faster than contemporary GPUs and CPUs, with TOPS per watt about 30 to 80 times higher. The comparison is against an Intel Haswell CPU and an Nvidia K80 GPU, on the workloads of the period, so the figures apply to those workloads. The authors also state that if the TPU had the GDDR5 memory of the contemporary GPU, its achieved TOPS would roughly triple.

## Limitations

A fixed dataflow suits dense matrix work, and irregular or sparse operations map less naturally onto it. The paper covers only the first generation, an inference-only chip, so its results do not describe later generations. Comparisons of this kind depend on the workloads and the software stack used.

## Open questions

- **Sparse workloads.** Whether a systolic design can exploit sparsity without losing its efficiency is an open design question. [Eyeriss v2](../eyeriss-v2/index.md) approaches it differently.
- **Memory bandwidth.** The paper's own hypothetical suggests that memory, rather than the matrix unit, limits the chip. Gholami et al. make the same point for serving large models, in the memory-wall analysis cited below.
- **Related designs.** The matrix units inside GPUs, the tensor cores, play a similar role with a more flexible control structure.

## Connections

The TPU's pods are connected by an inter-chip network, which the scaling discussion on the [AI hardware](../../index.md) overview depends on. Its dense-matrix design is also why the [transformer](../../../../theory/models/transformer/index.md) layer is a natural fit for it.

## References

### Seminal papers

- Jouppi, N. P., et al. (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — Describes the first TPU and reports about 15 to 30 times the speed and 30 to 80 times the TOPS per watt of contemporary CPUs and GPUs.
- Chen, Y.-H., et al. (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — A contrasting design that exploits sparsity with a flexible on-chip network, evaluated on compact models.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. DOI:10.48550/arXiv.2205.14135. https://doi.org/10.48550/arXiv.2205.14135 — Shows how reducing memory traffic between memory tiers speeds up exact attention on accelerators.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the architectures and dataflows that make dense matrix work efficient.

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is becoming the main limit on serving large Transformer models on server hardware.
