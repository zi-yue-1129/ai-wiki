---
status: draft
last_reviewed: 2026-10-28
---

# Neural machine translation with learned alignment (Bahdanau et al., 2015)

The decoder searches the source sentence with learned soft alignment weights, instead of relying on one fixed-length vector.

## Problem

Encoder–decoder translation compresses a whole source sentence into one fixed-length vector, which loses information in long sentences.

## Core idea

At each output step, the decoder searches the source sentence with a soft alignment, a weighted average of the encoder's states. The weights are learned from how well each source position matches the current decoder state.

## Results

The paper reports that the attention model keeps translation quality on long sentences better than the fixed-vector baseline.

## Limitations

The encoder and decoder are still recurrent, so training remains sequential. The alignment costs time proportional to the source length for each output word.

## Connections

- Parent topic: [Transformers & Attention](../index.md)
- Other method on this topic: [Attention Is All You Need](../attention-is-all-you-need/index.md)

## References

### Seminal papers

- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, replacing recurrence with multi-head self-attention.
- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — Adds learned attention to sequence-to-sequence translation, the idea the Transformer later generalised.
- Elhage, N., et al. (2021). *A Mathematical Framework for Transformer Circuits*. Anthropic. https://transformer-circuits.pub/2021/framework/index.html — Treats the Transformer as a set of linear paths between residual-stream reads and writes, the basis of mechanistic interpretability work.

### Surveys and textbooks

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — Surveys the many attempts to reduce the quadratic cost of attention, with a taxonomy of approaches.

### Lectures and videos

- Luong, M.-T., Pham, H. & Manning, C. D. (2015). *Effective Approaches to Attention-based Neural Machine Translation*. EMNLP. arXiv:1508.04025. https://arxiv.org/abs/1508.04025 — Compares global and local attention mechanisms for neural machine translation, with several scoring functions.

### Articles and documentation

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — Paper-by-paper PyTorch implementation with commentary alongside the original text.

## Further learning

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — Live coding of a small GPT from an empty file, explaining each part of the Transformer as it is written.
