---
related:
- theory/models/ssm/selective-state-spaces
- theory/models/ssm
aliases:
  - Mamba-2
  - Structured State Space Duality
  - SSD
  - 結構化狀態空間對偶
tags:
  - state-space models
  - structured matrices
  - attention duality
  - hardware-efficient training
last_reviewed: 2026-10-28
---

# Mamba-2

Mamba-2 is a selective state-space architecture introduced by Dao and Gu in the 2024 paper "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality" (arXiv:2405.21060, ICML 2024). It restricts the state transition of each head to a scalar multiple of the identity, which makes the layer a form of structured masked attention and lets most of its computation run as matrix multiplications.

## Problem

Mamba's selective scan is faster than earlier SSM implementations, but it runs as a sequential scan that does not use the matrix-multiplication units that dominate modern accelerators. The paper also observes that state-space models and attention are usually presented as two separate families. The authors ask whether reformulating the computation can make a selective SSM faster, and whether the same reformulation shows how the two families are related.

## Core idea

Mamba-2 sets the state matrix in each head to a scalar times the identity, where Mamba uses a diagonal matrix. The paper calls the resulting correspondence state space duality (SSD). With scalar transitions, the map from input to output is a semiseparable matrix, and it can be computed in two equivalent ways: as a linear recurrence over a state, or as a single masked matrix product with the same shape as attention. The layer splits the sequence into chunks. Inside a chunk it uses the matrix form, which maps well onto matrix units. Between chunks it passes a compressed state through a short scan. The paper reports that the recurrent state can be made larger with little slowdown.

## Equation or algorithm

With a scalar transition \(a_t\), the recurrence is

\[
h_t = a_t\, h_{t-1} + B_t\, x_t, \qquad y_t = C_t^{\top} h_t,
\]

and the same map over the whole sequence is \(y = Mx\), where

\[
M_{ji} = (a_j a_{j-1}\cdots a_{i+1})\,(C_j^{\top} B_i) \qquad (j \ge i).
\]

In matrix form \(M = L \circ (C B^{\top})\), where \(L\) is a lower-triangular mask of cumulative products of the \(a_t\). The dual quadratic form is \((L \circ QK^{\top})V\), with \(Q = C\), \(K = B\) and \(V = X\). The chunked algorithm evaluates the diagonal blocks of \(M\) with this quadratic form. It handles the off-diagonal blocks with low-rank factors in three steps: each chunk computes its final state from zero, a short scan across chunks propagates the true states, and each chunk maps its incoming state to outputs.

## Results

The abstract reports that the SSD layer is "2-8X faster" than the optimized selective-scan implementation of Mamba. The paper reports that the recurrent state can be "8× the size of Mamba or even higher, with minimal slowdown". Against FlashAttention-2, the paper reports that its SSD implementation is competitive, crossing over at sequence length about 2K and running 6 times faster at sequence length 16K. On the Pile, Mamba-2 with 2.7B parameters trained on 300B tokens outperforms Mamba-2.8B, Pythia-2.8B and Pythia-6.9B trained on the same data. The paper also claims that Mamba-2 Pareto-dominates Mamba and Transformer++ in perplexity and wall-clock time under Chinchilla-style scaling; the experimental details for that claim were not checked for this page.

## Limitations

The scalar transition is a real restriction. The paper says it "slightly decreas[es] the expressive power in return for significant training efficiency improvements". The connection to attention covers only certain flavours of attention, and the dual form drops softmax. The 1-SS form is strictly less expressive than general semiseparable structured masked attention, and it cannot be written as a standard SSM. For short sequences the quadratic mode can be more efficient than the linear mode, and in the paper's comparison the SSD implementation is slower than FlashAttention-2 below about 2K tokens.

## Connections

Mamba-2 refines the selective SSM of [Mamba](../mamba/index.md): it keeps input-dependent parameters but gives each head a scalar transition. It sits in the [selective state spaces](../index.md) family, which belongs to the [state-space models](../../index.md) family. The static structured model that the lineage starts from is [S4](../../structured-state-spaces/s4/index.md). The attention duality links Mamba-2 to the [attention variants](../../../transformer/attention-variants/index.md) page, which covers the other route to efficient long context.

## Open issues and further variants

- **Cost of the scalar transition.** The paper accepts a small loss of expressive power in exchange for speed. How large that loss is on tasks that need many different decay rates within one head is not measured on this page.
- **Scope of the duality.** The equivalence covers certain attention flavours and drops softmax. Whether a similar structure holds for softmax attention, and what general semiseparable forms add beyond the 1-SS case, are open questions.
- **Short-context speed.** The chunked quadratic form trades memory for speed on matrix units. Below about 2K tokens the paper's own FlashAttention-2 comparison favours FlashAttention-2, and kernel designs that close this gap are not covered here.

## References

### Seminal papers

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". arXiv:2405.21060 — Mamba-2, which links selective SSMs to attention through a structured matrix duality.
- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". arXiv:2312.00752 — Input-dependent state-space parameters with a hardware-aware scan.
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, a structured state-space model that handles very long sequences efficiently.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — The HiPPO framework that gives the state matrix its long-range memory.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Shows that carefully designed linear recurrent units can match SSMs on long-sequence benchmarks.
