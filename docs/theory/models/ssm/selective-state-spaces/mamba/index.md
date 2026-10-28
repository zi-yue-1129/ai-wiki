---
related:
- theory/models/ssm/selective-state-spaces
- theory/models/ssm
aliases:
  - Linear-Time Sequence Modeling with Selective State Spaces
  - Mamba
  - 線性時間序列建模
tags:
  - state-space models
  - selection
  - hardware-aware scan
last_reviewed: 2026-10-28
---

# Mamba

Mamba is a selective state-space model introduced by Gu and Dao in their 2023 paper "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". It makes the state-space parameters depend on the input, so the model can choose what to keep from each token, and a hardware-aware parallel scan keeps training efficient.

## Problem

Attention scales quadratically with window length, while subquadratic models have been less effective on discrete, information-dense data such as text. The authors attribute this to weak content-based reasoning.

## Core idea

The idea is selection. The parameters Δ, B and C are functions of the input, so the model can keep or discard information depending on the current token. Input dependence removes the convolution form, so the recurrence runs as a hardware-aware parallel scan that avoids writing the expanded state to slow GPU memory.

## Equation or algorithm

Under zero-order hold, the discrete transition is \(\bar A = \exp(\Delta A)\), with Δ computed from the input at each step. The recurrence is then

\[
h_t = \bar A_t\, h_{t-1} + \bar B_t\, x_t,
\]

which is evaluated as a scan.

## Results

The abstract reports 5× higher throughput than Transformers. The paper reports that Mamba-3B outperforms Transformers of the same size and matches Transformers twice its size, in pretraining and downstream evaluation. The scan is up to 3× faster than prior methods on A100 GPUs.

## Limitations

Efficiency depends on the hardware-aware scan. Removing the convolution form that earlier SSMs used for speed means the model needs this specialised kernel to run quickly.

## Connections

Mamba is the input-dependent member of the [selective state spaces](../index.md) family, which sits within the [state-space models](../../index.md) family. It extends the static structured model [S4](../../structured-state-spaces/s4/index.md), whose convolution form it gives up. The selection mechanism answers the gating question raised by the [gated cells](../../../rnn/gated-cells/index.md) in the RNN family, and its duality with attention links it to the [attention variants](../../../transformer/attention-variants/index.md) page.

## Open issues and further variants

- **Recall limits.** Whether selective SSMs can match attention on tasks that need exact recall of many items, without hybrids, is still being tested.
- **What is selected.** Selection works well empirically, but the criteria the model learns are hard to inspect.
- **Scaling.** How selective SSMs scale with data and compute compared with Transformers is an active area of measurement.

## References

### Seminal papers

- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". [arXiv:2312.00752](https://arxiv.org/abs/2312.00752) — Input-dependent state-space parameters with a hardware-aware scan.
- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". [arXiv:2111.00396](https://arxiv.org/abs/2111.00396) — S4, a structured state-space model that handles very long sequences efficiently.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". [arXiv:2008.07669](https://arxiv.org/abs/2008.07669) — The HiPPO framework that gives the state matrix its long-range memory.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". [arXiv:2405.21060](https://arxiv.org/abs/2405.21060) — Mamba-2, which links selective SSMs to attention through a structured matrix duality.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". [arXiv:2303.06349](https://arxiv.org/abs/2303.06349) — Shows that carefully designed linear recurrent units can match SSMs on long-sequence benchmarks.
