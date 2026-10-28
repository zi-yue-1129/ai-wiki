---
related:
- theory/models/rnn/sequence-modes
- theory/models/rnn
aliases:
  - Sequence to Sequence Learning
  - Seq2Seq
  - 序列到序列學習
tags:
  - recurrent networks
  - sequence modelling
  - machine translation
last_reviewed: 2026-10-28
---

# Sequence to Sequence Learning

Sequence to sequence learning is an encoder–decoder method in which a multilayer LSTM maps an input sequence to an output sequence of a different length. It was introduced by Sutskever, Vinyals and Le in their 2014 NeurIPS paper "Sequence to Sequence Learning with Neural Networks", and it showed that translation could be learned end to end by a neural network.

## Problem

Deep networks need inputs and targets of a fixed dimension, but translation maps sequences whose lengths are not known in advance. A method that works for machine translation therefore has to accept a source sentence of any length and produce a target sentence of any length.

## Core idea

A multilayer LSTM reads the source sentence and encodes it into one fixed-size vector. A second LSTM then generates the target sentence one word at a time, starting from that vector. The source words are fed in reverse order.

## Equation or algorithm

The model factorises the probability of the target sentence as

\[
p(y_1,\dots,y_{T'} \mid x_1,\dots,x_T) = \prod_{t} p(y_t \mid v,\, y_1,\dots,y_{t-1}),
\]

where \(v\) is the fixed vector produced by the encoder, and each factor is a softmax over the vocabulary.

## Results

On WMT'14 English-to-French (the ntst14 test set), an ensemble of five reversed LSTMs with beam size 12 reached BLEU 34.81, against 33.30 for the phrase-based SMT baseline. Reversing the source raised a single model's BLEU from 25.9 to 30.6.

## Limitations

The paper reports no degradation on sentences under 35 words and only a minor drop on the longest ones. The authors say they "do not have a complete explanation" for why reversing the source helps. Training took about ten days on an 8-GPU setup.

## Connections

The [sequence modes](../index.md) page describes the encoder–decoder pattern alongside bidirectional and stacked recurrence, and the [recurrent neural networks](../../index.md) page places it among the other recurrent models. The [LSTM](../../gated-cells/lstm/index.md) page explains the cell used in both the encoder and the decoder. The fixed-size vector is the bottleneck that attention was introduced to relieve, as discussed in [attention variants](../../../transformer/attention-variants/index.md).

## Open issues and further variants

- **Fixed-size bottleneck.** A single vector limits how much of a long input can pass to the decoder, which is the gap that attention was designed to close.
- **Reversal.** The benefit of reversing the source is observed but not explained by the authors, so the reason remains open.
- **Long inputs.** Accuracy drops only slightly on the longest sentences in the paper, but the behaviour on much longer inputs is a separate question.

## References

### Seminal papers

- Sutskever, I., Vinyals, O. & Le, Q. V. (2014). "Sequence to Sequence Learning with Neural Networks". NeurIPS. [arXiv:1409.3215](https://arxiv.org/abs/1409.3215) — Encoder–decoder LSTMs for machine translation, trained end to end.
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". [arXiv:1406.1078](https://arxiv.org/abs/1406.1078) — Introduces the GRU and the encoder–decoder setup for sequence-to-sequence tasks.
- Bahdanau, D., Cho, K. & Bengio, Y. (2014). "Neural Machine Translation by Jointly Learning to Align and Translate". [arXiv:1409.0473](https://arxiv.org/abs/1409.0473) — Adds attention so the decoder can look back over the whole input.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 10 covers bidirectional and encoder–decoder recurrent networks and truncated backpropagation through time.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Chung, J., et al. (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". [arXiv:1412.3555](https://arxiv.org/abs/1412.3555) — Compares LSTM and GRU with the plain recurrent cell on several sequence tasks.
