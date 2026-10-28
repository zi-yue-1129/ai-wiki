---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/initialisation
tags:
  - Glorot initialisation
  - Xavier initialisation
  - initialisation
aliases:
  - Glorot 初始化
  - Xavier 初始化
  - Glorot initialization
---

# Glorot (Xavier) initialisation

Glorot initialisation chooses the variance of a linear layer's weights from the fan-in and fan-out, so that the signal in the forward pass and the gradient in the backward pass keep similar scales. It was proposed for networks with saturating activations such as the sigmoid and the hyperbolic tangent, and it became a default for many layers.

## Overview

The [chapter](index.md) covers initialisation in general. This page covers the Glorot rule. The paper analysed why deep networks trained poorly with standard random initialisations, and it proposed a scale that keeps activations and gradients in a useful range.

## Problem

With weights drawn from a fixed distribution, the activations in deep networks with saturating nonlinearities drift towards the flat regions of the activation function, where gradients vanish. The paper asked how the variance of the weights should depend on the layer's size to avoid this.

## Core idea

Choose the weight variance so that the forward variance is preserved, which needs a variance involving the fan-in $n_{\text{in}}$, and the backward variance is preserved, which needs one involving the fan-out $n_{\text{out}}$. Glorot and Bengio use the average of the two. The weights are drawn uniformly or from a normal distribution with that variance.

## Equation

For a layer with $n_{\text{in}}$ inputs and $n_{\text{out}}$ outputs, the uniform form draws

$$W \sim \mathcal{U}\left[-\sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}},\; \sqrt{\frac{6}{n_{\text{in}} + n_{\text{out}}}}\right]$$

which has variance $2 / (n_{\text{in}} + n_{\text{out}})$. The normal form uses the same variance.

## Results

The paper shows that the proposed scheme trains deep networks with sigmoid and tanh activations more reliably than the common fixed-scale initialisations of the time. Specific numbers are in its experiments.

## Limitations

- The derivation assumes linear layers with activations that are roughly linear near zero, so it is less accurate for rectified activations. [He initialisation](he-initialisation.md) addresses that case.
- It does not account for residual connections or normalisation, which change the scale of signals.

## Connections

The rule is the starting point for [He initialisation](he-initialisation.md). The overall picture of signal propagation is in the [chapter](index.md). The gradient computations behind the variance argument are in [Automatic differentiation](../../math/automatic-differentiation/index.md).

## Applications

Default initialisation in many framework layers, especially for dense and recurrent layers with tanh or sigmoid activations.

## Open questions

- How should Glorot-style scaling be generalised to attention and gated layers?
- Is it still the right default for very wide models trained with modern optimisers?

## References

### Seminal papers

- Glorot and Bengio, *Understanding the difficulty of training deep feedforward neural networks*, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (2010). https://proceedings.mlr.press/v9/glorot10a.html — The original analysis and the fan-in and fan-out variance rule.
- He, Zhang, Ren and Sun, *Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification* (2015). https://arxiv.org/abs/1502.01852 — The rectifier variant that corrects the Glorot scale for ReLU.
- Schoenholz, Gilmer, Ganguli and Sohl-Dickstein, *Deep Information Propagation* (2016). https://arxiv.org/abs/1611.01232 — Mean-field analysis of how variance propagates in random deep networks.
- Saxe, McClelland and Ganguli, *Exact solutions to the nonlinear dynamics of learning in deep linear neural networks* (2013). https://arxiv.org/abs/1312.6120 — Learning dynamics in deep linear networks, relevant to scale choices.
- Ioffe and Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift* (2015). https://arxiv.org/abs/1502.03167 — Normalisation that reduces dependence on the initial scale.
