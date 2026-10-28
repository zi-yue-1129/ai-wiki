---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic
tags:
  - optimization
  - learning theory
aliases:
  - 黑箱變分推論
  - 黑盒變分推論
  - BBVI
  - Black-box variational inference
---

# Black-Box Variational Inference

Black-box variational inference (BBVI), introduced by Ranganath, Gerrish and Blei (2013), maximises the evidence lower bound with Monte Carlo gradients that need only the joint density and samples from the approximating family. One algorithm can therefore be applied to many models without model-specific derivations. It is a method within the [Variational Inference](../index.md) overview.

## Overview

Classical variational algorithms are derived by hand for each model. Mean-field coordinate ascent needs conditional distributions whose expectations have closed forms, which is practical mainly for conditionally conjugate models (Blei et al., 2016). Stochastic variational inference (Hoffman et al., 2012) scales these updates to large datasets with noisy natural gradients, but it still relies on the exponential-family structure of the model. Ranganath et al. argue that this model-specific work slows down the process of fitting and comparing new models.

BBVI removes that requirement. It uses stochastic optimisation of the ELBO, where each gradient is estimated from samples of the variational distribution, and it adds generic variance-reduction tools so that the estimates are usable in practice.

## Key concepts

- **Score function**: the gradient \(\nabla_\lambda \log q(z\mid\lambda)\) of the log density of the variational distribution. Its expectation under \(q\) is zero, and the identity that uses it gives unbiased gradient estimates.
- **Rao-Blackwellisation**: replacing a sampled term by its conditional expectation over the variables it does not depend on, which removes variance without adding bias.
- **Control variates**: subtracting a zero-mean function \(h\), scaled by a coefficient \(a\). The best \(a\) equals \(\mathrm{Cov}(f,h)/\mathrm{Var}(h)\), and the paper estimates it from the same samples.
- **Robbins–Monro step sizes**: a decreasing sequence of learning rates that lets noisy gradient ascent converge.

## How it works

The gradient of the ELBO can be written as an expectation under the variational distribution:

\[
\nabla_\lambda \mathcal{L} = \mathbb{E}_{q}\Big[\nabla_\lambda \log q(z\mid\lambda)\big(\log p(x,z) - \log q(z\mid\lambda)\big)\Big].
\]

Averaging over \(S\) samples \(z_s \sim q(z\mid\lambda)\) gives an unbiased estimate. The paper applies the Rao-Blackwellised estimator, which exploits the mean-field factorisation, and then subtracts a control variate built from the score function. The procedure is:

1. Initialise the variational parameters \(\lambda\).
2. Draw \(S\) samples from \(q(z\mid\lambda)\).
3. Form the variance-reduced gradient estimate, with the control-variate coefficient estimated from the same samples.
4. Update \(\lambda\) with a step size \(\rho_t\) from a Robbins–Monro sequence.
5. Stop when \(\lambda\) changes by less than a threshold (0.01 in the paper).


## Results

The paper evaluates BBVI on a hospital dataset, and on a sampling baseline.

- **Against sampling.** On one model, BBVI was compared with Metropolis–Hastings inside Gibbs sampling under a fixed budget of 20 hours. BBVI reached better held-out predictive likelihood, and reached it sooner. The Gibbs sampler's progress slowed considerably after about five hours (Figure 1).
- **Variance.** Rao-Blackwellisation reduced the variance of the gradient by several orders of magnitude, and control variates reduced it further. Without these steps the basic algorithm made no noticeable progress in the time allowed (Figure 2).
- **Model exploration.** The data come from 976 patients with chronic kidney disease, with 17 laboratory measurements at each visit. Four non-conjugate models were fitted with the same code. The best model scored a held-out predictive likelihood of −32.7 and the weakest −175. The paper attributes the gap to modelling the time structure and to the negative correlations between labs (Table 1).

## Limitations

- **Noise remains.** Variance reduction lowers the noise of the gradient but does not remove it, so the method needs many samples per step.
- **Tuning.** The paper sets the AdaGrad scaling separately for each model, so step sizes still need tuning.
- **Weak baseline.** The sampling comparison uses one simple sampler on one model. The authors note that Hamiltonian Monte Carlo might do better.
- **Local optima.** The ELBO is generally non-convex, so the result depends on initialisation (Blei et al., 2016).

## Open questions

- How does the score-function estimator compare with reparameterised gradients on high-dimensional continuous models? The survey by Mohamed et al. (2019) sets out the trade-offs between estimator types.
- Can step-size and variance-reduction choices be automated, so that the black-box promise holds in practice?

## References

### Seminal papers

- Ranganath, R., Gerrish, S. & Blei, D. M. (2013). *Black Box Variational Inference*. arXiv. https://arxiv.org/abs/1401.0118 — Introduces the score-function estimator with Rao-Blackwellisation and control variates, which makes the ELBO optimisable for many models.
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2012). *Stochastic Variational Inference*. arXiv. https://arxiv.org/abs/1206.7051 — Scales variational inference to large corpora by using noisy natural gradients on minibatches.
- Mnih, A. & Gregor, K. (2014). *Neural Variational Inference and Learning in Belief Networks*. arXiv. https://arxiv.org/abs/1402.0030 — Trains a feedforward inference network with a score-function estimator whose high variance is reduced by several simple methods.
- Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine Learning*. https://doi.org/10.1007/BF00992696 — Introduces the REINFORCE family of score-function gradient estimators, the same identity that BBVI uses.

### Surveys and textbooks

- Mohamed, S., Rosca, M., Figurnov, M. & Mnih, A. (2019). *Monte Carlo Gradient Estimation in Machine Learning*. arXiv. https://arxiv.org/abs/1906.10652 — Surveys pathwise, score-function and measure-valued gradient estimators.
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — Reviews mean-field and coordinate-ascent methods, and the ELBO's local optima and variance underestimation.
- Zhang, C., Butepage, J., Kjellstrom, H. & Mandt, S. (2017). *Advances in Variational Inference*. arXiv. https://arxiv.org/abs/1711.05597 — Reviews scalable and black-box variational methods and flexible families.

### Articles and documentation

- Kucukelbir, A., Tran, D., Ranganath, R., Gelman, A. & Blei, D. M. (2016). *Automatic Differentiation Variational Inference*. arXiv. https://arxiv.org/abs/1603.00788 — Derives a variational algorithm automatically from the model alone.
