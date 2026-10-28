---
tags:
  - unsupervised learning
  - representation learning
  - autoencoders
---

# Autoencoders and Representation Learning

Autoencoders learn to compress data through a bottleneck and reconstruct it. The bottleneck representation is useful on its own, and the same idea underlies much of modern representation learning.

## Overview

An autoencoder has an encoder $f_\phi$ that maps an input $x$ to a code $z$, and a decoder $g_\theta$ that maps the code back to $\hat x$. Training minimises reconstruction error $\lVert x-\hat x\rVert^2$, or a likelihood-based loss. A code is only useful if it captures structure, so the bottleneck, noise or sparsity constraints determine what is learned.

## Types of autoencoder

| Variant | Constraint | What it learns |
|---|---|---|
| Undercomplete | Code is smaller than input | Compressed summary, similar to PCA when linear |
| Denoising | Input corrupted before encoding | Robust features that undo the corruption |
| Sparse | Penalty on code activity | Parts-based features |
| Contractive | Penalty on Jacobian of encoder | Locally invariant features |
| Variational | Probabilistic code with a prior | A smooth latent space that can be sampled |
| Masked | Random patches hidden from the encoder | Context-based features, used for pre-training |

## Representation learning

A good representation makes downstream tasks easier with few labels. Autoencoders pre-train features by reconstruction; contrastive and masked methods pre-train features by predicting or matching views of the data (see [self-supervised learning](../../self-supervised/index.md)). Bengio, Courville and Vincent identify smoothness, disentangling of factors and depth as properties of useful representations.

## Connections

Linear autoencoders recover PCA, so [dimensionality reduction](../dimensionality-reduction/index.md) is a special case. Variational autoencoders are the latent-variable models of [density estimation](../density-and-generative-models/index.md). The encoder's code is also used for retrieval and as an embedding.

## Applications

Anomaly detection by reconstruction error, denoising scanned documents and medical images, compressing images for storage, learning features for downstream classification, and as the encoder inside latent diffusion models.

## Open questions

Reconstruction does not guarantee that the representation is useful, since the model can copy irrelevant detail. Measuring whether a representation is disentangled, and choosing the right pre-training objective for a new modality, are unresolved.

## References

### Seminal papers

- Hinton & Salakhutdinov (2006), "Reducing the dimensionality of data with neural networks", *Science* 313. https://pubmed.ncbi.nlm.nih.gov/16873662/ — Deep autoencoders pre-trained layer by layer, which outperform PCA on image data.
- Vincent, Larochelle, Bengio & Manzagol (2008), "Extracting and composing robust features with denoising autoencoders", ICML. https://icml.cc/imls/conferences/2008/papers/592.pdf — Denoising autoencoders learn features that are robust to input corruption.
- Kingma & Welling (2014), "Auto-encoding variational Bayes", ICLR, arXiv:1312.6114 — The variational autoencoder, a probabilistic version with a smooth latent space.
- He et al. (2022), "Masked autoencoders are scalable vision learners", CVPR, arXiv:2111.06377 — Masking most image patches and reconstructing them gives strong pre-trained vision models.

### Surveys and textbooks

- Bengio, Courville & Vincent (2013), "Representation learning: a review and new perspectives", *IEEE TPAMI* 35(8), arXiv:1206.5538 — Survey of what makes representations useful and how to learn them.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

- Goodfellow, Bengio & Courville, *Deep Learning* (2016), chapter 14 on autoencoders. Free online: https://www.deeplearningbook.org/
