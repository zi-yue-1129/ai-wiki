---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic/variational-inference/normalising-flow-posteriors
tags:
  - generative models
  - normalising flows
  - density estimation
aliases:
  - Masked autoregressive flow
  - MAF
  - 遮罩自回歸流
  - 自回歸流
---

# Masked Autoregressive Flow

Masked autoregressive flow (MAF), introduced by Papamakarios, Pavlakou and Murray (2017), is a [normalising flow](../index.md) built from autoregressive affine transforms. Each variable is transformed using only the variables before it, so the density of a data point is computed in one parallel pass, while sampling must proceed one variable at a time. MAF generalises [RealNVP](../realnvp/index.md) and is closely related to inverse autoregressive flow.

## Overview

An autoregressive model factorises a joint density into conditionals, \(p(x) = \prod_i p(x_i \mid x_{1:i-1})\), and gives exact likelihoods. The MADE architecture (Germain et al., 2015) computes all the conditionals in one pass, using masks so that output \(i\) depends only on inputs \(1, \ldots, i-1\). Sampling from MADE still takes \(D\) sequential passes.

MAF observes that an autoregressive model also defines a map from random numbers \(u\) to data \(x\). Each data variable is an affine function of its noise variable, with scale and shift that depend on the earlier data variables. This map is invertible, and its inverse, which recovers \(u\) from \(x\), needs only one masked pass. MAF uses that inverse for density evaluation and stacks several such maps to form a flow.

## Key concepts

- **Autoregressive conditional**: a Gaussian for \(x_i\) whose mean \(\mu_i\) and log-scale \(\alpha_i\) depend only on \(x_{1:i-1}\).
- **Random-number view**: the model is a transformation of i.i.d. Gaussian noise \(u\). The map from \(u\) to \(x\) is the generative direction, and its inverse gives the density.
- **Masking (MADE)**: binary masks on the weights of a feedforward network enforce the variable ordering.
- **Ordering**: autoregressive models depend on the order of the variables. MAF can use a different order in each layer, which avoids committing to a single ordering.
- **Inverse autoregressive flow (IAF)**: the same building blocks in the opposite direction, used by Kingma et al. (2016) for fast sampling at the cost of sequential density evaluation.

## How it works

Each conditional is Gaussian, with parameters given by the earlier variables:

\[
p(x_i \mid x_{1:i-1}) = \mathcal{N}\big(x_i \mid \mu_i, (\exp\alpha_i)^2\big), \qquad \mu_i = f_{\mu_i}(x_{1:i-1}), \quad \alpha_i = f_{\alpha_i}(x_{1:i-1})
\]

Sampling runs \(x_i = u_i \exp\alpha_i + \mu_i\) for \(i = 1, \ldots, D\), with \(u_i \sim \mathcal{N}(0,1)\). Each \(\mu_i\) and \(\alpha_i\) depends on the values already produced, so this recursion is sequential. The inverse map is

\[
u_i = (x_i - \mu_i)\exp(-\alpha_i)
\]

and all \(\mu_i\) and \(\alpha_i\) can be computed from the data at once. Its Jacobian is triangular with determinant \(\exp(-\sum_i \alpha_i)\), so

\[
\log p(x) = \log \mathcal{N}(u; 0, I) - \sum_{i=1}^{D} \alpha_i
\]

A stack of \(K\) such transforms adds one log-determinant term per layer. Training computes \(u\) for a minibatch in one masked pass per layer and maximises the average log-likelihood. Sampling draws \(u\) and runs the recursion, which the paper notes takes \(D\) sequential passes.

## Results

The paper evaluates unconditional density estimation on four UCI datasets and on 8 × 8 natural image patches from BSDS300. The scores are average test log-likelihoods in nats, where higher is better. Both models have ten layers:

| Dataset | RealNVP (10 layers) | MAF (10 layers) |
|---|---|---|
| POWER | 0.17 | 0.24 |
| GAS | 8.33 | 10.08 |
| HEPMASS | −18.71 | −17.73 |
| MINIBOONE | −13.84 | −12.24 |
| BSDS300 | 153.28 | 154.93 |

The paper reports that MAF outperforms RealNVP on every dataset. Its best single model on BSDS300, with mixture-of-Gaussian conditionals, reaches 156.36 nats.

## Limitations

- **Slow sampling.** Sampling takes \(D\) sequential passes, which is much slower than density evaluation for high-dimensional data.
- **Gaussian conditionals.** The affine transform assumes Gaussian conditionals. The mixture variant gives the best BSDS300 result, which suggests that richer conditionals matter.
- **Ordering.** A fixed ordering can fail to represent a simple density, as the paper's example shows. Varying the order across layers reduces the problem but does not remove the choice.

## Open questions

- Can a flow have both fast density evaluation and fast sampling? Parallel WaveNet (van den Oord et al., 2017) distils a sequential WaveNet into a feed-forward inverse autoregressive flow, which is one route to that goal.
- Are learned orderings, or orderings matched to the structure of the data, better than the fixed reversals used in the paper?

## References

### Seminal papers

- Papamakarios, G., Pavlakou, T. & Murray, I. (2017). *Masked Autoregressive Flow for Density Estimation*. NeurIPS. https://arxiv.org/abs/1705.07057 — The paper itself: the autoregressive affine transform, parallel density evaluation and the benchmark results discussed here.
- Germain, M., Gregor, K., Murray, I. & Larochelle, H. (2015). *MADE: Masked Autoencoder for Distribution Estimation*. ICML. https://arxiv.org/abs/1502.03509 — Uses binary masks in an autoencoder so that one pass computes all autoregressive conditionals.
- Kingma, D. P., Salimans, T., Jozefowicz, R., Chen, X., Sutskever, I. & Welling, M. (2016). *Improving Variational Inference with Inverse Autoregressive Flow*. NeurIPS. https://arxiv.org/abs/1606.04934 — Proposes the inverse direction of autoregressive flows, which samples in parallel and scales to high-dimensional latent spaces.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — Introduces the coupling flows that MAF generalises, and the baseline for its comparisons.
- van den Oord, A. et al. (2017). *Parallel WaveNet: Fast High-Fidelity Speech Synthesis*. arXiv. https://arxiv.org/abs/1711.10433 — Distils a sequential WaveNet into a feed-forward inverse autoregressive flow that generates speech faster than real time.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Surveys flows, including autoregressive designs and the trade-off between density evaluation and sampling.
