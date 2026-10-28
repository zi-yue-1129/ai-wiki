---
related:
- theory/models/rnn/gated-cells
- theory/models/rnn
aliases:
  - Gated Recurrent Unit
  - GRU
  - 門控循環單元
tags:
  - recurrent networks
  - gating
  - long-term dependencies
last_reviewed: 2026-10-28
---

# Gated Recurrent Unit

The gated recurrent unit (GRU) is a recurrent cell with two gates and no separate memory state. It was introduced by Cho et al. in their 2014 paper "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation", and it offers most of the long-range benefit of the LSTM with fewer parameters.

## Problem

A plain recurrent cell, trained by backpropagation through time, has gradients that vanish or explode over many steps, so it struggles to link inputs to outputs that lie far apart. The LSTM solved this with a separate additive memory and three gates, but that design is larger. The GRU asks whether a smaller gated cell can keep the same gradient benefit.

## Core idea

The GRU merges the memory and the hidden state into one vector. It uses two gates:

- An **update gate** decides how much of the old state to keep and how much to replace with a new candidate. Because the new state is a weighted average of the old state and the candidate, the unit acts as an adaptive leaky integrator.
- A **reset gate** decides how much of the old state is used when the candidate is computed. When the reset gate is close to zero, the candidate ignores the previous state, so the unit can forget its past and start afresh.

The paper calls the cell a hidden unit "that adaptively remembers and forgets". Having no separate output gate, the GRU exposes its whole state at every step.

## Equation or algorithm

The paper defines the cell in its Section 2.3 with Eqs. 5 to 8. The equations below are the paper's, written for one unit \(j\) at time \(t\), with \(\sigma\) the logistic sigmoid and \(\varphi\) the candidate activation:

\[
r_j = \sigma\big([W_r x]_j + [U_r h_{t-1}]_j\big) \qquad \text{(reset gate)}
\]

\[
z_j = \sigma\big([W_z x]_j + [U_z h_{t-1}]_j\big) \qquad \text{(update gate)}
\]

\[
\tilde{h}_j = \varphi\big([W x]_j + [U(r \odot h_{t-1})]_j\big) \qquad \text{(candidate state)}
\]

\[
h_j^{\langle t \rangle} = z_j\, h_j^{\langle t-1 \rangle} + (1 - z_j)\, \tilde{h}_j^{\langle t \rangle} \qquad \text{(new state)}
\]

The paper writes these per component and omits bias terms. Its experiments section names \(\tanh\) as the candidate activation. In vector form, which is the standard notation for the same cell, with \(\odot\) the element-wise product:

\[
r_t = \sigma(W_r x_t + U_r h_{t-1}), \quad z_t = \sigma(W_z x_t + U_z h_{t-1}),
\]
\[
\tilde{h}_t = \tanh\big(W x_t + U (r_t \odot h_{t-1})\big), \quad h_t = z_t \odot h_{t-1} + (1 - z_t) \odot \tilde{h}_t.
\]

Some later texts and libraries swap the roles of \(z\) and \(1 - z\) in the last line. Check the convention before comparing code or equations across sources.

## Results

The paper reports BLEU scores for a statistical machine translation system in which an RNN encoder-decoder rescores phrase pairs. Table 1 of the paper gives the following scores, reproduced from the checked text:

| Model | BLEU dev | BLEU test |
|---|---|---|
| Baseline | 30.64 | 33.30 |
| RNN | 31.20 | 33.87 |
| CSLM + RNN | 31.48 | 34.64 |
| CSLM + RNN + WP | 31.50 | 34.54 |

These scores describe the whole translation system. The checked text does not give a separate score for the gated unit alone.

Chung et al. (2014) later compared the GRU with the LSTM and the plain cell on several sequence tasks. As summarised on the [gated cells](../index.md) page, both gated cells clearly outperformed the plain cell, and neither of the two gated cells was consistently better than the other.

## Limitations

The paper reports that an ungated unit did not work in its preliminary experiments: "We were not able to get meaningful result with an oft-used tanh unit without any gating." The gating is therefore part of what made the cell trainable in those runs.

The paper also states a limit of its method: "we only consider rescoring the phrase pairs in the phrase table." Using the model to replace the phrase table would require expensive repeated sampling. This limit concerns the translation setup rather than the GRU cell itself.

## Connections

The GRU is the two-gate member of the [gated cells](../index.md) family, next to the [LSTM](../lstm/index.md), which keeps a separate cell state and an output gate. The [recurrent neural networks](../../index.md) page places both among the recurrent models. The paper's encoder-decoder setup is the same pattern used by [sequence to sequence](../../sequence-modes/sequence-to-sequence/index.md) models. The [Transformer](../../../transformer/index.md) replaces recurrence with attention, and the [state-space models](../../../ssm/index.md) return to recurrence with different long-range machinery. The comparison with working memory is covered in [memory and learning](../../../../../brain-mind/memory-learning/index.md).

## Open issues and further variants

- **Merged state.** It is not settled whether removing the separate memory costs capacity on tasks that need long, independent storage, as the LSTM's cell state provides.
- **Gate roles.** Which of the two gates matters more for accuracy, and whether the reset gate is needed at all on different tasks, varies across studies and is not fully resolved.
- **Ungated baselines.** The paper's finding that a tanh unit without gating failed comes from preliminary experiments, and how far it holds across tasks and scales has not been fully tested.

## References

### Seminal papers

- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". [arXiv:1406.1078](https://arxiv.org/abs/1406.1078) — Introduces the GRU and the encoder–decoder setup for sequence-to-sequence tasks.
- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — The LSTM, with gated memory cells that address the vanishing gradient problem.
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — Shows why gradient descent struggles to learn long-range dependencies in recurrent networks.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Chung, J., et al. (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". [arXiv:1412.3555](https://arxiv.org/abs/1412.3555) — Compares LSTM and GRU with the plain recurrent cell on several sequence tasks.
- Greff, K., et al. (2017). "LSTM: A Search Space Odyssey". [arXiv:1503.04069](https://arxiv.org/abs/1503.04069) — Benchmarks several LSTM variants and finds that the vanilla design is hard to beat.
- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". [arXiv:1211.5063](https://arxiv.org/abs/1211.5063) — Analyses exploding and vanishing gradients and proposes gradient norm clipping.
