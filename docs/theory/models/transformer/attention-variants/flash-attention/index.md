---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/transformer
- theory/models/transformer/attention-variants
- theory/models/transformer/kv-cache
- engineering/hardware/memory-hierarchy
- engineering/hardware/co-design
tags:
- attention
- FlashAttention
- IO-aware
- exact attention
- GPU kernels
- long context
aliases:
  - FlashAttention
  - FlashAttention-2
  - FlashAttention-3
  - IO-aware attention
  - 快速注意力
---

# FlashAttention

FlashAttention computes exact scaled dot-product attention with far less traffic to high-bandwidth memory. It does not approximate the attention matrix. It tiles the computation so that blocks of queries, keys and values stay in fast on-chip memory, and it never writes the full \(n \times n\) score matrix to slow memory. Dao et al. (2022) introduced it, and later versions improved its parallelism and its use of newer GPUs. It is the standard example of an [IO-aware](../index.md) exact attention variant, listed beside the other families on the [attention variants](../index.md) overview.

## Problem

Standard attention computes the score matrix \(S = QK^\top / \sqrt{d}\), applies a softmax to each row, and multiplies by \(V\). The matrix has \(n^2\) entries for a sequence of length \(n\). On a GPU, writing it to and reading it from high-bandwidth memory costs more time than the arithmetic, so attention is limited by memory traffic rather than by FLOPs, as the [memory hierarchy](../../../../../engineering/hardware/memory-hierarchy/index.md) page explains.

## Core idea

Split \(Q\), \(K\) and \(V\) into blocks that fit in on-chip SRAM. For each block of queries, stream over the blocks of keys and values, compute the partial scores, and update the output as each block arrives. The softmax is computed incrementally, so the full row of scores never exists in memory at once. In the backward pass, the method recomputes the scores that it did not store, which trades a little extra arithmetic for much less memory traffic.

## Equation or algorithm

For one query row, let the running maximum be \(m\) and the running normaliser be \(\ell\). When a new block of scores \(s\) arrives, the update is

\[
m' = \max(m, \max(s)), \qquad
\ell' = e^{m - m'}\,\ell + \sum e^{s - m'}
\]

and the partial output is rescaled by the same factor \(e^{m - m'}\) before the new block's contribution is added. The final output equals the standard softmax attention exactly, because the rescaling keeps every term relative to the final maximum. The incremental form of the softmax follows the running-normaliser technique described by Milakov and Gimelshein (2018).

The memory needed for the attention output and the statistics is \(O(n)\) rather than \(O(n^2)\), while the arithmetic remains \(O(n^2 d)\).

## Results

Dao et al. (2022) report that the method is faster than standard exact attention and uses less memory, with the same output. FlashAttention-2 (Dao, 2023) reports about twice the speed of the original, and reaches roughly 50 to 73 percent of the A100's theoretical peak FLOPs per second. FlashAttention-3 (Shah et al., 2024) reports attention that runs 1.5 to 2 times faster on H100 GPUs, at about 740 TFLOPs per second in FP16 and nearly 1.2 PFLOPs per second in FP8.

## Limitations

The method is exact, so its time complexity remains \(O(n^2)\). Rabe and Staats (2021) show that exact attention can be computed in \(O(\log n)\) memory, but that bound still needs quadratic time, so long sequences remain costly. The kernels are written for specific GPU architectures, and each generation requires new work. Gains also depend on the sequence length, head dimension and batch size, so benchmark numbers from one configuration do not transfer directly to another.

## Open issues and related variants

- **Long-context cost.** Exact attention stays quadratic in time. Whether sparse or linear variants keep quality as the sequence grows is task dependent; see the [attention variants](../index.md) overview.
- **Low precision.** FlashAttention-3 uses FP8 on recent hardware. How much accuracy the lower precision costs across tasks is an open question, and it links to the [co-design](../../../../../engineering/hardware/co-design/index.md) trade-offs.
- **Decoding.** During generation, each step reads the whole [KV cache](../../kv-cache/index.md) rather than computing a large score matrix, so FlashAttention helps prefill more than single-token decoding.
- **Related:** the [KV cache](../../kv-cache/index.md) and shared-head designs address a different cost, the memory of keys and values, rather than the traffic of the score matrix.

## Connections

FlashAttention is a software answer to the memory-bound behaviour analysed in the [memory hierarchy](../../../../../engineering/hardware/memory-hierarchy/index.md) page. It shows how a kernel can change the bytes term of the roofline without changing the model, which is the same logic as the [co-design](../../../../../engineering/hardware/co-design/index.md) page.

## References

### Seminal papers

- Dao, T., et al. (2022). *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*. arXiv:2205.14135. https://arxiv.org/abs/2205.14135 — Tiled, IO-aware exact attention that avoids writing the score matrix to high-bandwidth memory.
- Dao, T. (2023). *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*. arXiv:2307.08691. https://arxiv.org/abs/2307.08691 — Reports about twice the speed of the original, through better parallelism across GPU threads.
- Shah, J., et al. (2024). *FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision*. arXiv:2407.08608. https://arxiv.org/abs/2407.08608 — Reports 1.5 to 2 times faster attention on H100 GPUs, including FP8 kernels.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Rabe, M. N., Staats, C. (2021). *Self-attention Does Not Need O(n²) Memory*. arXiv:2112.05682. https://arxiv.org/abs/2112.05682 — Shows that exact self-attention can be computed in logarithmic memory, while its time remains quadratic.
- Milakov, M., Gimelshein, N. (2018). *Online normalizer calculation for softmax*. arXiv:1805.02867. https://arxiv.org/abs/1805.02867 — Computes softmax with fewer memory accesses by updating a running maximum and normaliser.
