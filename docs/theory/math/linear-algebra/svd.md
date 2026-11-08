---
status: complete
last_reviewed: 2026-11-08
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

The singular value decomposition expresses a real matrix as a sum of rank-one maps. Each map takes one input direction to an output direction, scaled by a non-negative singular value. Retaining the largest terms gives an optimal approximation for a chosen rank in both the Frobenius and spectral norms.[^svd][^approx]

## Shapes and geometry

Let $A\in\mathbb R^{m\times n}$, $p=\min(m,n)$ and $r=\operatorname{rank}(A)$. Order the singular values as $\sigma_1\ge\cdots\ge\sigma_p\ge0$. Exactly $r$ are positive. The same matrix can be represented with factors of several sizes.[^svd]

| Form | Factor shapes | Singular values kept |
|---|---|---|
| Full | $U$ is $m\times m$, $\Sigma$ is $m\times n$, $V^\top$ is $n\times n$ | All $p$ on the diagonal of rectangular $\Sigma$ |
| Economy | $U_p$ is $m\times p$, $\Sigma_p$ is $p\times p$, $V_p^\top$ is $p\times n$ | All $p$, including zeros |
| Rank compact | $U_r$ is $m\times r$, $\Sigma_r$ is $r\times r$, $V_r^\top$ is $r\times n$ | The $r$ positive values |

In the full factorisation $A=U\Sigma V^\top$, $U$ and $V$ are square orthogonal matrices. The economy and compact factors keep orthonormal columns in $U$ and $V$. Reading the map from right to left, $V^\top$ expresses the input in a new orthonormal basis, $\Sigma$ scales the coordinates and can change their number, and $U$ maps the result to the output basis.[^svd]

For $i\le p$, paired singular vectors satisfy $Av_i=\sigma_i u_i$ and $A^\top u_i=\sigma_i v_i$. The full factors give

$$
A^\top A=V(\Sigma^\top\Sigma)V^\top,
\qquad AA^\top=U(\Sigma\Sigma^\top)U^\top.
$$

The right and left vectors thus come from the two Gram matrices, with eigenvalues given by squared singular values and any additional zeros required by the shapes. The products $\Sigma^\top\Sigma$ and $\Sigma\Sigma^\top$ are square even when $\Sigma$ is rectangular. In numerical work, dense SVD routines such as LAPACK's xGESVD reduce $A$ directly to bidiagonal form and compute the SVD of the bidiagonal matrix.[^svd]

## Truncation and error

For $0\le k<r$, retain the first $k$ rank-one terms to construct $A_k$. The Eckart–Young–Mirsky result states that $A_k$ minimises both errors over matrices of rank at most $k$.[^ey][^approx]

$$
A_k=\sum_{i=1}^k \sigma_i u_i v_i^\top,\qquad
\|A-A_k\|_F=\left(\sum_{i=k+1}^p \sigma_i^2\right)^{1/2},
\qquad
\|A-A_k\|_2=\sigma_{k+1}.
$$

The Frobenius norm measures the square root of the sum of squared entries. The spectral norm measures the largest output length over unit-length inputs. Accordingly, the first error accumulates every discarded direction, while the second measures the strongest remaining error direction. For $k\ge r$, the approximation is exact and both errors are zero.[^approx]

### Worked rectangular example

Take the matrix

$$
A=\begin{pmatrix}
3&3&0&0\\
0&0&2&2\\
1&-1&0&0
\end{pmatrix}.
$$

Its rows are orthogonal, so $AA^\top=\operatorname{diag}(18,8,2)$. The singular values are $3\sqrt{2}$, $2\sqrt{2}$ and $\sqrt{2}$. The first left singular vector is the first coordinate vector, so the rank-one approximation retains the first row and sets the other rows to zero. Its Frobenius error is $\sqrt{8+2}=\sqrt{10}$. Its spectral error is $2\sqrt{2}$. It retains $18/28=9/14$ of the original squared Frobenius norm.

For an $m\times n$ weight matrix stored as two dense factors of inner dimension $k$, the scalar count is $k(m+n)$ after folding $\Sigma_k$ into one factor. Storage shrinks when that count is less than $mn$. The approximation theorem controls matrix error. Model quality and latency depend on the surrounding model and implementation and can be measured on the deployment workload.[^approx]

## Least squares, PCA and adaptation

- **Least squares.** The Moore–Penrose pseudoinverse is $A^+=V_r\Sigma_r^{-1}U_r^\top$. For a right-hand side $b$, the vector $A^+b$ has minimum Euclidean norm among minimisers of $\|Ax-b\|_2$. Small positive singular values can amplify noise when inverted. A numerical rank threshold treats selected small values as zero and changes the problem being solved.[^approx][^accuracy]
- **PCA.** Let $X$ have $m>1$ centred observations in its rows. The right singular vectors of $X$ are principal directions, the sample covariance eigenvalues are $\sigma_i^2/(m-1)$ with additional zeros as needed, and the top $k$ scores are $XV_k=U_k\Sigma_k$. See [Principal component analysis](../../paradigms/unsupervised/dimensionality-reduction/pca.md).[^pca]
- **Model weights.** [Truncated SVD](../../model-compression/low-rank-and-efficient-architectures/truncated-svd/index.md) approximates an existing weight matrix. [LoRA](../../model-compression/low-rank-and-efficient-architectures/lora/index.md) freezes the base weights and learns an update $BA$ whose rank is at most the chosen adapter rank.[^lora]

## Interpreting the factors

A singular-vector pair can have both signs flipped without changing its rank-one term. Repeated singular values permit different orthonormal bases in their shared subspace. Closely spaced singular values can also make individual computed vectors sensitive to perturbations. The reconstruction and the relevant subspace are useful comparisons when factors differ between solvers.[^accuracy]

[^svd]: *LAPACK Users' Guide*, “Singular Value Decomposition”, defines the factors and describes bidiagonal reduction.
[^ey]: Eckart and Young (1936) formulate and solve the least-squares lower-rank approximation problem.
[^approx]: Benner, *Matrix Equations and Model Reduction*, section 2.1, gives the spectral and Frobenius approximation results and the minimum-norm least-squares interpretation.
[^accuracy]: *LAPACK Users' Guide*, “Further Details: Error Bounds for the Singular Value Decomposition”, explains precision and the sensitivity of clustered singular vectors.
[^pca]: Strang, MIT 18.065, Lecture 7, relates the data matrix SVD and principal component analysis.
[^lora]: Hu et al. (2021) define the frozen base model and trainable low-rank weight update.

## References

### Seminal papers

- Eckart, C. & Young, G. (1936). *The Approximation of One Matrix by Another of Lower Rank*. Psychometrika 1, 211–218. https://link.springer.com/article/10.1007/BF02288367 — Formulates and solves lower-rank matrix approximation under the least-squares criterion.
- Hu, E. J. et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. https://arxiv.org/abs/2106.09685 — Introduces trainable low-rank updates to frozen pretrained weights during adaptation.

### Surveys and textbooks

- Benner, P. *Matrix Equations and Model Reduction*, section 2.1. Max Planck Institute for Dynamics of Complex Technical Systems. https://www.mpi-magdeburg.mpg.de/2519809/MathBasics.pdf — States the truncation theorem and connects the SVD to the pseudoinverse.
- Golub, G. H. & Van Loan, C. F. (2013). *Matrix Computations*, 4th ed. Johns Hopkins University Press. https://www.press.jhu.edu/books/title/10678/matrix-computations — Covers matrix factorisations, computational algorithms and numerical least-squares problems.

### Lectures

- Strang, G. (2018). *18.065 Matrix Methods in Data Analysis, Signal Processing, and Machine Learning*, Lecture 7. MIT OpenCourseWare. https://www.ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/resources/lecture-7-eckart-young-the-closest-rank-k-matrix-to-a/ — Connects principal component analysis with the closest rank-k matrix theorem.

### Articles and documentation

- *LAPACK Users' Guide*. *Singular Value Decomposition*. https://netlib.org/lapack/lug/node53.html — Describes the factorisation conventions and the bidiagonal reduction used by LAPACK.
- *LAPACK Users' Guide*. *Further Details: Error Bounds for the Singular Value Decomposition*. https://netlib.org/lapack/lug/node97.html — Describes numerical error bounds for singular values, vectors and subspaces.
