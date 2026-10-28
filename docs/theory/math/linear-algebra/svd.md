---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/model-compression/low-rank-and-efficient-architectures
tags:
  - mathematics
  - linear algebra
  - low rank
aliases:
  - 奇異值分解
  - Singular value decomposition
  - SVD
  - 截斷SVD
---

# Singular Value Decomposition (SVD)

The singular value decomposition factorises any real matrix into two rotations and a diagonal stretch, \(A = U\Sigma V^\top\). Keeping only its largest terms gives the best low-rank approximation of the matrix. This result underlies principal component analysis, low-rank compression and LoRA. Part of [Linear algebra](index.md).

## Overview

Every real \(m\times n\) matrix \(A\) can be written as \(A = U\Sigma V^\top\). The matrices \(U\) and \(V\) are orthogonal, so they only rotate or reflect vectors. The matrix \(\Sigma\) is diagonal, with non-negative entries \(\sigma_1 \ge \sigma_2 \ge \dots \ge 0\) called the singular values. Read from right to left, the map first rotates the input, then stretches along the coordinate axes by the singular values, then rotates the result.

Unlike an eigendecomposition, the SVD exists for every matrix, including rectangular ones, which is why it applies to data matrices and weight matrices.

## Key concepts

- **Singular values and vectors**: \(\sigma_i\) is a singular value, \(\mathbf{v}_i\) a right singular vector and \(\mathbf{u}_i\) a left singular vector. They satisfy \(A\mathbf{v}_i = \sigma_i \mathbf{u}_i\).
- **Rank**: the number of nonzero singular values.
- **Frobenius norm**: \(\|A\|_F^2 = \sum_i \sigma_i^2\), the square root of the sum of all squared entries.
- **Pseudoinverse**: \(A^+ = V\Sigma^+U^\top\), where \(\Sigma^+\) inverts the nonzero singular values. It gives least-squares solutions.

## How it works

The SVD is closely tied to the eigendecomposition. Since \(A^\top A = V\Sigma^2 V^\top\), the right singular vectors are eigenvectors of \(A^\top A\), and the squared singular values are its eigenvalues. The SVD can be computed by reducing the matrix to bidiagonal form and then running an iterative QR-type algorithm; see the algorithms chapters of Golub and Van Loan.

The key property is the Eckart–Young result. Keep the first \(k\) terms of the sum:

\[
A_k = \sum_{i=1}^{k} \sigma_i \mathbf{u}_i \mathbf{v}_i^\top
\]

Among all matrices \(B\) of rank at most \(k\), \(A_k\) is the closest to \(A\) in the Frobenius norm, and the error is

\[
\|A - A_k\|_F = \sqrt{\sum_{i>k} \sigma_i^2}.
\]

Eckart and Young (1936) proved this optimality for the least-squares criterion. The discarded singular values tell you exactly how much error the truncation introduces. A matrix whose singular values fall off quickly can be compressed with little loss; a flat spectrum cannot.

## Key methods

- [Eigendecomposition](eigendecomposition.md): factorises a square symmetric matrix into orthogonal eigenvectors. The SVD generalises it to any matrix, and for a symmetric positive semidefinite matrix the two factorisations coincide.
- [Truncated SVD](../../model-compression/low-rank-and-efficient-architectures/truncated-svd/index.md): the practical use of the Eckart–Young result to shrink a trained weight matrix.
- [Low-Rank Adaptation (LoRA)](../../model-compression/low-rank-and-efficient-architectures/lora/index.md): constrains the weight update to a low-rank product \(BA\) during fine-tuning, rather than factorising a trained matrix after the fact.

## Connections

- [Principal component analysis](../../paradigms/unsupervised/dimensionality-reduction/pca.md) takes the top right singular vectors of a centred data matrix as the principal directions.
- [Linear algebra](index.md) gives the overview of where the SVD sits among other matrix tools.
- For the brain, the SVD is an analysis tool for neural population data, not a model of neural computation.

## Applications

- **Compression**: truncated SVD of weight matrices reduces storage and multiply cost in deployed models.
- **Fine-tuning**: LoRA learns a rank-\(r\) update, with \(r\) far smaller than the matrix dimensions (Hu et al., 2021).
- **Dimensionality reduction**: PCA on high-dimensional data, computed through the SVD of the centred data matrix.
- **Least squares**: the pseudoinverse gives the minimum-norm least-squares solution of a linear system.

## Open questions

- Choosing the rank \(k\) for a given task. The spectrum tells you the error for each choice, but not which error is acceptable for downstream accuracy.
- Whether the singular-value spectrum of trained networks decays fast enough for truncation to be safe across layers and tasks.

## References

### Seminal papers

- Eckart, C. & Young, G. (1936). The approximation of one matrix by another of lower rank. *Psychometrika* 1(3), 211–218. https://doi.org/10.1007/BF02288367 — Gives the best rank-k approximation of a matrix in the least-squares sense, the basis of truncated SVD.
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685. https://arxiv.org/abs/2106.09685 — Learns low-rank weight updates during fine-tuning, a modern use of the rank-truncation idea.

### Surveys and textbooks

- Stewart, G. W. (1993). On the early history of the singular value decomposition. *SIAM Review*. https://epubs.siam.org/doi/10.1137/1035134 — History of the SVD. The abstract page was listed, but its full text was not retrieved for this draft.
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — Covers the computation of the SVD and its use in least-squares problems.
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — Graduate text covering the SVD and its numerical behaviour.

### Lectures

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — The course lecture list includes a lecture on the singular value decomposition.
