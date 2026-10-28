---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - initialisation
  - signal propagation
  - hyperparameters
aliases:
  - 權重初始化
  - 訊號傳播
  - 參數初始化
  - Weight initialisation
---

# Weight initialisation and signal propagation

The starting values of a network's weights decide whether signals and gradients survive the trip through many layers. If activations grow or shrink exponentially with depth, training stalls or diverges before it begins. Initialisation schemes choose the variance of the weights so that signals keep a stable scale, and the analysis of signal propagation explains why some architectures are easier to start than others.

## Overview

A network computes its output by repeated linear maps and nonlinearities. At initialisation, the weights are random, so the size of the activations after each layer is a product of random factors. Choosing the variance well keeps that product near one. Residual connections and normalisation layers change the picture, and they make many initialisations work that would otherwise fail.

## Key concepts

- **Variance preservation**: a design goal in which the variance of activations and gradients stays roughly constant across layers.
- **Fan-in and fan-out**: the number of inputs and outputs of a layer, which set the variance of a well-scaled weight matrix.
- **Edge of chaos**: the regime at the boundary between ordered and chaotic signal propagation, where deep networks are most trainable.
- **Hyperparameter transfer**: reusing hyperparameters tuned on a small model for a larger one.

## How it works

For a linear layer with random weights of variance $\sigma^2$, the variance of the output scales with $n\sigma^2$, where $n$ is the fan-in. Glorot and Bengio chose a variance that balances the forward signal and the backward gradient, using the average of fan-in and fan-out [(Glorot and Bengio, 2010)](https://proceedings.mlr.press/v9/glorot10a.html). For rectified linear units, half the inputs are zeroed, so the variance must be doubled. He and colleagues derived an initialisation for this case, which made very deep rectifier networks trainable [(He et al., 2015)](https://arxiv.org/abs/1502.01852).

Saxe and colleagues studied the learning dynamics of deep linear networks and found exact solutions for the time course of learning under certain initial conditions [(Saxe, McClelland and Ganguli, 2013)](https://arxiv.org/abs/1312.6120). Schoenholz and colleagues used mean-field theory to study how signals propagate in random networks, and identified the depth scale over which correlations between inputs are lost, which is the basis of the edge-of-chaos view [(Schoenholz et al., 2016)](https://arxiv.org/abs/1611.01232).

## Key methods

- [Glorot (Xavier) initialisation](glorot-initialisation.md): variance chosen to balance forward and backward signals.
- [He initialisation](he-initialisation.md): variance adjusted for rectified activations.
- [Maximal update parametrisation (muP)](mup.md): a parametrisation under which the optimal hyperparameters stay stable as width grows.

## Residual connections and normalisation

A residual connection adds the input of a block to its output, so the identity path carries the signal through many layers. Normalisation keeps the scale of activations stable within each block. Together they make the choice of initialisation less critical, and they are part of why very deep networks train at all. The interaction is covered in [Normalisation](../normalisation/index.md).

## Scaling and hyperparameter transfer

As models grow wider, the best learning rate often changes, which makes large-scale tuning expensive. muP is a parametrisation under which the optimal hyperparameters for a narrow model are reported to remain close to optimal for a wide one. This allows tuning on a small model and transferring to a large one [(Yang et al., 2022)](https://arxiv.org/abs/2203.03466).

## Connections

The gradients that initialisation must keep stable are computed as in [Automatic differentiation](../../math/automatic-differentiation/index.md). The Transformer-specific placement of normalisation is in [Transformers](../../models/transformer/index.md), and the neural-network basics are in [Deep learning](../index.md).

## Applications

Starting any deep network, including very deep convolutional and residual networks, and choosing learning rates for large language models through transfer methods.

## Open questions

- Is the edge of chaos the right target for initialisation in architectures with attention and gating?
- How far do scaling rules such as muP extend to new architectures and optimisers?

## References

### Seminal papers

- Glorot and Bengio, *Understanding the difficulty of training deep feedforward neural networks*, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (2010). https://proceedings.mlr.press/v9/glorot10a.html — The variance rule that balances forward and backward signals.
- He, Zhang, Ren and Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (2015). https://arxiv.org/abs/1502.01852 — Derives an initialisation for rectifier networks.
- Saxe, McClelland and Ganguli, *Exact solutions to the nonlinear dynamics of learning in deep linear neural networks* (2013). https://arxiv.org/abs/1312.6120 — Exact learning dynamics for deep linear networks.
- Schoenholz, Gilmer, Ganguli and Sohl-Dickstein, *Deep Information Propagation* (2016). https://arxiv.org/abs/1611.01232 — Mean-field analysis of signal propagation in random deep networks.
- Yang et al., *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer* (2022). https://arxiv.org/abs/2203.03466 — The muP parametrisation and zero-shot hyperparameter transfer.
