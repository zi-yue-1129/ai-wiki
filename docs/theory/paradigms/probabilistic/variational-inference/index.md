---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/math/probability-statistics
  - theory/paradigms/unsupervised/density-and-generative-models/vae
tags:
  - probabilistic models
  - approximate inference
  - bayesian
aliases:
  - 變分推論
  - Variational Bayes
  - Variational inference
  - ELBO
---

# Variational Inference

Variational inference (VI) approximates a hard-to-compute posterior distribution by the closest distribution in a simpler, tractable family. It turns inference into optimisation: it maximises a lower bound on the log evidence, the evidence lower bound (ELBO). Part of [Probabilistic & Bayesian methods](../index.md).

## Overview

Bayesian inference asks for the posterior \(p(z\mid x)\) over latent variables \(z\) given data \(x\). Computing it needs the evidence \(p(x)=\int p(x,z)\,dz\), which is usually an intractable integral. Sampling methods such as [MCMC](../mcmc/index.md) estimate the posterior with a chain of samples. Variational inference instead chooses a distribution \(q(z)\) from a family that is easy to work with, and makes \(q\) as close to \(p(z\mid x)\) as possible.

Closeness is measured by the Kullback–Leibler divergence \(\mathrm{KL}(q\|p)\). Because the evidence is fixed, minimising this divergence is the same as maximising the ELBO. The method trades exactness for speed and scalability, and its accuracy depends on how expressive the family \(q\) is.

## Key concepts

- **Evidence**: \(p(x)\), the normalising constant that makes the posterior a distribution. It measures how well the model explains the data.
- **Evidence lower bound (ELBO)**: \(\mathcal{L}(q) = \mathbb{E}_q[\log p(x,z)] - \mathbb{E}_q[\log q(z)]\). It satisfies \(\log p(x) = \mathcal{L}(q) + \mathrm{KL}(q(z)\|p(z\mid x))\), so \(\mathcal{L}(q)\le\log p(x)\).
- **Variational family**: the set of candidate distributions \(q\). Mean-field families factorise over variables; richer families include normalising-flow posteriors.
- **Amortised inference**: a single neural network learns to output the approximate posterior for every data point, instead of optimising a separate \(q\) for each point.

## How it works

Maximising the ELBO improves the approximation and gives a bound on the evidence at the same time. For a model with observations \(x\) and latent variables \(z\), the gradient of the ELBO with respect to the parameters of \(q\) can be estimated with samples from \(q\). The reparameterisation trick makes the gradient low-variance when \(q\) is Gaussian, and the score-function estimator works for any \(q\) at higher variance (Ranganath et al., 2014).

Three choices define a variational method: the family of \(q\), how the ELBO is optimised, and whether the optimisation runs over each data point or is amortised across the dataset.

## Key methods

Four main routes are used in practice. Two have their own pages in this section, and the third is covered by the VAE page.

- [Mean-field variational inference](mean-field.md): factorises \(q\) over latent variables and updates each factor in turn. Exact coordinate updates exist for conjugate models (Jordan et al., 1999).
- [Stochastic variational inference](stochastic-variational-inference.md): optimises the ELBO with noisy gradients from data mini-batches, so it scales to very large datasets (Hoffman et al., 2013).
- [Variational autoencoder](../../unsupervised/density-and-generative-models/vae/index.md): amortised variational inference in which an encoder network produces \(q\) and a decoder network models the data (Kingma & Welling, 2014).

## Connections

- [Probability and statistics](../../../math/probability-statistics/index.md) gives the posterior, evidence and KL divergence that the method uses.
- [Markov chain Monte Carlo](../mcmc/index.md) is the sampling alternative. MCMC is asymptotically exact but slower; VI is biased but faster.
- The free-energy principle in neuroscience proposes that the brain minimises a quantity closely related to the ELBO. This is a theoretical proposal, not an established result, and it is discussed in the [neuroscience-AI connections](../../../../brain-mind/neuroai/index.md).

## Applications

- **Topic models**: scalable posterior approximation for latent Dirichlet allocation and related models (Blei et al., 2017).
- **Generative models**: VAEs for images, speech and molecules, which use amortised VI (Kingma & Welling, 2014).
- **Bayesian deep learning**: approximate posteriors over network weights, used to estimate uncertainty (Blei et al., 2017).

## Open questions

- The ELBO can be loose, so the approximating family limits accuracy. Richer families, such as normalising flows, reduce the gap at added computational cost.
- Mean-field factorisation underestimates posterior variance, and the reasons and remedies are an active research topic.
- Amortisation introduces an extra gap, and its size is hard to measure for a given dataset.

## References

### Seminal papers

- Jordan, M. I., Ghahramani, Z., Jaakkola, T. S. & Saul, L. K. (1999). An introduction to variational methods for graphical models. *Machine Learning* 37(2), 183–233. https://doi.org/10.1023/A:1007665907178 — Introduces variational methods for graphical models, including the bound and mean-field updates.
- Kingma, D. P. & Welling, M. (2014). Auto-encoding variational Bayes. *ICLR*. arXiv:1312.6114. https://arxiv.org/abs/1312.6114 — Introduces the VAE, an amortised VI method with the reparameterisation trick.
- Ranganath, R., Gerrish, S. & Blei, D. M. (2014). Black box variational inference. *AISTATS*. https://proceedings.mlr.press/v33/ranganath14.html — Gives a general gradient estimator for the ELBO that applies to models without conjugacy.
- Hoffman, M. D., Blei, D. M., Wang, C. & Paisley, J. (2013). Stochastic variational inference. *Journal of Machine Learning Research* 14. https://www.jmlr.org/papers/v14/hoffman13a.html — Scales VI to large datasets with stochastic natural-gradient updates.

### Surveys and textbooks

- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2017). Variational inference: a review for statisticians. *Journal of the American Statistical Association* 112(518), 859–877. https://doi.org/10.1080/01621459.2017.1285773 — Review of VI that explains the ELBO, mean-field and stochastic methods for statisticians.
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — Monograph linking variational methods to exponential families and log-partition functions.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers VI alongside sampling-based inference.
