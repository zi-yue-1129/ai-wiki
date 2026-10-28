---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/kv-cache
  - engineering/inference-optimization
  - engineering/on-device-edge
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - KIVI
  - 2-bit KV cache quantisation
---

# KIVI

!!! info "Part of KV Cache Compression and Eviction"
    This method page belongs to [KV Cache Compression and Eviction](kv-cache-compression.md). It explains KIVI in detail; the parent page compares it with the other methods.

KIVI is a tuning-free method that quantises the KV cache to 2 bits. It keeps every token, but stores each one in far fewer bits, and it quantises keys and values along different axes because their statistics differ. The authors report that it reduces peak memory, including the model weights, by 2.6 times, and allows a batch size up to 4 times larger, which gives 2.35 to 3.47 times the throughput on a real LLM inference workload.

## Problem

Eviction reduces the cache by dropping tokens, which can remove content that a later token needs. Quantising every token avoids that loss, but a naive 2-bit quantisation of the cache destroys accuracy. The reason is that keys and values have different distributions: some key channels contain large outliers, while values vary more smoothly from token to token. A single scheme for both does not fit either.

## Core idea

The authors analyse the keys and values and find that keys have outliers concentrated in certain channels, while values do not. KIVI therefore quantises keys per channel, so that each channel uses its own scale and the outliers do not spread to the rest. It quantises values per token. The scheme is asymmetric, with a zero point per group, and needs no tuning, so it can be applied to an existing model directly.

## Procedure

1. Keep a small residual of the most recent tokens in full precision, because they are read most often.
2. Quantise the keys per channel to 2 bits, with a scale and zero point for each group.
3. Quantise the values per token to 2 bits, with a scale and zero point for each token.
4. Store the quantised cache, and dequantise each block inside the attention kernel when it is read.
5. Run attention over the dequantised values, and write new tokens to the residual.

## Results

The abstract reports that KIVI, applied to the tested models, uses 2.6 times less peak memory including weights, enables up to 4 times larger batch size, and brings 2.35 to 3.47 times throughput on real LLM inference workloads. The paper reports that the accuracy loss is small on the benchmarks it uses. The memory and throughput figures depend on the hardware, the batch size and the baseline, so they should be read with the paper's setup.

## Limitations

- **Quantisation overhead.** Dequantising inside attention adds work, so the throughput gain depends on the kernel and on whether the workload is memory-bound.
- **Group size.** The accuracy depends on the group size and on how outliers are distributed, which varies across models.
- **Long-context quality.** Small average losses can grow on long-context retrieval tasks, so long-context evaluation is needed before use.
- **Not a retrieval method.** Quantisation keeps every token, but it does not change what the model can attend to, and the cache still grows with length.

## Connections

- The alternative that drops tokens rather than reducing their precision is [H2O](h2o.md).
- Attention sinks, which should always be kept at full precision if a window method is combined with quantisation, are discussed in [StreamingLLM](streamingllm.md).
- Quantisation of weights, which is a different use of the same bit-width ideas, is covered for edge devices in [on-device and edge AI](../on-device-edge/index.md).

## Open questions

- Can the key outlier channels be predicted before quantisation, so that the scale is set once per model rather than per group?
- Should the full-precision residual size be chosen per request, based on the length and the task?

## References

### Seminal papers

- Liu, Z. et al. (2024). *KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache*. arXiv:2402.02750. https://arxiv.org/abs/2402.02750 — The primary paper: 2-bit KV-cache quantisation with per-channel keys and per-token values, and no tuning.
- Zhang, Z. et al. (2023). *H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models*. arXiv:2306.14048. https://arxiv.org/abs/2306.14048 — The eviction alternative, which trades dropped tokens for a smaller cache.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The paged cache layout in which quantised blocks are stored and read.
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — The architectural reduction of the cache, which needs training and is compared with post-hoc quantisation.
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need*. arXiv:1911.02150. https://arxiv.org/abs/1911.02150 — The earliest shared-head cache reduction, for comparison with quantising an existing cache.
