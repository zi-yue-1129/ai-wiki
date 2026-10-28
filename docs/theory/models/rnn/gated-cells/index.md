---
related:
- brain-mind/memory-learning
aliases:
  - Gated Recurrent Units
  - LSTM Variants
  - GRU
  - 門控循環單元
  - 長短期記憶網路
tags:
  - recurrent networks
  - gating
  - long-term dependencies
last_reviewed: 2026-10-28
---

# Gated Cells

A gated recurrent cell decides, at each step, how much of the old memory to keep and how much new information to write. The gates are learned sigmoid functions of the input and the previous state, and they let the cell carry information over many steps without the gradient vanishing as quickly as in a plain recurrent network. Three cells dominate: the plain cell, the long short-term memory (LSTM) cell, and the gated recurrent unit (GRU). Their differences are about how many gates they use and whether they keep a separate memory from the output.

## Overview

| Cell | Gates | Separate cell state | Parameters per unit |
|---|---|---|---|
| Plain (Elman) | None | No | Fewest |
| LSTM | Input, forget, output | Yes | About four times the plain cell |
| GRU | Update, reset | No | About three times the plain cell |

## Approaches

### Plain recurrent cell

The plain cell computes the new state as a nonlinear function of the input and the old state. It is simple and cheap, but its gradients through time are products of many Jacobians, which vanish or explode. This is the failure that Bengio et al. (1994) analysed and that motivated gating.

### Long short-term memory

The LSTM keeps a separate cell state that is updated additively. A forget gate scales the old cell state, an input gate scales the candidate update, and an output gate decides what part of the cell is exposed as the hidden state. Because the cell state is updated by addition, gradients can pass through many steps without shrinking. Hochreiter and Schmidhuber (1997) introduced this design, and it became the standard recurrent cell for many years.

### Gated recurrent unit

The GRU merges the cell and hidden states and uses two gates: an update gate that interpolates between the old and new state, and a reset gate that controls how much of the old state enters the candidate. It has fewer parameters than an LSTM. Cho et al. (2014) introduced it, and Chung et al. (2014) compared it with the LSTM across several sequence tasks, finding that both gated cells clearly outperformed the plain cell and neither was consistently better.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Long short-term memory (LSTM) | 1997 | Memory cell updated by addition, with gates that control writing and reading | [LSTM](lstm/index.md) |
| Gated recurrent unit (GRU) | 2014 | A two-gate cell with no separate memory, cheaper than the LSTM | [GRU](gru/index.md) |

## Trade-offs

- **Capacity versus cost.** The LSTM has more parameters and can keep more information separate, while the GRU is cheaper and often trains faster on smaller data.
- **Forget bias.** Initialising the forget gate to keep information, a common practice, speeds early training, but the effect on final accuracy depends on the task.
- **Interpretability.** Gate activations can be inspected, which helps analysis but does not by itself explain the learned computation.

## Connections

Gating is the recurrent ancestor of the learned, multiplicative control used in other families, including the selective updates of [state-space models](../../ssm/selective-state-spaces/index.md). In neuroscience, gated memory has been compared with the control of working memory by prefrontal circuits; see [memory and learning](../../../../brain-mind/memory-learning/index.md).

## Open issues and further variants

- **Why gating works.** The gates solve the gradient problem, but the full account of what the learned gates compute on real tasks is incomplete.
- **Hybrids with attention.** Gated cells combined with attention or convolution are common, and the best combinations are not settled.
- **Long-context limits.** Even gated cells degrade over very long sequences, which motivates the newer linear recurrences.

## References

### Seminal papers

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — The LSTM cell with additive cell-state updates and multiplicative gates.
- Cho, K., et al. (2014). "Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation". arXiv:1406.1078 — Introduces the GRU, a cell with two gates and no separate memory.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Chung, J., et al. (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". arXiv:1412.3555 — Compares LSTM and GRU with the plain recurrent cell on several sequence tasks.
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — Analyses why gradients fail over long spans in plain recurrent networks.
- Greff, K., et al. (2017). "LSTM: A Search Space Odyssey". arXiv:1503.04069 — Benchmarks several LSTM variants and finds that the vanilla design is hard to beat.
