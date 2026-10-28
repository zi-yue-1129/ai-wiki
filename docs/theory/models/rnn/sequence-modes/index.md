---
related:
- theory/models/transformer
aliases:
  - Sequence Modes
  - Bidirectional RNN
  - Encoder–Decoder
  - 序列模式
  - 雙向循環網路
tags:
  - recurrent networks
  - sequence modelling
  - training
last_reviewed: 2026-10-28
---

# Sequence Modes

The same recurrent cell can be wired in several ways to fit a task. The choices are the direction in which the sequence is read, how an input sequence is mapped to an output sequence, how cells are stacked, and how training is organised over long sequences. Each choice changes what information the network can use at each step and how expensive training is.

## Overview

| Mode | Information available at step \(t\) | Typical use |
|---|---|---|
| Unidirectional | Inputs up to \(t\) | Streaming, generation |
| Bidirectional | All inputs | Labelling a complete sequence |
| Encoder–decoder | Whole input, then generated outputs | Translation, summarisation |
| Stacked | Deeper features at each step | Higher capacity |

## Approaches

### Bidirectional recurrence

A bidirectional RNN runs one recurrent pass forward and one backward, and concatenates the two hidden states at each position. Each output can then use the full context, which suits tagging and recognition tasks where the whole recording is available. It cannot be used for streaming, because it needs future inputs.

### Encoder–decoder

An encoder reads the input sequence and compresses it into a state. A decoder then generates the output one token at a time, starting from that state and feeding back its own predictions. Sutskever et al. (2014) showed that this setup could translate with a neural network end to end. A single fixed-size state limits how much information passes between the two parts, which is what attention was introduced to relieve.

### Stacking and depth

Several recurrent layers can be stacked, with each layer's outputs as the next layer's inputs. Deeper stacks represent more abstract features, but they make the gradient path longer, so residual or gated connections between layers are often used.

### Training over long sequences

Backpropagation through time unrolls the network over the whole sequence, which costs memory linearly in its length. Truncated backpropagation through time processes long sequences in fixed-length chunks, carrying the state across chunks but limiting gradient flow to each chunk. Teacher forcing feeds the true previous output during training, which speeds learning but can create a mismatch with generation, when the model's own outputs are fed back.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Sequence to sequence | 2014 | An encoder LSTM and a decoder LSTM, trained end to end for translation | [Sequence to sequence](sequence-to-sequence/index.md) |

## Trade-offs

- **Context versus latency.** Bidirectional modes see more context but cannot stream. Unidirectional modes stream but cannot use future context.
- **Memory versus accuracy.** Truncated training saves memory and can miss dependencies longer than the chunk.
- **Teacher forcing.** It stabilises and speeds training, but generation errors can compound at inference, a problem studied under the name exposure bias.

## Connections

The encoder–decoder pattern was the setting in which attention was first added to sequence models, as discussed in [attention variants](../../transformer/attention-variants/index.md). Stacking and residual connections are shared with the [Transformer](../../transformer/index.md) family, and the streaming question returns in the [state-space](../../ssm/index.md) family.

## Open issues and further variants

- **Exposure bias.** Methods that train on the model's own outputs, such as scheduled sampling, reduce the mismatch, but they complicate training and their gains vary.
- **Long-sequence training.** Chunked training trades memory for missed long-range structure, and better schemes for choosing chunk boundaries are not settled.
- **Bidirectional generation.** Using both directions for generation, not only for labelling, is hard because the future is what the model is generating.

## References

### Seminal papers

- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215) — Encoder–decoder recurrent networks for machine translation, end to end.
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". [arXiv:1406.1078](https://arxiv.org/abs/1406.1078) — The RNN encoder–decoder with gated units for translation.
- Bahdanau, D., Cho, K. & Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate". [arXiv:1409.0473](https://arxiv.org/abs/1409.0473) — Adds attention so the decoder can look back over the whole input.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 10 covers bidirectional and encoder–decoder recurrent networks and truncated backpropagation through time.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". [arXiv:1211.5063](https://arxiv.org/abs/1211.5063) — Analyses the gradient problems that make long-sequence training hard.
