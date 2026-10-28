---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
tags:
- AI hardware
- accelerators
- sparsity
- edge inference
aliases:
  - Eyeriss v2
  - Eyeriss
  - Eyeriss v2 accelerator
---

# Eyeriss v2

Eyeriss v2 is a research accelerator for emerging neural networks on mobile devices, designed by Chen et al. It keeps the reuse of data that makes spatial accelerators efficient, adds a flexible on-chip network, and processes compressed, sparse weights and activations directly. The abstract reports that on sparse MobileNet at batch size one it is 12.6 times faster and 2.5 times more energy efficient than the original Eyeriss. It is an [AI accelerator](../index.md) built for compact and sparse models rather than dense matrix work.

## Problem

Compact models such as MobileNet are small and often sparse, so a chip built for dense matrix multiplication wastes work on zeros, and its data movement does not match the varying reuse of different layers. Mobile devices need low latency at batch size one, which such chips handle poorly.

## Core idea

Organise the processing elements in a hierarchical mesh network, so that the on-chip routing adapts to the different reuse patterns and bandwidth needs of weights, activations and partial sums. Store and process compressed sparse data directly, so that zero values are skipped instead of multiplied.

## Equation or algorithm

The chip computes the convolutions of a layer with a dataflow chosen to reuse each operand as much as possible. For sparse data, the processing elements receive only the non-zero values together with their indices, so the work scales with the number of non-zero products rather than with the full layer size. The mesh routes these values to the elements that need them.

## Results

The abstract reports that, on sparse MobileNet at batch size one in 65 nm CMOS, Eyeriss v2 reaches 1470.6 inferences per second and 2560.3 inferences per joule. It is reported as 12.6 times faster and 2.5 times more energy efficient than the original Eyeriss on the same network.

## Limitations

The design is a research chip evaluated on a specific process and network family, and its results do not transfer directly to other process nodes or models. The flexibility of the mesh network costs area and control complexity compared with a fixed systolic array.

## Open issues and related variants

- **Sparsity support.** Whether the benefit of skipping zeros holds for less sparse or differently structured models is open.
- **Related:** the [TPU](../tpu/index.md) uses a fixed systolic dataflow for dense matrix work, which is the contrasting design.
- **Compression.** Sparsity in the models comes from the compression methods described in [pruning](../../../../theory/model-compression/pruning/index.md), so the hardware benefit depends on those methods.

## Connections

The mobile-device setting connects this design to on-device models, discussed under [AI hardware](../../index.md) and in the [model compression](../../../../theory/model-compression/index.md) pages on the edge.

## References

### Seminal papers

- Chen, Y.-H., et al. (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — Reports 12.6 times the speed and 2.5 times the energy efficiency of the original Eyeriss on sparse MobileNet.
- Jouppi, N. P., et al. (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — The fixed-dataflow contrast, with a systolic array for dense inference.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys the dataflow and sparsity techniques that this design builds on.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Explains why data movement, which this design reduces, limits accelerators.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — A software-side example of reducing memory traffic.
