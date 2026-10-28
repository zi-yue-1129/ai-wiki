---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/mlp
tags:
  - adversarial training
  - generative models
aliases:
  - 原始 GAN
  - 生成對抗網路原始論文
  - Generative adversarial nets
  - GAN (2014)
---

# Original GAN: Generative Adversarial Nets

The original GAN, introduced by Goodfellow et al. (2014), trains a generator and a discriminator as the two players of a minimax game. It is the method at the core of the [Generative Adversarial Networks](../index.md) topic, and the reference point for every later variant.

## Overview

Goodfellow et al. proposed a new way to estimate a generative model through an adversarial process. Two models are trained at the same time: a generative model \(G\) that captures the data distribution, and a discriminative model \(D\) that estimates whether a sample came from the training data or from \(G\). The paper's main case uses multilayer perceptrons (MLPs) for both networks. Such a system can be trained with backpropagation and dropout, and samples are drawn by a single forward pass, with no Markov chains or approximate inference.

The authors were motivated by the difficulty of maximum likelihood training for deep generative models, which the framework sidesteps.

## Key concepts

- **Noise prior and generator**: the generator \(G(z; \theta_g)\) is a differentiable function of noise \(z\) drawn from a prior \(p_z\). It defines a distribution \(p_g\) over data space without an explicit density.
- **Discriminator**: \(D(x; \theta_d)\) returns a single scalar, the probability that \(x\) came from the data rather than from \(p_g\).
- **Value function**: the game is defined by \(V(D, G)\), which the discriminator maximises and the generator minimises.
- **Optimal discriminator**: for a fixed \(G\), the best \(D\) is \(D^*_G(x) = p_{\text{data}}(x) / (p_{\text{data}}(x) + p_g(x))\).
- **Non-saturating objective**: a variant in which the generator maximises \(\log D(G(z))\) instead of minimising \(\log(1 - D(G(z)))\).

## How it works

The two players solve

\[
\min_G \max_D V(D, G) = \mathbb{E}_{x \sim p_{\text{data}}}\big[\log D(x)\big] + \mathbb{E}_{z \sim p_z}\big[\log\big(1 - D(G(z))\big)\big]
\]

In the paper's analysis the criterion for a fixed generator becomes \(C(G) = -\log 4 + 2\,\text{JSD}(p_{\text{data}} \,\|\, p_g)\), where JSD is the Jensen–Shannon divergence. Its minimum, \(-\log 4\), is reached only when \(p_g = p_{\text{data}}\). The proof assumes a non-parametric setting in which both networks have unlimited capacity.

In practice the paper uses minibatch stochastic gradients (Algorithm 1):

1. For \(k\) steps, sample \(m\) noise vectors and \(m\) real examples, then ascend the gradient of \(\frac{1}{m}\sum_i [\log D(x^{(i)}) + \log(1 - D(G(z^{(i)})))]\) with respect to the discriminator parameters.
2. Sample \(m\) new noise vectors and descend the gradient of \(\frac{1}{m}\sum_i \log(1 - D(G(z^{(i)})))\) with respect to the generator parameters.
3. Repeat. The experiments used \(k = 1\).

The paper notes that its convergence result does not carry over to MLPs, whose parameter space has many critical points.

## Results

The paper trains on MNIST, the Toronto Face Database (TFD) and CIFAR-10. Because the generator has no likelihood, it is evaluated by fitting a Gaussian Parzen window to generated samples and reporting the log-likelihood of held-out test data.[^1] On MNIST the adversarial nets score 225 ± 2, the highest value in the paper's table, ahead of deep GSN at 214 ± 1.1. On TFD they score 2057 ± 26, behind the stacked contractive autoencoder at 2110 ± 50. The authors say that the estimator has high variance and performs poorly in high dimensions. They make no claim that the samples are better than those of existing models, only that they are at least competitive.

## Limitations

- **Evaluation**: the Parzen estimate is coarse, and the paper calls for better ways to evaluate samplers without likelihoods.
- **Saturation**: the original generator loss gives little gradient early on, when the discriminator rejects poor samples confidently.
- **Theory gap**: the optimality proof is non-parametric, and convergence is not guaranteed for MLPs or other practical networks.
- **Stability**: later work shows that unregularised training may not converge, and that the objective can lead to vanishing gradients or mode collapse (Arjovsky et al., 2017; Mescheder et al., 2018).

## Open questions

- Which practical training procedures converge, and under what regularisation? Mescheder et al. (2018) give counterexamples for unregularised training.
- How should samples be scored when no likelihood is available? The Fréchet Inception Distance was introduced later to address this (Heusel et al., 2017).

## References

### Seminal papers

- Goodfellow, I. et al. (2014). *Generative Adversarial Nets*. NeurIPS. https://arxiv.org/abs/1406.2661 — The paper itself: the adversarial framework, the minimax objective, the proofs and the MLP experiments described here.
- Arjovsky, M. & Bottou, L. (2017). *Towards Principled Methods for Training Generative Adversarial Networks*. ICLR. https://arxiv.org/abs/1701.04862 — Analyses why GAN training is unstable and why the original objective saturates.
- Arjovsky, M., Chintala, S. & Bottou, L. (2017). *Wasserstein GAN*. ICML. https://arxiv.org/abs/1701.07875 — Proposes a different objective and reports that it removes problems such as mode collapse, with learning curves that track sample quality.
- Mescheder, L., Geiger, A. & Nowozin, S. (2018). *Which Training Methods for GANs do actually Converge?* ICML. https://arxiv.org/abs/1801.04406 — Shows counterexamples to unregularised GAN convergence and analyses which regularisers converge.
- Heusel, M. et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. NeurIPS. https://arxiv.org/abs/1706.08500 — Proposes the Fréchet Inception Distance, a sample-based score for GANs without a likelihood.

### Surveys and textbooks

- Creswell, A. et al. (2018). *Generative Adversarial Networks: An Overview*. IEEE Signal Processing Magazine. https://doi.org/10.1109/MSP.2017.2765202 — A review of the framework and its variants for signal-processing readers.

### Lectures and videos

- Goodfellow, I. (2016). *NIPS 2016 Tutorial: Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1701.00160 — The author's tutorial on the original framework, its training details and open problems, with exercises.

[^1]: Table 1 of Goodfellow et al. (2014). Parzen-window estimates have high variance, so small differences between methods in this table should not be over-read.
