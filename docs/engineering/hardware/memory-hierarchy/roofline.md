---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- engineering/inference-optimization
tags:
- roofline
- performance model
- memory bandwidth
- arithmetic intensity
aliases:
  - Roofline model
  - Roofline performance model
  - Roofline plot
---

# Roofline Model

The roofline model is a chart that bounds the performance a program can reach on a given machine. It plots attainable performance against operational intensity, the number of operations a program performs for each byte it moves from memory. Two ceilings bound the chart: a horizontal line for the peak floating-point rate, and a sloped line for the peak memory bandwidth. Williams, Waterman and Patterson introduced it for multicore processors in 2008 and 2009. The [memory hierarchy](index.md) page uses it to show why bandwidth limits many workloads.

## Problem

A programmer who measures a kernel at, say, a few gigaflops per second cannot tell from that number alone whether the kernel is limited by memory, by arithmetic, or by poor code, or how much faster it could run. Williams et al. wanted one chart that gives insight to both programmers and architects, and that shows which resource limits a floating-point kernel on a given machine.

## Key concepts

- **Operational intensity:** the number of operations per byte of DRAM traffic, measured between the caches and main memory. It is the horizontal axis of the chart.
- **Compute ceiling:** the peak floating-point performance of the machine. It is a horizontal line, and no kernel can go above it. The paper obtains it from the hardware specifications or from microbenchmarks.
- **Memory ceiling:** the peak memory bandwidth, drawn as a diagonal on log-log axes. The paper describes it as the steady-state bandwidth the memory can sustain, not the nominal pin bandwidth of the DRAM chips.
- **Ridge point:** the intensity where the two ceilings meet. It is the peak performance divided by the peak bandwidth.

## How it works

The bound is

\[
P_{\text{attainable}} = \min\left(P_{\text{peak}},\; B \cdot I\right)
\]

where \(P_{\text{peak}}\) is the compute ceiling, \(B\) is the memory bandwidth and \(I\) is the operational intensity. A kernel with an intensity below the ridge point is limited by memory, and a kernel above it is limited by compute.

To use the chart, a kernel is measured and plotted as a point:

- A point far below the roof has a large gap that better code could close.
- Moving a point to the right needs more reuse of each byte, for example by tiling or fusing operations. Moving it up needs better use of the same hardware.

The ceilings are computed once for each machine, not once for each kernel. Every kernel on that machine is then judged against the same two lines.

## Hierarchical roofline

The original model counts only traffic to main memory, and it assumes the working set does not fit in on-chip caches. When caches do serve much of the traffic, a single memory ceiling gives a misleading bound. Yang et al. (2020) extend the model to a ceiling for each level of the memory hierarchy of NVIDIA GPUs. Each level has its own intensity, which is the operations per byte moved at that level, so a kernel can be limited by one level and not by another. They also extend the Empirical Roofline Toolkit to more numerical precisions and to Tensor Core operations, and apply the analysis to a deep learning climate segmentation application written in TensorFlow and PyTorch.

## Applying the model to LLM inference

Yuan et al. (2024) use a roofline framework to analyse the efficiency of LLM inference. Their analysis explains why LLMs are memory-bound during decoding, how much memory and computation each method needs, and how to choose hardware. The same arithmetic is set out in the [memory hierarchy](index.md) page: when a model generates one token for one sequence, each weight is read once and used for about one operation, so the intensity is roughly one, far to the left of the ridge point. Batching sequences reuses each weight across the batch and moves the point to the right.

## Results

The model has been extended to GPUs and applied to deep learning workloads. Yang et al. (2020) use the per-level charts to show how an application uses the compute and memory resources of a GPU, and how its TensorFlow and PyTorch implementations differ. Yuan et al. (2024) use the roofline framework to analyse efficient LLM inference techniques by their effect on memory access and computation.

## Limitations

- **The original bound assumes memory is the main limit.** The memory ceiling treats off-chip bandwidth as the constraining resource, so a single-level chart is weaker when caches are effective.
- **The ceilings are peak values.** Achieved bandwidth and achieved throughput are often lower than the ceilings, so the roof is an upper bound, not a prediction.
- **Latency and overlap are ignored.** The model says nothing about the time a kernel spends waiting for data, or about how much of its compute overlaps with its memory traffic.
- **Intensity depends on implementation.** Counting bytes needs the cache behaviour of the real code, which must be measured. A fused kernel can have a much higher intensity than the same operations run separately.
- **Communication between chips is outside the basic chart.** The model describes one machine, so the costs of links between chips need a separate analysis; see [interconnects](../interconnects/index.md).

## Open questions

- **Multi-chip roofline.** Whether a chart with a ceiling for inter-chip links gives useful bounds for large model training and serving is an open question for the scaling discussion.
- **Workloads that change shape.** The intensity of LLM inference depends on batch size and context length, so one point per model is not enough. How to present the whole range of these shapes on one chart is still being worked out.

## Connections

The roofline model is the analysis tool behind the bandwidth argument in the [memory hierarchy](index.md) page, and it explains why reducing bytes per value helps, as in [mixed-precision training](../co-design/mixed-precision.md) and [quantisation](../../../theory/model-compression/quantisation/index.md). A kernel that moves fewer bytes for the same operations has a higher intensity, which is the effect [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) relies on. The [inference optimisation](../../inference-optimization/index.md) chapter applies the same idea to serving.

## References

### Seminal papers

- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM 52(4), 65–76. https://doi.org/10.1145/1498765.1498785 — Introduces the chart, which bounds attainable performance by peak compute and by peak memory bandwidth times operational intensity.
- Williams, S., Waterman, A. & Patterson, D. (2008). *Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures*. Technical Report UCB/EECS-2008-134, UC Berkeley. https://www2.eecs.berkeley.edu/Pubs/TechRpts/2008/EECS-2008-134.pdf — The original technical report, which defines the ceilings and states that they are computed once for each machine.

### Surveys and textbooks

- Yang, C., Wang, Y., Farrell, S., Kurth, T. & Williams, S. (2020). *Hierarchical Roofline Performance Analysis for Deep Learning Applications*. arXiv:2009.05257. https://arxiv.org/abs/2009.05257 — Extends the model to a ceiling for each memory level of NVIDIA GPUs and applies it to a deep learning application.
- Yuan, Z., et al. (2024). *LLM Inference Unveiled: Survey and Roofline Model Insights*. arXiv:2402.16363. https://arxiv.org/abs/2402.16363 — Uses a roofline framework to survey efficient LLM inference and explain why LLMs are memory-bound.

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the primary bottleneck for AI serving, which is the regime the memory ceiling describes.
