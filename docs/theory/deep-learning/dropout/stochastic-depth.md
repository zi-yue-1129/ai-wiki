---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/dropout
  - theory/models/cnn
tags:
  - stochastic depth
  - residual networks
  - regularisation
aliases:
  - 隨機深度
  - Stochastic depth
---

# Stochastic depth

Stochastic depth trains a residual network while randomly skipping entire residual blocks in each mini-batch. The full network is used at test time. The method regularises by making the network behave as an ensemble of shallower networks, and it shortens training time because skipped blocks cost nothing on that step.

## Overview

The [chapter](index.md) covers randomised regularisers. This page covers stochastic depth, which applies the dropout idea to whole layers rather than to single units.

## Problem

Very deep residual networks can be hard to train and can overfit. Training depth is also costly. The question is whether randomly removing layers during training can keep the performance of the deep network while reducing cost.

## Core idea

Each residual block $l$ is kept with probability $p_l$. When a block is dropped, its input passes straight through the identity connection. The survival probability can decrease with depth, so early blocks are kept more often than later ones. At test time all blocks are used, with each residual branch scaled by its survival probability.

## Equation

For a residual block with branch function $f_l$, the training update is

$$\mathbf{h}_{l} = \mathbf{h}_{l-1} + b_l \, f_l(\mathbf{h}_{l-1}), \qquad b_l \sim \mathrm{Bernoulli}(p_l)$$

At test time the branch is multiplied by its expected value, $p_l$. The survival probabilities used in the paper decrease linearly with depth.

## Results

The paper reports lower test error on several image classification benchmarks and a substantial reduction in training time, with the numbers in its experiments section.

## Limitations

- The benefit depends on the residual structure. The method does not transfer directly to networks without skip connections.
- The choice of survival probabilities is a design decision that the results depend on.
- The regularisation effect is partly a depth effect, so the gains may shrink for models trained on very large datasets.

## Connections

Stochastic depth applies the logic of [Dropout](dropout-method.md) to residual blocks, and it is commonly used in [convolutional networks](../../models/cnn/index.md) with residual connections. Normalisation inside those blocks is covered in [Normalisation](../normalisation/index.md).

## Applications

Training deep residual image classifiers and detectors, and the backbones of models trained with long schedules.

## Open questions

- Can the survival schedule be chosen automatically for a new architecture?
- How does stochastic depth interact with pre-norm and post-norm placement in Transformers?

## References

### Seminal papers

- Huang, Sun, Liu, Sedra and Weinberger, *Deep Networks with Stochastic Depth* (2016). https://arxiv.org/abs/1603.09382 — Introduces stochastic depth, the random skipping of residual blocks during training.
- He, Zhang, Ren and Sun, *Deep Residual Learning for Image Recognition*, IEEE Conference on Computer Vision and Pattern Recognition (2016). https://doi.org/10.1109/CVPR.2016.90 — The residual networks that stochastic depth regularises.
- Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, Journal of Machine Learning Research (2014). https://jmlr.org/papers/v15/srivastava14a.html — The unit-level method that stochastic depth generalises to layers.
- Zhang, Cisse, Dauphin and Lopez-Paz, *mixup: Beyond Empirical Risk Minimization* (2017). https://arxiv.org/abs/1710.09412 — A data-level regulariser that is often combined with it.
- Ioffe and Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift* (2015). https://arxiv.org/abs/1502.03167 — The normalisation used inside the residual blocks of many such networks.
