---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - brain-mind/neuroscience
tags:
  - dimensionality reduction
  - representation learning
aliases:
  - 主成分分析
  - PCA
  - Principal component analysis
  - Eigenfaces
  - 特徵臉
---

# Principal Component Analysis

Principal component analysis (PCA) finds the orthogonal directions along which a set of data varies most, and describes each data point by its coordinates along the leading directions. It is the linear member of the [dimensionality reduction](../../../paradigms/unsupervised/dimensionality-reduction/index.md) family and one of the three key methods of [linear algebra for AI](../index.md).

## Overview

Many datasets have far more measured features than underlying factors. Faces, gene-expression profiles and recordings from hundreds of neurons are examples. PCA looks for a few new axes that capture as much variation as possible, so the data can be described with fewer numbers.

Pearson (1901) introduced the geometric idea of the line or plane of closest fit to a cloud of points. Hotelling (1933) developed the method in the form still used, under the name principal components, and showed that the components are the eigenvectors of the covariance matrix. Its eigenvectors are orthogonal, so the components are uncorrelated.

## Key concepts

- **Centred data**: data $X \in \mathbb{R}^{n\times d}$ with the mean of each column subtracted. PCA is defined on centred data.
- **Covariance matrix**: $C = \frac{1}{n}X^\top X$, a symmetric positive semidefinite matrix whose entries are the covariances between features.
- **Principal component**: a unit vector $v$ that maximises the variance $v^\top C v$, subject to being orthogonal to the components already found.
- **Explained variance ratio**: for the $i$-th component with eigenvalue $\lambda_i$, the fraction $\lambda_i / \sum_j \lambda_j$ of the total variance.
- **Scores**: the coordinates $Z = XV_k$ of each data point along the first $k$ components.

## How it works

The first component solves

$$
v_1 = \arg\max_{\lVert v\rVert = 1} v^\top C v ,
$$

and the solution is the eigenvector of $C$ with the largest eigenvalue. The remaining components are the next eigenvectors. Writing $C = V\Lambda V^\top$, the top $k$ columns of $V$ give the best linear subspace of dimension $k$. The projection onto that subspace reconstructs the data with the smallest possible squared error among all rank-$k$ linear maps. This is the optimality result of the [truncated SVD](../truncated-svd/index.md), applied to centred data.

The algorithm has four steps:

1. Subtract the mean of each feature. Divide by the standard deviation as well when features have different units.
2. Compute the SVD $X = U\Sigma V^\top$. The columns of $V$ are the principal directions, and the variances are $\sigma_i^2 / n$. Forming $C$ first is less stable for ill-conditioned data.
3. Choose $k$ from a threshold on the cumulative explained variance, or from the needs of the next model.
4. Compute the scores $Z = XV_k$. To reconstruct, use $\hat X = ZV_k^\top$.

## Results

PCA is a closed-form procedure, so its main results are theoretical: the directions are the eigenvectors and the reconstruction is optimal among linear maps of the same rank. Empirical evidence concerns how it compares with other methods and how it has been used.

- **Faces.** Sirovich and Kirby (1987) represented face images with a small set of principal components. Turk and Pentland (1991) built a recognition system on the same idea, in which faces are projected onto a feature space spanned by these components, which they called eigenfaces. Their system recognises known individuals in near real time, according to the abstract.
- **Autoencoders versus PCA.** Hinton and Salakhutdinov (2006) trained deep autoencoders whose codes, by their abstract, work much better than PCA. Nonlinear encoders can thus beat the linear optimum in practice.
- **Neural populations.** Churchland and colleagues (2012) and Gallego and colleagues (2017) describe motor-cortex population activity in low-dimensional projections, often computed by PCA-like methods.

## Limitations

- **Linearity.** PCA can only find flat subspaces. A curved manifold of data is represented poorly by a few linear axes.
- **Variance is not relevance.** The direction of greatest variance may be noise, while the signal of interest sits in a low-variance one.
- **Scale dependence.** Features with large units dominate the components unless the data are standardised, which changes the answer.
- **Sensitivity to outliers.** Squared errors give extreme points large influence on the components.
- **Interpretation.** Each component is a weighted mix of all features, which can be hard to name.

## Open questions

- Which nonlinear extensions, such as kernel PCA or autoencoders, give representations that are both compact and stable across datasets?
- Do the leading components of neural population activity correspond to computations, or are they a by-product of the recording and the preprocessing?
- How should the number of components be chosen when the goal is prediction rather than description?

## References

### Seminal papers

- Hotelling, H. (1933). Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*. https://doi.org/10.1037/h0071325 — Introduces principal components as successive uncorrelated combinations of variables with the largest variance.
- Pearson, K. (1901). LIII. On lines and planes of closest fit to systems of points in space. *Philosophical Magazine*. https://doi.org/10.1080/14786440109462720 — Finds the lines and planes that best fit a cloud of points, the geometric origin of the method.
- Sirovich, L. & Kirby, M. (1987). Low-dimensional procedure for the characterization of human faces. *Journal of the Optical Society of America A*. https://doi.org/10.1364/JOSAA.4.000519 — Represents face images with a small set of principal components, an early use of PCA for faces.
- Turk, M. & Pentland, A. (1991). Eigenfaces for Recognition. *Journal of Cognitive Neuroscience*. https://doi.org/10.1162/jocn.1991.3.1.71 — Describes a face recognition system that projects images onto eigenfaces, the principal components of face images.
- Hinton, G. E. & Salakhutdinov, R. R. (2006). Reducing the Dimensionality of Data with Neural Networks. *Science*. https://doi.org/10.1126/science.1127647 — Compares deep autoencoder codes with PCA for dimensionality reduction, reporting that the autoencoder codes work better.
- Churchland, M. M. et al. (2012). Neural population dynamics during reaching. *Nature*. https://doi.org/10.1038/nature11129 — Analyses motor-cortex population activity during reaching using low-dimensional projections, a common use of PCA in neuroscience.
