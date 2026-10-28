---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/creative
tags:
  - generative models
  - normalising flows
  - density estimation
aliases:
  - Glow
  - Generative flow with invertible 1x1 convolutions
  - 可逆 1×1 卷積
  - Glow 生成流
---

# Glow

Glow (Kingma and Dhariwal, 2018) is a [normalising flow](../index.md) for images. Each step of the flow combines an actnorm layer, an invertible 1×1 convolution that mixes channels, and an affine coupling layer. It keeps the multi-scale design of [RealNVP](../realnvp/index.md), improves log-likelihood on the same image benchmarks, and shows realistic synthesis and manipulation of large images.

## Overview

RealNVP reverses the order of the channels between coupling layers. Glow replaces this fixed reversal with a learned invertible 1×1 convolution. The paper shows that this lowers the negative log-likelihood and speeds convergence, compared with either a reversal or a fixed random permutation.

Glow also replaces batch normalisation with actnorm. The authors give as the reason that batch normalisation degrades with small minibatches per processing unit, and large images force a minibatch of one. Actnorm is a per-channel scale and bias, initialised on a first minibatch so that activations start with zero mean and unit variance.

## Key concepts

- **Flow step**: actnorm, then a 1×1 convolution, then an affine coupling layer. The ablations use \(K = 32\) steps per level and \(L = 3\) levels.
- **Invertible 1×1 convolution**: a learned matrix \(W\) applied to the channel vector at every spatial position. It is invertible when \(W\) is non-singular.
- **LU parameterisation**: writing \(W\) as a permutation, a unit lower-triangular matrix and an upper-triangular matrix. This reduces the cost of its log-determinant from \(O(c^3)\) to \(O(c)\) for \(c\) channels.
- **Multi-scale architecture**: at each level the tensor is squeezed, the steps are run, and half of the channels are split off into the latent vector, as in RealNVP.

## How it works

For a tensor of height \(h\), width \(w\) and \(c\) channels, the paper gives the forward map and log-determinant of each component:

| Component | Forward map | Log-determinant |
|---|---|---|
| Actnorm | \(y_{i,j} = s \odot x_{i,j} + b\) | \(h \cdot w \cdot \sum \log\lvert s\rvert\) |
| Invertible 1×1 convolution | \(y_{i,j} = W x_{i,j}\) | \(h \cdot w \cdot \log\lvert\det W\rvert\) |
| Affine coupling | As in RealNVP, with scale \(s\) and shift \(t\) computed from half of the channels | \(\sum_j s_j\) over the coupled half |

The total log-determinant is the sum over all steps. The scale and shift networks are convolutional, with 512 channels in the hidden layers.

Training proceeds as follows:

1. Initialise each actnorm layer on the first minibatch.
2. At each level, squeeze the tensor, run the flow steps, and split off half of the channels.
3. Add the log-determinants and the log-density of the latent vector under a Gaussian prior, and maximise the average log-likelihood.

To sample, draw a latent vector from the prior and invert the steps. The paper finds that sampling from a reduced-temperature model, \(p_{\theta,T}(x) \propto p_\theta(x)^T\), often gives better samples. For additive couplings this scales the prior's standard deviation by \(T\). The paper's random samples use \(T = 0.7\).

## Results

On the image benchmarks, Glow reports lower bits per dimension than RealNVP on every dataset, using the same preprocessing:

| Dataset | RealNVP | Glow |
|---|---|---|
| CIFAR-10 | 3.49 | 3.35 |
| ImageNet 32 × 32 | 4.28 | 4.09 |
| ImageNet 64 × 64 | 3.98 | 3.81 |
| LSUN (bedroom) | 2.72 | 2.38 |
| LSUN (tower) | 2.81 | 2.46 |
| LSUN (church outdoor) | 3.08 | 2.67 |

In the CIFAR-10 ablation, the learned 1×1 convolution beats both alternatives for additive and affine couplings, and converges fastest. The paper reports about 0.2% more parameters and about 7% more wall-clock time. The paper also shows 256 × 256 CelebA-HQ samples and attribute edits, made by moving latent codes along directions learned from labels such as smiling.

## Limitations

- **Cost at high resolution.** The paper reports about 130 ms to generate a 256 × 256 image at batch size one on one GPU. Training at this scale needs gradient checkpointing and one image per device.
- **Memory with depth.** Activation memory grows with the number of steps, which reversibility could reduce; the authors leave this to future work.
- **Dequantisation.** Glow inherits the discretisation issue of image density models, which Ho et al. (2019) show affects the likelihood that flows achieve.
- **Scope.** The attribute experiments use faces with binary labels, and the paper does not test other image domains.

## Open questions

- Which channel-mixing and coupling designs give the best likelihood per parameter? Flow++ (Ho et al., 2019) and neural spline flows (Durkan et al., 2019) change the coupling transform itself.
- Can the memory cost of deep flows be cut in practice, as the reversibility argument suggests, without losing exact likelihood?

## References

### Seminal papers

- Kingma, D. P. & Dhariwal, P. (2018). *Glow: Generative Flow with Invertible 1x1 Convolutions*. NeurIPS. https://arxiv.org/abs/1807.03039 — The paper itself: actnorm, invertible 1×1 convolutions, the image benchmarks and the face-editing experiments discussed here.
- Dinh, L., Sohl-Dickstein, J. & Bengio, S. (2016). *Density estimation using Real NVP*. arXiv. https://arxiv.org/abs/1605.08803 — The coupling architecture and multi-scale design that Glow extends, and the baseline for the comparisons above.
- Ho, J., Chen, X., Srinivas, A., Duan, Y. & Abbeel, P. (2019). *Flow++: Improving Flow-Based Generative Models with Variational Dequantization and Architecture Design*. ICML. https://arxiv.org/abs/1902.00275 — Shows that uniform dequantisation and affine coupling choices limit flows, and improves on them.
- Durkan, C., Bekasov, A., Murray, I. & Papamakarios, G. (2019). *Neural Spline Flows*. NeurIPS. https://arxiv.org/abs/1906.04032 — Replaces the affine coupling transform with splines that remain analytically invertible.

### Surveys and textbooks

- Papamakarios, G., Nalisnick, E., Rezende, D. J., Mohamed, S. & Lakshminarayanan, B. (2019). *Normalizing Flows for Probabilistic Modeling and Inference*. arXiv. https://arxiv.org/abs/1912.02762 — Surveys flows, with a discussion of the design trade-offs that Glow's components address.
