---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - regression
  - tabular data
aliases:
  - LocalGLMnet
  - 局部廣義線性網路
  - 可解釋神經網路定價
---

# LocalGLMnet (Richman & Wüthrich 2021)

LocalGLMnet is a neural network that keeps the additive, coefficient-based form of a generalised linear model, but lets each coefficient depend on the policy being priced. It is designed for tabular insurance data, where accuracy and explanation are both required. It is one of the methods described on the parent page [Insurance and Actuarial Science](../index.md).

## Overview

On tabular data, deep networks often predict better than generalised linear models, but their learned structure is hard to read, and variable selection happens inside the model where it cannot be inspected. Richman and Wüthrich (2021) ask whether the structure of a GLM can be kept while the power of representation learning is retained. Their answer is an architecture that stays close to a GLM in form. Its coefficients are functions of the input, so the model can be read as a GLM that changes from one policy to another.

The paper tests the architecture on a synthetic regression problem with a known nonlinear mean, and on a French motor third-party liability (MTPL) dataset with claim counts.

## Key concepts

- **Regression attention**: a coefficient $\hat\beta_j(x)$ for feature $j$ that depends on the whole input vector $x$. The paper calls these regression attentions.
- **Local GLM**: in a small neighbourhood of any policy, the model behaves like a GLM with coefficients fixed at the values for that policy.
- **Skip connection**: the raw features feed the output layer directly, alongside the deep part of the network.
- **Additive decomposition**: the linear predictor splits into one term per feature, $\hat\beta_j(x)\,x_j$. The paper relates these terms to Shapley values and integrated gradients.
- **Poisson deviance**: the loss used to fit claim counts, consistent for the mean of a Poisson model.

## How it works

The network has two parts. A feedforward network maps the input $x$ to a vector $\beta(x)$ of the same dimension as $x$. The output is the link of the mean, computed as an inner product of $\beta(x)$ with the raw input:

$$
g\big(\mu(x)\big) = \beta_0 + \langle \beta(x),\, x \rangle,
$$

where $g$ is the link function, $\beta_0$ is an intercept, and $\beta(x)$ is the learned regression attention. With $\beta(x)$ fixed, this is a GLM. Because $\beta(x)$ varies, it is a local GLM.

The fitting procedure follows standard practice for neural networks.

1. Pass each policy's features through the feedforward network to obtain $\beta(x)$.
2. Take the inner product of $\beta(x)$ with the raw features $x$, and apply the log link for counts.
3. Minimise the Poisson deviance on training data with stochastic gradient descent.
4. Stop early, using a validation split, to avoid overfitting.
5. Read off each $\hat\beta_j(x)$ for individual policies, and plot them against feature values to check whether the learned effects are sensible.

## Results

On the synthetic example, the paper compares out-of-sample mean squared errors against the known regression function, which has an MSE of about 1 because the responses have unit variance.[^1] The GLM reaches an out-of-sample MSE of 1.527, the null model 1.792, and LocalGLMnet 1.005. The GLM is limited by the linear form of its predictor, while LocalGLMnet approaches the true function.

On the MTPL data, the paper reports out-of-sample Poisson deviance losses (in units of $10^{-2}$) of 25.445 for the null model with only an intercept, 23.873 for a plain feedforward network, and 23.945 for LocalGLMnet. A reduced version of LocalGLMnet reaches 23.912. The authors state that LocalGLMnet gives up a little predictive power for the interpretable structure. Its gap to the plain network is small compared with the gap to the null model.

[^1]: Table 1 of Richman and Wüthrich (2021), arXiv:2107.11059. Table 2 gives the MTPL losses quoted in the paragraph above.

## Limitations

- **Interpretation is local and approximate.** The reading of each $\hat\beta_j(x)$ as a coefficient holds only where the learned attention changes smoothly. Noisy attentions can mislead.
- **Some accuracy is lost.** On the MTPL data, the interpretable model is less accurate than a plain network, as the paper acknowledges.
- **Decomposition is not causation.** The additive terms explain the fitted model. They do not show that a feature causes claims.
- **Limited evaluation.** The paper uses one synthetic setting and one insurance dataset. Results on other tabular domains, and against modern boosted trees, need separate tests.
- **Training effort.** Neural networks need careful tuning and early stopping, which GLM practitioners may not have in place.

## Open questions

- Will regulators accept the learned regression attentions as an explanation of a price, and what documentation would they need?
- Does the advantage over a GLM hold when the features include text, images or telematics sequences?
- Can a fairness constraint, such as that of Lindholm and colleagues (2022), be built into the architecture rather than applied afterwards?

## References

### Seminal papers

- Richman, R. & Wüthrich, M. V. (2021). LocalGLMnet: interpretable deep learning for tabular data. arXiv. https://arxiv.org/abs/2107.11059 — The architecture described on this page, with its synthetic and French MTPL experiments.
- Lindholm, M. et al. (2022). A multi-task network approach for calculating discrimination-free insurance prices. arXiv. https://arxiv.org/abs/2207.02799 — Neural network for insurance prices that avoids proxy discrimination, trained with partial protected-attribute data.

### Surveys and textbooks

- Wüthrich, M. V. & Merz, M. (2023). *Statistical Foundations of Actuarial Learning and its Applications*. Springer. https://doi.org/10.1007/978-3-031-12409-9 — Textbook on GLMs and feedforward networks for actuarial data, which the paper uses as its benchmark setting.
- Ohlsson, E. & Johansson, B. (2010). *Non-Life Insurance Pricing with Generalized Linear Models*. Springer. https://doi.org/10.1007/978-3-642-10791-7 — The GLM practice that LocalGLMnet is designed to extend.

### Articles and documentation

- Rudin, C. (2018). Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead. arXiv. https://arxiv.org/abs/1811.10154 — Argues that high-stakes decisions should use models that are interpretable by design.
