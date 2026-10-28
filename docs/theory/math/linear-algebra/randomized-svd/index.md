---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/model-compression
  - engineering/vector-databases
tags:
  - efficient inference
  - efficient computation
aliases:
  - 隨機化奇異值分解
  - 隨機 SVD
  - Randomized SVD
  - Randomised SVD
  - Randomized low-rank approximation
---

# Randomized SVD

Randomized SVD computes an approximate truncated singular value decomposition by projecting a matrix onto a small random subspace, and then performing an exact SVD on a much smaller matrix. It makes low-rank approximation practical for matrices too large for the classical algorithm. It is one of the three key methods of [linear algebra for AI](../index.md), and it builds on the [truncated SVD](../truncated-svd/index.md).

## Overview

The truncated SVD is the best low-rank approximation, but computing the exact SVD of a dense $m\times n$ matrix costs on the order of $mn\min(m,n)$ operations, and it needs the whole matrix in memory at once. Many AI problems need only the top few singular vectors of very large matrices, such as embedding tables or large weight matrices. For these, an exact decomposition of every direction is wasteful.

Halko, Martinsson and Tropp (2011) showed that a random sample of the matrix's action captures most of its important directions. The procedure is simple, needs few passes over the data and maps well onto parallel hardware. Its accuracy depends on how quickly the singular values of the matrix decay.

## Key concepts

- **Range of a matrix**: the set of all vectors $Ax$, which is the span of the columns of $A$. The top singular vectors span the most important part of the range.
- **Sketch**: a product $Y = A\Omega$ with a random matrix $\Omega$. It is a small set of random combinations of the columns of $A$.
- **Orthonormal basis**: a matrix $Q$ with orthonormal columns that spans the sketch. The projection $QQ^\top A$ approximates $A$.
- **Oversampling**: drawing a few more random vectors than the target rank, which improves accuracy at a small cost.
- **Power iteration**: multiplying the sketch by $AA^\top$ a few times. It sharpens the spectrum, so the random subspace favours the large singular values.

## How it works

Given a matrix $A \in \mathbb{R}^{m\times n}$, a target rank $k$, a small oversampling amount $p$ and a number of power iterations $q$, the algorithm proceeds in six steps:

1. Draw a Gaussian random matrix $\Omega \in \mathbb{R}^{n\times(k+p)}$.
2. Form the sketch $Y = (AA^\top)^q A\,\Omega$. The power iterations are applied in place of the single product $A\Omega$.
3. Compute an orthonormal basis $Q$ for the columns of $Y$, for example by a QR decomposition. The matrix $QQ^\top A$ is then a good approximation of $A$ when the singular values decay quickly.
4. Form the small matrix $B = Q^\top A \in \mathbb{R}^{(k+p)\times n}$.
5. Compute the exact SVD of $B$, which is cheap because $B$ has few rows: $B = \tilde U \Sigma V^\top$.
6. Set $U = Q\tilde U$ and keep the first $k$ singular values and vectors.

The output has the same form as the truncated SVD, $A \approx U_k\Sigma_k V_k^\top$. The essential point is that the expensive work is done on $A$ only through products with thin matrices. In the dense case, the authors state that the randomized approach needs $O(mn\log k)$ floating-point operations, against $O(mnk)$ for classical methods, according to their abstract.

## Results

The paper supports its claims with extensive numerical experiments and a detailed error analysis. Its abstract reports that, in many cases, the randomized approach beats classical methods in accuracy, robustness and speed, and that the benefits depend on the computing environment.

Rokhlin, Szlam and Tygert (2009) apply a randomized low-rank algorithm to PCA. Their abstract reports accuracy very close to the best possible for matrices of arbitrary size, in cases where earlier fast algorithms had no accuracy guarantee unless one or both dimensions of the matrix were small. Their evidence is numerical examples.

No single benchmark summarises these results, so the comparison is qualitative: the method is most attractive when the target rank is small compared with the matrix size, and when the spectrum decays.

## Limitations

- **Approximate, not exact.** The output is an approximation whose error depends on the spectrum. When singular values decay slowly, the sketch misses important directions, and the error can be far from the best rank-$k$ error.
- **Randomness.** Different random draws give slightly different results. The variation is small when the method is well conditioned, but it is part of the output.
- **Passes over the data.** Each power iteration requires an extra pass over the matrix, so accuracy and cost trade off directly.
- **Small matrices.** For matrices that fit comfortably in memory, the classical SVD is simpler and often fast enough.

## Open questions

- Can single-pass, streaming versions reach the accuracy of multi-pass methods on matrices whose data arrive once?
- What guarantees are possible when the spectrum is nearly flat, as it often is in learned weights?
- How do reduced-precision arithmetic and distributed hardware change the trade-offs of the sketch?

## References

### Seminal papers

- Halko, N., Martinsson, P. G. & Tropp, J. A. (2011). Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions. *SIAM Review*. https://doi.org/10.1137/090771806 — Presents a modular framework for randomized algorithms that compute partial matrix decompositions by sampling a subspace.
- Rokhlin, V., Szlam, A. & Tygert, M. (2009). A Randomized Algorithm for Principal Component Analysis. *SIAM Journal on Matrix Analysis and Applications*. https://doi.org/10.1137/080736417 — Applies a randomized low-rank approximation to PCA with accuracy close to the best possible.
- Eckart, C. & Young, G. (1936). The Approximation of One Matrix by Another of Lower Rank. *Psychometrika*. https://doi.org/10.1007/BF02288367 — Gives the exact truncated SVD that the randomized method approximates.

### Surveys and textbooks

- Martinsson, P.-G. & Tropp, J. A. (2020). Randomized numerical linear algebra: Foundations and algorithms. *Acta Numerica*. https://doi.org/10.1017/S0962492920000021 — Survey of probabilistic algorithms, covering low-rank approximation, subspace iteration and error estimation.
- Woodruff, D. P. (2014). Sketching as a Tool for Numerical Linear Algebra. https://arxiv.org/abs/1411.4357 — Survey of linear sketching, including its use for low-rank approximation and regression.
