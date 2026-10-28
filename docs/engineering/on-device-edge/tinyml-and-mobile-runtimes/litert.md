---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/on-device-edge
  - engineering/frameworks
  - engineering/hardware
tags:
  - engineering
  - on-device
  - runtimes
aliases:
  - LiteRT
  - TensorFlow Lite
  - TFLite
  - 輕量執行環境
---

# LiteRT

!!! info "Part of TinyML and Mobile Runtimes"
    This method page belongs to [TinyML and Mobile Runtimes](index.md). It explains LiteRT in detail; the parent page compares it with the other runtimes.

LiteRT is Google's on-device runtime for machine learning, formerly known as TensorFlow Lite. It loads a model in a compact flatbuffer format and runs it on the device, using the CPU or hardware delegates for GPUs and neural processing units (NPUs). The official page describes it as a way to run models on a range of devices with CPU, GPU and NPU acceleration, and it lists export paths from PyTorch, TensorFlow and JAX.

## Problem

A model trained in a data-centre framework is large, uses 32-bit floating point, and depends on operators that a phone does not run efficiently. Shipping it means converting it to a smaller format, running it on hardware that varies from one phone to the next, and keeping the app within the memory and battery of the device. Each phone has a different mix of CPU, GPU and NPU, so the runtime must choose the best unit for each operator without the developer writing separate code for each chip.

## Core idea

Convert the trained model once into a flatbuffer file that the runtime can map into memory without a long parsing step. At run time, an interpreter executes the graph, and for each operator it asks a delegate whether the accelerator can run it. Supported operators go to the GPU or NPU; the rest run on the CPU. The developer writes one application, and the runtime handles the mapping.

## Procedure

1. Train the model in PyTorch, TensorFlow or JAX, and export it to the runtime's format.
2. Quantise the model, typically to 8-bit integers, using calibration data where needed.
3. Load the file in the application and create an interpreter.
4. Attach a delegate for the GPU or NPU, if the device has one.
5. Run inference, and measure latency and memory on each target device.

## Results

The official page describes the runtime's acceleration on CPU, GPU and NPU and its export paths. It does not publish benchmark figures in the material this page relies on, so this page gives no speed-up numbers. A reader who needs them should measure the model on the target phone with the delegate that will ship.

## Limitations

- **Operator coverage.** A delegate supports only some operators. When a model uses an unsupported one, the graph splits, and each split adds a copy between the CPU and the accelerator.
- **Quantisation effort.** Integer models need calibration, and some layers lose accuracy when quantised, so the conversion is not always a single step.
- **Device variation.** The same model can be fast on one phone and slow on another, depending on which delegate the device supports.
- **Large language models.** The runtime was designed for models that fit the device's memory. A large language model needs the cache and quantisation choices covered on the [on-device and edge AI](../index.md) page.

## Connections

- The quantisation step relies on the integer arithmetic of [Jacob et al. (2017)](https://arxiv.org/abs/1712.05877).
- The efficient architectures that suit this runtime are covered under the [CNN family](../../../theory/models/cnn/index.md), where MobileNets is a standard example.
- For a PyTorch-first alternative, see [ExecuTorch](executorch.md).
- For the smallest devices, see [MCUNet](mcunet.md).

## Open questions

- How should a runtime choose between a fast NPU delegate with few operators and a slower GPU delegate with more coverage?
- Can the conversion check, before shipping, whether the chosen delegate will run the whole model?

## References

### Seminal papers

- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — An efficient architecture of the kind this runtime is built to run, using depthwise separable convolutions.
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — The integer quantisation scheme behind 8-bit mobile deployment.
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — Compression methods that reduce a model before it is converted for a device.

### Articles and documentation

- Google. *LiteRT: On-device AI runtime*. https://developers.google.com/edge/litert — The official page for the runtime, its CPU, GPU and NPU acceleration, and its export paths.
- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — The PyTorch edge runtime, which covers the same deployment problem from a PyTorch export path.
