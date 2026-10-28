---
status: draft
last_reviewed: 2026-10-28
related:
- engineering/hardware
- engineering/inference-optimization
- theory/models/transformer
tags:
- AI hardware
- memory
- memory wall
- roofline
- LLM inference
aliases:
  - Memory hierarchy
  - Memory bandwidth
  - Roofline model
  - 記憶體階層
---

# Memory Hierarchy and Bandwidth

On an AI accelerator, speed is usually limited less by how fast the arithmetic units run than by how fast data can reach them. Memory is organised as a hierarchy of small, fast storage close to the arithmetic units and large, slow storage far from them. The arithmetic intensity of a computation, and the roofline model built on it, say whether a workload is limited by memory or by compute. LLM decoding is a clear case of a memory-bound workload. This page is a subchapter of [AI Hardware](../index.md) and sits alongside the [AI accelerators](../accelerators/index.md) comparison.

## Problem

A modern accelerator can perform far more multiply-accumulate operations per second than it can load operands for. Every operand fetched from a distant level costs time and energy, so achieved throughput is often set by memory traffic rather than by the peak FLOP rating of the chip.

## Core idea

Keep data close to where it is used, and reuse it as many times as possible before it is evicted. Each level of the hierarchy trades capacity for speed:

| Level | Location | Capacity | Speed |
|---|---|---|---|
| Registers | Inside each processing unit | Very small | Fastest |
| On-chip SRAM | Caches, shared memory and scratchpads on the chip | Small | Very fast |
| Off-chip high-bandwidth memory (HBM) or DRAM | Packages beside the chip | Large | Much slower than on-chip SRAM |
| Host memory and storage | Across a host or network link | Very large | Far slower |

Software decides how much of the work stays in the fast levels. Tiling a matrix multiplication so that each tile is reused in SRAM is the classic example.

## Equation or algorithm

The arithmetic intensity of a kernel is the number of floating-point operations divided by the number of bytes it moves to or from off-chip memory:

\[
I = \frac{\text{FLOPs}}{\text{bytes moved}}
\]

The roofline model (Williams et al., 2009) bounds the attainable performance \(P\) by the peak compute \(P_{\text{peak}}\) and the memory bandwidth \(B\):

\[
P = \min\left(P_{\text{peak}},\; B \cdot I\right)
\]

The two terms meet at the ridge point \(I^* = P_{\text{peak}} / B\). A kernel with \(I < I^*\) is memory-bound, and a kernel with \(I > I^*\) is compute-bound.

Decoding shows why this matters for LLMs. For a dense model with \(N\) parameters stored in two bytes each, generating one token for one sequence performs about \(2N\) FLOPs and reads about \(2N\) bytes of weights, so \(I \approx 1\). That is far below the ridge point of any accelerator that has a large arithmetic unit, so the step is limited by how fast the weights can be read. Serving \(b\) sequences in one batch reads each weight once for all of them, which raises the intensity to roughly \(b\). The KV cache adds further reads that grow with context length, so long contexts push decoding further toward the memory limit.

## Results

Ivanov et al. argue that data movement, not arithmetic, is the key bottleneck when training transformers. Their data-movement optimisation gives a 1.30× speedup on a BERT encoder layer compared with the frameworks they tested. Gholami et al. argue that memory bandwidth, not compute, is the primary bottleneck for AI serving. Dao et al. show that restructuring attention so that it reads and writes high-bandwidth memory less often speeds it up, while computing exactly the same result; see the [FlashAttention](../../../theory/models/transformer/attention-variants/flash-attention/index.md) page. Pope et al. build an analytical model of inference efficiency and use it to choose partitioning strategies suited to TPU v4 slices.

## Limitations

The roofline model is a simplified picture. It ignores latency, the overlap between compute and memory, cache hit rates and communication between chips. Arithmetic intensity depends on the implementation as well as the algorithm: a fused kernel can have much higher intensity than the same operations run one at a time. Peak bandwidth and peak FLOPs are rarely reached in practice, so measured numbers are lower than either bound.

## Open questions

- **The memory wall.** Gholami et al. argue that memory bandwidth has grown more slowly than compute, so the gap widens over time. Whether new memory technology closes it is an open question.
- **Model-side fixes.** Storing weights in fewer bits reduces the bytes read per token and so raises intensity; see [quantisation](../../../theory/model-compression/quantisation/index.md).
- **Software-side fixes.** [PagedAttention](../../inference-optimization/paged-attention.md) manages KV cache memory so that less of it is wasted, and [speculative decoding](../../inference-optimization/speculative-decoding.md) spreads each weight read over several tokens.
- **Related:** the [KV cache](../../../theory/models/transformer/kv-cache/index.md) explains why reads grow with context length.

## Connections

Off-chip memory is the boundary between a single chip and the rest of the system. Moving data between chips and hosts is a further, slower level, which the scaling discussion depends on. The [TPU](../accelerators/tpu/index.md) and the [AI accelerators](../accelerators/index.md) overview show how different designs place their memory.

## References

### Seminal papers

- Ivanov, A., et al. (2020). *Data Movement Is All You Need: A Case Study on Optimizing Transformers*. arXiv:2007.00072. https://arxiv.org/abs/2007.00072 — Argues that data movement is the key bottleneck when training transformers, and reports a data-movement optimisation with a 1.30× speedup on a BERT encoder layer.
- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — Computes exact attention with fewer reads and writes to high-bandwidth memory, which makes it faster.
- Williams, S., Waterman, A. & Patterson, D. (2009). *Roofline: An Insightful Visual Performance Model for Multicore Architectures*. Communications of the ACM 52(4). https://doi.org/10.1145/1498765.1498785 — Introduces the roofline model, which bounds attainable performance by peak compute and memory bandwidth.

### Surveys and textbooks

- Sze, V., Chen, Y.-H., Yang, T.-J., Emer, J. S. (2017). *Efficient Processing of Deep Neural Networks: A Tutorial and Survey*. arXiv:1703.09039. https://arxiv.org/abs/1703.09039 — Surveys dataflows that reuse data in local storage to reduce the energy cost of data movement.

### Articles and documentation

- Gholami, A., et al. (2024). *AI and Memory Wall*. arXiv:2403.14123. https://arxiv.org/abs/2403.14123 — Argues that memory bandwidth, not compute, is the primary bottleneck for AI serving.
- Pope, R., et al. (2022). *Efficiently Scaling Transformer Inference*. arXiv:2211.05102. https://arxiv.org/abs/2211.05102 — Builds an analytical model of inference efficiency and uses it to choose partitioning strategies for TPU v4 slices.
