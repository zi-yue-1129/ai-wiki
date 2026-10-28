---
status: draft
last_reviewed: 2026-10-28
---

# Attention Is All You Need (Vaswani et al., 2017)

Replaces recurrence and convolution with multi-head scaled dot-product attention, so each position attends to all others in parallel.

## Problem

Recurrent sequence models process tokens one after another. That limits parallel training and makes long-range dependencies hard to learn.

## Core idea

Remove recurrence and convolution entirely. Each position attends to all others through multi-head scaled dot-product attention, and positional information is added to the embeddings.

## Equation or algorithm

The encoder and the decoder each stack layers of multi-head attention and a feed-forward network. The decoder masks future positions, so each output depends only on earlier outputs.

## Results

28.4 BLEU on WMT 2014 English-to-German, more than 2 BLEU above the previous best results, including ensembles. A single model reached 41.8 BLEU on English-to-French. Training took 3.5 days on eight GPUs.

## Limitations

The cost of attention grows with the square of the sequence length (see Efficiency above). The original model is an encoder–decoder for translation, not the decoder-only form that most language models use today.

## Connections

- Parent topic: [Transformers & Attention](../index.md)
- Other method on this topic: [Additive Attention (Bahdanau)](../bahdanau-attention/index.md)

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, replacing recurrence with multi-head self-attention.
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — Adds learned attention to sequence-to-sequence translation, the idea the Transformer later generalised.
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — Treats the Transformer as a set of linear paths between residual-stream reads and writes, the basis of mechanistic interpretability work.

### Surveys and textbooks

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — Surveys the many attempts to reduce the quadratic cost of attention, with a taxonomy of approaches.

### Lectures and videos

- Radford, A., Wu, J., Child, R., Luan, D., Amodei, D. & Sutskever, I. (2019). *Language Models are Unsupervised Multitask Learners*. OpenAI technical report. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf — The GPT-2 technical report, describing the decoder-only Transformer language model that the video builds.

### Articles and documentation

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — Paper-by-paper PyTorch implementation with commentary alongside the original text.

## Further learning

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — Live coding of a small GPT from an empty file, explaining each part of the Transformer as it is written.
