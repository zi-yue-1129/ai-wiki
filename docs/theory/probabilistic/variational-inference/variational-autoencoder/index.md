---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/generative
  - theory/paradigms/unsupervised/autoencoders-and-representations
tags:
  - generative models
  - representation learning
aliases:
  - 變分自編碼器
  - 變分自動編碼器
  - VAE
  - Variational autoencoder
---

# Variational Autoencoder

The variational autoencoder (VAE), introduced by Kingma and Welling (2013), trains a latent-variable generative model and an encoder network together by maximising a variational bound. It is the best-known example of amortised variational inference, one of the methods in the [Variational Inference](../index.md) overview.

## Overview

A VAE treats the code of an autoencoder as a latent variable \(z\) with prior \(p(z)\), and the data \(x\) as drawn from a decoder \(p_\theta(x\mid z)\). The posterior \(p_\theta(z\mid x)\) is intractable, so the VAE learns an encoder \(q_\phi(z\mid x)\) that approximates it, and both networks are trained with one objective.

Earlier variational methods fitted a separate approximation for each data point. The VAE shares one encoder across all points, so inference for a new point costs one forward pass. Kingma and Welling pair this with a gradient estimator that differentiates through the sampling step, which makes deep models trainable with ordinary stochastic gradient methods.

## Key concepts

- **Encoder (recognition model)** \(q_\phi(z\mid x)\): a network that outputs the parameters of a distribution over \(z\), usually Gaussian.
- **Decoder** \(p_\theta(x\mid z)\): a network that gives the distribution of the data for a given code.
- **Reparameterisation trick**: writing a sample as a differentiable function of the parameters and of noise that does not depend on them. For a Gaussian, \(z = \mu_\phi(x) + \sigma_\phi(x)\odot\varepsilon\) with \(\varepsilon\sim\mathcal N(0, I)\).
- **Amortised inference**: one inference network serves every data point, so the cost of inference is paid during training.

## How it works

The bound on the log-likelihood of one data point is

\[
\mathcal{L}(\theta,\phi;x) = \mathbb{E}_{q_\phi(z\mid x)}\big[\log p_\theta(x\mid z)\big] - \mathrm{KL}\big(q_\phi(z\mid x)\,\|\,p(z)\big).
\]

The first term rewards good reconstructions; the second penalises encodings that drift from the prior. For a Gaussian encoder and prior the KL term has a closed form, so only the reconstruction term is estimated by sampling (Kingma & Welling, 2013, Appendix B). With \(z^{(l)} = g_\phi(\varepsilon^{(l)}, x)\) and \(\varepsilon^{(l)}\sim p(\varepsilon)\), the reconstruction term becomes

\[
\mathbb{E}_{q_\phi}\big[\log p_\theta(x\mid z)\big] \approx \frac{1}{L}\sum_{l=1}^{L}\log p_\theta\big(x\mid z^{(l)}\big),
\]

which is differentiable in both \(\theta\) and \(\phi\). The minibatch procedure in the paper is:

1. Draw a minibatch of \(M\) data points.
2. For each point, draw \(L\) noise samples and form the codes \(z^{(l)} = g_\phi(\varepsilon^{(l)}, x)\).
3. Compute the estimated bound over the minibatch and its gradient with respect to \(\theta\) and \(\phi\).
4. Take a stochastic gradient ascent step on both sets of parameters, and repeat.


## Results

The paper trains generative models on MNIST and the Frey Face dataset. Its main comparison uses the same encoder and decoder under two training methods: the proposed estimator and the wake-sleep algorithm of Hinton et al. (1995).

- **Bound during training.** On both datasets, and for every latent dimensionality tested, the VAE converged considerably faster than wake-sleep and reached a higher bound. Adding latent units did not cause overfitting (Figure 2 of the paper).
- **Marginal likelihood.** For a three-dimensional latent space on MNIST, the VAE and wake-sleep converged faster than a Monte Carlo EM baseline with Hybrid Monte Carlo, which could not be applied to the full dataset (Figure 3 of the paper).

These results are shown as curves and measure how well the bound and likelihood are optimised. They say little about sample quality.

## Limitations

- **Restricted posterior.** The VAE usually assumes an approximately factorial posterior with parameters from a regression network. Burda et al. (2015) argue that this can give overly simple representations that do not use the model's full capacity.
- **Amortisation gap.** One encoder cannot find the best local posterior for every point. Cremer et al. (2018) find that much of the error in trained VAEs comes from imperfect encoders.
- **Bound, not likelihood.** The ELBO is a lower bound, so it does not give the exact fit of the model to the data.

## Open questions

- Can the bound be tightened without losing the speed of amortised inference, and do tighter bounds give better representations? Burda et al. (2015) report richer latent spaces, but the link to usefulness is not settled.
- How much of the amortisation gap needs a richer family rather than a better encoder? [Normalising flow posteriors](../normalising-flow-posteriors/index.md) address this.

## References

### Seminal papers

- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — Introduces the VAE, the reparameterised estimator of the variational bound and the shared recognition model.
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. arXiv. https://arxiv.org/abs/1401.4082 — Derives the same reparameterised gradient for deep latent-variable models.
- Hinton, G. E., Dayan, P., Frey, B. J. & Neal, R. M. (1995). The "Wake-Sleep" Algorithm for Unsupervised Neural Networks. *Science*. https://doi.org/10.1126/science.7761831 — Trains a multilayer generative network with a separate recognition network, the paper's baseline.

### Surveys and textbooks

- Kingma, D. P. & Welling, M. (2019). *An Introduction to Variational Autoencoders*. arXiv. https://arxiv.org/abs/1906.02691 — The authors' tutorial on the VAE and its extensions.
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — Places the VAE objective within general variational inference.

### Articles and documentation

- Burda, Y., Grosse, R. & Salakhutdinov, R. (2015). *Importance Weighted Autoencoders*. arXiv. https://arxiv.org/abs/1509.00519 — Proposes a tighter bound from several importance-weighted samples, with richer latent representations than the VAE.
- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. arXiv. https://arxiv.org/abs/1801.03558 — Shows that much of the approximation error in trained VAEs comes from imperfect recognition networks.
