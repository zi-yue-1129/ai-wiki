---
status: draft
last_reviewed: 2026-10-28
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

!!! info "Part of TinyML and Mobile Runtimes"
    This method page belongs to [TinyML and Mobile Runtimes](index.md). It explains MCUNet in detail; the parent page compares it with the runtimes.

MCUNet is a system for running image classification on microcontrollers, which have a few hundred kilobytes of SRAM and about a megabyte of flash memory. It designs the network and the inference memory schedule together, under the limits of one specific device, instead of shrinking a large network afterwards. The paper reports ImageNet classification above 70 percent top-1 accuracy on a microcontroller with 320 kB of SRAM and 1 MB of flash.

## Problem

A standard image classifier has tens of megabytes of weights and large activation tensors. A microcontroller can hold neither in its memory, so the usual approach of pruning or quantising a big model is not enough: the peak activation memory during inference must also fit. Scaling a network down after design often wastes the budget, because the architecture was not chosen for the memory that the device has.

## Core idea

MCUNet has two parts that are designed together. TinyNAS searches a space of small networks for the one that best fits the memory and compute budget of the target. TinyEngine is an inference library that schedules the computation of that network to keep the peak memory low, without the dynamic allocation that a general runtime needs. The search and the scheduler share one objective, so the network is chosen for the memory the scheduler can actually deliver.

## Procedure

1. Define the device budget, the SRAM and flash sizes, and the target accuracy task.
2. Search a space of network architectures, using the budget as a constraint.
3. Generate a memory plan for the chosen network, so that each layer's activations reuse a fixed buffer.
4. Compile the network into a program that runs with no dynamic memory allocation.
5. Measure accuracy and peak memory on the device.

## Results

The paper reports ImageNet top-1 accuracy above 70 percent on a microcontroller with 320 kB of SRAM and 1 MB of flash. The same work reports results for other budgets and tasks, and it compares the designed network with standard architectures that do not fit the device. The numbers depend on the device and the software version, so a reader should use the paper's tables for the exact figures and not treat the single headline result as a general speed or accuracy claim.

## Limitations

- **One device class.** The network is designed for a fixed memory budget. A larger device needs a new search, not a rescaled copy.
- **Accuracy ceiling.** Even with co-design, a microcontroller reaches less accuracy than a phone-class model on the same task.
- **Task scope.** The results concern image classification. Detection, speech and language models have different memory profiles that the method does not address directly.
- **Maintenance cost.** Each new device, task or software update may need its own search and measurement.

## Connections

- The depthwise separable convolution used by efficient mobile networks is the building block behind [MobileNets](https://arxiv.org/abs/1704.04861), covered under the [CNN family](../../../theory/models/cnn/index.md).
- The integer arithmetic that microcontrollers use is the setting of [Jacob et al. (2017)](https://arxiv.org/abs/1712.05877).
- For phones, where the runtime maps a model onto several accelerators, see [LiteRT](litert.md) and [ExecuTorch](executorch.md).

## Open questions

- Can the search cover many device budgets at once, so that one search serves a family of microcontrollers?
- How much accuracy is lost when the memory schedule must also share SRAM with the rest of the firmware?

## References

### Seminal papers

- Lin, J. et al. (2020). *MCUNet: Tiny Deep Learning on IoT Devices*. NeurIPS 2020. arXiv:2007.10319. https://arxiv.org/abs/2007.10319 — The main paper: co-designed architecture search and inference library for microcontrollers, with the ImageNet results on 320 kB SRAM.
- Howard, A. G. et al. (2017). *MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications*. arXiv:1704.04861. https://arxiv.org/abs/1704.04861 — The efficient convolutional baseline whose depthwise separable blocks make small networks practical.
- Jacob, B. et al. (2017). *Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference*. arXiv:1712.05877. https://arxiv.org/abs/1712.05877 — Integer-only inference, which microcontrollers need for their arithmetic units.
- Han, S., Mao, H. & Dally, W. J. (2016). *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*. ICLR 2016. arXiv:1510.00149. https://arxiv.org/abs/1510.00149 — The compression approach that MCUNet's design avoids relying on alone.

### Articles and documentation

- PyTorch. *ExecuTorch documentation*. https://docs.pytorch.org/executorch/stable/index.html — Official documentation of a runtime with a Cortex-M backend, for comparison with a co-designed microcontroller stack.
