---
tags:
  - unsupervised learning
  - dimensionality reduction
  - visualisation
---

# Dimensionality Reduction

Dimensionality reduction maps high-dimensional data to a smaller set of coordinates while keeping the structure that matters. It supports compression, denoising, visualisation and as a preprocessing step for other models.

## Overview

Real data often lies near a low-dimensional subspace or manifold. Dimensionality reduction tries to find that structure. Methods differ in what they preserve: variance, statistical independence, non-negativity of parts, or local neighbourhoods.

## Linear methods

- **Principal component analysis (PCA)** finds orthogonal directions of maximal variance. Equivalently, it gives the best rank-$k$ linear reconstruction in squared error, computed from the eigenvectors of the covariance matrix or the singular value decomposition.
- **Independent component analysis (ICA)** finds sources that are statistically independent, not merely uncorrelated. It solves the "cocktail party" problem, and it is used to remove eye-blink and muscle artefacts from EEG recordings.
- **Non-negative matrix factorisation (NMF)** writes a non-negative data matrix as the product of two non-negative factors. The parts are often easier to interpret, which is why it is used for topics and images.

## Nonlinear methods

- **t-SNE** converts distances into neighbour probabilities and matches the low-dimensional map to them, preserving local neighbourhoods well.
- **UMAP** builds a weighted neighbour graph and optimises a low-dimensional layout, usually faster than t-SNE and better at keeping some global structure.
- **Autoencoders** learn nonlinear encoders and decoders through a bottleneck; see [autoencoders and representations](../autoencoders-and-representations/index.md).

!!! warning "Reading maps"
    In t-SNE and UMAP, cluster sizes and distances between distant clusters are not meaningful. Use these plots to find structure, then check it with the data.

## Choosing a method

PCA first, for speed and interpretability. Use ICA when independence matters, NMF for non-negative data such as counts and spectra, and t-SNE or UMAP only for visualisation or for exploring neighbourhoods. Always check that the result holds up after adjusting the hyperparameters.

## Connections

PCA is the linear special case of the autoencoder, and kernel PCA is a nonlinear version. The reduced space is often where [clustering](../clustering/index.md) works best. Self-supervised pre-training produces similar low-dimensional representations, see [self-supervised learning](../../self-supervised/index.md).

## Applications

Visualising single-cell gene expression, compressing sensor and financial data, removing noise from images and spectra, extracting topics from text, and speeding up nearest-neighbour search.

## Open questions

Preserving local structure is easy, but reliably preserving global geometry is not. Choosing the target dimension and checking that reduction did not hide the signal of interest remain practical challenges.

## References

### Seminal papers

- Hyvärinen & Oja (2000), "Independent component analysis: algorithms and applications", *Neural Networks* 13(4–5). https://itb.biologie.hu-berlin.de/%7Ekempter/Teaching/2004_SS/hyvarinen_oja_2000.pdf — The standard tutorial on ICA, its assumptions and its fast algorithms.
- Lee & Seung (1999), "Learning the parts of objects by non-negative matrix factorization", *Nature* 401. https://doi.org/10.1038/44565 — Shows that non-negativity yields parts-based representations of images.
- van der Maaten & Hinton (2008), "Visualizing data using t-SNE", *JMLR* 9. https://jmlr.org/papers/v9/vandermaaten08a.html — Introduces t-SNE, the most widely used method for two-dimensional visualisation.
- McInnes, Healy & Melville (2018), "UMAP: Uniform Manifold Approximation and Projection for dimension reduction", [arXiv:1802.03426](https://arxiv.org/abs/1802.03426) — Introduces UMAP, a faster neighbour-graph method that also keeps more global structure.

### Surveys and textbooks

- Jolliffe, *Principal Component Analysis*, Springer (2002). https://link.springer.com/doi/10.1007/b98835 — The standard reference on PCA and its many variants, with applications.

### Lectures and videos


### Articles and documentation

(none beyond the entries above)

## Further learning

- StatQuest with Josh Starmer, episodes on principal component analysis, YouTube. https://www.youtube.com/@statquest — Animated explanation of PCA, with the variance and loading ideas made concrete.
