---
related:
- theory/models/rnn
aliases:
  - Structured State Spaces
  - HiPPO
  - S4
  - 結構化狀態空間
tags:
  - state-space models
  - long-range memory
  - initialisation
last_reviewed: 2026-10-28
---

# Structured State Spaces

A linear state-space model can only remember a long history if its state matrix is chosen carefully. A random matrix forgets exponentially fast, so most of the design effort in this family goes into the structure and initialisation of the state matrix \(A\). The structured variants use a special initial form, such as the HiPPO matrices, and then restrict the matrix to a simple form that can be computed quickly. The result is a model that remembers a long history through a fixed-size state and trains in parallel.

## Overview

| Variant | State matrix | Main idea | Example |
|---|---|---|---|
| Random or unconstrained | Learned freely | Simple, but forgets quickly | Early linear recurrences |
| HiPPO | Designed | Projects history onto orthogonal polynomials | HiPPO-LegS |
| Normal plus low-rank | Structured | Diagonal plus low rank, computable with Cauchy kernels | S4 |
| Diagonal | Diagonal, complex | Simpler, nearly as good | S4D, S5 |

## Approaches

### HiPPO initialisation

HiPPO defines a state matrix that, at every time, stores the best polynomial approximation of the input history under a chosen measure. Gu et al. (2020) showed that this projection gives a state that compresses the past in a principled way, and that the recurrence built from it can represent long dependencies. The matrix is a fixed design, which is used as the starting point for learning.

### S4 and the structured parameterisation

S4 represents the state matrix as a diagonal plus low-rank matrix, which it can convert into a convolution kernel and evaluate with a fast algorithm. This makes training as fast as a convolution, while the HiPPO structure gives the long memory. Gu et al. (2021) reported strong results on long-range benchmarks where Transformers struggled, which is why the family drew wide attention.

### Diagonal and linear recurrent variants

Later work showed that a diagonal state matrix, with complex entries, captures most of the benefit with a simpler implementation. S5 uses a diagonal form with a parallel scan, and linear recurrent units use careful initialisation of a diagonal recurrence. These variants made the family easier to implement and extend.

## Trade-offs

- **Fixed dynamics.** Because the matrix does not depend on the input, the model cannot decide what to keep, which limits content-based recall. The selective variants address this.
- **Initialisation sensitivity.** Performance depends on the initialisation and the time-scale parameters, so careful setup matters.
- **Expressivity.** A linear time-invariant system can only compute linear functions of the input history, which is a real limit compared with attention.

## Connections

The structured family is the static, input-independent side of the [state-space models](../index.md) family, whose input-dependent extension is covered in [selective state spaces](../selective-state-spaces/index.md). Its link to the older recurrent view is the long-memory question also studied in the [RNN](../../rnn/index.md) family.

## Open issues and further variants

- **Choosing the measure.** HiPPO uses a specific measure for the history. Whether other measures suit other data types is not well studied.
- **Simplicity versus memory.** Diagonal forms are simpler and nearly as good on benchmarks, but why they work so well is not fully understood.
- **Multidimensional inputs.** Extending the structure to images and other grids is an active area with several competing designs.

## References

### Seminal papers

- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — Derives the HiPPO state matrices that let a recurrence remember a history through polynomial projections.
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, with the normal-plus-low-rank structure and fast convolution kernel.
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". arXiv:2206.11893 — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". arXiv:2208.04933 — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Careful initialisation of diagonal linear recurrences that matches S4 on long-range benchmarks.
