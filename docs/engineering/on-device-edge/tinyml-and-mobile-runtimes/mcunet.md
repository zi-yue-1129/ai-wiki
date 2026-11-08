---
last_reviewed: 2026-11-04
related:
  - engineering/on-device-edge
  - engineering/hardware
tags:
  - engineering
  - on-device
  - tinyml
aliases:
  - MCUNet
  - Tiny deep learning
  - 微控制器網路
---

# MCUNet

MCUNet is a system for running image classification on microcontrollers, which have a few hundred kilobytes of SRAM and about a megabyte of flash memory. It designs the network and the inference memory schedule together, under the limits of a specific device, instead of shrinking a large network afterwards. The paper reports 70.7% ImageNet top-1 accuracy on an STM32H743 microcontroller, with 512 kB of SRAM and 2 MB of flash.

!!! info "Part of TinyML and Mobile Runtimes"
    This method page belongs to [TinyML and Mobile Runtimes](index.md). It explains MCUNet in detail; the parent page compares it with the runtimes.

## Problem

A standard image classifier has tens of megabytes of weights and large activation tensors. A microcontroller can hold neither in its memory, so the usual approach of pruning or quantising a big model is not enough: the peak activation memory during inference must also fit. Scaling a network down after design often wastes the budget, because the architecture was not chosen for the memory the device has.

## Core idea

MCUNet has two parts that are designed together. TinyNAS is a two-stage neural architecture search. It first narrows the search space to fit the tight memory limits of the target, and then searches for a model inside that space. TinyEngine is a memory-efficient inference engine that schedules the network's computation using the structure of the whole network, which keeps peak memory low. The search and the engine are designed for one another, so the network is chosen for the memory the engine can deliver.

## Procedure

1. Define the device budget: the SRAM and flash sizes, and the task, here ImageNet-scale classification.
2. Run TinyNAS to find a network architecture that fits the budget.
3. Generate a memory plan for the chosen network, so that the activations of each layer reuse a fixed set of buffers.
4. Compile the network into a program that runs with the memory plan.
5. Measure accuracy and peak memory on the device.

## Results

The paper's headline is 70.7% ImageNet top-1 accuracy, reported on the STM32H743 microcontroller (512 kB SRAM, 2 MB flash). The paper's default board for its other reported results is the STM32F746, which has 320 kB of SRAM and 1 MB of flash, and the abstract reports that MCUNet uses 3.5 times less SRAM and 5.7 times less flash than quantised MobileNetV2 and ResNet-18. The exact figures depend on the board and the software version, so readers should use the paper's tables rather than a single headline number.

## Limitations

- **One device class.** The network is designed for a fixed memory budget. A larger device needs a new search, not a rescaled copy.
- **Accuracy ceiling.** Even with co-design, a microcontroller reaches less accuracy than a phone-class model on the same task.
- **Task scope.** The results concern image classification. Detection, speech and language models have different memory profiles, which the method does not address directly.
- **Maintenance cost.** Each new device, task or software update may need its own search and measurement.

## Later work

The follow-up [MCUNetV2](https://arxiv.org/abs/2110.15352) reduces peak memory with patch-based inference, which computes parts of a feature map at a time. Its abstract reports 4 to 8 times lower peak memory for existing networks and 71.8% ImageNet top-1 accuracy on a microcontroller. It does not yet have its own page in this wiki.

## Connections

- The depthwise separable convolution used by efficient mobile networks is the building block of [MobileNets](https://arxiv.org/abs/1704.04861), covered under the [CNN family](../../../theory/models/cnn/index.md).
- The integer arithmetic that microcontrollers use is the setting of [Jacob et al. (2017)](https://arxiv.org/abs/1712.05877).
- For phones, where the runtime maps a model onto several accelerators, see [LiteRT](litert.md) and [ExecuTorch](executorch.md).

## Open questions

- Can the search cover many device budgets at once, so that one search serves a family of microcontrollers?
- How much accuracy is lost when the memory schedule must also share SRAM with the rest of the firmware?

## References

### Seminal papers

- Lin, J., Chen, W.-M., Lin, Y., Cohn, J., Gan, C. & Han, S. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — The main paper: co-designed architecture search (TinyNAS) and inference engine (TinyEngine) for microcontrollers, with the 70.7% result on STM32H743.
- Lin, J., Chen, W.-M., Cai, H., Gan, C. & Han, S. (2021). *MCUNetV2: Memory-Efficient Patch-based Inference for Tiny Deep Learning*. arXiv:2110.15352. https://arxiv.org/abs/2110.15352 — Follow-up that reduces peak memory with patch-based inference and reports 71.8% ImageNet top-1 on a microcontroller.
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — Introduces depthwise separable convolutions for efficient vision networks, a building block of many tiny networks.
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Describes integer-only quantised inference, the arithmetic style that microcontroller deployments rely on.
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — The compression approach that MCUNet's co-design is designed not to rely on alone.

### Articles and documentation

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — Official documentation of a runtime with an Arm Cortex-M backend, for comparison with a co-designed microcontroller stack.
