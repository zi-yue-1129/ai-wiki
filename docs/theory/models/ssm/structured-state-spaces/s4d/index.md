---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Diagonal S4
  - S4D
  - 對角結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - initialisation
last_reviewed: 2026-10-28
---

# S4D: A Diagonal Version of S4

S4D is a diagonal state-space model that Gu, Gupta, Goel and Ré introduced in their 2022 paper "On the Parameterization and Initialization of Diagonal State Space Models". It keeps the computation and parameterisation of S4 but replaces the diagonal-plus-low-rank state matrix with a diagonal complex matrix. Its performance depends mainly on how that diagonal is initialised.

## Problem

S4 is a strong model for long-range dependencies, but its state matrix is diagonal-plus-low-rank (DPLR), and computing its convolution kernel needs a complicated algorithm. A diagonal state matrix would be much simpler, but earlier diagonal models performed poorly. DSS showed that a diagonal matrix derived from HiPPO-LegS can perform nearly as well as S4. However, DSS uses a complex softmax kernel, and the reason the diagonal approximation works was not explained.

## Core idea

S4D combines S4's computation and parameterisation with DSS's initialisation. Its kernel is a Vandermonde matrix-vector product, which has the same complexity as S4's. The paper stresses that initialisation is critical, so the choice of the diagonal matrix \(A\) matters most. Its theory shows that removing the low-rank term from HiPPO-LegS gives a diagonal matrix, HiPPO-D. As the state size \(N\) grows, the kernels of this diagonal model converge to the S4-LegS kernels. The paper proposes three initialisations:

- **S4D-LegS**, the diagonalised HiPPO-LegS matrix, as in DSS.
- **S4D-Inv**, where the imaginary parts follow an inverse law that approximates S4D-LegS.
- **S4D-Lin**, where the imaginary parts are linearly spaced, approximating the Fourier-like initialisation of S4.

## Equation or algorithm

The continuous system is \(x'(t) = Ax(t) + Bu(t)\), \(y(t) = Cx(t)\), with kernel \(K(t) = Ce^{tA}B\). Bilinear discretisation gives \(\bar A = (I - \tfrac{\Delta}{2}A)^{-1}(I + \tfrac{\Delta}{2}A)\). With a diagonal \(\bar A\), the discrete kernel is a Vandermonde product, \(\bar K = (\bar B^\top \circ C)\,V_L(\bar A)\), where \(V_L(\bar A)_{n,\ell} = \bar A_n^{\ell}\). Entrywise,

\[
\bar K_\ell = \sum_{n=1}^{N} C_n\,\bar B_n\,\bar A_n^{\ell}, \qquad \ell = 0, \dots, L-1 .
\]

The two named initialisations use these diagonal entries:

\[
A_n^{\text{Inv}} = -\tfrac{1}{2} + i\,\tfrac{N}{\pi}\left(\tfrac{N}{2n+1} - 1\right), \qquad A_n^{\text{Lin}} = -\tfrac{1}{2} + i\pi n .
\]

## Results

The abstract states that S4D averages 85% on the Long Range Arena (LRA). The LRA table gives 85.50 for S4D-Inv, 84.89 for S4D-LegS, and 80.48 for the original S4. On Speech Commands at 8 kHz, S4D-Inv scores 91.80 and S4-LegS scores 91.32. On sCIFAR, S4-LegS scores 91.80, against 90.69 for S4D-Inv and 90.42 for S4D-Lin. The paper reports that, under its LRA settings, only S4D-Inv achieves above random chance on Path-X.

## Limitations

The authors point out that diagonalisability is not enough. Almost all matrices are diagonalisable, but random diagonal or dense real initialisations perform poorly, so the initialisation carries the performance. The proof ignores numerical representation, which is why S4 needed its low-rank correction. Even with the same spectrum, a real-valued variant performs worse. S4D-LegS is a noisy approximation of S4-LegS and is usually slightly worse. The convergence result holds for HiPPO-LegS, and random rank-one perturbations produce kernels that diverge. The asymptotic law for the imaginary parts is a conjecture supported by experiments. Freezing \(A\) and \(B\) hurts Speech Commands noticeably, and leaving \(\Re(A)\) unconstrained may cause instability.

## Connections

S4D is the diagonal case of the [S4](../s4/index.md) layer, and it sits within the [structured state spaces](../index.md) family, which in turn belongs to the wider [state-space models](../../index.md) family. Its initialisation descends from [HiPPO](../hippo/index.md). The diagonal recurrence with parallel computation is also the design of [S5](../s5/index.md) and the [linear recurrent units](../linear-recurrent-units/index.md). Its input-dependent successor is covered in [selective state spaces](../../selective-state-spaces/index.md).

## Open issues and further variants

- **Why the diagonal form works.** The paper leaves open why bilinear discretisation smooths the kernel so that it matches S4, and whether other initialisations can work as well.
- **Initialisation design.** The imaginary-part law is supported empirically but not proved, so other diagonal choices may do better.
- **Path-X.** Most S4D variants fail on Path-X under the LRA settings, which marks a limit of the diagonal form on the hardest task.

## References

### Seminal papers

- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — Derives the HiPPO state matrices that let a recurrence remember a history through polynomial projections.
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, with the normal-plus-low-rank structure and fast convolution kernel.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Careful initialisation of diagonal linear recurrences that matches S4 on long-range benchmarks.
