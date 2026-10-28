---
related:
- theory/models/rnn
- theory/models/transformer
aliases:
  - State-Space Models
  - SSM
  - Mamba
  - 狀態空間模型
tags:
  - state-space models
  - sequence modelling
  - architecture
last_reviewed: 2026-10-28
---

# State-Space Models

A state-space model (SSM) describes a sequence through a hidden state that evolves by a linear recurrence, with the output read out from that state. The recurrence can be run step by step like an RNN, which gives constant cost per generated token, or unrolled as a convolution over the whole sequence, which allows parallel training. Recent SSM architectures, starting with S4 and Mamba, showed that this design can model very long sequences with much less memory than attention, while staying close to Transformers on language. They form the second main sequence family after attention, and a growing set of models mix the two.

## Core idea

A continuous linear system \(x'(t)=Ax(t)+Bu(t)\), \(y(t)=Cx(t)\) is discretised into a recurrence over steps. The matrix \(A\) controls how the state remembers past inputs, which is the key design question. The state-space family asks how to choose \(A\) so that the state can summarise long histories, and, in newer models, how to let the parameters depend on the input. These two questions define the components below.

## Components and variants

- [Structured state spaces](structured-state-spaces/index.md): how \(A\) is initialised and structured (HiPPO, diagonal forms) so that long-range memory is possible, as in S4, S5 and linear recurrent units.
- [Selective state spaces](selective-state-spaces/index.md): input-dependent parameters that let the model decide what to keep, as in Mamba and Mamba-2.

## Key methods

| Method | Year | Core idea | Page |
|---|---|---|---|
| S4 | 2021 | A structured state matrix whose convolution kernel can be computed quickly | [S4](structured-state-spaces/s4/index.md) |
| Mamba | 2023 | Input-dependent parameters with a hardware-aware parallel scan | [Mamba](selective-state-spaces/mamba/index.md) |

S4 gives a long-memory state that trains as fast as a convolution. Mamba makes the parameters depend on the input, so the model can choose what to keep.

## Trade-offs

- **Cost.** Recurrent inference needs constant memory per token, with no key–value cache, while attention grows with context length.
- **Recall.** Fixed-size states must compress history, so exact retrieval of an earlier detail is weaker than in attention. This is the main reason hybrids keep a few attention layers.
- **Training.** Linear time-invariant SSMs train with convolutions in parallel, while selective models need a hardware-aware parallel scan.

## Where it is used

Long-sequence modelling in audio, genomics and time series, and language models that need long contexts at low cost. Hybrid models interleave SSM and attention layers.

## Connections

SSMs are the modern answer to the recurrence trade-off explored in the [RNN](../rnn/index.md) family, and they are a leading alternative to attention in the [Transformer](../transformer/index.md) family. The Transformer page lists them under alternative architectures, and the [attention variants](../transformer/attention-variants/index.md) page covers the other route to efficient long context.

## Open issues and further variants

- **Recall versus efficiency.** Whether pure SSMs can match attention on tasks that need exact recall of many earlier items is not settled, and hybrids are the common compromise.
- **Theory of selection.** Input-dependent state transitions are powerful but harder to analyse, and their expressivity compared with attention is still being mapped.
- **Hardware.** Efficient scans and kernels are needed for each new variant, which slows adoption of new designs.

## References

### Seminal papers

- Gu, A., Goel, K. & Ré, C. (2021). "Efficiently Modeling Long Sequences with Structured State Spaces". arXiv:2111.00396 — S4, a structured state-space model that handles very long sequences efficiently.
- Gu, A., et al. (2020). "HiPPO: Recurrent Memory with Optimal Polynomial Projections". arXiv:2008.07669 — The HiPPO framework that gives the state matrix its long-range memory.
- Gu, A. & Dao, T. (2023). "Mamba: Linear-Time Sequence Modeling with Selective State Spaces". arXiv:2312.00752 — Input-dependent state-space parameters with a hardware-aware scan.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Dao, T. & Gu, A. (2024). "Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality". arXiv:2405.21060 — Mamba-2, which links selective SSMs to attention through a structured matrix duality.
- Orvieto, A., et al. (2023). "Resurrecting Recurrent Neural Networks for Long Sequences". arXiv:2303.06349 — Shows that carefully designed linear recurrent units can match SSMs on long-sequence benchmarks.
