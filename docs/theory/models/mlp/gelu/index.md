---
related:
- theory/models/mlp
- theory/models/transformer
aliases:
  - Gaussian Error Linear Units
  - GELU
  - 高斯誤差線性單元
tags:
  - activation functions
  - feedforward networks
  - transformers
last_reviewed: 2026-10-28
---

# Gaussian Error Linear Units

The Gaussian error linear unit (GELU) is a smooth activation function proposed by Hendrycks and Gimpel in their 2016 paper "Gaussian Error Linear Units (GELUs)". It weights each input by the standard normal cumulative distribution function evaluated at that input, rather than cutting the input off at zero. It is now common in Transformer feedforward blocks.

## Problem

An activation function is usually chosen as a fixed architectural decision. It is treated separately from stochastic regularisers such as dropout, even though both shape how much of a neuron's input reaches its output.

## Core idea

A ReLU gates its input by the sign of the input. GELU instead weights each input by its value. It can be read as the expected output of a stochastic mask that either passes the input unchanged or sets it to zero, where the probability of keeping the input is the standard normal CDF. Larger inputs are kept with higher probability, and the function stays smooth everywhere.

## Equation or algorithm

The exact form is

\[
\mathrm{GELU}(x) = x\,\Phi(x) = x \cdot \tfrac{1}{2}\left[1 + \mathrm{erf}\!\left(\tfrac{x}{\sqrt{2}}\right)\right],
\]

where \(\Phi\) is the standard normal CDF. The paper's tanh approximation,

\[
0.5\,x\left(1 + \tanh\!\left[\sqrt{2/\pi}\,\left(x + 0.044715\,x^3\right)\right]\right),
\]

was used in all of its experiments.

## Results

Median test error on CIFAR-10, for a 9-layer CNN without data augmentation, was 7.89% for GELU, against 8.16% for ReLU and 8.41% for ELU. On CIFAR-100, for a 40-layer wide residual network, it was 20.74% for GELU and 21.77% for ReLU.

## Limitations

The tanh form is an approximation, and the approximations trade accuracy for speed. The authors advise using an optimiser with momentum. Their MNIST results appear only in figures, so they are not quoted here.

## Connections

GELU is common in [Transformer](../../transformer/index.md) feedforward blocks, and it is one of the activation choices discussed in the [MLP](../index.md) family page. The normalisation method that the same page discusses alongside it is described in [layer normalisation](../layer-normalisation/index.md).

## Open issues and further variants

- **Activation choice.** Empirical gains from new activations are often small and inconsistent across tasks, and the reasons are not fully understood.
- **Exact versus approximate form.** The tanh approximation trades accuracy for speed, so the choice between it and the exact erf form is a practical decision for each implementation.
- **The stochastic reading.** Whether the mask interpretation explains GELU's behaviour beyond the experiments reported in the paper is an open question.

## References

### Seminal papers

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". [arXiv:1606.08415](https://arxiv.org/abs/1606.08415) — The GELU activation, used in many Transformer models.
- Rumelhart, D. E., Hinton, G. E. & Williams, R. J. (1986). "Learning representations by back-propagating errors". *Nature* 323: 533–536. https://doi.org/10.1038/323533a0 — Popularised backpropagation for training multilayer networks with hidden units.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". [arXiv:1512.03385](https://arxiv.org/abs/1512.03385) — Residual connections that make deep networks trainable.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 6 covers feedforward networks, activations and the universal approximation results.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". [arXiv:1607.06450](https://arxiv.org/abs/1607.06450) — Normalises over features rather than over the batch.
