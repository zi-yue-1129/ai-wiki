---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
tags:
  - muP
  - hyperparameter transfer
  - scaling
aliases:
  - 最大更新參數化
  - muP
  - Maximal update parametrisation
---

# Maximal update parametrisation (muP)

Maximal update parametrisation, usually written muP, is a way of scaling the initialisation and learning rates of a network with its width so that the optimal hyperparameters stay roughly the same as the model grows. Hyperparameters tuned on a narrow model can then be reused for a wide one, which saves most of the cost of tuning very large models.

## Overview

The [chapter](index.md) describes initialisation as a question of signal scale. muP asks a related question: how should the scale of weights, updates and learning rates depend on width, so that the training dynamics stay comparable across sizes?

## Problem

When a network is widened in the standard parametrisation, the best learning rate typically changes with width. Tuning a large model by search is expensive, and a learning rate found on a small model may not transfer. The question is whether there is a parametrisation under which the optimum is stable.

## Core idea

Yang and colleagues study the infinite-width limit and identify a parametrisation in which the size of the updates to hidden activations stays of order one as width grows. In that parametrisation, the learning rate and initialisation scale are set according to the layer's width, and the optimal hyperparameters for a small network are reported to remain close to optimal for a large one. They call this zero-shot hyperparameter transfer [(Yang et al., 2022)](https://arxiv.org/abs/2203.03466).

## Equation

The standard scaling multiplies each hidden layer's weights by $1/\sqrt{n}$, where $n$ is the width. In muP, the output layer and the learning rates are scaled with width so that the feature updates have a width-independent size. The rules differ by layer type and by optimiser. The paper gives the initialisation, multiplier and learning-rate rules for SGD and Adam in its tables. This page does not restate them, so check the paper before using them.

## Results

The abstract reports that hyperparameters tuned on a small model can be used on a much larger one without tuning the large model, and that this is verified on Transformer and ResNet models. Specific numbers are in the paper's results.

## Limitations

- The theory is developed for the infinite-width limit, and its guarantees are approximate at finite width.
- The exact rules depend on the architecture and optimiser, so each setting needs its own derivation.
- Transfer across depth is a separate question from transfer across width.

## Connections

muP is a scaling rule for the same initial variance argument as [Glorot initialisation](glorot-initialisation.md) and [He initialisation](he-initialisation.md). Normalisation layers change the width dependence, which the paper's setting does not fully include; see [Normalisation](../normalisation/index.md).

## Applications

Tuning large language models and other very wide networks, where a full hyperparameter search is too costly.

## Open questions

- How far does transfer extend across depth, batch size and architecture?
- How does muP interact with normalisation and with optimisers other than Adam?

## References

### Seminal papers

- Yang et al., *Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer* (2022). https://arxiv.org/abs/2203.03466 — Introduces muP and zero-shot hyperparameter transfer.
- Glorot and Bengio, *Understanding the difficulty of training deep feedforward neural networks*, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (2010). https://proceedings.mlr.press/v9/glorot10a.html — The fan-based variance rule that muP generalises to training dynamics.
- He, Zhang, Ren and Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (2015). https://arxiv.org/abs/1502.01852 — The rectifier initialisation that scaling rules must respect.
- Schoenholz, Gilmer, Ganguli and Sohl-Dickstein, *Deep Information Propagation* (2016). https://arxiv.org/abs/1611.01232 — Mean-field analysis of signal propagation with depth.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — The Transformer architecture in which muP is most often applied.
