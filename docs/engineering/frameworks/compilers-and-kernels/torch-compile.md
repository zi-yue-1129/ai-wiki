---
status: draft
last_reviewed: 2026-10-28
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

!!! info "Part of Compilers and Kernels"
    This method page belongs to [Compilers and Kernels](index.md). It explains PyTorch's compiler stack in detail; the parent page compares it with the other systems.

`torch.compile` is PyTorch's entry point for compiling a model while keeping the eager Python programming style. It captures the program with TorchDynamo, captures the backward pass with AOTAutograd, and hands the graph to a backend. The default backend is TorchInductor, which generates fast code for several accelerators and, for NVIDIA, AMD and Intel GPUs, uses OpenAI Triton kernels.

## Problem

PyTorch's eager mode is easy to debug, but it runs one operation at a time, so intermediate results are written to slow memory between operations. A compiler can fuse operations, but it must capture a Python program that may branch, call external code and change shape. The problem is to capture the program reliably, without asking the user to rewrite it.

## Core idea

Trace the Python frames that run the model, record the tensor operations as a graph, and compile that graph. When the tracer meets code it cannot capture, it splits the graph there and runs the rest in Python. TorchDynamo does the capture, and the official page says it "uses a CPython feature called the Frame Evaluation API to safely capture PyTorch graphs."

## Procedure

1. The user calls `torch.compile` on a model or function.
2. TorchDynamo captures the forward graph from the Python bytecode.
3. AOTAutograd captures the backward pass ahead of time, so that the compiler can optimise both directions.
4. The backend compiles the graphs. By default this is TorchInductor, which generates code and calls Triton for GPU kernels.
5. Other backends can be selected, and the page lists examples such as cudagraphs, TensorRT, TVM and OpenVINO.

Where capture fails, the graph is broken into pieces. The official page refers readers to its guide on graph breaks, rather than describing them itself.

## Results

The official documentation describes the components and the default backend, and it does not report benchmark results. This page does not give speed-up figures. Readers who need numbers should measure their own model and record the PyTorch version, since results change between releases.

## Limitations

- **Graph breaks.** Code that the tracer cannot capture splits the graph. Many breaks reduce the benefit, and finding them takes effort.
- **Compile time and recompilation.** Changing input shapes can trigger new compilations.
- **Backend dependence.** Speed depends on TorchInductor and the Triton version for the target GPU.
- **Debugging.** Errors can come from the compiler stack rather than the model, which makes them harder to trace than eager errors.

## Connections

- The language that TorchInductor generates kernels in is [Triton](triton.md).
- The compiler that JAX users rely on is [XLA](xla.md).
- Fused attention kernels, which compilers try to reproduce, are discussed in [Inference Optimization](../../inference-optimization/index.md).

## Open questions

- How often does a real model fall back to eager execution, and what is the cost of each break?
- Will general-purpose compilers match hand-tuned kernels on the newest attention variants?

## References

### Seminal papers

- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — A compiler that optimises graphs and operators for many back-ends, one of the systems TorchInductor's backend list names.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — The kernel-level argument that reducing memory traffic speeds attention, which compilers try to recover.

### Articles and documentation

- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official description of TorchDynamo, AOTAutograd, TorchInductor and the default backend.
- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of the compiler used by JAX and TensorFlow, for comparison.
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of the kernel language that TorchInductor uses for GPU code.

: PyTorch, *torch.compiler: Compiling PyTorch models*, listed in References.
