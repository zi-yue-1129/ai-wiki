---
status: draft
last_reviewed: 2026-10-28
tags:
  - deep learning
  - neuroscience
aliases:
  - 反向傳播
  - 誤差反向傳播
  - backpropagation
  - 連結主義
  - connectionism
  - 隱藏層
---

# Backpropagation and the Connectionist Revival (1986)

Backpropagation is a method for training multi-layer networks by sending the output error back through the network, so that every weight, including those of hidden units, is adjusted in proportion to its share of the error. Rumelhart, Hinton and Williams brought it to a wide audience in 1986, and it made the connectionist programme of the late 1980s practical.

## Overview

The perceptron could learn only a single layer of weights. Minsky and Papert's 1969 analysis showed that a single layer cannot compute exclusive-or (see the [perceptron](../../symbolic-era/perceptron/index.md) page). The missing piece was a way to train hidden units, whose correct values the training data do not give.

Backpropagation answers this with the chain rule. It computes how the error changes with each weight, passing an error signal backward from the output layer, and changes each weight a small step against that gradient. The 1986 *Nature* paper stated the method for neuron-like units and showed that hidden units come to represent features of the task. It contrasted this with the perceptron-convergence procedure, which could not create such features (Rumelhart et al., 1986). The idea had been derived in other settings before then.

## Key concepts

- **Hidden layer**: units between the inputs and the outputs. Their activity is not specified by the training data, so the learning rule must determine what they represent.
- **Gradient descent**: changing each weight a small amount in the direction that reduces the error. See [gradient descent](../../../../theory/math/calculus/gradient-descent/index.md).
- **Sigmoid unit**: a smooth threshold unit whose output is differentiable, which is what makes gradient-based training possible.
- **Connectionism**: the research programme that uses networks of such units to model perception, memory and language.

## How it works

Take sigmoid units $y = \sigma(z)$ with $z_j = \sum_i w_{ji}\, y_i$, and squared error $E = \tfrac{1}{2}\sum_k (y_k - t_k)^2$ over output units $k$ with targets $t_k$. For the output layer, the error signal is

$$
\delta_k = (y_k - t_k)\, y_k (1 - y_k),
$$

and for each hidden unit $j$ it is passed back through the weights,

$$
\delta_j = y_j (1 - y_j) \sum_k \delta_k\, w_{kj}.
$$

Each weight then changes by $\Delta w_{ji} = -\eta\, \delta_j\, y_i$, where $\eta$ is the learning rate. The procedure runs a forward pass to compute outputs, a backward pass to compute the $\delta$ values, and an update step. It is reverse-mode differentiation applied to a layered network (see [reverse-mode automatic differentiation](../../../../theory/math/automatic-differentiation/reverse-mode/index.md)). The notation is modern; the 1986 paper states the procedure in its own terms.

## Results

The 1986 paper's evidence is demonstrational. On small tasks, hidden units develop internal representations, but no benchmark is measured. Later work tested the method on practical problems. LeCun and colleagues (1989) built task constraints into a network's architecture and applied it to handwritten zip-code digits, reporting that such constraints greatly improve generalisation. Hinton (1989) surveys the learning procedures of the period, including backpropagation.

## Limitations

- **Cost.** Training needs many passes over the data. With the computers and datasets of the 1980s, the method suited only small problems.
- **Long sequences.** Error signals decay as they pass back through many steps. Hochreiter and Schmidhuber (1997) describe the resulting "insufficient, decaying error backflow", which makes it slow to learn across long intervals. Their [LSTM](../../../../theory/models/rnn/gated-cells/lstm/index.md) was designed to address it.
- **No guarantee of the best solution.** Gradient descent on a non-convex error surface can settle in a poor local minimum.
- **Biological plausibility.** Backpropagation needs error signals that travel backwards along connections that carry activity forwards. Whether the brain learns by anything similar is still debated.

## Connections

Backpropagation links the connectionist programme to neuroscience. Its units are simplified neurons, and its hidden layers are often compared with intermediate representations in sensory cortex. The [NeuroAI](../../../../brain-mind/neuroai/index.md) pages follow this line.

The method also sits beside the statistical turn. Both learned parameters from data, but backpropagation fits a network to an error measure, while the statistical methods estimate probability models of language (see [statistical language processing](../statistical-nlp/index.md)). Later sequence models, from the LSTM to the [transformer](../../../../theory/models/transformer/index.md), were trained with variants of the same gradient method.

## Open questions

- Does the brain learn by anything like backpropagation? Several biologically motivated rules have been proposed, and how far they match it on hard tasks is still being tested.
- Why did networks that used the same basic method fail to scale until data and computation grew by orders of magnitude? Sejnowski (2018) offers a neuroscientist's history of this period.

## References

### Seminal papers

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*. https://doi.org/10.1038/323533a0 — Shows how error can be propagated backwards to adjust hidden units, so that a network learns its own internal features.
- LeCun, Y. et al. (1989). Backpropagation applied to handwritten zip code recognition. *Neural Computation*. https://doi.org/10.1162/neco.1989.1.4.541 — Applies a backpropagation network with task-specific constraints to handwritten zip-code digits and shows that the constraints improve generalisation.
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Identifies the decaying error signal in recurrent backpropagation and introduces the LSTM architecture to address it.

### Surveys and textbooks

- Sejnowski, T. J. (2018). *The Deep Learning Revolution*. MIT Press. https://doi.org/10.7551/mitpress/11474.001.0001 — A history of neural networks and deep learning from a neuroscientist's viewpoint, covering the period in which backpropagation was revived.

### Articles and documentation

- Hinton, G. E. (1989). Connectionist learning procedures. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(89)90049-0 — Surveys the learning procedures developed for connectionist networks, including backpropagation.
