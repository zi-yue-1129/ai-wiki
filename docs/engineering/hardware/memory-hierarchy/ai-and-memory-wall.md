---
related:
  - engineering/hardware/co-design
  - theory/model-compression/quantisation
  - theory/models/transformer
tags:
  - hardware
  - memory bandwidth
  - scaling
last_reviewed: 2026-11-01
aliases:
  - AI and Memory Wall
  - Memory wall
  - 記憶體牆
---

# AI and the Memory Wall (Gholami et al., 2024)

Gholami and colleagues (2024) argue that the main performance bottleneck of large AI models is shifting from compute to memory bandwidth. Over the past twenty years, peak server FLOPS have grown much faster than DRAM and interconnect bandwidth, so that moving data, rather than doing arithmetic, now limits how fast models can be trained and served (Gholami et al., 2024).

## Overview

The paper begins with the scaling trends that drive model size. Neural scaling laws and the availability of large unsupervised datasets have increased the compute and memory that LLMs need for both training and serving. The authors' point is that the hardware trend is uneven: compute has grown much faster than the bandwidth that feeds it, and this gap is the memory wall (Gholami et al., 2024).

## Key concepts

- **Peak FLOPS**: the maximum arithmetic throughput of a processor, in floating-point operations per second.
- **Memory bandwidth**: the rate at which data can move between memory and the processor, measured in bytes per second.
- **Arithmetic intensity**: the number of floating-point operations performed per byte loaded from memory. The paper defines it as FLOPs divided by memory operations (Section II-A).
- **Memory bound**: a workload whose speed is set by bandwidth rather than by arithmetic, which happens when its arithmetic intensity is low.

## The scaling gap

The abstract reports that over the past 20 years peak server hardware FLOPS has been scaling at 3.0 times every two years, while DRAM and interconnect bandwidth have scaled at 1.6 and 1.4 times every two years (Gholami et al., 2024). The rates are linear regression fits to the data, as stated in the paper's footnote 3 (Figure 1). Over the same 20 years, the paper gives an overall increase of about 60,000 times for peak FLOPS, against about 100 times for DRAM bandwidth and about 30 times for interconnect bandwidth.

Because compute outpaces bandwidth, a processor can perform more operations than memory can supply. A design that wants to use its full compute must therefore reduce the bytes it moves per operation.

## Why decoding is memory-bound

The paper argues that autoregressive decoding is the clearest case of a memory-bound workload. Generating each token multiplies a large weight matrix by a single activation vector, so each weight is loaded for very few operations. The authors attribute the low arithmetic intensity of this matrix-vector work to autoregressive inference, and they report that GPT-2 has orders of magnitude smaller arithmetic intensity in their profiling (Section II-B, Figure 3). The result is that the memory wall can become the main bottleneck for decoder models at low batch sizes, rather than compute (Section II-B).

The profiling assumes 8-bit precision and a batch size of 1. The authors note that the conclusion may not hold for every decoder application, for example for long input prompts or large batches (footnotes 5 and 6).

## Proposed responses

The paper's Section III discusses several responses, and it argues that the architecture itself must be rethought, since many large Transformers are scaled versions of nearly the same base design:

- **Efficient training.** Second-order methods, the ZeRO framework, rematerialisation that stores only a subset of activations, and low-precision training (Section III-A).
- **Efficient deployment.** Quantisation, which the paper says is relatively easy to bring down to INT4 with minimal accuracy impact, pruning, and smaller language models (Section III-B).
- **Accelerator design.** Trading peak compute for better compute-to-bandwidth ratios, more efficient caching, and higher-capacity DRAM, possibly in a hierarchy with different bandwidths (Section III-C).

## Connections

- The [roofline model](roofline.md) gives the standard way to decide whether a kernel is limited by compute or by bandwidth, which is the test the memory wall argument depends on.
- [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) is a concrete response: it reduces the memory traffic of exact attention rather than its arithmetic.
- [Quantisation](../../../theory/model-compression/quantisation/quantisation-survey.md) reduces the bytes per value, and [hardware co-design](../co-design/index.md) changes the model and the hardware together.
- [Scaling laws](../../../theory/models/llm/scaling-laws/kaplan-scaling-laws.md) explain why model size and therefore memory demand keep rising.

## Applications

The argument applies to serving large language models, where the weights are read for every generated token, and to training very large models, where communication between chips becomes a bottleneck. The paper's conclusion is that intra- and inter-chip memory transfer will soon become the main limiting factor in serving large AI models (Section IV).

## Open questions

- How far bandwidth can grow relative to compute, and whether memory technology can change the trend the paper fits.
- Whether architectures can be designed to raise arithmetic intensity without losing accuracy.

## References

### Seminal papers

- Gholami, A., Yao, Z., Kim, S. et al. (2024). *AI and Memory Wall*. arXiv. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is becoming the main bottleneck for large models, with the scaling rates discussed on this page.
- Dao, T. et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv. https://arxiv.org/abs/2205.14135 — Reduces the memory traffic of exact attention by tiling computation in fast memory.
- Kaplan, J. et al. (2020). *Scaling Laws for Neural Language Models*. arXiv. https://arxiv.org/abs/2001.08361 — The scaling laws that drive the growth in model size and memory demand.
- Frantar, E. et al. (2022). *GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers*. arXiv. https://arxiv.org/abs/2210.17323 — Low-bit weight quantisation that reduces the bytes read during decoding.

### Surveys

- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline*. Communications of the ACM, 52(4), 65–76. https://doi.org/10.1145/1498765.1498785 — The roofline model, which relates arithmetic intensity to attainable performance.
