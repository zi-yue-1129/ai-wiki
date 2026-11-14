---
last_reviewed: 2026-11-04
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

A deep-learning model is a graph of tensor operations. Running it fast on a specific chip means turning that graph into device code: a compiler performs this translation, and a kernel is the code that runs one, often fused, operation on the hardware.

!!! info "Part of Frameworks & Tools"
    This page sits under [Frameworks & Tools](../index.md). It compares the compiler and kernel layer; each method has its own page with the detail.

## Overview

Two needs drive this layer. First, a researcher writes a model in Python, and the framework must capture it as a graph without rewriting it by hand. Second, a new architecture or a new chip should not wait for an expert to write a hand-tuned kernel for every operation. Compilers meet the first need by capturing the program and rewriting its graph. Kernel languages meet the second by letting an engineer write a fused operation close to the hardware, without writing low-level device code.

The cost that these tools attack is memory traffic. Many operations spend more time moving data between slow and fast memory than computing, so the order and grouping of operations often matters more than the raw arithmetic. [FlashAttention](https://arxiv.org/abs/2205.14135) makes this argument for attention: an IO-aware kernel reads and writes less of the slow memory and computes exact attention faster.

## Key concepts

- **Graph capture.** Turning eager Python execution into a graph that a compiler can optimise.
- **Operator fusion.** Combining several operations into one kernel, so that intermediate results stay in fast memory instead of returning to slow memory.
- **Tiling.** Splitting a large tensor operation into blocks that fit in fast on-chip memory.
- **Lowering.** Translating a graph through intermediate representations until it becomes device code.
- **Hand-written kernels.** Operations written by an expert for one chip, such as the attention kernels that FlashAttention describes.

## How it works

```mermaid
flowchart LR
  P[Python model] --> C[Graph capture]
  C --> G[Graph IR]
  G --> F[Fusion and tiling]
  F --> K[Device kernels]
  K --> H[Accelerator]
```

The framework captures the model, the compiler rewrites the graph and chooses a fusion and tiling plan, and the backend emits kernels for the chip. Each step can run ahead of time or on the first call. The stages differ between systems: XLA lowers through its own intermediate representation, while TorchInductor generates Triton code for GPUs.

## Key methods

Three systems are the main examples. Each has its own page, which gives the design, the programming model and the limits.

- [XLA](xla.md): a compiler for linear algebra that the official project describes as usable from PyTorch, TensorFlow and JAX. It is built on MLIR and targets GPUs, CPUs and ML accelerators.
- [torch.compile and TorchInductor](torch-compile.md): PyTorch's graph capture and default compiler. It keeps the eager programming style, and TorchInductor uses Triton kernels on NVIDIA, AMD and Intel GPUs.
- [Triton](triton.md): a Python-based language for writing tiled GPU kernels by hand. Engineers use it directly, and TorchInductor uses it as a backend.

Earlier systems set the vocabulary. Halide separates what a pipeline computes from how it is scheduled, a split that later compilers built on. TVM searches for schedules automatically for many back-ends. MLIR provides the shared compiler infrastructure on which XLA is built. Each is cited in the references below.

## Connections

- The chip-side view of fusion, number formats and kernels is on [AI Hardware](../../hardware/index.md) and its [co-design](../../hardware/co-design/index.md) page.
- Fused attention and KV-cache handling are central to [Inference Optimization](../../inference-optimization/index.md).
- The model-side view, including quantisation that changes the number format a kernel uses, is in [Model compression](../../../theory/model-compression/index.md).

## Applications

Kernel and compiler work matters most where one operation dominates cost, such as attention in long-context serving. It also matters when a new architecture needs fast kernels before any hand-tuned library exists. Compilers are used to train and serve large models across many accelerator types, where writing a separate kernel for each would not be practical.

## Open questions

- **Hand kernels or compilers.** Hand-written kernels give the most control, while compilers reach more hardware with less effort. The balance is still moving.
- **Portability.** A kernel tuned for one chip can lose much of its speed on another, and it is not yet clear how far compilers can close that gap.
- **Reproducibility.** Speed-ups depend on compiler and library versions, so they are hard to compare across software stacks.

## References

### Seminal papers

- Ragan-Kelley, J. et al. (2013). *Halide*. PLDI 2013. https://doi.org/10.1145/2491956.2462176 — Separates the algorithm of an image pipeline from its schedule, the split that schedule-based compilers reuse.
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv:1802.04799. https://arxiv.org/abs/1802.04799 — Describes a compiler that applies graph-level and operator-level optimisation across diverse hardware back-ends.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — Shows that tiling attention to reduce reads and writes between GPU memory levels gives exact attention with lower memory traffic.
- Tillet, P., Kung, H. T. & Cox, D. (2019). *Triton: an intermediate language and compiler for tiled neural network computations*. MAPL 2019. https://doi.org/10.1145/3315508.3329973 — Introduces the intermediate language and compiler behind Triton's tiled kernels.
- Lattner, C. et al. (2020). *MLIR: A Compiler Infrastructure for the End of Moore's Law*. arXiv:2002.11054. https://arxiv.org/abs/2002.11054 — Describes MLIR, the shared compiler infrastructure that XLA's official page says it leverages.
- Ansel, J. et al. (2024). *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*. ASPLOS 2024. https://doi.org/10.1145/3620665.3640366 — Describes the graph-capture and compilation design behind PyTorch 2's compiler.

### Articles and documentation

- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of XLA, the frameworks it supports, its backends and its optimisation passes.
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official description of TorchDynamo, AOTAutograd, TorchInductor and the default backend.
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of Triton, a Python-based environment for writing GPU kernels.
