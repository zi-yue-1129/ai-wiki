---
status: draft
last_reviewed: 2026-10-28
tags:
  - attention
  - transformer
  - sequence modelling
aliases:
  - Transformer paper
  - Transformer 原始論文
---

# Attention Is All You Need (Vaswani et al., 2017)

The paper introduces the Transformer, a sequence model built only from multi-head scaled dot-product attention. It removes recurrence and convolution, so every position can be computed in parallel and any two positions are connected in a fixed number of steps.

## Problem

Recurrent sequence models such as LSTM and GRU encoder–decoders read a sentence one token at a time. Within one example, the computation cannot be parallelised across positions, and information from distant tokens must pass through many steps. The paper's Table 1 makes this concrete: a recurrent layer needs $O(n)$ sequential operations for a sequence of length $n$, whereas a self-attention layer needs $O(1)$ and connects any two positions in $O(1)$ steps.

## Core idea

The model computes attention from queries $Q$, keys $K$ and values $V$. Each query is compared with every key, and the softmax weights form a mixture of the values. The paper runs $h = 8$ attention functions in parallel, each on its own learned projections of the inputs, and concatenates the results. This is multi-head attention.

Attention alone ignores order, so the embeddings receive a positional encoding. The paper uses sinusoids of different wavelengths. The authors also tried learned positional embeddings and report nearly identical results.

## Equation or algorithm

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V
$$

The scaling factor $1/\sqrt{d_k}$ is there because, for large $d_k$, the dot products grow in magnitude and push the softmax into regions with very small gradients. The paper's stated reason for the scaling is this, and it reports that additive attention outperforms unscaled dot-product attention for large $d_k$.

The encoder is a stack of $N = 6$ identical layers. Each layer has a multi-head self-attention sub-layer and a position-wise feed-forward network, with residual connections and layer normalisation around each. The decoder also has $N = 6$ layers. It adds an encoder–decoder attention sub-layer and masks future positions in its self-attention, so the prediction at position $t$ depends only on earlier outputs. The model width is $d_{\text{model}} = 512$, the feed-forward inner width is $d_{ff} = 2048$, and each head uses $d_k = d_v = 64$.

## Results

- WMT 2014 English-to-German: 28.4 BLEU for the big model, more than 2.0 BLEU above the best previously reported results, including ensembles.
- WMT 2014 English-to-French: 41.8 BLEU for a single model, after 3.5 days of training on eight P100 GPUs (big model).
- The base model trained for 100,000 steps, about 12 hours on eight P100 GPUs.

The paper also reports that the model transfers to English constituency parsing.

## Limitations

- Self-attention costs $O(n^2 \cdot d)$ per layer (Table 1), so compute and memory grow quadratically with sequence length. The paper leaves restricted attention, which looks only at a neighbourhood of each position, to future work.
- The experiments cover translation and parsing. The original model is an encoder–decoder. The decoder-only form used by most later language models is an adaptation, shown for example in the GPT-2 report.
- Order is injected through a fixed encoding that the paper chose. Later models changed this design.

## Key methods

A brief comparison of the attention designs this paper sits between:

- [Additive attention (Bahdanau)](../bahdanau-attention/index.md): scores each source position with a small feed-forward network, inside a recurrent encoder–decoder. The Transformer removes the recurrence and uses dot-product scores.
- [Attention variants](../attention-variants/index.md): later changes to the attention operator itself, which alter its cost or its structure.

## Connections

- Parent topic: [Transformers & Attention](../index.md)
- Cognitive science: the word "attention" borrows from the selection of some information over other information in perception and memory. The Transformer operation is a learned weighting over representations. It is not a model of attention in the brain, and the paper makes no biological claim.

## Applications

- Machine translation, the paper's own task, followed by language modelling, where decoder-only Transformers became the standard architecture.
- Vision: see [Vision Transformer](../vision-transformer/index.md).

## Open questions

- How to keep the modelling power of full attention while reducing its quadratic cost for long inputs.
- What the attention weights reveal about a model's computation, and where that reading breaks down. The Elhage et al. framework in References treats the residual stream as the object of study.

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, replacing recurrence with multi-head self-attention.
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — Adds learned attention to sequence-to-sequence translation, the idea the Transformer later generalised.
- Luong, M.-T., Pham, H. & Manning, C. D. (2015). *Effective Approaches to Attention-based Neural Machine Translation*. EMNLP. https://arxiv.org/abs/1508.04025 — Compares global and local attention for neural machine translation, with several scoring functions.
- Radford, A., et al. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI technical report. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf — The GPT-2 report, which describes the decoder-only Transformer language model that later models adopted.
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — Treats the residual stream as the shared space that attention heads and MLP layers read from and write to, the basis of mechanistic interpretability work.

### Surveys and textbooks

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — Surveys the many attempts to reduce the quadratic cost of attention, with a taxonomy of approaches.

### Articles and documentation

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — Paper-by-paper PyTorch implementation with commentary alongside the original text.

## Further learning

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — Live coding of a small GPT from an empty file, explaining each part of the Transformer as it is written.
