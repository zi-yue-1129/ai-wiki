---
related:
- theory/models/llm
aliases:
  - Attention Variants
  - Efficient Attention
  - 注意力變體
  - 高效注意力
tags:
  - attention
  - efficient inference
  - long context
last_reviewed: 2026-10-28
---

# Attention Variants

Standard scaled dot-product attention costs \(O(n^2)\) time and memory in the sequence length \(n\). During training this limits context length. During generation it also makes each new token read a large [key–value cache](../kv-cache/index.md). Most attention variants target one of three costs: the number of key–value heads that must be stored, the number of query–key pairs that are computed, or the memory traffic needed to compute the exact result. This page covers the variants that change the attention computation itself; the choice of positional encoding is covered in [Positional encodings](../positional-encodings/index.md).

## Overview

| Family | What is reduced | Examples | Cost after change |
|---|---|---|---|
| Shared heads | Size of the key–value cache | MQA, GQA | Same compute, less memory |
| Sparse or local patterns | Number of query–key pairs | Sparse Transformer, Longformer, sliding window | About \(O(n\sqrt{n})\) or \(O(nw)\) |
| Linear attention | Use of the softmax | Linear Transformers, Performers | \(O(n)\), approximate |
| IO-aware exact attention | Memory traffic | FlashAttention | Same result, less memory and time |

## Approaches

### Shared key and value heads

In multi-head attention each head has its own keys and values. Multi-query attention (MQA) keeps one shared set of keys and values for all query heads, which shrinks the key–value cache by the number of heads. Grouped-query attention (GQA) shares keys and values within groups of query heads, so it sits between full multi-head and multi-query attention. GQA can be obtained by converting an existing multi-head checkpoint with a short extra training run, which is why many open models use it.

### Sparse and local patterns

Instead of attending to all earlier tokens, sparse attention restricts each query to a fixed pattern. The Sparse Transformer uses strided and fixed patterns that reach far back while keeping cost near \(O(n\sqrt{n})\). Longformer combines a sliding window with a few global tokens, which gives linear cost in \(n\). Sliding-window attention with a fixed window is used in Mistral 7B, where information still spreads through the layers because each layer passes information forward by one window. Local patterns are fast but cannot retrieve arbitrary distant tokens unless other mechanisms exist.

### Linear attention

Linear attention replaces the softmax with a kernel feature map \(\phi\), so that the product can be reordered as \(\phi(Q)\,(\phi(K)^\top V)\). The expression \(\phi(K)^\top V\) can be accumulated as a running state, which turns attention into a recurrent update with constant cost per token. Katharopoulos et al. (2020) showed this equivalence and its autoregressive form. Performers approximate the softmax kernel with random features (FAVOR+), so that the approximation can be made as accurate as needed by using more features.

### IO-aware exact attention

FlashAttention computes exactly the same result as standard attention, but it tiles the computation so that blocks of queries, keys and values stay in fast on-chip memory. It avoids writing the full \(n \times n\) score matrix to slow memory and recomputes parts of the forward pass in the backward pass. The result is lower memory use and much higher speed. FlashAttention-2 improved the parallelism and the partitioning of work across GPU threads.

## Trade-offs

- **Exact versus approximate.** Shared heads and FlashAttention keep the exact attention computation. Sparse, linear and random-feature methods change what is computed, and their quality depends on the task.
- **Retrieval.** Methods that compress or restrict context can lose a specific distant token. Tasks that require retrieving one fact from a long input expose this loss most clearly.
- **Hardware.** Speed depends on kernels and memory layout. A variant that saves operations may not save time on a particular accelerator.
- **Training and inference.** A variant can be used in both, or only at inference after conversion, which changes the cost of experimentation.

## Connections

These variants are the main tools behind long-context [large language models](../../llm/index.md). The cache that shared heads and latent attention reduce is discussed in [KV cache management](../kv-cache/index.md). The alternatives to attention altogether, such as state-space models, are covered on the [Transformers & Attention](../index.md) overview.

## Open issues and further variants

- **Recall gap.** Linear and state-space models are efficient but often weaker than attention at recalling exact details from long inputs. Hybrids that mix a few full-attention layers with efficient layers are one response, and the best mix is not settled.
- **Learned sparsity.** Most sparse patterns are fixed by hand. Learning which tokens to attend to, for example with routing or top-k selection, is promising but harder to train.
- **Head configuration.** The number of key–value groups in GQA is usually chosen by trial. A principled way to set it for a target quality and memory budget is missing.
- **Kernel design.** Feature maps for linear attention are mostly hand-designed. Their approximation error for the softmax is well understood only for simple cases.
- **Long-context evaluation.** Benchmarks that test whether an attention variant keeps information across very long inputs are still inconsistent.

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. arXiv:1706.03762 — Introduces scaled dot-product and multi-head attention, the baseline for all variants here.
- Shazeer, N. (2019). "Fast Transformer Decoding: One Write-Head is All You Need". arXiv:1911.02150 — Multi-query attention, with one shared key–value head for all queries.
- Ainslie, J., et al. (2023). "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints". arXiv:2305.13245 — Grouped-query attention, converted from multi-head checkpoints.
- Child, R., et al. (2019). "Generating Long Sequences with Sparse Transformers". arXiv:1904.10509 — Factorised sparse attention patterns with near-\(O(n\sqrt{n})\) cost.
- Beltagy, I., Peters, M. E. & Cohan, A. (2020). "Longformer: The Long-Document Transformer". arXiv:2004.05150 — Sliding-window attention with global tokens for long documents.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Katharopoulos, A., et al. (2020). "Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention". ICML 2020. arXiv:2006.16236 — Linear attention with a recurrent form for fast autoregressive decoding.
- Choromanski, K., et al. (2020). "Rethinking Attention with Performers". arXiv:2009.14794 — Random-feature approximation of softmax attention (FAVOR+).
- Dao, T., et al. (2022). "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness". arXiv:2205.14135 — Tiled, IO-aware exact attention.
- Dao, T. (2023). "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning". arXiv:2307.08691 — Improved parallelism and work partitioning of FlashAttention.
- Jiang, A. Q., et al. (2023). "Mistral 7B". arXiv:2310.06825 — Uses sliding-window attention in a widely used open model.
