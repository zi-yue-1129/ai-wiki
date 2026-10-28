---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Additive attention
  - Bahdanau attention
  - 加性注意力
---

# Neural machine translation with learned alignment (Bahdanau et al., 2015)

The paper proposes an encoder–decoder translation model in which the decoder searches the source sentence with learned soft alignment weights at every output word. It replaces the single fixed-length vector that earlier models used with a weighted average over all source positions. The scoring mechanism is now usually called additive attention.

## Problem

In the basic encoder–decoder, the encoder compresses the whole source sentence into one fixed-length vector, and the decoder must generate the translation from that vector alone. The authors argue that this fixed-length vector is a bottleneck. Their experiments show that the basic model's performance deteriorates rapidly as the sentence length grows.

## Core idea

The model has three parts:

1. A **bidirectional recurrent encoder** reads the source sentence in both directions. Each position's annotation $h_j$ concatenates its forward and backward states, so it summarises the words around position $j$.
2. An **alignment model** $a$, a small feed-forward network trained jointly with the rest of the system, scores how well the decoder's previous state matches each annotation.
3. The **decoder** builds a context vector for each output word as a weighted average of all annotations, then predicts the word from its own state and that context.

The weights are normalised with a softmax, so they sum to one. The paper reports that the learned soft alignments are linguistically plausible, including the reordering needed between English and French.

## Equations

$$
e_{ij} = a(s_{i-1}, h_j), \qquad
\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k=1}^{T_x} \exp(e_{ik})}, \qquad
c_i = \sum_{j=1}^{T_x} \alpha_{ij} h_j
$$

$$
s_i = f(s_{i-1}, y_{i-1}, c_i), \qquad
p(y_i \mid y_{<i}, x) = g(y_{i-1}, s_i, c_i)
$$

Here $s_i$ is the decoder state, $y_i$ the output word and $T_x$ the source length. The recurrent unit $f$ is the gated hidden unit the paper uses. Because the alignment model is a differentiable feed-forward network, the whole system is trained end to end by gradient descent.

## Results

The experiments use the WMT '14 English-to-French corpus, evaluated on the news-test-2014 set. Table 1 reports BLEU on all test sentences and on the subset with no unknown words.

| Model | All sentences | No unknown words |
|---|---|---|
| RNNencdec-30 | 13.93 | 24.19 |
| RNNsearch-30 | 21.50 | 31.44 |
| RNNencdec-50 | 17.82 | 26.71 |
| RNNsearch-50 | 26.75 | 34.16 |
| RNNsearch-50, trained longer | 28.45 | 36.15 |
| Moses (phrase-based) | 33.30 | 35.63 |

The suffix gives the training sentence limit, 30 or 50 words. RNNsearch-30 already beats the fixed-vector model trained on 50-word sentences, and the attention model holds up better as test sentences grow longer. On the subset without unknown words, the longest-trained attention model passes the phrase-based baseline. On the full set, the baseline is still higher.

## Limitations

- The encoder and decoder remain recurrent, so training still runs through the sentence in order.
- Each output word scores every source position, so the cost per output word grows with source length.
- The full-set scores are held back by unknown words. The paper reports the no-unknown subset separately for this reason.

## Key methods

A brief comparison with the attention design that followed:

- [Attention Is All You Need](../attention-is-all-you-need/index.md): removes the recurrence altogether and uses scaled dot-product attention, so all positions attend in parallel.
- [Attention variants](../attention-variants/index.md): later changes to the attention operator, which this page does not cover in detail.

## Connections

- Parent topic: [Transformers & Attention](../index.md)
- Cognitive science: the learned alignment selects the relevant parts of the input for each output, which resembles selective attention. The paper makes no claim about neural mechanisms.

## Applications

- Neural machine translation, in the sequence-to-sequence systems that followed this paper.
- Inspecting alignments: the soft alignment weights form a word-to-word matrix that can be read against the sentence pair.

## Open questions

- Whether the learned weights faithfully explain a model's output, or only correlate with it.
- How the cost of attention should scale for very long inputs.

## References

### Seminal papers

- Bahdanau, D., Cho, K. & Bengio, Y. (2015). Neural Machine Translation by Jointly Learning to Align and Translate. ICLR. https://arxiv.org/abs/1409.0473 — The original paper: a bidirectional encoder with a learned soft alignment for translation.
- Vaswani, A., et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, which replaces recurrence with multi-head self-attention.
- Luong, M.-T., Pham, H. & Manning, C. D. (2015). *Effective Approaches to Attention-based Neural Machine Translation*. EMNLP. https://arxiv.org/abs/1508.04025 — Compares global and local attention for neural machine translation, with several scoring functions.

### Surveys and textbooks

- Tay, Y., et al. (2020). *Efficient Transformers: A Survey*. arXiv. https://arxiv.org/abs/2009.06732 — Surveys the many attempts to reduce the quadratic cost of attention, with a taxonomy of approaches.

### Articles and documentation

- Rush, A. M. (2018). *The Annotated Transformer*. Proceedings of Workshop for NLP Open Source Software (NLP-OSS). https://doi.org/10.18653/v1/w18-2509 — Paper-by-paper PyTorch implementation with commentary alongside the original text.

## Further learning

- Karpathy, A. (2023). *Let's build GPT: from scratch, in code, spelled out*. YouTube. https://www.youtube.com/watch?v=kCc8FmEb1nY — Live coding of a small GPT from an empty file, explaining each part of the Transformer as it is written.
