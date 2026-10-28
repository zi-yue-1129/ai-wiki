---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/cnn
tags:
  - regularisation
  - dropout
  - generalisation
aliases:
  - 隨機正則化
  - 丟棄法
  - Dropout
  - Stochastic regularisation
---

# Dropout and stochastic regularisation

Dropout and related methods regularise a network by injecting randomness during training. Units, paths or whole training examples are randomly removed or mixed, so the model cannot rely on any single feature. The methods reduce overfitting and are also read as approximations of model averaging and Bayesian inference.

## Overview

Overfitting occurs when a model fits the training set well and generalises poorly. Classical regularisers penalise large weights. Stochastic methods regularise differently: they change the training signal at random, so the learned function must work across many perturbed versions of the network or the data.

## Key concepts

- **Dropout**: randomly setting a fraction of activations to zero during training, and scaling the remainder so the expected output is unchanged.
- **Stochastic depth**: randomly skipping whole residual blocks during training.
- **Mixup**: training on convex combinations of pairs of examples and their labels.
- **Label smoothing**: replacing one-hot targets with a softened distribution, which discourages overconfident predictions.
- **Bayesian interpretation**: reading dropout as approximate inference over model weights.

## How it works

In the original dropout method, each unit is kept with probability $p$ on each training step, and at test time all units are used with weights scaled to match. Srivastava and colleagues showed that this reduces overfitting across several architectures and tasks [(Srivastava et al., 2014)](https://jmlr.org/papers/v15/srivastava14a.html). Stochastic depth applies the same idea to layers: a residual block is skipped at random, which shortens the network during training and speeds it up [(Huang et al., 2016)](https://arxiv.org/abs/1603.09382).

Mixup changes the data instead of the network. Two examples and their labels are combined with a random weight, which encourages linear behaviour between training points [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412). Label smoothing changes the target. Szegedy and colleagues used it in their Inception v3 work to reduce overconfidence [(Szegedy et al., 2016)](https://arxiv.org/abs/1512.00567).

## Key methods

- [Dropout](dropout-method.md): random unit removal, the original method and its scaling rule.
- [Mixup](mixup.md): convex combinations of training pairs.
- [Stochastic depth](stochastic-depth.md): random skipping of residual blocks.

## Interpretations

Dropout can be read as training an ensemble of thinned networks that share weights. Gal and Ghahramani showed that dropout applied at test time can be interpreted as approximate Bayesian inference, which gives a way to estimate model uncertainty from repeated stochastic predictions [(Gal and Ghahramani, 2016)](https://arxiv.org/abs/1506.02142). These readings are useful, but they are approximations, and the exact connection depends on the model and the choice of dropout rate.

## Connections

Normalisation layers, covered in [Normalisation](../normalisation/index.md), also act as a form of regularisation during training. Convolutional networks use dropout in their classifier heads and stochastic depth in deep residual stacks; see [CNNs](../../models/cnn/index.md). The statistical ideas behind uncertainty are in [Probability and statistics](../../math/index.md).

## Applications

Dropout and mixup are common in image classification. Stochastic depth is used in deep vision backbones. Label smoothing appears in translation and language modelling, where it discourages overconfident token predictions.

## Open questions

- When do stochastic regularisers help a large model that is trained on enough data to avoid overfitting?
- How should dropout be combined with normalisation, since the two interact?
- Does the Bayesian reading give calibrated uncertainty in practice?

## References

### Seminal papers

- Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, Journal of Machine Learning Research (2014). https://jmlr.org/papers/v15/srivastava14a.html — The original dropout method and its experiments.
- Huang, Sun, Liu, Sedra and Weinberger, *Deep Networks with Stochastic Depth* (2016). https://arxiv.org/abs/1603.09382 — Randomly skips residual blocks during training.
- Zhang, Cisse, Dauphin and Lopez-Paz, *mixup: Beyond Empirical Risk Minimization* (2017). https://arxiv.org/abs/1710.09412 — Introduces mixup for training on convex combinations of examples.
- Gal and Ghahramani, *Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning* (2016). https://arxiv.org/abs/1506.02142 — Links dropout to approximate Bayesian inference.
- Szegedy et al., *Rethinking the Inception Architecture for Computer Vision*, IEEE Conference on Computer Vision and Pattern Recognition (2016). https://arxiv.org/abs/1512.00567 — Popularised label smoothing as a regulariser.
