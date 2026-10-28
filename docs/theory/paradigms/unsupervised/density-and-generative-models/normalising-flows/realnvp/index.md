---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - generative models
  - normalising flows
  - density estimation
aliases:
  - Real NVP
  - RealNVP
  - 實值非體積保持變換
  - Real-valued non-volume preserving
---

# RealNVP

RealNVP (Dinh, Sohl-Dickstein and Bengio, 2016) is a [normalising flow](../index.md) built from affine coupling layers. Each layer copies half of its input unchanged and scales and shifts the other half, using functions of the copied half. Its inverse and Jacobian determinant are both cheap, so the model gives exact likelihoods and exact sampling.

## Overview

NICE (Dinh et al., 2014) introduced additive coupling layers. They shift one half of the input by a function of the other half, so their Jacobian determinant is one and they preserve volume. RealNVP adds a scale to each shift, so a layer can stretch some directions and shrink others. This is the "non-volume preserving" of the title.

## Key concepts

- **Affine coupling**: the input is split into \(x_{1:d}\) and \(x_{d+1:D}\). The first part passes through unchanged and conditions the transformation of the second part, which is scaled by \(\exp(s(\cdot))\) and shifted by \(t(\cdot)\). The functions \(s\) and \(t\) are arbitrary networks and never need inverting.
- **Masking and squeezing**: a binary mask sets which dimensions are copied. For images the paper alternates a spatial checkerboard with a channel-wise pattern, and squeezes each 2 × 2 block of pixels into channels.
- **Multi-scale architecture**: after some layers, half of the dimensions are factored out directly into the latent vector, and the rest continue through more layers.

## How it works

In the generative direction, the data are formed from the latent variables as

\[
x_{1:d} = z_{1:d}, \qquad x_{d+1:D} = z_{d+1:D} \odot \exp\big(s(z_{1:d})\big) + t(z_{1:d})
\]

The inverse needs no inversion of \(s\) or \(t\):

\[
z_{d+1:D} = \big(x_{d+1:D} - t(x_{1:d})\big) \odot \exp\big(-s(x_{1:d})\big)
\]

The Jacobian is block triangular, with an identity block and a diagonal block \(\operatorname{diag}(\exp s)\). Its log-determinant is therefore the sum of the scale outputs. For a stack of layers with a standard Gaussian base,

\[
\log p(x) = \log \mathcal{N}(z; 0, I) - \sum_{\text{layers}} \sum_j s_j
\]

where \(z\) is obtained by running the inverse maps on \(x\). In the paper, \(s\) is a \(\tanh\) output times a learned scale, and \(t\) is an affine output of a residual network.

Training maps each pixel into a continuous space with a logit transform, runs the data through the inverse direction of the multi-scale stack, and maximises the log-likelihood with Adam. Sampling draws \(z\) from the Gaussian and runs the generative direction, updating all dimensions of each layer in parallel.

## Results

The paper compares its bits-per-dimension scores with PixelRNN, an autoregressive baseline. Lower is better. CIFAR-10 is reported on the test set and the others on the validation set.

| Dataset | RealNVP | PixelRNN |
|---|---|---|
| CIFAR-10 (test) | 3.49 | 3.00 |
| ImageNet 32 × 32 (validation) | 4.28 | 3.86 |
| ImageNet 64 × 64 (validation) | 3.98 | 3.63 |

On LSUN and CelebA the paper reports 2.72 to 3.08 and 3.02. The authors say RealNVP does not improve on PixelRNN, but is competitive, and that performance grows with the number of parameters. Its natural-image samples look sharp.

## Limitations

- **Likelihood gap.** RealNVP is about 0.5 bits per dimension behind PixelRNN on CIFAR-10, and each layer leaves half of the dimensions unchanged, so many layers are needed.
- **Affine transforms.** Scale and shift are a limited way to reshape a distribution. Ho et al. (2019) list inexpressive affine flows among the limits of flows, and Durkan et al. (2019) replace them with splines.
- **Sample quality.** Maximum likelihood values diversity over sample quality when capacity is limited, and some CelebA samples are highly improbable.

## Open questions

- How much of the gap to autoregressive models comes from the coupling structure, and how much from the scale, dequantisation or conditioning choices? Later work such as [Glow](../glow/index.md) and Flow++ changed several of these at once.
- Can the transform be made more flexible while its inverse stays cheap? Splines are one answer, and the trade-off is not fully mapped.

## References

### Seminal papers

- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — The paper itself: affine coupling layers, the multi-scale architecture and the natural-image results discussed here.
- Dinh, L., Krueger, D. & Bengio, Y. (2014). *NICE: Non-linear Independent Components Estimation*. arXiv. https://arxiv.org/abs/1410.8516 — The predecessor with additive coupling layers, whose unit Jacobian determinant RealNVP generalises.
- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS. https://arxiv.org/abs/1807.03039 — Replaces the fixed channel reversal of RealNVP with learned invertible 1×1 convolutions.
- Ho, J., Chen, X., Srinivas, A., Duan, Y. & Abbeel, P. (2019). *Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design*. ICML. https://arxiv.org/abs/1902.00275 — Shows that the affine transform of coupling layers can be improved.
- Durkan, C., Bekasov, A., Murray, I. & Papamakarios, G. (2019). *Neural Spline Flows*. NeurIPS. https://arxiv.org/abs/1906.04032 — Replaces affine coupling transforms with monotonic splines that remain analytically invertible.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Surveys flows, including coupling designs and the trade-off between expressive power and cost.
