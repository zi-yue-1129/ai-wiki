---
last_reviewed: 2026-11-04
related:
  - engineering/hardware
tags:
  - engineering
  - frameworks
  - compilers
aliases:
  - torch.compile
  - TorchInductor
  - TorchDynamo
  - 編譯 PyTorch 模型
---

# torch.compile and TorchInductor

`torch.compile` is PyTorch's entry point for compiling a model while keeping the eager Python programming style. It captures the forward program with TorchDynamo, captures the backward pass with AOTAutograd, and hands the graphs to a backend. The default backend is TorchInductor, which generates code for several accelerators and, for NVIDIA, AMD and Intel GPUs, uses OpenAI Triton kernels.

!!! info "Part of Compilers and Kernels"
    This method page belongs to [Compilers and Kernels](index.md). It explains PyTorch's compiler stack in detail; the parent page compares it with the other systems.

## Problem

PyTorch's eager mode is easy to debug, but it runs one operation at a time, so each intermediate result is written to slow memory before the next operation reads it. A compiler can fuse operations, but it must capture a Python program that may branch, call external code and change shape. The problem is to capture the program reliably, without asking the user to rewrite it.

## Core idea

Trace the Python frames that run the model, record the tensor operations as a graph, and compile that graph. When the tracer meets code it cannot capture, it splits the graph there and runs the rest in Python. TorchDynamo does the capture. The official documentation says it "uses a CPython feature called the Frame Evaluation API to safely capture PyTorch graphs."

The design is described in the ASPLOS 2024 paper on PyTorch 2, which covers the graph capture and compilation stack that `torch.compile` uses.

## Procedure

1. The user calls `torch.compile` on a model or function.
2. TorchDynamo captures the forward graph from the Python bytecode.
3. AOTAutograd captures the backward pass ahead of time, so that the compiler can optimise both directions.
4. The backend compiles the graphs. By default this is TorchInductor, which generates code and calls Triton for GPU kernels.
5. Other backends can be selected. The official documentation lists options for this choice.

Where capture fails, the graph is broken into pieces. The official documentation has a separate guide to graph breaks, which is the place to look when a model runs slower than expected.

## Results

The official documentation describes the components and the default backend, and it does not report benchmark results. This page therefore gives no speed-up figures. The ASPLOS 2024 paper reports its own evaluation, which should be read in that paper. Readers who need numbers for their own model should measure it and record the PyTorch version, since results change between releases.

## Limitations

- **Graph breaks.** Code that the tracer cannot capture splits the graph. Many breaks reduce the benefit, and finding them takes effort.
- **Compile time and recompilation.** Compilation takes time on the first call, and a change in input shape can trigger a new compilation.
- **Backend dependence.** Speed depends on TorchInductor and the Triton version for the target GPU.
- **Debugging.** An error can come from the compiler stack rather than the model, which makes it harder to trace than an eager-mode error.

## Connections

- The language that TorchInductor generates GPU kernels in is [Triton](triton.md).
- The compiler that JAX users rely on is [XLA](xla.md), which is also available as a PyTorch backend.
- Fused attention kernels, which compilers try to reproduce, are discussed in [Inference Optimization](../../inference-optimization/index.md).

## Open questions

- How often does a real model fall back to eager execution, and what is the cost of each break?
- Will general-purpose compilers match hand-tuned kernels on the newest attention variants?

## References

### Seminal papers

- Ansel, J. et al. (2024). *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*. ASPLOS 2024. https://doi.org/10.1145/3620665.3640366 — Describes the graph capture and compilation design that `torch.compile` builds on.
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv:1802.04799. https://arxiv.org/abs/1802.04799 — A compiler that optimises graphs and operators for many back-ends, an alternative design to TorchInductor.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — The kernel-level argument that reducing memory traffic speeds attention, which compilers try to recover.

### Articles and documentation

- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official description of TorchDynamo, AOTAutograd, TorchInductor and the default backend.
- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of the compiler used by JAX and TensorFlow, for comparison.
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of the kernel language that TorchInductor uses for GPU code.
