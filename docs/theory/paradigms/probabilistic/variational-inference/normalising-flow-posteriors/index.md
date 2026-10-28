---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/generative-models
tags:
  - generative models
  - optimization
aliases:
  - 正規化流
  - 正規化流後驗
  - Normalising flows
  - Normalizing flows
---

# Normalising Flow Posteriors

Normalising-flow posteriors, introduced by Rezende and Mohamed (2015), make the variational family of [Variational Inference](../index.md) much richer. A simple density is transformed through a chain of invertible maps whose Jacobian determinants are cheap to compute, and the chain is trained together with the model, so the approximate posterior can take shapes that a Gaussian cannot.

## Overview

A mean-field family treats the latent variables as independent, and a Gaussian family cannot represent skew or strong dependence between variables. Rezende and Mohamed argue that this restriction limits the quality of inference.

Flows were already used as density models (Dinh et al., 2014). The 2015 paper uses them as the approximate posterior inside deep latent Gaussian models (Rezende et al., 2014), with an inference network that maps each data point to the parameters of its flow.

## Key concepts

- **Change of variables**: if \(z = f(z_0)\) is invertible, the density of \(z\) equals the base density at \(z_0\) divided by the absolute Jacobian determinant of \(f\).
- **Flow length \(K\)**: the number of transformations composed in the chain.
- **Planar flow**: \(f(z) = z + u\,h(w^\top z + b)\). It contracts and expands space perpendicular to a hyperplane.
- **Volume-preserving flow**: a transformation with determinant one, as in NICE. It is cheap but needs a separate mixing step between layers.

## How it works

For a chain \(z_K = f_K \circ \cdots \circ f_1(z_0)\), the density follows from the change-of-variables rule:

\[
\ln q_K(z_K) = \ln q_0(z_0) - \sum_{k=1}^{K}\ln\left|\det\frac{\partial f_k}{\partial z_{k-1}}\right|.
\]

For planar flows the determinant reduces, by the matrix determinant lemma, to \(|1 + u^\top\psi(z)|\) with \(\psi(z) = h'(w^\top z + b)\,w\). It therefore costs linear time in the dimension. The objective is the ELBO with this family:

\[
\mathcal{L} = \mathbb{E}_{q_0}\big[\log p(x, z_K) - \log q_K(z_K)\big].
\]

The training procedure is:

1. An inference network maps the data point \(x\) to the parameters of the flow.
2. Sample \(z_0\) from a simple base density.
3. Apply the \(K\) transformations and accumulate the log-determinant terms.
4. Estimate the ELBO with this sample, and backpropagate through the flow and the inference network, since the sample is a differentiable function of the parameters.
5. Anneal an inverse temperature \(\beta\) from 0.01 to 1 over the first 10,000 iterations.

## Results

The paper reports three kinds of evidence.

- **Two-dimensional densities.** For four non-Gaussian targets, approximation quality improves substantially as the flow length grows from 2 to 8 to 32. The planar flow and NICE reach similar performance with more layers, but the planar flow needs far fewer parameters (Figure 3).
- **Binarised MNIST.** Deep latent Gaussian models with 40 latent variables were trained for 500,000 updates. Table 2 gives upper bounds on the negative log-probability (lower is better). The diagonal-Gaussian posterior gave at most 89.9. The planar flow gave at most 87.5 with \(K = 10\) and 85.1 with \(K = 80\). NICE with \(K = 80\) gave at most 87.2 (Table 2).
- **CIFAR-10 patches.** Longer flows systematically improved test log-likelihood (Table 3).


## Limitations

- **Cost.** Each layer adds parameters and computation, and a planar layer contracts or expands space in one direction only, so many layers may be needed.
- **Structure.** Cheap determinants restrict the form of each map. Papamakarios et al. (2019) review the design trade-offs between expressiveness and cost.
- **Inherited limits.** A richer family does not change the non-convexity of the ELBO (Blei et al., 2016). Cremer et al. (2018) find that error in amortised inference often comes from imperfect recognition networks rather than from the limited complexity of the approximating distribution, so a flexible family may not help much if the inference network is poor.

## Open questions

- Which flow architecture gives the best trade-off in high dimensions? Papamakarios et al. (2019) set out the options. Kingma et al. (2016) propose an autoregressive flow for large latent spaces, and Glow (Kingma & Dhariwal, 2018) shows invertible convolutions working at scale.
- Can improvements to the family and to the inference network be combined to close the amortisation gap?

## References

### Seminal papers

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. arXiv. https://arxiv.org/abs/1505.05770 — Builds flexible posteriors by composing invertible maps, with planar and radial flows, and trains them inside deep latent Gaussian models.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Proposes volume-preserving invertible maps for density modelling, compared here with planar flows.
- Rezende, D. J., Mohamed, S. & Wierstra, D. (2014). *Stochastic Backpropagation and Approximate Inference in Deep Generative Models*. arXiv. https://arxiv.org/abs/1401.4082 — Introduces the deep latent Gaussian models used in the experiments.
- Kingma, D. P., Salimans, T., Jozefowicz, R., Chen, X., Sutskever, I. & Welling, M. (2016). *Improving Variational Inference with Inverse Autoregressive Flow*. arXiv. https://arxiv.org/abs/1606.04934 — Proposes an autoregressive flow that scales to high-dimensional latent spaces and improves on diagonal Gaussian posteriors.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Reviews flows through the lens of probabilistic modelling and inference.
- Blei, D. M., Kucukelbir, A. & McAuliffe, J. D. (2016). *Variational Inference: A Review for Statisticians*. arXiv. https://arxiv.org/abs/1601.00670 — Reviews variational inference, its objective and the local optima of the ELBO.

### Articles and documentation

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. arXiv. https://arxiv.org/abs/1807.03039 — Uses invertible convolutions in a generative flow, with a significant gain in log-likelihood on standard benchmarks.
- Cremer, C., Li, X. & Duvenaud, D. (2018). *Inference Suboptimality in Variational Autoencoders*. arXiv. https://arxiv.org/abs/1801.03558 — Shows that much of the approximation error in trained VAEs comes from imperfect recognition networks.
