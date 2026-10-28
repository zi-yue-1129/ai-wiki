---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - JumpReLU SAE
  - JumpReLU sparse autoencoder
  - JumpReLU 稀疏自編碼器
---

# JumpReLU sparse autoencoders

A JumpReLU sparse autoencoder is a sparse autoencoder for language-model activations whose hidden units use a thresholded activation. Each feature has its own learned threshold: the encoder output passes through unchanged only if it exceeds that threshold, and is otherwise set to zero. Rajamanoharan et al. (2024) introduce it to improve reconstruction at a given level of sparsity, and to separate deciding whether a feature is active from estimating how strongly it is active.

## Problem

Sparse autoencoders for language models must do two things at once: reconstruct the model's activations faithfully, and keep most features inactive for each input. The common ReLU sparse autoencoder with an L1 penalty shrinks active features toward zero, which damages reconstruction. Top-k autoencoders fix the sparsity level but use a fixed number of active features per input. Rajamanoharan et al. note that training with an L1 penalty has known limitations, and they replace it with an L0 count of active features.

## Core idea

Replace the ReLU with a JumpReLU. Each feature $i$ has a threshold $\theta_i > 0$. If the encoder output for that feature is above $\theta_i$, the activation is passed through unchanged; otherwise it is zero. Because the threshold is separate from the activation value, the network can keep a feature's magnitude accurate once the feature is on, while the threshold decides whether it is on at all.

## Equation or algorithm

Let $\pi_i(x)$ be the encoder pre-activation for feature $i$. The JumpReLU feature activation is

$$
f_i(x) = \mathrm{JumpReLU}_{\theta_i}\big(\pi_i(x)\big) = \pi_i(x)\,\mathbf{1}\big[\pi_i(x) > \theta_i\big]
$$

and the reconstruction is $\hat{x} = W_{\text{dec}} f(x) + b_{\text{dec}}$. Training minimises reconstruction error plus a penalty on the number of active features,

$$
\mathcal{L} = \lVert x - \hat{x} \rVert^2 + \lambda \lVert f(x) \rVert_0
$$

where $\lVert f(x) \rVert_0$ counts the active features. The threshold is discontinuous, so the gradient of the count penalty with respect to the thresholds is zero almost everywhere. The paper handles this with a straight-through estimator, which passes gradients through the threshold as if it were a smooth function, so that the thresholds can be learned.

## Results

The abstract reports state-of-the-art reconstruction fidelity at a given sparsity level, compared with other recent sparse autoencoder architectures, including Gated and TopK SAEs. The experiments use activations from the Gemma 2 9B language model. The abstract does not give numerical results, so the comparison numbers are in the paper and are not repeated here.

## Limitations

- **Sparsity as a proxy.** The penalty counts active features, which is a proxy for interpretability. A sparse dictionary can still have features that are hard to interpret.
- **Training complexity.** The straight-through estimator and the thresholds add hyperparameters and training choices that must be tuned.
- **Feature splitting persists.** Like other dictionary learners, a JumpReLU dictionary can split concepts across features as its size grows.
- **Evidence scope.** The reported comparison is for one model family and a set of sparsity levels. Results on other models or on circuit-level analyses may differ.

## Connections

JumpReLU sits within the family of sparse autoencoders described in [sparse autoencoders](sparse-autoencoders.md), alongside the top-k variant described in [k-sparse autoencoders](k-sparse-autoencoders.md). The separation of "is it on" from "how strong" is a design choice rather than a claim about neurons, but it parallels the idea that a neuron has a firing threshold. The gated design that this paper compares against is described in [gated sparse autoencoders](gated-sae.md). For the transformer architecture whose activations the autoencoder reads, see [transformers](../../theory/models/transformer/index.md).

## Applications

- Building feature dictionaries for interpretability studies of large language models.
- Improving reconstruction when an autoencoder replaces part of a model during analysis.
- Comparing sparse autoencoder architectures at matched sparsity levels.

## Open questions

- Do JumpReLU features give more interpretable results than other architectures at matched reconstruction?
- How sensitive are the learned thresholds to the training schedule and the sparsity penalty?
- Does the gain in reconstruction carry over to the causal tests used in [mechanistic interpretability](mechanistic-interpretability.md)?

## References

### Seminal papers

- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Introduces a sparse autoencoder with a thresholded JumpReLU activation that improves reconstruction at a given sparsity.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces top-k sparsity, the main alternative to L1 penalties that JumpReLU is compared with.

### Surveys and textbooks

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies L1-penalised sparse autoencoders to language model activations, the setting in which JumpReLU is later applied.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of JumpReLU sparse autoencoders for Gemma 2 models.
