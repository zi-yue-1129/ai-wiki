---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning
  - theory/paradigms/unsupervised/dimensionality-reduction
tags:
  - mathematics
  - linear algebra
aliases:
  - 線性代數
  - Linear algebra for AI
  - Matrix factorisation
---

# Linear Algebra for AI

Linear algebra describes data as vectors and transformations as matrices. Almost every layer of a neural network, every embedding and every attention score is built from products of vectors and matrices, so this page covers the parts of the subject that AI uses most. It is the largest part of the [mathematics overview](../index.md).

## Overview

A vector is an ordered list of numbers. It can be read as a point in space or as a direction. A matrix is a table of numbers that acts on vectors: multiplying a vector by a matrix rotates, stretches or projects it. A neural-network layer computes \(y = \sigma(Wx + b)\), where \(W\) is a matrix that transforms the input and \(\sigma\) is a nonlinearity. Most of the arithmetic in training and inference is spent on such matrix products.

Three questions organise the subject. What does a transformation do to space? The directions it stretches most are given by its eigenvectors and singular vectors. How much information does a matrix really carry? That is its rank. How do we measure distances and similarities between vectors? That is the job of norms and inner products.

## Key concepts

- **Inner product and cosine similarity**: \(\mathbf{a}\cdot\mathbf{b} = \sum_i a_i b_i\). Normalising it by the vector lengths gives the cosine similarity used in semantic search and in comparing embeddings.
- **Matrix shapes**: multiplying an \(m\times n\) matrix by an \(n\times p\) matrix gives an \(m\times p\) matrix. Many bugs in deep-learning code are shape bugs.
- **Rank**: the number of linearly independent columns. A rank-\(r\) matrix can be written as a sum of \(r\) rank-one matrices.
- **Norms**: \(\|\mathbf{x}\|_2 = \sqrt{\sum_i x_i^2}\) and \(\|\mathbf{x}\|_1 = \sum_i |x_i|\). Penalties built from these norms regularise weights.
- **Projection**: the closest point to a vector within a subspace. Least-squares regression is a projection onto the span of the features.

## How it works

Two factorisations carry most of the weight in AI:

- [Eigendecomposition](eigendecomposition.md) writes a square symmetric matrix as \(A = Q\Lambda Q^\top\). The columns of \(Q\) are orthogonal eigenvectors and the diagonal of \(\Lambda\) holds the eigenvalues. It describes covariance matrices and the curvature of loss functions.
- [Singular value decomposition](svd.md) writes any matrix as \(A = U\Sigma V^\top\). The singular values on the diagonal of \(\Sigma\) rank the directions by importance, and keeping only the largest ones gives the best low-rank approximation:

\[
A_k = \sum_{i=1}^{k} \sigma_i\, \mathbf{u}_i \mathbf{v}_i^\top
\]

Projecting data onto the first \(k\) right singular vectors is principal component analysis (PCA). Low-rank adapters such as [LoRA](../../model-compression/low-rank-and-efficient-architectures/lora/index.md) apply the same low-rank idea to weight updates during fine-tuning.

## Key methods

Two landmark decompositions carry most of the subject. Each has its own page.

- [Singular value decomposition](svd.md): applies to any matrix, rectangular or square, and gives the optimal low-rank approximation.
- [Eigendecomposition](eigendecomposition.md): applies only to square matrices, and to symmetric ones it gives orthogonal directions of stretch.

Use SVD for rectangular data matrices and weight matrices. Use eigendecomposition for covariance and Hessian matrices, which are square and symmetric.

## Connections

- [Probability and statistics](../probability-statistics/index.md) uses covariance matrices, which are symmetric and positive semidefinite.
- [Calculus and optimisation](../calculus/index.md) uses the Hessian, whose eigenvalues measure curvature along each direction.
- [Principal component analysis](../../paradigms/unsupervised/dimensionality-reduction/pca.md) is the standard use of SVD and eigendecomposition in unsupervised learning.
- [Truncated SVD](../../model-compression/low-rank-and-efficient-architectures/truncated-svd/index.md) compresses trained weight matrices with the same rank truncation.
- Brain and cognition: neural recordings from many cells form matrices over time and neurons. Dimensionality-reduction methods such as PCA are widely used to find low-dimensional structure in such recordings. This is an analysis tool rather than a claim about how the brain computes.

## Applications

- **Low-rank fine-tuning**: LoRA freezes a pretrained weight matrix and learns a low-rank update, which keeps the number of trainable parameters small (Hu et al., 2021).
- **Model compression**: replacing a large weight matrix by a truncated SVD reduces storage and multiply cost, at the price of some approximation error.
- **Least squares**: the pseudoinverse \(A^+ = V\Sigma^+U^\top\) gives the least-squares solution of an overdetermined linear system, and it is computed through the SVD in practice.
- **Embeddings**: similarity search compares vectors with inner products, often after normalising them.

## Open questions

- How large a rank is enough? A truncation keeps the directions with the largest singular values, but no universal rule says how many to keep for a given task.
- Are weight updates during fine-tuning intrinsically low rank? Low-rank methods work well in many reported settings, but the answer depends on the model and task.
- Numerical precision: low-precision arithmetic, such as the [quantisation](../../model-compression/quantisation/index.md) used for training, changes the accuracy of matrix products, and the effect on decompositions is not fully characterised.

## References

### Seminal papers

- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika* 1(3), 211–218. https://doi.org/10.1007/BF02288367 — Proves that the best rank-k approximation of a matrix, in the least-squares sense, is given by a truncated decomposition. The result behind truncated SVD.
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Freezes pretrained weights and learns low-rank updates, the main modern use of low-rank structure in AI.

### Surveys and textbooks

- Stewart, G. W. (1993). On the early history of the singular value decomposition. *SIAM Review* 35(4), 551–566. https://doi.org/10.1137/1035134 — Surveys the work of Beltrami, Jordan, Sylvester, Schmidt and Weyl, who established the existence of the SVD and its theory.
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — Standard reference on the numerical algorithms behind decompositions, for readers who want to implement or analyse them.
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — Graduate textbook on numerical linear algebra, written for readers who want both the theory and its practical behaviour.

### Lectures

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — Undergraduate course whose lecture list covers elimination, eigenvalues, the singular value decomposition and projections. Suited to a first course.
