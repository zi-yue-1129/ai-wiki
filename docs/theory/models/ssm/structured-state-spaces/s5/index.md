---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Simplified State Space Layers
  - S5
  - 簡化狀態空間層
tags:
  - state-space models
  - sequence modelling
  - parallel scan
last_reviewed: 2026-10-28
---

# S5: Simplified State Space Layers

S5 is a simplified state-space layer that Smith, Warrington and Linderman introduced in their 2022 paper "Simplified State Space Layers for Sequence Modeling". It replaces the bank of single-input, single-output SSMs in S4 with one multi-input, multi-output diagonal SSM, and it computes the recurrence in the time domain with a parallel scan.

## Problem

An S4 layer relies on a bank of independent single-input, single-output (SISO) SSMs and on a frequency-domain convolution. The paper aims to keep S4's long-range performance while removing this machinery, which is complicated to implement.

## Core idea

S5 simplifies the S4 layer in two ways. First, it replaces the SISO bank with one multi-input, multi-output (MIMO) SSM with latent size \(P\). Second, it diagonalises the state matrix as \(A = V\Lambda V^{-1}\), so that the recurrence can be computed with a parallel scan rather than a convolution kernel. Conjugate symmetry halves the number of eigenvalues and states that must be stored. The paper also makes three choices for initialisation and timescales:

- HiPPO-LegS is not stably diagonalisable, so S5 uses the diagonalised HiPPO-N matrix. The paper extends a result from Gu et al. (2022) to show that this approximates HiPPO-LegS in the multi-input setting as \(N\) grows.
- The timescales form a learned vector of \(P\) values rather than a single scalar, which the paper found works better.
- A block-diagonal option with several HiPPO-N blocks is also used.

## Equation or algorithm

After diagonalisation, the system uses \(\tilde B = V^{-1}B\) and \(\tilde C = CV\). Zero-order-hold discretisation with step \(\Delta\) gives

\[
\bar\Lambda = \exp(\Lambda\Delta), \qquad \bar B = \Lambda^{-1}(\bar\Lambda - I)\tilde B ,
\]

and the recurrence is \(x_k = \bar\Lambda x_{k-1} + \bar B u_k\). Because each step is an affine map of the state, the composition of steps is associative, so a parallel scan computes all states in logarithmic depth. For a diagonal \(A\), the paper gives a total cost of \(O(PL)\) operations. With \(P = O(H)\), where \(H\) is the model width, the paper states that S5 matches S4's runtime and memory complexity.

## Results

On the Long Range Arena (LRA), the paper reports ListOps 62.15, Text 89.31, Retrieval 91.40, Image 88.00, Pathfinder 95.33, Path-X 98.58, and an average of 87.46. The S4-LegS average in the same table is 86.09. On Speech Commands at 16 kHz, S5 scores 96.52 with 280K parameters, against 96.08 for S4-LegS. Zero-shot at 8 kHz, S5 scores 94.53, against 91.32 for S4-LegS. The paper also reports training-step speed relative to S4D of 1.1 on ListOps, 1.0 on Text, and 4.7 on Path-X.

## Limitations

The authors state that HiPPO-LegS cannot be diagonalised stably, so S5 relies on HiPPO-N, which is justified only in the limit of infinite state dimension. The discrete-time HiPPO-N variant was hard to train because of stability issues, and it needed a much lower learning rate. A variant using S4D-Lin initialisation scored 65.60 with a standard deviation of 27.00 on Path-X, which shows high variance. The pendulum speed comparison benefits from JAX compilation, which the authors say does not fully explain the runtime gap. It is also unclear whether tying the output matrices across the S4 SSMs makes the model more or less expressive.

## Connections

S5 is a simplified form of the [S4](../s4/index.md) layer and shares the [structured state spaces](../index.md) family with it. Its diagonal choice follows [S4D](../s4d/index.md), and its initialisation builds on [HiPPO](../hippo/index.md). The diagonal recurrence with a parallel scan is also used by the [linear recurrent units](../linear-recurrent-units/index.md). The wider [state-space models](../../index.md) family covers the whole design, and the input-dependent successor is covered in [selective state spaces](../../selective-state-spaces/index.md).

## Open issues and further variants

- **Choice of diagonal matrix.** HiPPO-N is justified only as the state size grows, and the poor Path-X variance with S4D-Lin initialisation suggests that the choice of initial diagonal matters.
- **Tied outputs.** Whether sharing the output matrix across the S4 SSMs changes expressivity is not settled by the paper.
- **Training stability.** The paper reports that the discrete-time HiPPO-N variant needed a much lower learning rate, and a robust training recipe for it is not given in the sections checked.

## References

### Seminal papers

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, with the normal-plus-low-rank structure and fast convolution kernel.
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — Derives the HiPPO state matrices that let a recurrence remember a history through polynomial projections.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Careful initialisation of diagonal linear recurrences that matches S4 on long-range benchmarks.
