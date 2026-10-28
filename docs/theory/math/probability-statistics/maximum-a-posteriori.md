---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
tags:
  - mathematics
  - estimation
  - regularisation
aliases:
  - 最大後驗估計
  - MAP
  - Maximum a posteriori estimation
---

# Maximum a Posteriori Estimation

Maximum a posteriori (MAP) estimation picks the parameter with the highest posterior probability. It adds a prior to maximum likelihood, and this is how prior knowledge and regularisation enter the estimate. Part of [Probability and statistics](index.md).

## Overview

Bayes' rule gives the posterior \(p(\theta\mid D) \propto p(D\mid\theta)\,p(\theta)\). MAP chooses the \(\theta\) with the largest posterior. The data term \(p(D\mid\theta)\) pulls the estimate toward values that explain the data, and the prior \(p(\theta)\) pulls it toward values that are plausible before any data are seen.

## Key concepts

- **Prior**: a distribution over parameters that encodes beliefs before seeing the data.
- **Posterior**: the distribution over parameters after seeing the data.
- **Mode**: the point of highest density. MAP is the posterior mode, not the posterior mean.
- **Regulariser**: a penalty added to the loss. A log-prior added to the log-likelihood acts as one.

## How it works

The MAP estimate solves

\[
\hat\theta_{\text{MAP}} = \arg\max_\theta \big[\log p(D\mid\theta) + \log p(\theta)\big].
\]

With a Gaussian prior \(p(\theta)\propto \exp(-\lambda\|\theta\|_2^2/2)\), the log-prior becomes an L2 penalty, which is ridge regression when the likelihood is Gaussian. With a Laplace prior, it becomes an L1 penalty, the lasso. This is why many familiar regularisers can be read as priors. Bishop (2006) develops this correspondence for linear regression.

The MAP estimate is the posterior mode. For a Gaussian posterior, the mode, mean and median coincide, so MAP and the posterior mean agree. For other posteriors they can differ.

## Key methods

- [Maximum likelihood estimation](maximum-likelihood.md): the special case of MAP with a flat prior.

## Connections

- [Probabilistic and Bayesian methods](../../paradigms/probabilistic/index.md) covers the full posterior, which MAP approximates by a single point.
- [Variational inference](../../paradigms/probabilistic/variational-inference/index.md) and [MCMC](../../paradigms/probabilistic/mcmc/index.md) are methods that go beyond the posterior mode.
- Brain and cognition: the Bayesian brain hypothesis treats prior expectations as part of perception. MAP is one simple computational model of that combination, not a claim about neural implementation.

## Applications

- **Regularised regression**: ridge and lasso regression are MAP estimates with Gaussian and Laplace priors (Bishop, 2006).
- **Weight decay**: the L2 penalty commonly used when training neural networks corresponds to a Gaussian prior on the weights.
- **Small-data estimation**: priors stabilise estimates when data are scarce.

## Open questions

- MAP is not invariant to reparameterisation: changing the variables changes the mode. This makes the estimate depend on how the model is written.
- A point estimate ignores posterior uncertainty, so it can be overconfident. Full posterior approximations are needed for calibrated uncertainty.

## References

### Seminal papers

- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A* 222, 309–368. https://doi.org/10.1098/rsta.1922.0009 — Source of maximum likelihood, the estimator that MAP extends by adding a prior.
- Commentary on Fisher (1922), PubMed Central. https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — Peer-reviewed commentary on the paper and its treatment of likelihood.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Derives ridge and lasso regression as MAP estimates with Gaussian and Laplace priors.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers MAP estimation and its relation to regularisation.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — Discusses the posterior mode and how it compares with the posterior mean and full posterior.
