---
last_reviewed: 2026-11-04
related:
  - engineering/on-device-edge
  - engineering/frameworks
  - engineering/hardware
tags:
  - engineering
  - on-device
  - runtimes
aliases:
  - ExecuTorch
  - PyTorch edge runtime
  - 邊緣端執行環境
---

# ExecuTorch

ExecuTorch is PyTorch's runtime for on-device inference. A PyTorch model is exported ahead of time to a compact program, which a small runtime loads and runs on the device through pluggable backends. The official documentation states three design goals: portability, performance and productivity. It describes portability as running "from high-end mobile to constrained microcontrollers."

!!! info "Part of TinyML and Mobile Runtimes"
    This method page belongs to [TinyML and Mobile Runtimes](index.md). It explains ExecuTorch in detail; the parent page compares it with the other runtimes.

## Problem

A team that trains in PyTorch needs to ship the same model to phones, laptops and microcontrollers. Each target has its own accelerator and its own runtime, so a separate export path for each one doubles the work, and the exported model can differ from the one that was tested. The runtime must keep the model faithful to the training graph while letting each device use its own hardware.

## Core idea

Export the model with PyTorch's ahead-of-time tools into a graph that the runtime can execute without the Python interpreter. Lower the graph to the backend for the target device, which keeps the parts that backend supports and leaves the rest on a portable default. The runtime is small and has no dependency on a large framework, which suits devices with little memory. The official documentation describes the runtime as offering hardware acceleration across CPU, GPU, NPU and DSP targets.

## Procedure

1. Write and train the model in PyTorch.
2. Export the model with the ahead-of-time tools, so that the graph is fixed. The export builds on the graph capture described in [torch.compile and TorchInductor](../../frameworks/compilers-and-kernels/torch-compile.md).
3. Lower the exported graph to one or more backends for the target device.
4. Serialise the program to a file that the device runtime loads.
5. Run the program on the device and check its outputs against the PyTorch model.

## Backends

The official documentation lists a set of backends. Their names include XNNPACK, Core ML, Vulkan, Qualcomm AI Engine, MediaTek, OpenVINO, Arm Ethos-U and Arm Cortex-M. The documentation does not state the target hardware for every backend, so the backend page should be checked before a deployment relies on one.

## Results

The official documentation describes the design goals, the backends and the deployment steps. It does not report benchmark figures in the material this page relies on, so this page gives no speed or memory numbers. The comparison that matters for a project is between the backends on the target device, measured with the same inputs.

## Limitations

- **Backend support varies.** The set of supported operators and hardware depends on the backend and the release, so a model may run fully on one device and only partly on another.
- **Export strictness.** Ahead-of-time export needs a graph that can be captured, so dynamic control flow must be rewritten or limited.
- **Newer stack.** Compared with LiteRT, the PyTorch edge stack is more recent, and its interfaces change more often.
- **Verification.** Outputs of the exported program should be checked against the original model on each backend, since lowering can change numerical results.

## Connections

- The export and graph capture steps are related to the compiler layer described in [torch.compile and TorchInductor](../../frameworks/compilers-and-kernels/torch-compile.md).
- The mobile alternative built around a converter and delegates is [LiteRT](litert.md).
- For the smallest devices, where a co-designed model is needed, see [MCUNet](mcunet.md).

## Open questions

- How well can one exported graph serve both a phone NPU and a microcontroller without a separate lowering path for each?
- How should the team test that the exported program matches the training model across many backends?

## References

### Seminal papers

- Ansel, J. et al. (2024). *PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation*. ASPLOS 2024. https://doi.org/10.1145/3620665.3640366 — Describes the graph capture and compilation design that PyTorch's export tools build on.
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Integer quantisation, which several ExecuTorch backends use for NPUs and microcontrollers.
- Lin, J. et al. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — The microcontroller case, which the Arm Cortex-M backend addresses from the runtime side.

### Articles and documentation

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — The official documentation of the runtime, its design goals, its backends and its deployment steps.
- PyTorch. *torch.compiler: Compiling PyTorch models*. https://docs.pytorch.org/docs/2.14/user_guide/torch_compiler/torch.compiler.html — The PyTorch compiler documentation, which covers the graph capture that export builds on.
- Google. *LiteRT: High-Performance On-Device Machine Learning Framework*. https://developers.google.com/edge/litert — The alternative mobile runtime, for comparison with ExecuTorch's backend model.
