---
related:
  - theory/paradigms/unsupervised/density-and-generative-models/generative-models
tags:
  - unsupervised learning
  - density estimation
  - generative models
---

# Density Estimation and Generative Models

Density estimation learns the probability distribution $p(x)$ behind unlabelled data. A model that can assign a probability to any input can also generate new samples and flag unusual inputs.

## Overview

Given samples from an unknown distribution, density estimation asks for a function $p_\theta(x)$ that places high probability where data occur. Models differ in whether they give an exact likelihood, can sample efficiently, or can be trained stably.

## Trade-offs between methods

Density methods differ in three properties: whether they give an exact likelihood, how fast they sample, and how stable their training is. Kernel density estimates and Gaussian mixtures have an exact likelihood and sample easily, but kernel methods scale poorly to high-dimensional data. GANs sample quickly but have no likelihood and train adversarially. Diffusion models train stably but sample in many iterative steps. The concrete families, with their pros and cons, are compared in [Generative Models](generative-models/index.md).

## Key ideas

**Maximum likelihood** chooses parameters that maximise $\sum_i \log p_\theta(x_i)$, which is equivalent to minimising the KL divergence between the data and the model. Most of the methods above are different ways to make this objective tractable.

**Normalising flows** map a simple base distribution through a sequence of invertible transformations. The change-of-variables formula gives the exact likelihood, and the Jacobian must be cheap to compute. Real NVP uses coupling layers that make this easy. See [Normalising Flows](normalising-flows/index.md), and [Flow Matching](flow-matching/index.md) for the continuous-time successor that trains flows without simulating them.

**Variational autoencoders** introduce latent variables and optimise an evidence lower bound. The encoder approximates the posterior and the decoder models the data, so generation and inference are both available. See [Variational Autoencoders](vae/index.md).

**GANs** train a generator against a discriminator without writing down a likelihood. Training is powerful but can be unstable, and mode collapse, where samples cover only part of the data, is a known risk. See [Generative Adversarial Networks](gan/index.md).

**Autoregressive models** factorise $p(x)$ into a product of conditionals and predict one element at a time, which gives an exact likelihood at the cost of sequential sampling. See [Autoregressive Generative Models](autoregressive/index.md).

## Connections

Clustering with Gaussian mixtures is density estimation with discrete latent variables, see [clustering](../clustering/index.md). Anomaly detection uses the estimated density, see [anomaly detection](../anomaly-detection/index.md). Modern generative systems are covered in [Generative Models](generative-models/index.md), and diffusion models have their own method pages in [Diffusion Models](diffusion/index.md).

## Applications

Synthetic data generation, image and audio synthesis, detecting out-of-distribution inputs, compressing data with learned probability models, and scientific simulation where likelihoods are needed for inference.

## Open questions

Likelihood is not the same as sample quality. A model can assign high likelihood to images that look wrong, which makes evaluation hard. Scaling exact-likelihood models to very high resolution, and understanding when generative models memorise their training data, remain active problems.

## References

### Seminal papers

- Dinh, Sohl-Dickstein & Bengio (2017), "Density estimation using Real NVP", ICLR, arXiv:1605.08803 — Coupling-layer normalising flows that give exact likelihoods for images.
- Kingma & Welling (2014), "Auto-encoding variational Bayes", ICLR, arXiv:1312.6114 — The variational autoencoder, which combines a latent-variable model with amortised inference.
- Goodfellow et al. (2014), "Generative adversarial networks", NeurIPS, arXiv:1406.2661 — Introduces adversarial training of a generator against a discriminator.
- Fraley & Raftery (2002), "Model-based clustering, discriminant analysis, and density estimation", *JASA* 97(458). https://sites.stat.washington.edu/raftery/Research/PDF/fraley2002.pdf — Defines Gaussian mixture density estimation and model selection.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

- Dempster, A. P., Laird, N. M. & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B*, 39(1), 1–38. https://doi.org/10.1111/j.2517-6161.1977.tb01600.x — Introduces the EM algorithm for maximum likelihood with latent variables, used to fit mixture models.

### Articles and documentation

(none beyond the entries above)

## Further learning

- StatQuest with Josh Starmer, episodes on Gaussian distributions and mixture models, YouTube. https://www.youtube.com/@statquest — Animated introduction to the Gaussian building blocks behind mixture density models.

## Further reading

- Murphy, *Probabilistic Machine Learning: Advanced Topics* (2023), chapters on normalising flows and generative models. Free online: https://probml.github.io/pml-book/book2
