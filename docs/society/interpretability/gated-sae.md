---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - Gated SAE
  - Gated sparse autoencoder
  - Gated 稀疏自編碼器
  - 門控稀疏自編碼器
---

# Gated sparse autoencoders

A gated sparse autoencoder is a sparse autoencoder whose encoder has two paths. A gate decides which features are on, and a separate magnitude path estimates how strongly each active feature fires. Only the gate path receives the L1 penalty. Rajamanoharan et al. (2024) introduce the design to reduce shrinkage, the systematic underestimation of feature activations that an L1 penalty causes in a standard sparse autoencoder.

## Problem

A standard sparse autoencoder uses one ReLU encoder for two jobs: deciding which features are active, and estimating how large their activations are. An L1 penalty on the code pushes both toward zero. Deciding which features are on needs a sparsity pressure, but estimating their size does not, so a single penalty biases both. The result is shrinkage: reconstructions come out systematically smaller than the true activations, and the bias grows as the penalty increases.

## Core idea

Split the encoder into a gate and a magnitude path. A gate pre-activation passes through a Heaviside step, so a feature is on only when its gate is positive. A ReLU magnitude path then gives its strength, and only the gate path receives the L1 penalty. The magnitude path reuses the gate's directions, with a learned per-feature rescaling and its own bias, so the design adds only two parameters per feature over a baseline sparse autoencoder.

## Equation or algorithm

For a baseline sparse autoencoder with a ReLU encoder, the features and loss are

$$
f(x) = \mathrm{ReLU}\big(W_{\text{enc}}(x - b_{\text{dec}}) + b_{\text{enc}}\big), \qquad \mathcal{L} = \lVert x - \hat{x}(f(x)) \rVert_2^2 + \lambda \lVert f(x) \rVert_1
$$

The gated encoder uses a gate pre-activation $\pi_{\text{gate}}(x) = W_{\text{gate}}(x - b_{\text{dec}}) + b_{\text{gate}}$ and a magnitude pre-activation $\pi_{\text{mag}}(x) = W_{\text{mag}}(x - b_{\text{dec}}) + b_{\text{mag}}$:

$$
\tilde{f}(x) = \mathbf{1}\big[\pi_{\text{gate}}(x) > 0\big] \odot \mathrm{ReLU}\big(\pi_{\text{mag}}(x)\big)
$$

The magnitude weights are tied to the gate weights by a row-wise rescaling, $W_{\text{mag}} = \exp(r_{\text{mag}}) \odot W_{\text{gate}}$, where $r_{\text{mag}}$ is learned. The training loss is

$$
\mathcal{L}_{\text{gated}}(x) = \lVert x - \hat{x}(\tilde{f}(x)) \rVert_2^2 + \lambda \lVert \mathrm{ReLU}(\pi_{\text{gate}}(x)) \rVert_1 + \lVert x - \hat{x}_{\text{frozen}}\big(\mathrm{ReLU}(\pi_{\text{gate}}(x))\big) \rVert_2^2
$$

The last term is an auxiliary reconstruction that passes through a frozen copy of the decoder, so its gradient does not reach the decoder. The paper's ablations report that freezing this copy matters.

## Results

- **Reconstruction at fewer features.** At equal training compute, the paper reports a better trade-off than the baseline. The abstract puts it as needing about half as many firing features to reach comparable reconstruction fidelity.
- **Shrinkage.** Gated reconstructions are close to unbiased, with a fitted shrinkage coefficient near 1. Baseline sparse autoencoders have a coefficient below 1, and the bias worsens as the penalty grows.
- **Interpretability.** In a blinded rater study with 150 features from Pythia-2.8B and 192 from Gemma-7B, gated features were rated comparably interpretable. The one-sided test gave $p = 0.060$, so the authors conclude that gated features are at least comparable, not conclusively more interpretable.
- **Cost.** Computing the loss takes about 50% more compute per step, because the decoder runs twice. Wall-clock training time rises by less, since activation generation and I/O often dominate.

## Limitations

- **L1 remains.** The gate still receives an L1-type penalty, so the sparsity count is still a proxy for interpretability.
- **Interpretability gain not established.** The rater study does not show a clear improvement, and the paper says so.
- **Extra compute.** The decoder pass for the auxiliary term adds training cost per step.
- **Limited models.** The reported comparisons cover a small set of models and layers, so results on other models may differ.

## Connections

The gated design is one of the architectures that [JumpReLU sparse autoencoders](jumprelu-sae.md) compare against. The JumpReLU paper reports that its method is more faithful than the Gated SAE at a given sparsity, and the two papers share several authors. Both belong to the family described in [sparse autoencoders](sparse-autoencoders.md), alongside the top-k variant in [k-sparse autoencoders](k-sparse-autoencoders.md). The baseline that gated SAEs modify is the L1 design used by Cunningham et al. (2023). For the transformer architecture whose activations these methods read, see [transformers](../../theory/models/transformer/index.md).

## Applications

- Building feature dictionaries for language-model activations when shrinkage would bias later measurements.
- Comparing sparse autoencoder designs at matched numbers of active features.
- Separating the question "is this feature on?" from "how strongly is it on?" in an analysis.

## Open questions

- Does the interpretability advantage hold in larger rater studies?
- Does lower shrinkage improve causal tests, such as activation patching, as much as it improves reconstruction?
- Does the frozen auxiliary decoder help other architectures in the same way?

## References

### Seminal papers

- Rajamanoharan, S. et al. (2024). *Improving Dictionary Learning with Gated Sparse Autoencoders*. arXiv:2404.16014. https://arxiv.org/abs/2404.16014 — Introduces the gated encoder, which separates feature detection from magnitude estimation to reduce shrinkage.
- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Compares JumpReLU sparse autoencoders with Gated and TopK sparse autoencoders on Gemma 2 9B activations.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces top-k sparsity, an alternative to the L1 penalty.

### Surveys and textbooks

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies L1-penalised sparse autoencoders to language model activations, the baseline design that gated sparse autoencoders modify.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of JumpReLU sparse autoencoders for Gemma 2 models.
