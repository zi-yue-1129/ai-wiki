---
related:
- theory/deep-learning
aliases:
  - Multilayer Perceptron
  - MLP
  - Feedforward Network
  - 多層感知器
  - 前饋網路
tags:
  - feedforward networks
  - architecture
  - deep learning
last_reviewed: 2026-10-28
---

# Multilayer Perceptrons

A multilayer perceptron (MLP), also called a feedforward network, stacks layers of affine maps, each followed by a nonlinearity, from input to output with no loops. It is the simplest deep architecture, and it is a universal approximator of continuous functions on compact sets when wide enough. Other families are built from MLP pieces: the feedforward blocks inside Transformers, the readout heads of CNNs and RNNs, and the mixing layers of many newer models. Understanding the MLP is therefore part of understanding every other family.

## Core idea

A layer computes \(h = \sigma(Wx + b)\), where \(\sigma\) is a nonlinear activation. Stacking such layers builds a composition of simple functions, trained end to end by backpropagation. The general training theory, such as optimisation and generalisation, is covered in [Deep Learning](../../deep-learning/index.md). This page covers the design choices that define the architecture itself.

## Components and variants

- **Activation functions.** The sigmoid and tanh saturate, so most modern networks use rectified or smooth variants. The GELU, for example, multiplies the input by a Gaussian cumulative distribution and is common in Transformers (Hendrycks & Gimpel, 2016).
- **Normalisation.** Batch normalisation normalises over the batch, which suits CNNs, and layer normalisation normalises over features, which suits sequence models because it does not depend on batch statistics (Ba et al., 2016).
- **Residual connections.** Adding the input back to a block's output makes deep stacks trainable, a design introduced for CNNs and now used across families (He et al., 2015).
- **Width and depth.** A wide shallow MLP and a narrow deep one can represent similar functions, but deeper networks often do so with far fewer parameters.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| Gaussian error linear units (GELU) | 2016 | A smooth activation that weights each input by the Gaussian CDF | [GELU](gelu/index.md) |
| Layer normalisation | 2016 | Normalises each example over its features, not over the batch | [Layer normalisation](layer-normalisation/index.md) |

GELU is a smooth alternative to ReLU. Layer normalisation does not depend on batch statistics, which suits sequence models.

## Trade-offs

- **Generality versus structure.** An MLP makes no assumption about the input's structure, so it needs more data than a CNN or a graph network for structured inputs.
- **Parameter cost.** Dense layers grow quadratically with width, which is why the feedforward block in large models is often replaced with sparse or expert-based designs.
- **Interpretability.** Dense networks are hard to inspect directly, which motivates the interpretability work linked from the [Transformer](../transformer/index.md) family.

## Where it is used

Tabular prediction, the feedforward blocks of Transformers, encoders for embeddings, and the output heads of most other architectures.

## Connections

MLP blocks appear inside the [CNN](../cnn/index.md), [RNN](../rnn/index.md) and [Transformer](../transformer/index.md) families. The residual and normalisation choices made for MLPs are shared with the [backbones and scaling](../cnn/backbones-and-scaling/index.md) page. The early link to the brain comes from the McCulloch–Pitts neuron and the perceptron, which are the historical ancestors of this family.

## Open issues and further variants

- **Feedforward blocks in large models.** Whether dense feedforward layers are the best use of parameters at scale, or whether mixture-of-experts or structured layers do better, is being tested.
- **Activation choice.** Empirical gains from new activations are often small and inconsistent across tasks, and the reasons are not fully understood.
- **Expressivity versus learnability.** Universal approximation says what can be represented, not what can be learned from data, and this gap is the central open question for the family.

## References

### Seminal papers

- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors". *Nature* 323: 533–536. https://doi.org/10.1038/323533a0 — Popularised backpropagation for training multilayer networks with hidden units.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — Residual connections that make deep networks trainable.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". [arXiv:1607.06450](https://arxiv.org/abs/1607.06450) — Normalises over features rather than over the batch.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 6 covers feedforward networks, activations and the universal approximation results.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". [arXiv:1606.08415](https://arxiv.org/abs/1606.08415) — The GELU activation, used in many Transformer models.
