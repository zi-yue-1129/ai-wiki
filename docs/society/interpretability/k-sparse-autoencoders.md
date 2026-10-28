---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - k-sparse autoencoders
  - Top-k sparse autoencoder
  - k-稀疏自編碼器
  - Top-k 稀疏自編碼器
---

# k-sparse autoencoders

A k-sparse autoencoder enforces sparsity by keeping only the $k$ largest hidden activations for each input and setting the rest to zero. Makhzani and Frey (2014) introduced it as an alternative to the L1 penalty used in most sparse autoencoders. Because sparsity is set by a count, not by a penalty weight, the method avoids the shrinkage of activations that an L1 penalty causes. Later language-model sparse autoencoders often use the same top-k rule.

## Problem

A standard sparse autoencoder trades off reconstruction error against an L1 penalty on the hidden code. The penalty weight must be tuned, the penalty pushes active units toward zero, and the resulting sparsity level is not set directly. Makhzani and Frey ask whether sparsity can be enforced exactly, in a way that is simple to train and gives useful features.

## Core idea

Replace the penalty with a hard constraint. After the encoder computes its hidden activations, keep the $k$ largest and zero all others. The decoder reconstructs the input from these few units. Because the rule itself produces sparsity, no penalty weight needs tuning, and the number of active units for every input is exactly $k$.

## Algorithm

1. Compute the hidden pre-activations $h = W_{\text{enc}} x + b$ for an input $x$.
2. Select the indices of the $k$ largest values of $h$.
3. Set all other entries of $h$ to zero, giving the sparse code $z$.
4. Reconstruct the input as $\hat{x} = W_{\text{dec}} z + c$.
5. Minimise the reconstruction error $\lVert x - \hat{x} \rVert^2$ by gradient descent. Gradients flow only through the $k$ selected units for each input.

The method's sparsity is therefore fixed by $k$, not by a penalty weight. The paper also describes using the learned features as inputs to a classifier.

## Results

Makhzani and Frey (2014) evaluate the method on MNIST and NORB. The abstract reports better classification than denoising autoencoders, networks trained with dropout, and restricted Boltzmann machines. The tables show that this advantage holds mainly for unsupervised features with a logistic-regression classifier. After fine-tuning the results are mixed: on MNIST, a deep dropout autoencoder reaches 0.85% error against 0.97% for the deep k-sparse model, and on NORB, deep dropout (7.0%) and a third-order RBM (6.5%) beat the deep k-sparse model (7.4%). The abstract also says that training is simple and encoding is very fast. The paper supports the speed claim only qualitatively, with no timing measurements.

## Limitations

- **Fixed $k$.** Every input receives exactly $k$ active units, even inputs that are simpler or more complex than average. A learned, input-dependent sparsity can fit the data better.
- **Dead units.** Some units may rarely or never enter the top $k$, so they learn nothing useful. The rule gives no direct pressure for every unit to be used.
- **Dataset scale.** The paper's experiments use image datasets of modest size. Its results do not show behaviour on large language-model activations.
- **Feature splitting.** Like other dictionary learners, a k-sparse autoencoder can split one concept into several features as its dictionary grows.

## Connections

The top-k rule is the approach used in later language-model sparse autoencoders, described in [sparse autoencoders](sparse-autoencoders.md). It is an engineering change to classical sparse coding, which in neuroscience is motivated by the efficient-coding idea discussed in [sparse coding](../../brain-mind/computational-neuroscience/sparse-coding/index.md). For the transformer architecture whose activations these methods analyse, see [transformers](../../theory/models/transformer/index.md).

## Applications

- Learning sparse features from image data with a fixed sparsity level.
- Pretraining encoders whose features are then used for classification.
- Analysing language-model activations with top-k dictionaries, as in later sparse autoencoder work.

## Open questions

- Is a fixed $k$ a good inductive bias for natural data, or does it impose an unnatural structure?
- How should dead units be avoided without changing the top-k rule?
- How do top-k features compare with features from input-dependent sparsity on the same model?

## References

### Seminal papers

- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Introduces the k-sparse autoencoder, which enforces sparsity by keeping only the k largest hidden activations.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*, 381, 607–609. https://doi.org/10.1038/381607a0 — Shows that a sparse coding objective trained on natural images produces receptive-field-like filters.

### Surveys and textbooks

- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies sparse autoencoders to language model activations, the setting where top-k variants are later used.
- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of sparse autoencoders for an open model family.
