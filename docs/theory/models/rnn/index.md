---
related:
- brain-mind/memory-learning
- theory/models/ssm
aliases:
  - Recurrent Neural Networks
  - RNN
  - LSTM
  - 循環神經網路
  - 遞迴神經網路
tags:
  - recurrent networks
  - sequence modelling
  - architecture
last_reviewed: 2026-10-28
---

# Recurrent Neural Networks

A recurrent neural network (RNN) processes a sequence one step at a time and carries a hidden state from each step to the next. The state is a learned summary of everything seen so far, so the same network can read sequences of any length with a fixed number of parameters. RNNs dominated language and speech modelling until attention-based models replaced them for most tasks. They are still used where input arrives as a stream, where memory must be very cheap, or where a model must update its state online.

## Core idea

At each step the network combines the current input with the previous hidden state to produce a new hidden state and, optionally, an output. A plain recurrent cell does this with a single nonlinear transformation. Its weakness is training: gradients through many steps tend to vanish or explode, so the network struggles to learn dependencies that span long gaps. Gated cells were designed to fix this, and they are the first component below.

## Components and variants

- [Gated cells](gated-cells/index.md): the vanilla cell, LSTM and GRU, and how their gates control memory.
- [Sequence modes](sequence-modes/index.md): bidirectional processing, encoder–decoder pairs, stacking, and how training handles long sequences.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Long short-term memory (LSTM) | 1997 | Memory cell updated by addition, with gates that control writing and reading | [LSTM](gated-cells/lstm/index.md) |
| Sequence to sequence | 2014 | An encoder LSTM and a decoder LSTM, trained end to end for translation | [Sequence to sequence](sequence-modes/sequence-to-sequence/index.md) |

The LSTM made long dependencies trainable with gated memory. The sequence-to-sequence model showed that a single recurrent encoder–decoder can translate end to end.

## Trade-offs

- **Memory and streaming.** A recurrent state has constant size, so RNNs process streams cheaply and need no key–value cache.
- **Parallelism.** Each step depends on the previous one, so training cannot be parallelised across time the way Transformers can. This is the main reason they lost ground.
- **Long dependencies.** Gating helps, but very long-range information is still hard to keep, which is why attention and state-space models were developed.

## Where it is used

Speech recognition front ends, time series forecasting, online control and sensor processing, and some on-device language tasks where memory and latency are tight.

## Connections

The [state-space](../ssm/index.md) family returns to the recurrent view with better long-range behaviour, and the [Transformer](../transformer/index.md) replaces the recurrence with attention. In neuroscience, recurrent circuits are the default model of cortical dynamics, and the gating idea has been compared with working memory mechanisms; see [memory and learning](../../../brain-mind/memory-learning/index.md).

## Open issues and further variants

- **Recurrence versus attention.** Whether linear recurrent models can match attention at scale, and when each is preferable, is still being tested.
- **Training stability.** Gradient clipping and careful initialisation are used in practice, but a complete theory of when recurrent training succeeds is missing.
- **Biological plausibility.** Backpropagation through time is hard to reconcile with known neural mechanisms, and alternatives are actively studied.

## References

### Seminal papers

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — The LSTM, with gated memory cells that address the vanishing gradient problem.
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — Shows why gradient descent struggles to learn long-range dependencies in recurrent networks.
- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. arXiv:1409.3215 — Encoder–decoder LSTMs for machine translation, trained end to end.
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — Introduces the GRU and the encoder–decoder setup for sequence-to-sequence tasks.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 10 covers recurrent and recursive networks and backpropagation through time.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". arXiv:1211.5063 — Analyses exploding and vanishing gradients and proposes gradient norm clipping.
