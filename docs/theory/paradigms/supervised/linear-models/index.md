---
tags:
  - supervised learning
  - regression
  - classification
---

# Linear and Generalised Linear Models

Linear models predict from a weighted sum of input features. They are the oldest supervised learners, still the default baseline, and the building block of every neural network layer.

## Overview

Given features $x \in \mathbb{R}^d$, a linear model computes $z = w^\top x + b$ and passes $z$ through a link function. Because the prediction is monotone in each weight, the fitted coefficients can be read directly, which makes these models popular in medicine, economics and psychology.

## Key models

| Model | Output | Loss / likelihood |
|---|---|---|
| Ordinary least squares | Real value $z$ | Squared error (Gaussian noise) |
| Ridge ($\ell_2$) | Real value | Squared error $+ \lambda\lVert w\rVert_2^2$ |
| Lasso ($\ell_1$) | Real value, sparse $w$ | Squared error $+ \lambda\lVert w\rVert_1$ |
| Elastic net | Real value | Mix of $\ell_1$ and $\ell_2$ penalties |
| Logistic regression | $p = \sigma(z)$ | Bernoulli log-likelihood (cross-entropy) |
| Softmax regression | Distribution over $K$ classes | Categorical cross-entropy |
| Poisson regression | Non-negative counts, $\lambda = e^{z}$ | Poisson log-likelihood |
| Perceptron | Class sign$(z)$ | Mistake-driven updates |

These are all instances of **generalised linear models (GLMs)**: the target follows an exponential-family distribution whose mean is linked to $z$.

## How they are fitted

- Least squares has the closed form $\hat w = (X^\top X + \lambda I)^{-1} X^\top y$.
- Logistic and other GLMs are convex; they are solved by iteratively reweighted least squares, L-BFGS or stochastic gradient descent.
- The $\ell_1$ penalty drives coefficients exactly to zero, giving automatic feature selection; the $\ell_2$ penalty shrinks correlated coefficients together.
- Bayesian view: ridge is the MAP estimate under a Gaussian prior on $w$, lasso under a Laplace prior.

## Strengths and limits

Strengths: convex training, strong theory, calibrated probabilities (logistic), fast, easy to audit. Limits: can only draw linear decision boundaries in the given feature space. The usual fixes are feature engineering (polynomials, splines), [kernels](../kernel-methods-svm/index.md), or stacking layers with non-linearities, which is a [neural network](../../../deep-learning/index.md).

## Connections

The delta rule that trains a single linear unit is the same equation as the Rescorla–Wagner model of conditioning (see [Supervised Learning](../index.md)). Linear probes, a logistic regression trained on frozen features, are the standard way to test what a [self-supervised](../../self-supervised/index.md) representation has learned.

## References

### Seminal papers

- Tibshirani (1996), "Regression shrinkage and selection via the lasso", *JRSS B*. https://www.math.cuhk.edu.hk/~btjin/math6221/p7.pdf — Introduces the lasso, the L1 penalty that sets some coefficients exactly to zero.
- Kingma & Ba (2015), "Adam: a method for stochastic optimization", ICLR, arXiv:1412.6980 — The Adam optimiser, the default for training logistic and neural models by gradient descent.
- Guo et al. (2017), "On calibration of modern neural networks", ICML, arXiv:1706.04599 — Shows that predicted probabilities can be miscalibrated and proposes temperature scaling as a fix.

### Surveys and textbooks

- Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, Springer (2009), chapters 3–4. https://doi.org/10.1007/978-0-387-84858-7 — Standard textbook treatment of least squares, shrinkage and linear classifiers, with free PDF from the authors.

### Lectures and videos

- Tibshirani, R. (1996). Regression shrinkage and selection via the lasso. *Journal of the Royal Statistical Society: Series B*, 58(1), 267–288. https://doi.org/10.1111/j.2517-6161.1996.tb02080.x — Introduces the lasso, an L1-penalised regression that regularises and selects variables at once.

### Articles and documentation

- Andrew Ng, Stanford CS229 lecture notes. https://cs229.stanford.edu/main_notes.pdf — Derivations of linear and logistic regression and the generalised linear model framework.

## Further reading

- McCullagh & Nelder, *Generalized Linear Models*, 2nd ed. (1989). No free link checked.
