---
last_reviewed: 2026-11-04
related:
  - engineering/hardware
tags:
  - engineering
  - frameworks
  - compilers
aliases:
  - XLA
  - Accelerated Linear Algebra
  - 加速線性代數
---

# XLA

XLA (Accelerated Linear Algebra) is an open-source compiler for machine learning. It takes a model's graph, optimises it, and generates code for a specific device. The official project describes it as usable from PyTorch, TensorFlow and JAX, and as built collaboratively by hardware and software companies including Alibaba, Amazon Web Services, AMD, Apple, Arm, Google, Intel, Meta and NVIDIA.

!!! info "Part of Compilers and Kernels"
    This method page belongs to [Compilers and Kernels](index.md). It explains XLA in detail; the parent page compares it with the other systems.

## Problem

A framework produces a graph of tensor operations. Run one operation at a time, and each intermediate result returns to slow memory before the next operation reads it. Hand-optimising every model for every chip does not scale. XLA addresses both by compiling the whole graph for the device, so that the compiler chooses the fusions.

## Core idea

Capture the program as a graph, lower it to a linear-algebra intermediate representation, optimise that representation with a series of passes, and emit code for the target backend. The official page says XLA "leverages the power of MLIR" to bring its capabilities into a single compiler toolchain. The backend is pluggable, so the same front end can serve GPUs, CPUs and ML accelerators.

## Procedure

1. The framework, for example JAX, traces the model and hands a graph to XLA.
2. XLA lowers the graph to its intermediate representation, called HLO in XLA's documentation.
3. A sequence of optimisation passes runs over the representation. The official page describes these as production-tested, and mentions automated partitioning for model parallelism.
4. The backend generates device code, and the compiled program runs on the chip.

The official page links to a walkthrough of the journey from HLO to an executable, which is the place to look for the detail of these steps.

## Results

The official page describes the system and does not report benchmark results, so this page gives no speed-up figures. The claims it makes concern coverage: XLA is integrated with PyTorch, JAX and TensorFlow, and it targets GPUs, CPUs and ML accelerators.

## Limitations

- **Compile time.** Ahead-of-time compilation adds latency on the first call, and graphs that change shape often recompile.
- **Less control than hand kernels.** A compiler chooses fusions by its own rules. An engineer who needs a specific tiling may still need a hand-written kernel, as in [Triton](triton.md).
- **Backend quality varies.** A new backend reaches full speed only when its passes and kernels are mature.
- **Portability of results.** Speed depends on compiler versions and the backend, so measurements do not transfer cleanly between stacks.

## Connections

- The alternative for PyTorch users is [torch.compile and TorchInductor](torch-compile.md), which can use Triton kernels.
- Fusion at the chip level is discussed on the [hardware co-design](../../hardware/co-design/index.md) page.
- JAX, the framework that most often uses XLA, is listed in [Frameworks & Tools](../index.md).

## Open questions

- How far can an automatic compiler match a hand-written attention kernel on a new chip?
- How should compilers handle dynamic shapes, which are common in serving and cause repeated compilation?

## References

### Seminal papers

- Lattner, C. et al. (2020). *MLIR: A Compiler Infrastructure for the End of Moore's Law*. arXiv:2002.11054. https://arxiv.org/abs/2002.11054 — Describes MLIR, the shared compiler infrastructure on which XLA's official page says it is built.
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv:1802.04799. https://arxiv.org/abs/1802.04799 — A contemporary compiler that also optimises graphs and operators for many back-ends, for comparison with XLA's design.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — Shows the memory-traffic argument for fused kernels, which a compiler tries to reproduce automatically.

### Articles and documentation

- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of XLA, the frameworks it supports, its backends and its optimisation passes.
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official PyTorch documentation of torch.compile and its backend options, for comparison with XLA's approach.
- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of the hand-written kernel language that complements compilers such as XLA.
