---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/dimensionality-reduction
  - theory/optimization
tags:
  - mathematics
  - linear algebra
  - spectral
aliases:
  - 特徵值分解
  - Eigendecomposition
  - Spectral decomposition
  - 特徵向量
---

# Eigendecomposition

An eigendecomposition writes a square matrix in terms of its eigenvectors and eigenvalues. For a symmetric matrix the eigenvectors are orthogonal and the eigenvalues are real, which is why the factorisation is used for covariance matrices and the Hessians of loss functions. Part of [Linear algebra](index.md).

## Overview

An eigenvector of a square matrix \(A\) is a nonzero vector \(\mathbf{v}\) whose direction \(A\) leaves unchanged: \(A\mathbf{v} = \lambda \mathbf{v}\). The scalar \(\lambda\) is the eigenvalue, the factor by which \(A\) stretches \(\mathbf{v}\). Along an eigenvector a matrix acts as a simple scaling, so repeated application is easy to analyse: \(A^k\mathbf{v} = \lambda^k\mathbf{v}\).

## Key concepts

- **Eigenpair**: an eigenvalue together with its eigenvector.
- **Spectral theorem**: a real symmetric matrix has real eigenvalues and an orthonormal set of eigenvectors.
- **Positive semidefinite matrix**: a symmetric matrix whose eigenvalues are all non-negative. Covariance matrices are of this kind.
- **Spectral radius**: the largest absolute value of an eigenvalue. Repeated multiplication by a matrix grows or decays according to whether it is above or below one.

## How it works

For a real symmetric \(n\times n\) matrix, the spectral theorem gives

\[
A = Q\Lambda Q^\top, \qquad \Lambda = \operatorname{diag}(\lambda_1, \dots, \lambda_n),
\]

where the columns of the orthogonal matrix \(Q\) are the eigenvectors. The quadratic form then decomposes along the eigen-directions:

\[
\mathbf{x}^\top A \mathbf{x} = \sum_{i} \lambda_i \, (\mathbf{q}_i^\top \mathbf{x})^2 .
\]

So each eigenvalue is the curvature of the quadratic in its own direction. This is the reason the eigenvalues of a Hessian matter for optimisation: large eigenvalues mark steep directions and small ones mark flat directions (see [Calculus and optimisation](../calculus/index.md)).

A standard way to find the dominant eigenvector is power iteration, which repeatedly applies \(A\) and normalises the result. It converges to the eigenvector of the largest-magnitude eigenvalue when that eigenvalue is well separated from the rest (see Golub and Van Loan).

## Key methods

Eigendecomposition is one of the two landmark matrix factorisations of linear algebra. The other is the singular value decomposition.

- [Singular value decomposition](svd.md): works for any matrix. For a symmetric positive semidefinite matrix its singular values equal the eigenvalues, so the two factorisations agree there.

Use eigendecomposition when the matrix is square and symmetric, such as a covariance matrix or a Hessian. Use the SVD for rectangular data or weight matrices.

## Connections

- [Principal component analysis](../../paradigms/unsupervised/dimensionality-reduction/pca.md) takes the eigenvectors of the covariance matrix as its principal directions. The variance along each direction is the corresponding eigenvalue.
- [Probability and statistics](../probability-statistics/index.md) uses covariance matrices of multivariate Gaussians, which are diagonalised in this way.
- [Calculus and optimisation](../calculus/index.md) uses the Hessian and its eigenvalues to describe the local shape of a loss function.

## Applications

- **Principal component analysis**: the principal components of a dataset are eigenvectors of its covariance matrix (Bishop, 2006, covers PCA).
- **Curvature and conditioning**: the ratio of the largest to smallest Hessian eigenvalue indicates how hard a quadratic objective is to optimise by gradient descent (Boyd & Vandenberghe, 2004).
- **Stability analysis**: whether a linear dynamical system decays or grows is decided by the eigenvalues of its matrix.

## Open questions

- Computing eigendecompositions of very large matrices, such as the Hessians of large networks, is expensive, and practical methods use approximations whose accuracy is hard to guarantee.
- Non-symmetric matrices can have complex or ill-conditioned eigenvalues, which makes their eigendecompositions less reliable than symmetric ones.

## References

### Seminal papers

- Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf — Textbook treatment of PCA defined through the eigenvectors of the covariance matrix.

### Surveys and textbooks

- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — Covers symmetric eigenvalue problems and the power method.
- Trefethen, L. N. & Bau, D. (1997). *Numerical Linear Algebra*. SIAM. https://people.maths.ox.ac.uk/trefethen/text.html — Graduate text on eigenvalue problems and their numerical behaviour.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free online textbook that covers PCA and the covariance matrices it diagonalises.

### Lectures

- Strang, G., *18.06 Linear Algebra*, MIT. https://web.mit.edu/18.06/www/ — The course lecture list includes a lecture on eigenvalues and eigenvectors, followed by diagonalisation.

### Articles and documentation

- Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press. https://web.stanford.edu/~boyd/cvxbook/ — Free online text; covers the second-order conditions in which Hessian eigenvalues enter, and the conditioning of quadratic problems.
