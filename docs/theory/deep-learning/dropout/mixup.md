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

Mixup trains a network on convex combinations of pairs of examples and their labels. A random weight blends two images and their one-hot labels, and the model learns to predict the blended label. The method acts as a data-level regulariser and encourages simple, nearly linear behaviour between training points.

## Overview

The [chapter](index.md) covers stochastic regularisation. This page covers mixup, which regularises by changing the data rather than the network.

## Problem

Standard empirical risk minimisation fits the training points and can behave erratically between them, which makes models sensitive to small input changes and to label noise. Zhang and colleagues proposed mixup as a simple principle to alleviate these issues [(Zhang et al., 2017)](https://arxiv.org/abs/1710.09412).

## Core idea

For two examples $(x_i, y_i)$ and $(x_j, y_j)$, draw $\lambda \sim \mathrm{Beta}(\alpha, \alpha)$ and form $\tilde{x} = \lambda x_i + (1-\lambda) x_j$ and $\tilde{y} = \lambda y_i + (1-\lambda) y_j$. The network is trained on the mixed pairs. The training signal then asks the model to behave linearly between the original examples.

## Equation

The mixed training loss is

$$\mathcal{L}_{\text{mix}} = \mathbb{E}_{\lambda, i, j}\left[\,\ell\big(f_\theta(\lambda x_i + (1-\lambda)x_j),\; \lambda y_i + (1-\lambda) y_j\big)\right]$$

where $\ell$ is the usual classification loss, with one-hot labels $y_i$ and $y_j$. The parameter $\alpha$ controls how strongly examples are mixed; small values keep most mixed pairs close to one of the originals.

## Results

The paper reports improved generalisation on image classification benchmarks, and more robustness to some kinds of corrupted labels and adversarial examples. The exact figures are in its experiments section.

## Limitations

- Mixed images do not always correspond to realistic inputs, which can matter for tasks where the content must be recognisable.
- Mixing is less natural for structured inputs such as text or graphs, where a convex combination has no obvious meaning.
- The benefit depends on the choice of $\alpha$ and on training length.

## Connections

Mixup is related to the label-smoothing idea in the [chapter](index.md), since both soften targets. It is one of the regularisers used alongside [Dropout](dropout-method.md) and [Stochastic depth](stochastic-depth.md).

## Applications

Image classification and some speech and tabular tasks, where it is used as a standard augmentation.

## Open questions

- Which mixing schemes work best for detection and segmentation, where labels are spatial?
- Does mixup help with calibration as well as accuracy?

## References

### Seminal papers

- Zhang, Cisse, Dauphin and Lopez-Paz, *mixup: Beyond Empirical Risk Minimization* (2017). https://arxiv.org/abs/1710.09412 — Introduces mixup and the convex combination of examples and labels.
- Szegedy et al., *Rethinking the Inception Architecture for Computer Vision*, IEEE Conference on Computer Vision and Pattern Recognition (2016). https://arxiv.org/abs/1512.00567 — Soft targets through label smoothing, the closest related idea.
- Srivastava, Hinton, Krizhevsky, Sutskever and Salakhutdinov, *Dropout: A Simple Way to Prevent Neural Networks from Overfitting*, Journal of Machine Learning Research (2014). https://jmlr.org/papers/v15/srivastava14a.html — The standard regulariser that mixup is often combined with.
- Huang, Sun, Liu, Sedra and Weinberger, *Deep Networks with Stochastic Depth* (2016). https://arxiv.org/abs/1603.09382 — Another regulariser used in deep vision models.
- Gal and Ghahramani, *Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning* (2016). https://arxiv.org/abs/1506.02142 — The uncertainty view that shares the goal of calibrated predictions.
