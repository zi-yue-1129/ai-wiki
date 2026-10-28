---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/kv-cache
  - engineering/inference-optimization
tags:
  - engineering
  - efficiency
  - inference
aliases:
  - Heavy-Hitter Oracle
  - H2O
---

# H2O (Heavy-Hitter Oracle)

!!! info "Part of KV Cache Compression and Eviction"
    This method page belongs to [KV Cache Compression and Eviction](kv-cache-compression.md). It explains H2O in detail; the parent page compares it with the other methods.

H2O is a KV-cache eviction policy for generative inference. It keeps a small set of "heavy-hitter" tokens, the ones that have accumulated the most attention, together with a window of recent tokens, and evicts the rest. The authors report that the cache can be shrunk substantially with little loss of accuracy, and that the resulting throughput gains are large on OPT models.

## Problem

The cache of a decoder grows by one entry per layer and head for every generated token. For a long prompt and a large batch, this cache can exceed the model weights, so fewer requests fit on one GPU. Simply dropping the oldest tokens fails, because some early tokens are important throughout generation.

## Core idea

The authors observe that attention is sparse: a small subset of tokens receives most of the attention mass across the layers. They call these tokens heavy hitters. H2O tracks the accumulated attention each token has received, keeps the heavy hitters and the most recent tokens within a fixed budget, and evicts the others. The authors frame the choice of which tokens to keep as a submodular selection problem, and they give a theoretical guarantee under mild assumptions.

## Procedure

1. Fix a cache budget per layer, for example a share of the sequence length.
2. At each decoding step, add the new token's keys and values to the cache.
3. Accumulate each cached token's attention score across the steps.
4. When the cache exceeds the budget, keep the highest-scoring tokens and the recent window, and evict the rest.
5. Continue generation with the reduced cache.

## Results

The paper evaluates OPT, LLaMA and GPT-NeoX models. For OPT-6.7B and OPT-30B, with the heavy-hitter share set to 20 percent of the cache, the abstract reports throughput up to 29× higher than DeepSpeed Zero-Inference and Hugging Face Accelerate, and up to 3× higher than FlexGen. At the same batch size, it reports latency reduced by up to 1.9×. These comparisons are against offloading inference systems, so the gains reflect the memory they avoid moving, and they should not be read as a gain over a fully resident dense cache.

## Limitations

- **Early tokens that matter later.** A token that receives little attention while it is in the window can be evicted, and then a later question that needs it cannot be answered.
- **Accumulated scores are approximate.** Scores are summed across steps, which favours tokens that were present for a long time, and this bias can misjudge newer content.
- **Attention is computed under eviction.** The scores come from the reduced cache, so the policy can drift from what the full model would have attended to.
- **Baseline choice.** The largest reported gains use offloading baselines, which are slow by design.

## Connections

- The attention sinks that a recent window must keep are described in [StreamingLLM](streamingllm.md), which keeps the first tokens rather than the heavy hitters.
- Quantising the cache instead of evicting from it is the approach of [KIVI](kivi.md).
- The memory layout that allows evicted blocks to be reused is [PagedAttention and vLLM](paged-attention.md).

## Open questions

- Can the heavy-hitter choice use the query of the next question, rather than attention accumulated before the question is known?
- How should the budget be set per layer, when attention is concentrated in different layers for different tasks?

## References

### Seminal papers

- Zhang, Z. et al. (2023). *H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models*. arXiv:2306.14048. https://arxiv.org/abs/2306.14048 — The primary paper: heavy-hitter eviction with a recent window, with throughput results on OPT models.
- Xiao, G. et al. (2024). *Efficient Streaming Language Models with Attention Sinks*. ICLR 2024. arXiv:2309.17453. https://arxiv.org/abs/2309.17453 — The contrasting policy that keeps attention sinks rather than the heavy hitters.
- Liu, Z. et al. (2024). *KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache*. arXiv:2402.02750. https://arxiv.org/abs/2402.02750 — Quantisation of the same cache, as an alternative to eviction.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The paged memory layout in which evicted blocks are freed for reuse.
- Ainslie, J. et al. (2023). *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*. EMNLP 2023. arXiv:2305.13245. https://arxiv.org/abs/2305.13245 — The trained-in cache reduction that H2O's post-hoc approach is compared against.
