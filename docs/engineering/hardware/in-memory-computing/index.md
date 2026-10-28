---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- brain-mind/snn-neuromorphic
- engineering/hardware/memory-hierarchy
tags:
- AI hardware
- in-memory computing
- analogue computing
- memristor
- crossbar
- RRAM
aliases:
  - In-memory computing
  - Analogue computing
  - Analog in-memory computing
  - Compute-in-memory
  - 記憶體內運算
  - 類比運算
---

# In-Memory and Analogue Computing

In-memory computing performs multiply-accumulate operations inside the memory array that stores the weights, so the weights do not have to travel to a processor at all. Analogue variants use the physics of resistive devices to do the arithmetic, so one array operation computes a whole vector-matrix product at once. The approach targets the data-movement cost described in [memory hierarchy and bandwidth](../memory-hierarchy/index.md), and it trades exactness for efficiency. This page is a subchapter of [AI Hardware](../index.md). Spiking and event-driven hardware is a different approach, covered on the [spiking networks](../../../brain-mind/snn-neuromorphic/index.md) page, and is not repeated here.

## Problem

In a conventional accelerator, each weight is read from memory and sent to a multiply-accumulate unit for every use. The energy and time spent on those reads can exceed the arithmetic itself. A layer whose weights already sit inside the memory could compute its output where the data is stored.

## Core idea

Store each weight as a conductance in a resistive device, such as a resistive RAM (RRAM), phase-change or memristive cell, and arrange the devices in a crossbar. Apply the input as voltages on the rows. Each device then passes a current equal to its voltage times its conductance, and the currents on each column add together. The column currents are therefore the dot products of the input with the stored weights, computed in one step.

Digital in-memory designs keep the arithmetic exact by computing with bits stored in SRAM or similar cells. They avoid the analogue noise discussed below, but they keep some of the same benefit: the operands stay in place.

## Equation or algorithm

Ohm's law gives each device's current, and Kirchhoff's current law adds the currents on a shared column wire. For a crossbar with input voltages \(V_i\) on the rows and conductances \(G_{ij}\) at the crossings,

\[
I_j = \sum_i V_i \, G_{ij}
\]

The output of a layer is the vector of column currents, which is then digitised. Weights are usually stored with positive and negative conductances, or with pairs of devices, to represent signed values. Each operation needs digital-to-analogue conversion of the inputs and analogue-to-digital conversion of the outputs, and these converters often dominate the energy and area of the design.

Training is harder than inference. Updating a weight means reprogramming a device, which may be slow, may wear the device out, and may not change its conductance by the exact amount required. The approach in Ambrogio et al. is to perform the weight updates in place on analogue devices while keeping the accuracy of software training.

## Results

Ambrogio et al. (2018) report that in-place neural-network training on analogue memory hardware reaches the same accuracy as software training on common benchmarks, including MNIST and CIFAR-10 and CIFAR-100, and that it is more energy-efficient and faster than contemporary GPUs in the paper's comparison.

Wan et al. (2022) report a compute-in-memory chip built on RRAM, in which inference was measured entirely on the hardware for several edge AI tasks. Its accuracy is comparable to software models with 4-bit weights, and its energy-delay product is lower than that of earlier RRAM compute-in-memory chips.

Rasch et al. (2023) show that analogue in-memory inference introduces approximation errors that lower accuracy, and that retraining with a more realistic model of the hardware recovers accuracy close to floating point for large CNNs, RNNs and transformers.

## Limitations

Analogue results depend on device variation, drift over time, limited precision of the converters and the noise of the read-out circuits. Models must be trained or adapted for the hardware, and their accuracy is then specific to one device and one chip. Device endurance and programming speed limit how often weights can change, so the approach suits inference with fixed weights better than training. Benchmarks often report energy for the array alone and exclude converters and data movement at the array's edges.

## Open issues and related variants

- **Large language models.** An LLM's weights are much larger than a single crossbar, so a model must be split across many arrays, and the cost of the communication between them is not yet well characterised.
- **Dynamic matrices.** Attention multiplies by matrices that are created at run time, such as the KV cache, which means writing to the array for every token. This works against the fixed-weight advantage and is an open design question.
- **Digital versus analogue.** Digital in-memory designs trade some of the efficiency for exact arithmetic and simpler programming. Which approach wins in practice depends on precision requirements and on the cost of the converters.
- **Survey.** Sebastian et al. survey the memory devices and their applications for in-memory computing, which gives the device background that the results above depend on.
- **Related:** [quantisation](../../../theory/model-compression/quantisation/index.md) reduces the precision that analogue arrays must represent, and the [memory hierarchy](../memory-hierarchy/index.md) page describes the data-movement cost that in-memory designs try to avoid.

## Connections

In-memory designs are an alternative to the [GPU and TPU](../accelerators/index.md) architectures, which move data to fixed arithmetic units. Their training and inference trade-offs also affect the [model compression](../../../theory/model-compression/index.md) methods that a device can support.

## References

### Seminal papers

- Ambrogio, S., et al. (2018). *Equivalent-accuracy accelerated neural-network training using analogue memory*. Nature 558. https://doi.org/10.1038/s41586-018-0180-5 — Shows that in-place neural-network training on analogue memory reaches the accuracy of software training on common benchmarks.
- Wan, W., et al. (2022). *A compute-in-memory chip based on resistive random-access memory*. Nature 608. https://doi.org/10.1038/s41586-022-04992-8 — Reports an RRAM compute-in-memory chip whose inference accuracy is close to software models with 4-bit weights.
- Yao, P., et al. (2020). *Fully hardware-implemented memristor convolutional neural network*. Nature 577. https://doi.org/10.1038/s41586-020-1942-4 — Implements a full convolutional network on memristor arrays, with every layer computed on the hardware.

### Surveys and textbooks

- Sebastian, A., et al. (2020). *Memory devices and applications for in-memory computing*. Nature Nanotechnology. https://doi.org/10.1038/s41565-020-0655-z — Surveys the memory devices and applications that in-memory computing depends on.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Rasch, M. J., et al. (2023). *Hardware-aware training for large-scale and diverse deep learning inference workloads using in-memory computing-based accelerators*. arXiv:2302.08469. https://arxiv.org/abs/2302.08469 — Shows that retraining with a realistic hardware model recovers near floating-point accuracy for large CNNs, RNNs and transformers.
