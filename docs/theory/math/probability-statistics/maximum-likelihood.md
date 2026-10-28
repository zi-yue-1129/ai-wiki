---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
tags:
  - mathematics
  - estimation
aliases:
  - 最大概似估計
  - 最大似然估計
  - MLE
  - Maximum likelihood estimation
---

# Maximum Likelihood Estimation

Maximum likelihood estimation (MLE) chooses the parameter values under which the observed data are most probable. It is the default way to fit a parametric model, and training a neural network with cross-entropy or mean squared error is an instance of it. Part of [Probability and statistics](index.md).

## Overview

Suppose the data \(D = \{x_1, \dots, x_N\}\) are independent draws from a model \(p(x\mid\theta)\) with unknown parameters \(\theta\). The likelihood \(L(\theta) = \prod_i p(x_i\mid\theta)\) measures how probable the data are under each \(\theta\). MLE picks the \(\theta\) that maximises it. Because the logarithm is increasing, the same answer comes from maximising the log-likelihood, which turns the product into a sum.

## Key concepts

- **Likelihood**: \(L(\theta)\) is a function of \(\theta\) with the data held fixed. It is not a probability distribution over \(\theta\).
- **Negative log-likelihood (NLL)**: \(-\log L(\theta)\). Minimising the NLL is the usual training objective.
- **Consistency**: under standard regularity conditions, the MLE converges to the true parameter as the sample grows.
- **Asymptotic normality**: for large samples the MLE is approximately Gaussian around the true value, which gives standard errors.

## How it works

The MLE solves

\[
\hat\theta_{\text{MLE}} = \arg\max_\theta \sum_{i=1}^{N} \log p(x_i\mid\theta) = \arg\min_\theta \; \text{NLL}(\theta).
\]

Two worked examples show the idea. For a Gaussian with unknown mean and variance, the MLE of the mean is the sample mean, and the MLE of the variance divides by \(N\) rather than \(N-1\), which makes it biased in small samples. For a categorical classifier, maximising the likelihood of the correct labels is exactly minimising the cross-entropy loss.

For most models the maximum has no closed form, so it is found numerically. Gradient-based optimisers step against the gradient of the negative log-likelihood, the same calculation that trains neural networks (see [Calculus and optimisation foundations](../calculus/index.md)). When some data are missing or latent, as in mixture models, an iterative procedure can alternate between estimating the missing values and re-fitting the parameters. Dempster, Laird and Rubin (1977) analysed this procedure and proved that the likelihood never decreases from one iteration to the next [(Dempster et al., 1977)](https://doi.org/10.1111/j.2517-6161.1977.tb01600.x).

Fisher (1922) gave the method its modern form and introduced the properties of consistency, efficiency and sufficiency for estimators. Bishop (2006) and Murphy (2022) explain the same material in the machine-learning setting.

## Key methods

- [Maximum a posteriori estimation](maximum-a-posteriori.md): adds a log-prior to the log-likelihood. It reduces to MLE when the prior is flat.

## Connections

- [Probability and statistics](index.md) gives the overview and the other estimators in this area.
- [Probabilistic and Bayesian methods](../../paradigms/probabilistic/index.md) keeps the full posterior rather than a point estimate.
- [Information theory](../../information-theory/index.md) shows that the cross-entropy between the data distribution and the model equals the expected negative log-likelihood.

## Applications

- **Training classifiers**: cross-entropy loss, which is the NLL of a categorical distribution (Bishop, 2006).
- **Language models**: next-token training maximises the log-likelihood of the observed text.
- **Regression**: least-squares fitting is MLE under Gaussian noise with constant variance.
- **Incomplete data**: censored, truncated and missing observations, and factor analysis, which Dempster et al. (1977) treat with the same likelihood-based procedure.
- **Mixture models**: fitting a mixture of distributions when the component of each observation is unknown, the setting Dempster et al. (1977) analyse explicitly.

## Open questions

- MLE can overfit when data are scarce or the model is very flexible, and the likelihood alone does not say how much to trust the fit.
- In high-dimensional models the likelihood can have many equally good maxima or flat regions, and the MLE is then not unique.

## References

### Seminal papers

- Dempster, Laird and Rubin (1977). Maximum Likelihood from Incomplete Data Via the EM Algorithm. *Journal of the Royal Statistical Society: Series B*, 39(1), 1–22. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x — Analyses maximum likelihood with missing or latent data and proves that the likelihood improves monotonically under the iterative procedure.
- Fisher, R. A. (1922). On the mathematical foundations of theoretical statistics. *Philosophical Transactions of the Royal Society A* 222, 309–368. https://doi.org/10.1098/rsta.1922.0009 — Introduces maximum likelihood estimation in its modern form, with the properties of consistency and efficiency.
- Commentary on Fisher (1922): *From evidence to understanding*, PubMed Central. https://pmc.ncbi.nlm.nih.gov/articles/PMC4360088/ — Explains the content and influence of Fisher's paper, including its treatment of likelihood.

### Surveys and textbooks

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Shows how MLE gives least squares for Gaussian noise and cross-entropy for classification.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; treats maximum likelihood as the basis for fitting most models.
- Gelman, A. et al. (2013). *Bayesian Data Analysis*, 3rd ed. CRC Press. https://sites.stat.columbia.edu/gelman/book — Compares maximum likelihood with Bayesian estimation and discusses its asymptotic behaviour.
