---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/attention-variants/flash-attention/index.md
tags:
  - inference
  - GPU
  - kernels
aliases:
  - Fused Kernels
  - FlashAttention
  - IO-Aware Attention
  - 融合核心
  - 融合運算核心
  - 感知輸入輸出的注意力
---

# Fused kernels and IO-aware attention

A fused kernel performs several operations in one pass over the data, so that intermediate results stay in fast on-chip memory instead of being written out to slower memory and read back. For large language models, where many operations are limited by memory traffic rather than arithmetic, fusion is one of the main ways to lower latency and raise throughput during inference.

This page is part of [Inference Optimization](index.md).

## Overview

On a modern accelerator, the arithmetic units are often faster than the path to main memory. An operation that does little arithmetic per byte it reads or writes is therefore limited by memory bandwidth, and its speed depends on how many trips to memory it makes. Attention is a clear case. The naive computation writes a large score matrix to memory and reads it back for each step, so its cost grows with sequence length in both time and memory.

## Key concepts

- **Kernel:** a function that runs on the accelerator. A model's forward pass is a sequence of kernels.
- **Fusion:** combining several kernels into one, so that intermediate values are not stored in main memory.
- **IO-awareness:** designing an algorithm around the number of reads and writes between fast and slow memory, not only the number of arithmetic operations.
- **Memory-bound operation:** an operation whose speed is set by memory traffic.

## How it works

A fused attention kernel divides the query, key and value matrices into blocks that fit in fast memory. It loads a block, computes the attention scores for that block, updates a running normalisation, and writes only the final output. The full matrix of scores is never written out. The result is the same as standard attention, which is why the method is described as exact. Fusing small operations, such as adding a bias, applying an activation and normalising, follows the same principle on a smaller scale.

## Key methods

- [FlashAttention (Dao et al., 2022)](../../theory/models/transformer/attention-variants/flash-attention/index.md): exact attention computed in blocks, so the full score matrix is not stored. It is described on its own page in the Models section.
- Fused elementwise and normalisation kernels: combine bias, activation and normalisation layers into one kernel, which removes their extra memory round trips.
- Hand-written versus compiler-generated kernels: experts write fused kernels by hand for the hottest operations, while compilers generate fused kernels for the rest. See [Hardware](../hardware/index.md) for the memory system these choices target.

## Connections

- Reduced numerical precision lowers memory traffic as well; see [Mixed-precision training and inference](../hardware/co-design/mixed-precision.md).
- Serving-time memory management for the attention cache is the subject of [PagedAttention](paged-attention.md).
- The attention variant that FlashAttention accelerates is described on [Transformer attention variants](../../theory/models/transformer/attention-variants/index.md).

## Applications

- Long-context serving, where attention cost dominates.
- Lower-latency chat and code completion on GPU servers.
- Faster training runs, since the same kernels speed up the backward pass.

## Limitations

- **Hardware-specific.** A kernel tuned for one accelerator generation may not be fast on another, and it has to be maintained as hardware changes.
- **Engineering cost.** Hand-written kernels are difficult to write and debug, and a fused kernel is harder to change than separate operations.
- **Gains depend on the workload.** Operations that are compute-bound see little benefit from reduced memory traffic.

## Open questions

- How far can compilers generate fused kernels that match hand-written ones?
- How should kernel changes be checked for numerical differences?

## References

### Seminal papers

- Dao, T. et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. NeurIPS. https://arxiv.org/abs/2205.14135 — Introduces IO-aware exact attention that avoids storing the full attention matrix in memory.
- Dao, T. (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. arXiv. https://arxiv.org/abs/2307.08691 — A later revision that improves parallelism and work partitioning in the same kernel family.
- Micikevicius, P. et al. (2018). Mixed Precision Training. ICLR. https://arxiv.org/abs/1710.03740 — Shows that training with reduced-precision arithmetic can match full-precision accuracy, which reduces memory traffic.
- Kwon, W. et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention. SOSP. https://arxiv.org/abs/2309.06180 — Manages the attention cache in pages, which is a memory-system approach to serving.
- Chen, T. et al. (2018). TVM: An Automated End-to-End Optimizing Compiler for Deep Learning. OSDI. https://arxiv.org/abs/1802.04799 — A compiler that generates optimised kernels for many hardware targets, the automated counterpart to hand-written kernels.
