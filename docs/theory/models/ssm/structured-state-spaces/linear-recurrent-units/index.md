---
related:
- theory/models/ssm/structured-state-spaces
- theory/models/ssm
aliases:
  - Linear Recurrent Unit
  - LRU
  - 線性循環單元
tags:
  - state-space models
  - recurrent neural networks
  - initialisation
last_reviewed: 2026-10-28
---

# Linear Recurrent Units

The linear recurrent unit (LRU) is a diagonal, linear recurrent layer that Orvieto et al. introduced in their 2023 paper "Resurrecting Recurrent Neural Networks for Long Sequences". It asks whether a deep RNN can match deep state-space models on long sequences once the features that matter in those models are identified. It answers by removing the nonlinearity from the recurrence and using a stable complex diagonal parameterisation.

## Problem

Recurrent networks allow fast inference on long sequences, but they are hard to optimise and slow to train. Deep SSMs such as S4 perform well on long-range tasks and train in parallel, but it is unclear which of their features drive that performance. The paper asks whether deep RNNs can match the performance and efficiency of deep continuous-time SSMs.

## Core idea

The authors start from a standard deep RNN and apply a series of changes, ablating each one. The result is the LRU, which sits inside the same norm, recurrence, GLU and skip block structure as S4-style models. The changes are:

1. **Linear recurrence.** The nonlinearity is removed from the recurrence and placed in the position-wise MLP or GLU blocks.
2. **Complex diagonal recurrence.** The dense recurrence matrix is replaced by a diagonal one, which enables parallel scans.
3. **Stable exponential parameterisation.** The magnitude and phase of each eigenvalue are controlled separately, which keeps the eigenvalues inside the unit disk during training.
4. **Ring initialisation.** Eigenvalues are sampled uniformly from a ring between radii \(r_{\min}\) and \(r_{\max}\), and for very long sequences the phase is restricted to a thin slice near zero.
5. **Normalisation.** The input is scaled by a learned factor \(\gamma\), so the forward pass does not blow up when the eigenvalues are close to the unit circle.

## Equation or algorithm

Unrolled, a linear recurrence gives \(x_k = \sum_{j=0}^{k-1} A^j B u_{k-j}\), which is stable when \(|\lambda_j| < 1\) for all eigenvalues. The LRU parameterises each eigenvalue as

\[
\lambda_j = \exp\!\left(-\exp(\nu_j) + i\,\exp(\theta_j)\right),
\]

and uses the recurrence

\[
x_k = \Lambda\,x_{k-1} + \exp(\gamma)\odot(B u_k), \qquad y_k = C x_k + D u_k .
\]

At initialisation the normalisation factor is \(\gamma_j = \log\sqrt{1 - |\lambda_j|^2}\). The ring initialisation samples \(\nu = -\tfrac{1}{2}\log\left(u_1(r_{\max}^2 - r_{\min}^2) + r_{\min}^2\right)\) and \(\theta = 2\pi u_2\), with \(u_1, u_2 \sim U[0,1]\) independent. The paper shows that the expected forward-pass gain of this initialisation approaches \(1/(1 - r^2)\) as \(r \to 1\) when \(r_{\min} = r_{\max} = r\).

## Results

On the LRA, the paper reports test accuracy as a mean with its standard error. The LRU scores 89.0 on sCIFAR, 60.2 on ListOps, 89.4 on Text, 89.9 on Retrieval, 95.1 on Pathfinder, and 94.2 on Path-X. The paper's reproduced S4D scores 97.5 on Path-X, and the paper's S5 result is 98.6. The paper does not report a single LRA average. The authors state that the LRU "reaches similar performance as these deep SSMs on all LRA tasks". They also report that using both \(\gamma\) normalisation and a restricted initial eigenvalue phase was crucial for solving Path-X. On sCIFAR, diagonal linear RNNs were about 8 times faster to train than a dense RNN with ReLUs, which the authors say matches their S4D and S5 implementations.

## Limitations

Before the later modifications, linear RNN blocks alone remained far behind S4 on sCIFAR, Pathfinder and Path-X. Path-X failed without normalisation, and with normalisation alone the model still did not generalise. A restricted phase without \(\gamma\) normalisation could not be learned. The phase restriction was explored only for Path-X. The uniform-on-disk initialisation matches the Glorot initialisation only in the large-width limit. Diagonal models can be less stable to train than dense ones, and the authors note that the system is less likely to become unstable when the learning rate is small enough. Complex parameters must be stored as pairs of real floats. The experiments cover only the LRA, with six-layer networks and three seeds, and the authors state that their goal is not to surpass S4-based models.

## Connections

The LRU is a diagonal complex recurrence with parallel computation, so it sits beside [S4D](../s4d/index.md) and [S5](../s5/index.md) in the [structured state spaces](../index.md) family, which belongs to the wider [state-space models](../../index.md) family. Its initialisation is different from [HiPPO](../hippo/index.md), since it uses a ring rather than a polynomial projection. It is also a modernised deep RNN, which links it to the [RNN](../../../rnn/index.md) family and its question of how to train long-memory recurrences.

## Open issues and further variants

- **Phase restriction beyond Path-X.** The paper did not test a smaller initial phase on the other LRA tasks, so its benefit there is unknown.
- **Scale.** The results come from the LRA with six-layer networks and three seeds. Behaviour at larger scale, and on language, is not covered by the paper.
- **Initialisation theory.** The match between ring initialisation and standard initialisations is proved only in the large-width limit, so finite-width behaviour rests on experiments.

## References

### Seminal papers

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4, with the normal-plus-low-rank structure and fast convolution kernel.
- Gu, A., Gupta, A., Goel, K. & Ré, C. (2022). "On the Parameterization and Initialization of Diagonal State Space Models". [arXiv:2206.11893](https://arxiv.org/abs/2206.11893) — Diagonal complex state matrices, carefully initialised, that match S4 with a simpler implementation.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — Derives the HiPPO state matrices that let a recurrence remember a history through polynomial projections.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Smith, J. T. H., Warrington, A. & Linderman, S. W. (2022). "Simplified State Space Layers for Sequence Modeling". [arXiv:2208.04933](https://arxiv.org/abs/2208.04933) — S5, a diagonal state-space layer with a parallel scan.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — Shows that carefully designed linear recurrent units can match SSMs on long-sequence benchmarks.
