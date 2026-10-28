---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/hardware
  - engineering/inference-optimization
tags:
  - engineering
  - frameworks
  - compilers
aliases:
  - ML compilers
  - 機器學習編譯器
  - 核心程式語言
---

# Compilers and Kernels

!!! info "Part of Frameworks & Tools"
    This page sits under [Frameworks & Tools](../index.md). It compares the compiler and kernel layer; each method has its own page.

A deep-learning model is a graph of tensor operations, and running it fast means turning that graph into code for a specific chip. A compiler does this translation, and a kernel is the code that runs one fused operation on the hardware. Compilers and kernel languages decide how many times data travels between slow and fast memory, which is often what limits speed.

## Overview

Two needs drive this layer. First, a researcher writes a model in Python, and the framework must capture it as a graph without rewriting it by hand. Second, a new architecture or a new chip should not wait for an expert to write a hand-tuned kernel for every operation. Compilers meet the first need by tracing or capturing the program and rewriting it. Kernel languages meet the second by letting an engineer write a fused operation close to the hardware, without writing low-level device code.

## Key concepts

- **Graph capture.** Turning eager Python execution into a graph that a compiler can optimise.
- **Operator fusion.** Combining several operations into one kernel, so that intermediate results stay in fast memory instead of returning to slow memory.
- **Tiling.** Splitting a large tensor operation into blocks that fit in fast on-chip memory.
- **Lowering.** Translating a graph through intermediate representations until it becomes device code.
- **Hand-written kernels.** Operations written by an expert for one chip, such as the attention kernels in [FlashAttention](https://arxiv.org/abs/2205.14135), which read and write less memory than the unfused version.

## How it works

```mermaid
flowchart LR
  P[Python model] --> C[Graph capture]
  C --> G[Graph IR]
  G --> F[Fusion and tiling]
  F --> K[Device kernels]
  K --> H[Accelerator]
```

The framework captures the model, the compiler rewrites the graph and chooses a fusion and tiling plan, and the backend emits kernels for the chip. Each step can be done ahead of time or on first call.

## Key methods

Three systems are the main examples. Each has its own page, which gives the design, the programming model and the limits.

- [XLA](xla.md): a compiler for linear algebra used by JAX and TensorFlow, and integrated into PyTorch. It lowers graphs through an intermediate representation and targets many backends.
- [torch.compile and TorchInductor](torch-compile.md): PyTorch's graph capture and default compiler. It captures the Python program and generates code, using Triton for NVIDIA, AMD and Intel GPUs.
- [Triton](triton.md): a Python-based language for writing tiled GPU kernels by hand. It is used directly by engineers and as a backend by TorchInductor.

TVM, a compiler for deep-learning workloads across many back-ends, is an important earlier system. Chen et al. (2018) describe its graph-level and operator-level optimisations.[^tvm]

## Connections

- The chip-side view of fusion, number formats and kernels is on [AI Hardware](../../hardware/index.md) and its [co-design](../../hardware/co-design/index.md) page.
- Fused attention and KV-cache handling are central to [Inference Optimization](../../inference-optimization/index.md).
- The model-side view, including quantisation that changes the number format a kernel uses, is in [Model compression](../../../theory/model-compression/index.md).

## Applications

Kernel and compiler work matters most where a single operation dominates cost, such as attention in long-context serving, and where a new architecture needs fast kernels before any hand-tuned library exists.

## Open questions

- **Hand kernels or compilers.** Hand-written kernels give the most control, while compilers reach more hardware with less effort. The balance is still moving.
- **Portability.** A kernel tuned for one chip can lose much of its speed on another, and it is not yet clear how far compilers can close that gap.
- **Reproducibility.** Speed-ups depend on compiler versions, so they are hard to compare across software stacks.

## References

### Seminal papers

- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — Shows that tiling attention to reduce reads and writes between GPU memory levels gives exact attention with lower memory traffic.
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — Describes a compiler that applies graph-level and operator-level optimisation across diverse hardware back-ends.

### Articles and documentation

- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of XLA, its supported frameworks and its pluggable backend design.
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official description of TorchDynamo, AOTAutograd, TorchInductor and the default backend.
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of Triton, a Python-based language and compiler for writing GPU kernels.

[^tvm]: Chen et al. (2018), listed in References.
