---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/dropout
tags:
  - mixup
  - data augmentation
  - regularisation
aliases:
  - 混合增強
  - Mixup
---

# Mixup

Mixup trains a network on convex combinations of pairs of examples and their labels. For each pair, a random weight drawn from a Beta distribution blends the two inputs and the two one-hot labels, and the network is trained on the blended pair. The method changes the training data rather than the network.

## Overview

The [chapter](index.md) covers stochastic regularisation. This page covers mixup, which regularises by changing the data.

## Problem

Empirical risk minimisation fits the training points but can behave unpredictably between them. This makes models sensitive to small input perturbations and to corrupted labels. Zhang et al. propose mixup as a simple principle for these problems [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412).

## Core idea

For two examples $(x_i, y_i)$ and $(x_j, y_j)$, draw $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$ and form $\tilde{x} = \lambda x_i + (1-\lambda) x_j$ and $\tilde{y} = \lambda y_i + (1-\lambda) y_j$. The network is trained on the pairs $(\tilde{x}, \tilde{y})$.

## Equation

The mixed training loss is

$$\mathcal{L}_{\text{mix}} = \mathbb{E}_{\lambda, i, j}\left[\,\ell\big(f_\theta(\lambda x_i + (1-\lambda)x_j),\; \lambda y_i + (1-\lambda) y_j\big)\right]$$

where $\ell$ is the usual classification loss and $y_i$, $y_j$ are one-hot labels. The hyperparameter $\alpha$ sets the Beta distribution from which $\lambda$ is drawn.

## Results

The abstract reports improved generalisation on ImageNet-2012, CIFAR-10, CIFAR-100, Google commands and UCI datasets. It also reports that mixup reduces memorisation of corrupt labels, increases robustness to adversarial examples and stabilises GAN training. The figures are in the paper's experiments.

## Limitations

- The reported gains are for the datasets and models in the paper's experiments, and they do not automatically carry over to other tasks.
- The abstract reports results for a range of values of $\alpha$ only through the experiments, so the best choice for a new setting has to be checked.

## Connections

The [chapter](index.md) covers the other stochastic regularisers in this section, which act on the network rather than the data.

## Applications

Image classification, speech and tabular benchmarks, which are the kinds of tasks the paper evaluates.

## Open questions

- Which mixing schemes suit tasks whose labels have spatial structure, such as detection and segmentation?
- Does mixup change calibration as well as accuracy?

## References

### Seminal papers

- Zhang, Cisse, Dauphin and Lopez-Paz, *mixup: Beyond Empirical Risk Minimization* (2017). https://arxiv.org/abs/1710.09412 — Introduces mixup, the convex combination of examples and labels.
- Szegedy et al., *Rethinking the Inception Architecture for Computer Vision*, IEEE Conference on Computer Vision and Pattern Recognition (2016). https://arxiv.org/abs/1512.00567 — Introduces label smoothing as a way to soften training targets.
- Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, Journal of Machine Learning Research (2014). https://jmlr.org/papers/v15/srivastava14a.html — Introduces dropout, a standard regulariser for neural networks.
- Huang, Sun, Liu, Sedra and Weinberger, *Deep Networks with Stochastic Depth* (2016). https://arxiv.org/abs/1603.09382 — Introduces stochastic depth, which randomly skips residual blocks during training.
- Gal and Ghahramani, *Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning* (2016). https://arxiv.org/abs/1506.02142 — Connects dropout to approximate Bayesian inference.
