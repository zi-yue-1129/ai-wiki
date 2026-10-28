---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - High-order Polynomial Projection Operators
  - HiPPO
  - 高階多項式投影運算子
tags:
  - state-space models
  - long-range memory
  - online function approximation
last_reviewed: 2026-10-28
---

# HiPPO

HiPPO, short for High-order Polynomial Projection Operators, is a framework for building a recurrent memory that stores the history of an input as a vector of polynomial coefficients. Gu et al. introduced it in the 2020 paper "HiPPO: Recurrent Memory with Optimal Polynomial Projections". Its state matrices give the structured state-space models that follow their long-range memory.

## Problem

A sequence model has to summarise the full history of its input in bounded storage, and update that summary online. Recurrent networks suffer from vanishing gradients. Gated designs such as the LSTM and GRU, and earlier memory cells such as the LMU, often need a prior on the sequence length or timescale, and many lack guarantees on long-term dependencies.

## Core idea

The paper treats memory as online function approximation. The history of the input \(f\) is projected onto a polynomial basis under a time-varying measure \(\mu^{(t)}\) that weights past times. The coefficients \(c(t) \in \mathbb{R}^N\) evolve under a linear ODE, and this ODE can be discretised into a recurrence. The paper studies three measures:

- **LegT** (translated Legendre) puts uniform weight on a sliding window of length \(\theta\), so \(\theta\) is a hyperparameter.
- **LagT** (translated Laguerre) puts exponentially decaying weight on the past.
- **LegS** (scaled Legendre) puts uniform weight on the whole history \([0, t]\). It is the paper's main measure and needs no window length.

## Equation or algorithm

For the LegS measure, the coefficients follow

\[
\frac{dc}{dt} = -\frac{1}{t}\,A\,c(t) + \frac{1}{t}\,B\,f(t),
\]

with \(A_{nk} = \sqrt{2n+1}\sqrt{2k+1}\) if \(n > k\), \(A_{nk} = n+1\) if \(n = k\), and \(A_{nk} = 0\) if \(n < k\), and \(B_n = \sqrt{2n+1}\). A forward Euler step gives the recurrence

\[
c_{k+1} = \left(I - \tfrac{1}{k}A\right) c_k + \tfrac{1}{k}\,B\,f_k .
\]

The paper also gives the LegT and LagT matrices, and it uses a bilinear discretisation in its experiments.

## Results

On permuted MNIST, the paper reports 98.3% for HiPPO-LegS, above the listed baselines, including the Transformer at 97.9% and the LMU at 97.15%. The paper notes that its HiPPO numbers are validation accuracy averaged over three seeds, while the literature numbers it compares against are test accuracy. On Character Trajectories with a timescale shift or missing data, HiPPO-LegS scores 88.8% and 90.1% for the two timescale shifts, and 94.5% and 94.9% for the two missing-data settings. The abstract states that it outperforms the RNN and neural-ODE baselines by "25-40%" accuracy. On a copying task with length 200, LegS solves the task almost perfectly, while LegT depends strongly on its window length. The C++ implementation processes 470,000 time steps per second on one CPU core.

## Limitations

The translated measures need prior knowledge. LegT needs the correct window length \(\theta\), and LagT and LegT both need a step size \(\Delta t\). LegS removes the window, but the paper's efficiency result is proved only for LegS, and the authors conjecture it extends to other measures. The LegT update adds approximation error, because it assumes the current coefficients are accurate enough to recover the input at the start of the window. Forward Euler is less accurate than the bilinear method in this setting. The authors leave large-scale tasks, such as speech, video and reinforcement learning, and integration into other models as future work. The paper has no dedicated limitations section, so these points come from its discussion.

## Connections

HiPPO-LegS is the starting matrix for the [structured state spaces](../index.md) family. [S4](../s4/index.md) uses it through a normal-plus-low-rank form, [S4D](../s4d/index.md) takes its diagonal part, and [S5](../s5/index.md) uses a diagonalised HiPPO-N matrix. The [linear recurrent units](../linear-recurrent-units/index.md) use a different, ring-shaped initialisation. The wider [state-space models](../../index.md) family covers the whole design. The memory problem that HiPPO addresses is the same one studied in the [RNN](../../../rnn/index.md) family, and the input-dependent successor to this design is covered in [selective state spaces](../../selective-state-spaces/index.md).

## Open issues and further variants

- **Choice of measure.** LegS removes the window hyperparameter, but its efficiency result is not proved for other measures, and the authors leave this as a conjecture.
- **Discretisation.** Forward Euler is less accurate than the bilinear method here, and the effect of the discretisation on other tasks is not characterised.
- **Scale.** The paper's experiments are small. Speech, video and reinforcement learning are named as future work.

## References

### Seminal papers

- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — The HiPPO framework that gives the state matrix its long-range memory.
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4, a structured state-space model that handles very long sequences efficiently.
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". [arXiv:2206.11893](https://arxiv.org/abs/2206.11893) — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". [arXiv:2208.04933](https://arxiv.org/abs/2208.04933) — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — Shows that carefully designed linear recurrent units can match SSMs on long-sequence benchmarks.
