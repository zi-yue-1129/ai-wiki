---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- engineering/inference-optimization
- theory/model-compression
- theory/models/transformer
tags:
- AI hardware
- co-design
- kernels
- number formats
- mixed precision
- hardware-aware design
aliases:
  - Hardware-aware model design
  - Software-hardware co-design
  - Hardware-software co-design
  - 硬體感知模型設計
  - 軟硬體協同設計
---

# Hardware-Aware Model and Software Co-Design

A model's cost is not set by its parameter count or its FLOPs alone. Its speed depends on the number format it uses, on whether its operations are fused into kernels that keep data on chip, and on the chip it runs on. Hardware-aware design builds these facts into the model and the software stack from the start, rather than measuring a finished model and hoping it is fast. This page is a subchapter of [AI Hardware](../index.md). It covers the three main levers, which are number formats, kernels and compilers, and architecture choices measured on the target hardware, and it links to the pages on each of them.

## Problem

Counting FLOPs is a poor predictor of latency. Two networks with the same count can differ several times in speed, because one reads far more memory, uses a slower operation, or cannot be mapped efficiently onto the chip. Hardware changes faster than models, so a design tuned to one generation can be a poor fit for the next.

## Core idea

Three levers move the balance between compute and memory, and each has its own page elsewhere in the wiki:

- **Number formats.** Fewer bits per value means less memory traffic per operation. Mixed-precision training and 8-bit inference both rely on this, with the accuracy cost controlled by the training method.
- **Kernels and compilers.** A fused kernel performs several operations in one pass over the data, so intermediate results do not go back to off-chip memory. Hand-written kernels in CUDA and in the Triton language, and compiler paths such as XLA, are the software layer that makes this possible.
- **Architecture on the target.** A design choice, such as the number of key and value heads or the expert structure of a model, can be judged by its measured speed on the chip it will run on, not by its FLOPs.

## Equation or algorithm

The roofline model from [memory hierarchy and bandwidth](../memory-hierarchy/index.md) gives a first estimate of the time for a kernel:

\[
t \approx \max\left(\frac{\text{FLOPs}}{P_{\text{peak}}},\; \frac{\text{bytes moved}}{B}\right)
\]

Changing the number format changes the bytes term directly: storing weights in half the bits halves the bytes read per token for a memory-bound layer, and so roughly doubles its arithmetic intensity. Fusion changes the bytes term too, because intermediate results that stay on chip are not counted as traffic. Architecture choices change both terms at once, and only measurement on the target settles which one dominates.

## Results

Micikevicius et al. (2017) show that training with 16-bit floating-point values roughly halves the memory used across a range of architectures, provided a full-precision copy of the weights is kept and the loss is scaled.

Micikevicius et al. (2022) propose two 8-bit floating-point encodings, which they report can train CNNs, RNNs and transformers, including models with up to 175 billion parameters, to quality comparable with 16-bit training without changing hyperparameters.

Krishnamoorthi (2018) reports that post-training 8-bit integer quantisation with per-channel weights keeps many CNNs within about 2 percent of floating-point accuracy, with speed-ups of roughly 2 to 3 times on CPUs and up to 10 times on fixed-point hardware.

Dao et al. (2022) show that an attention kernel which avoids writing intermediate results to high-bandwidth memory is faster than the standard implementation while computing the same exact result. The method has its own page, [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md).

Tan et al. (2018) build measured inference speed on a phone into the search objective of MnasNet, so that the search favours networks that balance accuracy and latency on the device, instead of relying on FLOPs as a proxy.

## Limitations

Co-design ties a model to a chip. A network tuned for one accelerator may lose much of its speed on another, and portability suffers as a result. Reported speed-ups depend on compiler versions, batch sizes and the software stack, so they are hard to reproduce across environments. Lower-precision formats need care: they can change accuracy in ways that only appear on large or unusual workloads.

## Open issues and related variants

- **Which formats generalise.** It is not yet clear which 8-bit or 4-bit formats will remain usable across chip generations, or how far their accuracy holds for long reasoning chains.
- **Hand kernels versus compilers.** Hand-written CUDA kernels give the most control, while compilers and higher-level languages reach more hardware with less effort. The balance between them is changing.
- **[Mixture of experts](../../../theory/models/mixture-of-experts/index.md).** Shazeer et al. (2017) show that conditional computation can greatly increase model capacity at a similar compute cost. The cost moves to memory and to communication between chips, which is why the expert layout must be matched to the [interconnect](../interconnects/index.md).
- **Attention memory.** The [grouped-query attention](../../inference-optimization/grouped-query-attention.md) design reduces the [KV cache](../../../theory/models/transformer/kv-cache/index.md) that long-context decoding must read, and [PagedAttention](../../inference-optimization/paged-attention.md) reduces how much of that memory is wasted.
- **Related:** [quantisation](../../../theory/model-compression/quantisation/index.md) is the model-side half of the number-format lever, and the [model compression](../../../theory/model-compression/index.md) methods decide which formats a model can use.

## Connections

The hardware this page assumes is covered in [AI accelerators](../accelerators/index.md), with the [TPU](../accelerators/tpu/index.md) as an example of fixed-function matrix hardware. The training-side version of these trade-offs is in [distributed training](../../distributed-training/index.md).

## References

### Seminal papers

- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — An IO-aware attention kernel that is faster than the standard method while computing the same exact result.
- Micikevicius, P., et al. (2017). *Mixed Precision Training*. arXiv:1710.03740. https://arxiv.org/abs/1710.03740 — Shows that 16-bit training roughly halves memory use across architectures, with master weights and loss scaling.
- Micikevicius, P., et al. (2022). *FP8 Formats for Deep Learning*. arXiv:2209.05433. https://arxiv.org/abs/2209.05433 — Proposes two 8-bit floating-point encodings that train large models to quality comparable with 16-bit.
- Shazeer, N., et al. (2017). *Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer*. arXiv:1701.06538. https://arxiv.org/abs/1701.06538 — Introduces conditional computation that greatly increases capacity at similar compute cost.
- Tan, M., et al. (2018). *MnasNet: Platform-Aware Neural Architecture Search for Mobile*. arXiv:1807.11626. https://arxiv.org/abs/1807.11626 — Builds measured on-device latency into the architecture search objective.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys how dataflow and number format choices shape the efficiency of DNN hardware.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Krishnamoorthi, R. (2018). *Quantizing deep convolutional networks for efficient inference: A whitepaper*. arXiv:1806.08342. https://arxiv.org/abs/1806.08342 — Reports that per-channel 8-bit integer quantisation keeps many CNNs near floating-point accuracy and speeds inference on CPUs and fixed-point hardware.
