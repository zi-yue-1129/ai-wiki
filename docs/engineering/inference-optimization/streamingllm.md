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
  - StreamingLLM
  - Attention sinks
  - 注意力匯聚
---

# StreamingLLM

!!! info "Part of KV Cache Compression and Eviction"
    This method page belongs to [KV Cache Compression and Eviction](kv-cache-compression.md). It explains StreamingLLM in detail; the parent page compares it with the other methods.

StreamingLLM lets a language model generate over a stream far longer than its training context, by keeping a few initial tokens, the attention sinks, together with a recent window, and dropping everything in between. The authors report stable language modelling on up to 4 million tokens, without fine-tuning. It is a way to keep generation stable on long streams, not a way to remember distant content.

## Problem

A model trained on sequences of a few thousand tokens fails when it is run on much longer inputs, because the attention patterns it learned do not extend. Two obvious fixes both fail. Caching every token needs memory that grows without bound. Sliding a window over the most recent tokens, and recomputing the attention from scratch each time, keeps memory small but is slow, and the output also degrades once the initial tokens leave the window.

## Core idea

The authors observe an attention sink: the first few tokens receive large attention scores whatever their content, because the softmax needs somewhere to put attention mass that is not wanted. Keeping the key and value of these initial tokens recovers most of the performance of a window attention, even though the middle of the sequence is removed. StreamingLLM therefore keeps the initial sink tokens and a recent window, and it assigns positions within the cache rather than the original positions of the tokens.

## Procedure

1. Choose a number of sink tokens, usually the first few positions of the stream.
2. Choose a recent window length.
3. Keep the keys and values of the sink tokens and the window, and drop the tokens between them.
4. Assign positions relative to the cache, so that the model sees a contiguous sequence.
5. Generate the next token, add its keys and values to the window, and evict the oldest one.

## Results

The paper reports stable language modelling on up to 4 million tokens, and it reports speed-up of up to 22.2× over the sliding-window recomputation baseline, which recomputes the cache at each step. It also shows that window attention alone loses performance once the initial tokens leave the window, and that keeping the initial tokens' keys and values largely recovers it. The paper also reports that the method works without fine-tuning on the models it tests. These results measure stability and speed on streams, not accuracy on questions about the dropped middle of the input.

## Limitations

- **No long-range recall.** Tokens outside the window and not sinks are gone, so the method cannot answer questions about them. It stabilises generation but does not extend memory.
- **Sink tokens must stay.** Removing the initial tokens breaks the stabilisation, so serving code must never evict them.
- **Speed baseline.** The large speed-up is against recomputation, which is a weak baseline for a serving system that caches normally.
- **Fixed window.** The window length sets the recall distance, and no window length covers all tasks.

## Connections

- The heavy-hitter alternative, which keeps the tokens with the most attention instead of the first ones, is [H2O](h2o.md).
- The recent window in this method is the same window used by most eviction policies, and the memory layout that frees dropped blocks is [PagedAttention and vLLM](paged-attention.md).
- The position handling interacts with rotary embeddings, which are covered in the [Transformer KV cache](../../theory/models/transformer/kv-cache/index.md) page.

## Open questions

- Can the sink tokens be chosen by content rather than by position, so that a stream with a different start still stabilises?
- When a task needs a distant fact, how should a serving system combine the sink-and-window cache with retrieval of earlier content?

## References

### Seminal papers

- Xiao, G. et al. (2024). *Efficient Streaming Language Models with Attention Sinks*. ICLR 2024. arXiv:2309.17453. https://arxiv.org/abs/2309.17453 — The primary paper: attention sinks, the window cache and results on streams of up to 4 million tokens.
- Zhang, Z. et al. (2023). *H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models*. arXiv:2306.14048. https://arxiv.org/abs/2306.14048 — The heavy-hitter policy, which keeps different tokens than the sink-and-window design.
- Liu, Z. et al. (2024). *KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache*. arXiv:2402.02750. https://arxiv.org/abs/2402.02750 — Quantisation of the cache, which keeps every token rather than dropping them.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP 2023. arXiv:2309.06180. https://arxiv.org/abs/2309.06180 — The paged cache layout that makes dropping blocks in a window practical.
- Shazeer, N. (2019). *Fast Transformer Decoding: One Write-Head is All You Need*. arXiv:1911.02150. https://arxiv.org/abs/1911.02150 — The architectural reduction of the decoding cache, which is a different route to fixed memory.
