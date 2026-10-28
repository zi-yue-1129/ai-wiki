---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models
  - theory/paradigms/probabilistic/variational-inference/normalising-flow-posteriors
tags:
  - generative models
  - normalising flows
  - density estimation
aliases:
  - 正規化流
  - 流模型
  - Normalising flows
  - Normalizing flows
  - Flow-based generative models
---

# Normalising Flows

A normalising flow is a generative model that turns a simple probability distribution into a complicated one through a chain of invertible, differentiable maps. Because every map can be inverted and its effect on volume can be computed, the model gives exact likelihoods for data and exact sampling from the same network.

## Overview

Most generative models accept a trade-off. Variational autoencoders optimise a lower bound on the likelihood. [GANs](../gan/index.md) produce samples but define no tractable density. [Diffusion models](../diffusion/index.md) are trained with a variational bound. Autoregressive models give exact likelihoods, but they generate one variable at a time. Normalising flows aim for exact likelihood and parallel computation, and pay for it with constraints on the architecture.

The construction is simple. Draw a base sample from a simple distribution, usually a standard Gaussian, and apply invertible maps. The change-of-variables rule gives the density of the output from the base density and the local volume change of the maps. Dinh et al. (2014) proposed NICE as a deep model for density estimation, and later work such as [RealNVP](realnvp/index.md) and [Glow](glow/index.md) applied the idea to images. Rezende and Mohamed (2015) showed that flows also give richer approximate posteriors for [variational inference](../../../probabilistic/variational-inference/index.md), covered in [Normalising Flow Posteriors](../../../probabilistic/variational-inference/normalising-flow-posteriors/index.md).

## Key concepts

- **Bijection**: a one-to-one, onto map whose inverse is also differentiable. Flows are built from bijections.
- **Base distribution**: the simple density, such as a standard Gaussian, from which sampling starts.
- **Change of variables**: the rule that relates the density of the base variable to that of its image. It contains the absolute Jacobian determinant, which measures the local change of volume.
- **Jacobian determinant**: the determinant of a \(D \times D\) matrix. Computing it naively costs roughly \(O(D^3)\), so practical flows choose maps whose Jacobians have simple structure.
- **Coupling layer**: a map that updates one part of a vector using a function of the other part. Its Jacobian is triangular. [RealNVP](realnvp/index.md) and [Glow](glow/index.md) use coupling layers.
- **Autoregressive transform**: a map in which each output depends only on earlier inputs, which also gives a triangular Jacobian. [Masked autoregressive flow](masked-autoregressive-flow/index.md) is built from these.
- **Continuous flow**: a map defined as the solution of an ordinary differential equation (ODE). The log-density changes by the trace of the Jacobian, rather than its determinant. [FFJORD](ffjord/index.md) is the landmark example.
- **Dequantisation**: pixel values and other discrete data are not continuous densities, so models add noise or map the values into a continuous space first.[^1]

## How it works

Write the model as a chain of \(K\) invertible maps that carry a base sample \(z_0\) to the data-like variable \(x = z_K\):

\[
z_k = f_k(z_{k-1}), \qquad z_0 \sim p_0
\]

The change-of-variables rule gives the log-density of \(x\) as the base log-density minus the sum of the log-determinants of the layers:

\[
\log p(x) = \log p_0(z_0) - \sum_{k=1}^{K} \log\left|\det \frac{\partial f_k}{\partial z_{k-1}}\right|
\]

Here \(z_0\) is the base value that the chain maps to \(x\), so it is recovered by running the inverse maps. Training chooses the parameters to maximise the average log-likelihood of the data. Because the likelihood is exact, the loss is its negative, and ordinary gradient-based optimisers apply.

The design problem has three demands. Each map should be expressive, its inverse should be cheap, and its log-determinant should be cheap. The landmark methods differ in how they meet them:

```mermaid
flowchart LR
    Z0["Base sample z0 ~ N(0, I)"] -->|"f1"| Z1["z1"]
    Z1 -->|"f2"| Z2["..."]
    Z2 -->|"fK"| X["Data-like sample x"]
```

In a continuous flow the sum becomes an integral. The log-density changes along a trajectory at a rate given by the trace of the Jacobian of the dynamics, an identity that Chen et al. (2018) call the instantaneous change of variables.

## Key methods

Four landmark methods are compared below. Each has its own page with the equations, the reported results and the limitations.

| Method | Year | Core device | Density evaluation | Sampling |
|---|---|---|---|---|
| [RealNVP](realnvp/index.md) | 2016 | Affine coupling layers in a multi-scale architecture | One parallel pass | One parallel pass |
| [Glow](glow/index.md) | 2018 | Actnorm, invertible 1×1 convolution and coupling | One parallel pass | One parallel pass |
| [Masked autoregressive flow](masked-autoregressive-flow/index.md) | 2017 | Autoregressive affine transforms | One parallel pass | \(D\) sequential passes |
| [FFJORD](ffjord/index.md) | 2018 | Continuous flow with a trace estimator | One ODE solve | One ODE solve |

The table shows the main trade-off. Coupling flows are fast in both directions, but each map is restricted so that its Jacobian stays triangular. Autoregressive flows evaluate densities quickly, but sampling is sequential. Continuous flows remove the structural constraint on the dynamics, and pay for it with ODE solves.

## Connections

- **Variational inference.** A flow can serve as an approximate posterior, trained through the evidence lower bound rather than the data likelihood. See [Normalising Flow Posteriors](../../../probabilistic/variational-inference/normalising-flow-posteriors/index.md).
- **Density estimation.** Flows are likelihood-based models, and sit with the other estimators in [Density Estimation and Generative Models](../index.md).
- **Flow matching and diffusion.** The continuous form of a flow is a continuous normalising flow (Chen et al., 2018). Training one by maximum likelihood means solving the ODE at every step. [Flow matching](../flow-matching/index.md) instead regresses the velocity field onto known targets, so no ODE is simulated during training (Lipman et al., 2022). Albergo and Vanden-Eijnden (2022) also avoid backpropagation through ODE solvers, with a quadratic loss, and Tong et al. (2023) generalise conditional flow matching to continuous flows.
- **Autoregressive models.** The factorisation used by language models is the one that [masked autoregressive flows](masked-autoregressive-flow/index.md) invert. Most such models use the architecture described in [Transformers](../../../../models/transformer/index.md).
- **Brain and mind.** No neural circuit has been identified that implements a normalising flow, so the link to the brain is conceptual. Perception can be framed as inference with an internal generative model, and a flow makes such a model explicit, with a density that can be evaluated directly. See [Predictive Coding](../../../../../brain-mind/predictive-coding/index.md).

## Applications

- **Density estimation.** MAF and RealNVP were evaluated on tabular datasets and natural image patches. See their method pages.
- **Image synthesis and manipulation.** Glow reports realistic synthesis and manipulation of large images (Kingma and Dhariwal, 2018). For creative uses, see [Art & Creativity](../../../../../applications/creative/index.md).
- **Speech.** Parallel WaveNet trains a feed-forward inverse-autoregressive flow to match a trained WaveNet, and generates speech more than 20 times faster than real time (van den Oord et al., 2017).
- **Molecular simulation.** Boltzmann generators learn an invertible coordinate transformation from a simple distribution to the equilibrium distribution of a many-body system, giving one-step equilibrium samples (Noé et al., 2019). See [Life Sciences](../../../../../applications/life-science/index.md).

## Open questions

- **Expressiveness against structure.** Every speed-up constrains the maps. Whether more flexible transforms that remain cheap to invert, such as splines, can close the gap with autoregressive and diffusion models on large datasets is not yet settled (Durkan et al., 2019; Ho et al., 2019).
- **Scale.** The landmark image results are on datasets up to 256 × 256 pixels. Whether flows can match diffusion models and autoregressive Transformers on the largest text-to-image and video tasks is an open comparison.
- **Cost of continuous flows.** Continuous flows need ODE solves during training, and the trace estimator adds variance. Flow matching and stochastic interpolants reduce this cost, but their trade-offs for exact likelihood are still being studied.

[^1]: Bits-per-dimension values reported under different dequantisation schemes are not directly comparable, because each scheme defines a different continuous density.

## References

### Seminal papers

- Rezende, D. J. & Mohamed, S. (2015). *Variational Inference with Normalizing Flows*. ICML. https://arxiv.org/abs/1505.05770 — Builds flexible approximate posteriors by composing invertible maps, and trains them inside deep latent Gaussian models.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — Proposes deep invertible maps with a trivial Jacobian determinant for modelling complex densities.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — Introduces affine coupling layers that change volume, giving exact likelihood and sampling on natural images.
- Papamakarios, G., Pavlakou, T. & Murray, I. (2017). *Masked Autoregressive Flow for Density Estimation*. NeurIPS. https://arxiv.org/abs/1705.07057 — Stacks autoregressive transforms into a flow that evaluates densities in parallel, generalising RealNVP.
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS. https://arxiv.org/abs/1807.03039 — Adds actnorm and invertible 1×1 convolutions to coupling flows, improving log-likelihood on image benchmarks.
- Chen, R. T. Q., Rubanova, Y., Bettencourt, J. & Duvenaud, D. (2018). *Neural Ordinary Differential Equations*. NeurIPS. https://arxiv.org/abs/1806.07366 — Defines continuous normalising flows through an ODE, trained by maximum likelihood with an ODE solver.
- Grathwohl, W., Chen, R. T. Q., Bettencourt, J., Sutskever, I. & Duvenaud, D. (2018). *FFJORD: Free-form Continuous Dynamics for Scalable Reversible Generative Models*. arXiv. https://arxiv.org/abs/1810.01367 — Uses Hutchinson's trace estimator so that the dynamics of a continuous flow can be an unrestricted neural network.
- Lipman, Y., Chen, R. T. Q., Ben-Hamu, H., Nickel, M. & Le, M. (2022). *Flow Matching for Generative Modeling*. arXiv. https://arxiv.org/abs/2210.02747 — Trains continuous normalising flows by regressing onto known vector fields, without simulating the flow during training.
- Albergo, M. S. & Vanden-Eijnden, E. (2022). *Building Normalizing Flows with Stochastic Interpolants*. arXiv. https://arxiv.org/abs/2209.15571 — Learns the velocity field of a continuous flow with a simple quadratic loss, avoiding backpropagation through ODE solvers.
- Durkan, C., Bekasov, A., Murray, I. & Papamakarios, G. (2019). *Neural Spline Flows*. NeurIPS. https://arxiv.org/abs/1906.04032 — Replaces affine transforms with monotonic rational-quadratic splines, which keep each map analytically invertible.
- Ho, J., Chen, X., Srinivas, A., Duan, Y. & Abbeel, P. (2019). *Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design*. ICML. https://arxiv.org/abs/1902.00275 — Studies three design choices of flows, including uniform dequantisation and affine coupling, and improves on them.
- Tong, A. et al. (2023). *Improving and generalizing flow-based generative models with minibatch optimal transport*. arXiv. https://arxiv.org/abs/2302.00482 — Generalises conditional flow matching as a simulation-free objective for continuous normalising flows.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Surveys flows from the viewpoint of probabilistic modelling and inference, including expressive power and design trade-offs.
- Kobyzev, I., Prince, S. J. D. & Brubaker, M. A. (2021). *Normalizing Flows: An Introduction and Review of Current Methods*. IEEE Transactions on Pattern Analysis and Machine Intelligence. https://doi.org/10.1109/TPAMI.2020.2992934 — A comprehensive review of how flows are constructed and used for distribution learning.

### Articles and documentation

- Noé, F., Olsson, S., Köhler, J. & Wu, H. (2019). *Boltzmann generators: Sampling equilibrium states of many-body systems with deep learning*. Science. https://doi.org/10.1126/science.aaw1147 — Applies learned invertible transformations to generate unbiased one-shot equilibrium samples of molecular systems.
- van den Oord, A. et al. (2017). *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*. arXiv. https://arxiv.org/abs/1711.10433 — Distils a sequential WaveNet into a feed-forward flow that generates speech faster than real time.
