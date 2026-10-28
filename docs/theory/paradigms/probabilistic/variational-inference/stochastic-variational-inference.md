---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/probability-statistics
tags:
  - probabilistic models
  - approximate inference
  - scalable learning
aliases:
  - 隨機變分推論
  - Stochastic variational inference
  - SVI
---

# Stochastic Variational Inference

Stochastic variational inference (SVI) fits a variational approximation to very large datasets by using noisy gradients computed on minibatches. It uses natural-gradient updates for the global latent variables and the Robbins–Monro step-size conditions for convergence. Part of [Variational inference](index.md).

## Overview

Mean-field updates need a full pass over the data for each step, which becomes impractical for millions of documents. SVI replaces the full pass with a random minibatch. Each step uses a scaled estimate of the update computed from the minibatch, so on average it moves in the same direction as the exact update, with added noise. Hoffman et al. (2013) develop this for conjugate models with local and global latent variables.

## Key concepts

- **Global and local variables**: global variables are shared across the dataset, and local variables are specific to each data point.
- **Natural gradient**: a gradient rescaled by the geometry of the variational family. For exponential families it has a simple form that matches the conjugate updates.
- **Robbins–Monro conditions**: step sizes \(\rho_t\) with \(\sum_t \rho_t = \infty\) and \(\sum_t \rho_t^2 < \infty\) guarantee convergence of noisy updates (Robbins & Monro, 1951).
- **Minibatch scaling**: the minibatch estimate is multiplied by the ratio of dataset size to batch size, so its expectation equals the full update.

## How it works

For each step, sample a minibatch of data points, optimise the local variables for those points, compute the natural-gradient estimate for the global variables from the minibatch, and move the global variables by a step of size \(\rho_t\):

\[
\lambda_{t+1} = (1-\rho_t)\,\lambda_t + \rho_t\,\hat\lambda_t,
\]

where \(\lambda\) are the global variational parameters and \(\hat\lambda_t\) is the estimate obtained from the minibatch. The update is an average between the current value and the minibatch's estimate of the optimum.

For models that are not conjugate, SVI can use black-box gradient estimators in its place, which trades exactness for generality (Ranganath et al., 2014).

## Key methods

- [Mean-field variational inference](mean-field.md): the full-batch method whose updates SVI approximates with minibatches.
- [Variational autoencoder](../../unsupervised/density-and-generative-models/vae/index.md): a related scalable method that uses stochastic gradients with an encoder network, the amortised form of VI.

## Connections

- [Variational inference](index.md) explains the ELBO that SVI maximises.
- [Probability and statistics](../../../math/probability-statistics/index.md) gives the exponential-family background used by the natural gradient.
- The Robbins–Monro idea is shared with [stochastic gradient descent](../../../math/calculus/index.md) in training neural networks.

## Applications

- **Topic models on large corpora**: SVI fits latent Dirichlet allocation to very large document collections, which the paper reports as the main target (Hoffman et al., 2013).
- **Large-scale Bayesian models**: scalable posterior approximation whenever a full pass over the data is too costly.

## Open questions

- Minibatch noise and step-size choice strongly affect convergence speed, and tuning them for new models is still largely empirical.
- The method is most natural for conjugate exponential-family models. Extending it to deep, non-conjugate models is the main line of current work.

## References

### Seminal papers

- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2013). Stochastic variational inference. *Journal of Machine Learning Research* 14. https://www.jmlr.org/papers/v14/hoffman13a.html — Introduces SVI with natural-gradient minibatch updates for large conjugate models.
- Robbins, H. & Monro, S. (1951). A stochastic approximation method. *Annals of Mathematical Statistics*. https://projecteuclid.org/euclid.aoms/1177729586 — Gives the step-size conditions that ensure convergence of noisy updates.
- Ranganath, R., Gerrish, S. & Blei, D. M. (2014). Black box variational inference. *AISTATS*. https://proceedings.mlr.press/v33/ranganath14.html — Gives stochastic gradient estimators for VI that apply to models without conjugacy.

### Surveys and textbooks

- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association*. arXiv:1601.00670. https://arxiv.org/abs/1601.00670 — Reviews stochastic and black-box VI, with the trade-offs between them.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers scalable variational methods for large datasets.
- Kingma, D. P. & Welling, M. (2014). Auto-encoding variational Bayes. *ICLR*. arXiv:1312.6114. https://arxiv.org/abs/1312.6114 — Uses minibatch stochastic gradients for the amortised form of VI.
