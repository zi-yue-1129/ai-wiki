---
related:
- theory/models/rnn/gated-cells
- theory/models/rnn
aliases:
  - Long Short-Term Memory
  - LSTM
  - 長短期記憶
tags:
  - recurrent networks
  - gating
  - long-term dependencies
last_reviewed: 2026-10-28
---

# Long Short-Term Memory

The long short-term memory (LSTM) is a recurrent cell with a gated memory that can learn dependencies across long time lags. It was introduced by Hochreiter and Schmidhuber in their 1997 paper "Long Short-Term Memory", and it became the standard recurrent cell for many years.

## Problem

Errors sent back through many time steps tend to either blow up or shrink to nothing. A plain recurrent network trained by gradient descent therefore struggles to link an event to a cause that came many steps earlier, and learning such a link can take an impractically long time or fail altogether.

## Core idea

The LSTM replaces the plain recurrent unit with a memory cell built around a self-connected linear unit, which the paper calls the "constant error carousel". Because the cell's state is updated by addition, error can flow back through it without being repeatedly multiplied. Two multiplicative gates, one on the input and one on the output, decide when information is written into the cell and when it is read out.

## Equation or algorithm

For memory cell \(c\) at time \(t\), with input gate \(y_{\text{in}}\), output gate \(y_{\text{out}}\) and the squashing functions \(g\) and \(h\), the paper gives

\[
s_c(t) = s_c(t-1) + y_{\text{in}}(t)\, g\big(\text{net}_c(t)\big), \qquad y_c(t) = y_{\text{out}}(t)\, h\big(s_c(t)\big),
\]

where both gates are logistic sigmoids. Learning uses a truncated gradient, and the paper gives its update cost as O(W) per step, where W is the number of weights.

## Results

On the embedded Reber grammar, the LSTM always learned the task, with two failures in 150 trials, and the best configuration needed 8,440 sequence presentations. On a task with a 100-step delay, the LSTM succeeded in all trials after 5,040 sequences, while RTRL and BPTT did not succeed within 5 million sequence presentations.

## Limitations

The paper says the truncated algorithm "will not easily solve" strongly delayed XOR problems. It also reports that tasks which random weight guessing solves, such as 500-step parity, are hard for the truncated LSTM when its initial weights are small.

## Connections

The [gated cells](../index.md) page compares the LSTM with the plain cell and with the GRU, and the [recurrent neural networks](../../index.md) page places it among the other recurrent models. The [sequence to sequence](../../sequence-modes/sequence-to-sequence/index.md) page uses LSTMs as encoder and decoder for translation. The [Transformer](../../../transformer/index.md) replaces recurrence with attention, and [memory and learning](../../../../../brain-mind/memory-learning/index.md) covers the comparison with working memory.

## Open issues and further variants

- **Cell design.** Greff et al. (2017) benchmark several LSTM variants and find that the vanilla design is hard to beat, so the value of extra gates or connections is still unsettled.
- **Long sequences.** Even gated cells degrade over very long sequences, which is one motivation for newer linear recurrences.
- **Truncated training.** The paper's own failure cases, such as strongly delayed XOR and 500-step parity, show that truncated gradients remain a weak point for some tasks.

## References

### Seminal papers

- Hochreiter, S. & Schmidhuber, J. (1997). "Long Short-Term Memory". *Neural Computation* 9(8). https://doi.org/10.1162/neco.1997.9.8.1735 — The LSTM, with gated memory cells that address the vanishing gradient problem.
- Bengio, Y., Simard, P. & Frasconi, P. (1994). "Learning long-term dependencies with gradient descent is difficult". *IEEE Transactions on Neural Networks* 5(2). https://doi.org/10.1109/72.279181 — Shows why gradient descent struggles to learn long-range dependencies in recurrent networks.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 10 covers recurrent and recursive networks and backpropagation through time.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Pascanu, R., Mikolov, T. & Bengio, Y. (2013). "On the difficulty of training Recurrent Neural Networks". arXiv:1211.5063 — Analyses exploding and vanishing gradients and proposes gradient norm clipping.
- Greff, K., et al. (2017). "LSTM: A Search Space Odyssey". arXiv:1503.04069 — Benchmarks several LSTM variants and finds that the vanilla design is hard to beat.
