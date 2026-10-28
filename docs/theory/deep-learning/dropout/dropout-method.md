---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/dropout
tags:
  - dropout
  - regularisation
  - overfitting
aliases:
  - 丟棄法
  - Dropout
---

# Dropout

Dropout randomly removes units from a network during each training step. The remaining units must learn features that work without any particular partner, which reduces overfitting. At test time the full network is used, with activations scaled so their expected value matches training.

## Overview

The [chapter](index.md) covers stochastic regularisation. This page covers the original dropout method, its scaling rule and its variants.

## Problem

Large networks with many parameters can memorise a training set. Adding a penalty on weights helps, but units in a layer can co-adapt, each depending on specific others. The method targets co-adaptation directly.

## Core idea

On each training step, every unit in a layer is kept with probability $p$ and set to zero otherwise, independently. The gradients flow only through the kept units. Because each step trains a different thinned network that shares weights with the others, the training behaves like an ensemble of many networks.

## Equation

For an activation vector $\mathbf{h}$, the training-time output is $\tilde{\mathbf{h}} = \mathbf{m} \odot \mathbf{h}$ with mask $m_i \sim \mathrm{Bernoulli}(p)$. The network is then used at test time with $\mathbf{h}$ itself, which is equivalent in expectation to scaling the training output.

## Results

The paper reports reduced overfitting and improved results across several classification tasks and architectures, with figures in its experiments section. The specific numbers are not restated here.

## Limitations

- Training takes longer, because the network needs more steps to converge with noisy units.
- The benefit shrinks when the model is not overfitting, and it can hurt performance in convolutional layers where neighbouring activations are highly correlated.
- Dropout interacts with normalisation layers, and placing both naively can change the variance seen at test time.

## Connections

The Bayesian reading of dropout is in the [chapter](index.md), where Gal and Ghahramani connect test-time dropout to approximate inference [(Gal and Ghahramani, 2016)](https://arxiv.org/abs/1506.02142). The method is used alongside [Mixup](mixup.md) and [Stochastic depth](stochastic-depth.md).

## Applications

Classifier heads and fully connected layers in many networks, and the regularisation of small datasets.

## Open questions

- Is dropout still needed for large models trained on very large data?
- How should the rate be set for different layers and architectures?

## References

### Seminal papers

- Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, Journal of Machine Learning Research (2014). https://jmlr.org/papers/v15/srivastava14a.html — The original dropout method and its experiments.
- Gal and Ghahramani, *Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning* (2016). https://arxiv.org/abs/1506.02142 — The Bayesian interpretation of dropout.
- Huang, Sun, Liu, Sedra and Weinberger, *Deep Networks with Stochastic Depth* (2016). https://arxiv.org/abs/1603.09382 — A related method that drops whole residual blocks.
- Ioffe and Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift* (2015). https://arxiv.org/abs/1502.03167 — Shows why dropout and normalisation need care when used together.
- Zhang, Cisse, Dauphin and Lopez-Paz, *mixup: Beyond Empirical Risk Minimization* (2017). https://arxiv.org/abs/1710.09412 — A data-level regulariser used alongside dropout.
