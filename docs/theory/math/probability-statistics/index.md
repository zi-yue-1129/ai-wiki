---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
  - theory/information-theory
tags:
  - mathematics
  - probability
  - statistics
aliases:
  - 機率與統計
  - Probability and statistics
  - Statistics for AI
  - 貝氏定理
---

# Probability and Statistics for AI

Probability is the language AI uses for uncertainty, and statistics is the set of methods for learning from data under that uncertainty. This page explains the parts of both fields that AI uses most: random variables, common distributions, Bayes' rule, estimators, and the statistical view of a loss function. It is one of the areas covered in the [mathematics overview](../index.md).

## Overview

A random variable \(X\) takes values according to a probability distribution \(p(x)\). A classifier outputs a distribution over labels, a language model outputs a distribution over the next token, and a regression model can output a mean and a variance. Statistics asks the inverse question: given observed data \(D\), which distribution or parameter values explain it best, and how sure can we be?

Two views run through the subject. The frequentist view treats parameters as fixed unknown numbers and asks how an estimator behaves over repeated samples. The Bayesian view treats parameters as random variables with a prior, and updates that prior with data. Most modern AI uses both: maximum likelihood is the workhorse for training, and Bayesian reasoning governs uncertainty and regularisation.

## Key concepts

- **Expectation and variance**: \(\mathbb{E}[X] = \sum_x x\,p(x)\) and \(\operatorname{Var}[X] = \mathbb{E}[(X-\mathbb{E}X)^2]\). Expected loss is the quantity training tries to minimise.
- **Common distributions**: Bernoulli for a binary outcome, categorical for one of \(K\) classes, Gaussian for real-valued noise, and Poisson for counts.
- **Conditional probability and independence**: \(p(x\mid y) = p(x,y)/p(y)\). Conditional independence is what makes graphical models tractable.
- **Bayes' rule**: \(p(\theta\mid D) = \dfrac{p(D\mid\theta)\,p(\theta)}{p(D)}\), combining a prior with a likelihood to give a posterior.
- **Estimator**: a rule that turns data into a parameter estimate. Its bias and variance describe its typical error.
- **Law of large numbers and central limit theorem**: sample averages converge to expectations, and their fluctuations are approximately Gaussian for large samples. These results justify Monte Carlo estimates and confidence intervals.

## How it works

The statistical view explains most of the loss functions used in practice. Maximising the likelihood of a model is the same as minimising the negative log-likelihood, and common losses are special cases of this:

- Cross-entropy loss for classification is the negative log-likelihood of a categorical distribution.
- Mean squared error is the negative log-likelihood of a Gaussian with fixed variance, up to constants.
- L2 weight regularisation corresponds to a Gaussian prior on the weights when a MAP estimate is computed.

Estimation has two standard routes. [Maximum likelihood](maximum-likelihood.md) picks the parameter that makes the observed data most probable. [Maximum a posteriori](maximum-a-posteriori.md) estimation adds the log-prior to the likelihood, so the prior acts as a regulariser. Full Bayesian inference keeps the whole posterior, which is usually intractable and is approximated by [variational inference](../../paradigms/probabilistic/variational-inference/index.md) or [Markov chain Monte Carlo](../../paradigms/probabilistic/mcmc/index.md).

## Key methods

Two estimators are the landmark methods of this area. Each has its own page.

- [Maximum likelihood estimation](maximum-likelihood.md): chooses the parameter that maximises the probability of the data. Used to train almost every parametric model.
- [Maximum a posteriori estimation](maximum-a-posteriori.md): adds a prior to the likelihood. It equals maximum likelihood when the prior is flat, and it turns priors such as Gaussians into regularisers.

## Connections

- [Probabilistic and Bayesian methods](../../paradigms/probabilistic/index.md) builds on this page with graphical models, inference and Bayesian deep learning.
- [Information theory](../../information-theory/index.md) defines entropy and KL divergence, which are the expectations behind cross-entropy losses.
- [Linear algebra](../linear-algebra/index.md) supplies the covariance matrix of a multivariate Gaussian and its eigendecomposition.
- Brain and cognition: the Bayesian brain hypothesis proposes that neural systems represent uncertainty and combine prior expectations with sensory evidence. It is debated, and it is treated in the [probabilistic methods page](../../paradigms/probabilistic/index.md).

## Applications

- **Training**: maximum likelihood training of classifiers and language models, with cross-entropy as the negative log-likelihood (Bishop, 2006).
- **Uncertainty**: credible intervals and posterior predictive distributions from Bayesian models (Gelman et al., 2013).
- **Evaluation**: confidence intervals and significance tests for comparing model accuracy on benchmarks. The statistical tools here are standard, and the textbooks listed in References cover them.
- **Experimental design in science**: the same estimation and testing methods underlie empirical studies in neuroscience and psychology.

## Open questions

- Calibration: a model's stated probabilities often do not match observed frequencies, particularly for large neural networks. See [uncertainty quantification and calibration](../../paradigms/probabilistic/index.md).
- Prior choice: priors that are reasonable for one problem can distort results on another. How to choose them for large models is unsettled.
- Statistical testing of benchmarks: many reported differences between models are small compared with the variance across runs, and it is unclear how to report them reliably.

## References

### Seminal papers

- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A*. https://digital.library.adelaide.edu.au/handle/2440/15172 — Sets out maximum likelihood estimation and the notions of sufficiency and efficiency. Copy from the University of Adelaide repository.
- Commentary on Fisher (1922): *From evidence to understanding: a commentary on Fisher (1922)*, published in PubMed Central. https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — Peer-reviewed commentary that explains the content and influence of Fisher's paper on maximum likelihood.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Free PDF from the author's publisher page. Covers probability distributions, Bayesian inference and the link between regularisation and priors.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free online textbook, with probability, estimation and Bayesian inference developed for machine learning readers.
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A. & Rubin, D. B. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — Standard applied Bayesian textbook; the author site hosts the book and related material.
