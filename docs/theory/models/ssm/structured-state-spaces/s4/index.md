---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Structured State Spaces for Long Sequences
  - S4
  - 長序列結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - efficient computation
last_reviewed: 2026-10-28
---

# S4: Structured State Spaces for Long Sequences

S4 is a structured state-space model for long sequences. Gu, Goel and Ré introduced it in their 2021 paper "Efficiently Modeling Long Sequences with Structured State Spaces". It keeps the long-range memory of a HiPPO-initialised recurrence and makes training as fast as a convolution, so the model can be run on very long inputs.

## Problem

Models of that period, including the Long Range Arena (LRA) baselines, performed poorly on long-range dependencies. The earlier LSSL approach needed \(O(N^2 L)\) operations and \(O(NL)\) space, which made it impractical.

## Core idea

S4 reparameterises the HiPPO state matrix as a normal-plus-low-rank matrix, \(A = V\Lambda V^* - PQ^\top\). The resulting convolution kernel can then be computed fast, so training runs as fast as a convolution.

## Equation or algorithm

The SSM is unrolled as the convolution kernel

\[
\bar K = (C\bar B,\; C\bar A\bar B,\; \dots,\; C\bar A^{L-1}\bar B).
\]

S4 evaluates this kernel through a generating function at roots of unity, uses the Woodbury identity for the low-rank term, reduces the problem to a Cauchy kernel, and recovers \(\bar K\) with an inverse FFT.

## Results

S4 averages 80.48% across the LRA tasks, where the paper states that every baseline averages under 60%. On Path-X it reaches 88.10%, where the paper says prior work was at about 50%, random guessing. It is up to 30× faster and uses 400× less memory than LSSL.

## Limitations

The authors say S4 "may not necessarily be the most suitable model for all types of data". A gap to Transformers on language modelling remains. The paper's GPU implementation uses the naive \(O(NL)\) Cauchy algorithm.

## Connections

S4 is the structured, input-independent model described on the [structured state spaces](../index.md) page, which sits within the wider [state-space models](../../index.md) family. Its input-dependent successor is [Mamba](../../selective-state-spaces/mamba/index.md), which gives up the convolution form that S4 relies on. Its recurrent ancestry connects to the long-memory question in the [RNN](../../../rnn/index.md) family.

## Open issues and further variants

- **Choice of measure.** HiPPO uses a specific measure for the history, and whether other measures suit other data types is not well studied.
- **Diagonal forms.** Diagonal state matrices are nearly as good on benchmarks, but why they work so well is not fully understood.
- **Multidimensional inputs.** Extending the structure to images and other grids has several competing designs.

## References

### Seminal papers

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, a structured state-space model that handles very long sequences efficiently.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — The HiPPO framework that gives the state matrix its long-range memory.
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Careful initialisation of diagonal linear recurrences that matches S4 on long-range benchmarks.
