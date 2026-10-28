---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- theory/models/transformer
tags:
- AI hardware
- accelerators
- GPU
- TPU
- NPU
aliases:
  - AI accelerators
  - Hardware accelerators
  - AI 加速器
---

# AI Accelerators

AI accelerators are chips built to run the matrix multiplications and convolutions that dominate neural networks. GPUs, TPUs, NPUs and other application-specific integrated circuits (ASICs) make different trade-offs between general-purpose flexibility and efficiency on a fixed workload. Comparing them by design principle, rather than by vendor specifications, shows why a chip suits training, datacentre inference or a phone. This page is the overview of the [AI hardware](../index.md) chapter.

## Overview

Most accelerators share one idea: keep many multiply-accumulate units busy, and move data as little as possible. They differ in how much control they keep. A GPU runs thousands of threads and offers programmable kernels, so it adapts to many workloads. A TPU or other ASIC hard-wires a dataflow for dense matrix multiplication, so it spends less energy per operation on that workload but adapts less. An NPU in a phone targets low-power inference with fixed precision formats.

## Comparison by design principle

| Family | Design principle | Strength | Limit | Page |
| --- | --- | --- | --- | --- |
| GPU | Many programmable parallel cores, with tensor units for matrix multiplication | Flexible; large software ecosystem | Power and memory traffic per operation | Overview on this page |
| TPU | Systolic array of multiply-accumulate units with a fixed dataflow | High throughput per watt on dense matrix work | Less adaptable to irregular or sparse operations | [TPU](tpu/index.md) |
| Sparse-aware edge accelerator | Reconfigurable on-chip network that exploits sparsity and reuse | Efficient on compact, sparse models | Narrower software support | [Eyeriss v2](eyeriss-v2/index.md) |
| Mobile NPU | Fixed-function inference units at low voltage | Low energy for on-device models | Limited to supported operators and formats | Overview on this page |

The GPU and mobile NPU rows are covered by the chapter overview, because their design choices are shared across vendors and are described in the Key concepts there.

## Key concepts

- **Systolic arrays.** A grid of multiply-accumulate units in which data flows from cell to cell, so each input is read from memory once and reused many times.
- **Tensor cores.** Units inside a GPU that multiply small matrix tiles in one instruction, usually at low precision.
- **Dataflow.** The order in which weights and activations are reused. The dataflow decides how much memory traffic a layer causes.
- **Specialisation.** A chip built for dense matrix multiplication gains efficiency and loses flexibility. The right balance depends on the workload, which is why training and inference often use different chips.

## Open issues

- **Sparsity in hardware.** Structured sparsity, such as N:M patterns, is supported on a few chips, but unstructured sparsity rarely gives a speed-up on accelerators.
- **Attention.** Attention is memory-bound in practice, and accelerator designs for long contexts are still changing quickly.
- **Measuring efficiency.** Peak throughput and power figures from vendors are hard to compare, because precision, memory and software differ.

## Connections

Accelerator design sets the cost of [training](../../training/index.md) and serving, and the precision formats that chips support decide which [compression methods](../../../theory/model-compression/index.md) pay off in practice. The attention cost that drives accelerator design is discussed in the [KV cache](../../../theory/models/transformer/kv-cache/index.md) page.

## References

### Seminal papers

- Jouppi, N. P., et al. (2017). *In-Datacenter Performance Analysis of a Tensor Processing Unit*. arXiv:1704.04760. https://arxiv.org/abs/1704.04760 — Reports that the TPU runs about 15 to 30 times faster than contemporary CPUs and GPUs, with much higher performance per watt.
- Chen, Y.-H., et al. (2018). *Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices*. arXiv:1807.07928. https://arxiv.org/abs/1807.07928 — A reconfigurable on-chip network that exploits sparsity, reported as 12.6 times faster than the original Eyeriss on MobileNet.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — A tutorial and survey of DNN hardware platforms, architectures and benchmarking metrics.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is now the main bottleneck for AI serving.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — An IO-aware attention kernel that reduces reads and writes between GPU memory levels.
