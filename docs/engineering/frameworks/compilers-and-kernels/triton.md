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
  - Triton kernel language
  - OpenAI Triton
  - Triton 語言
---

# Triton

!!! info "Part of Compilers and Kernels"
    This method page belongs to [Compilers and Kernels](index.md). It explains the kernel language in detail; the parent page compares it with the compiler systems.

Triton is a language and compiler for writing GPU kernels in Python. The official documentation describes it as providing a "Python-based programming environment" for "productively writing custom DNN compute kernels," with the aim of reaching "maximal throughput on modern GPU hardware." It sits between a fully automatic compiler and hand-written device code: the programmer chooses the tiling, and Triton handles the low-level details.[^triton]

## Problem

Some operations, such as attention, are fast only when they are fused and tiled to fit in on-chip memory. Writing those kernels in CUDA takes expert time for each chip and each variant. Automatic compilers do not always find the best tiling, so a faster kernel needs someone to write it. The problem is to make that kind of kernel practical to write, without losing most of the hardware speed.

## Core idea

The programmer writes a block of a computation in Python, and the compiler maps it onto the chip's threads and memory. The program is organised around tiles, which are blocks of data loaded from slow memory, computed on, and written back. Because the programmer controls the tile size and the order of loads, the kernel can keep intermediate values on chip, which is the memory argument behind fused attention.

## Procedure

1. The engineer writes a kernel as a Python function that operates on blocks of data.
2. The programmer picks block sizes and the loads and stores for each block.
3. The Triton compiler lowers the function and generates GPU code for the target device.
4. The kernel is called from Python, the same way as a library function.

Triton is also used as a backend. TorchInductor generates Triton code for NVIDIA, AMD and Intel GPUs, as described on the [torch.compile page](torch-compile.md).

## Results

The official documentation is a description of the language and its goals, and it does not report benchmark results. This page gives no speed-up figures. Kernels written in Triton should be measured on the target GPU, with the Triton version recorded.

## Limitations

- **Programmer effort.** A faster kernel still needs knowledge of tiling and memory. The language lowers the effort compared with CUDA, but does not remove it.
- **Target coverage.** The set of supported hardware and features depends on the Triton version and the backend.
- **Tuning.** The best block sizes differ across chips and input shapes, so kernels need autotuning or careful selection.
- **Newer levels.** The official page mentions a lower-level programming model called Gluon, which is less mature and is not described in detail here.

## Connections

- The compiler that generates Triton code for PyTorch is [torch.compile and TorchInductor](torch-compile.md).
- The compiler for linear algebra, which fuses operations automatically, is [XLA](xla.md).
- The reason fused kernels matter for attention is on the [FlashAttention](https://arxiv.org/abs/2205.14135) paper and in [Inference Optimization](../../inference-optimization/index.md).

## Open questions

- Will hand-written kernels in a higher-level language keep their advantage as compilers improve?
- How should kernels be shared across chips with different memory hierarchies?

## References

### Seminal papers

- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — A fused, tiled attention kernel that shows the speed gain Triton-style kernels aim for.
- Chen, T. et al. (2018). *TVM: An Automated End-to-End Optimizing Compiler for Deep Learning*. arXiv. https://arxiv.org/abs/1802.04799 — The automatic alternative, which searches for schedules rather than asking the programmer to write them.

### Articles and documentation

- Triton contributors. *Triton documentation*. https://triton-lang.org/main/index.html — Official documentation of the language, its Python-based environment and its goals.
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — Official description of how TorchInductor uses Triton for GPU kernels.
- OpenXLA. *XLA: Optimized compiler for machine learning*. https://openxla.org/xla — Official description of the compiler path that competes with hand-written kernels.

[^triton]: Triton contributors, *Triton documentation*, listed in References.
