---
status: draft
last_reviewed: 2026-11-06
related:
  - theory/models/transformer/index.md
tags:
  - time series
  - forecasting
  - attention
aliases:
  - Informer
  - Informer 長序列預測
---

# Informer

Informer adapts the [Transformer](../transformer/index.md) to long-sequence time-series forecasting. It replaces full self-attention with a sparse approximation, shortens the sequence between encoder layers, and produces the whole forecast in one pass. It is one of the three landmark methods compared on the [Time-Series Forecasting](index.md) page.

## Problem

Long-horizon forecasting needs a model to read a long history and to predict many steps ahead. Standard self-attention compares every position with every other, so its time and memory grow with the square of the input length. The original encoder–decoder Transformer also produces its output one step at a time, which adds error accumulation and slows inference. The paper argues that long-sequence forecasting demands high prediction capacity, but that the Transformer as it stands is too expensive for it.

## Core idea

Informer changes three parts of the Transformer:

- **ProbSparse self-attention.** Each query is scored by how far its attention distribution departs from uniform. Only the queries with the highest scores attend to all keys, and the remaining queries receive a simple average of the values. The paper reports that this reduces the cost of attention to $O(L \log L)$ in time and memory, where $L$ is the input length.
- **Self-attention distilling.** Between encoder layers, the sequence is shortened by about half, which lets very long inputs be processed with less memory and computation.
- **Generative decoder.** The decoder receives a start segment and a block of placeholder positions, and it predicts the entire output sequence in one forward pass rather than step by step.

## Equation and algorithm

Standard attention is

$$\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d}}\right) V.$$

ProbSparse attention keeps this form but estimates which queries matter. For query $q_i$, the sparsity score is the gap between its largest and its average inner product with the keys,

$$M(q_i, K) = \max_j \frac{q_i k_j^\top}{\sqrt{d}} - \frac{1}{L_K}\sum_{j} \frac{q_i k_j^\top}{\sqrt{d}}.$$

The paper selects the top-scoring queries by this measure, computes full attention for them, and fills the other rows of the output with the mean of the values. Because only a small set of queries is computed in full, the cost falls below that of standard attention.

## Results

The abstract reports that Informer significantly outperforms existing methods on four large-scale datasets. The paper's comparisons are on the datasets and horizons that the authors chose, so the figures for each setting should be read in its tables rather than taken from this summary.

## Limitations

- **Evaluation scope.** The benchmarks are chosen by the authors. A later study found that a much simpler model could beat it on other benchmarks (see below).
- **Attention may not be the bottleneck.** Self-attention is permutation invariant, so the order of the inputs must be supplied through positional encodings. Zeng et al. (2022) argue that this loses temporal order, and report that simple one-layer linear models outperformed Transformer-based forecasters on nine real-world datasets.
- **Sparse approximation.** The sparsity score only chooses which queries to compute in full, so the benefit depends on attention being concentrated on a few keys in the data.
- **Design tuning.** Distilling and the generative decoder are built around long inputs and long outputs. For short horizons a simpler model may be preferable.

## Connections

Informer inherits the attention machinery described on the [Transformer](../transformer/index.md) page and its [attention variants](../transformer/attention-variants/index.md). The recurrent alternative for sequence forecasting is [DeepAR](deepar.md) on the [Recurrent Networks](../rnn/index.md) page, and the non-attention alternative is [N-BEATS](n-beats.md).

## References

### Seminal papers

- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2020). *Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting*. arXiv. https://arxiv.org/abs/2012.07436 — The original paper: ProbSparse attention, self-attention distilling and a generative decoder for long-horizon forecasting.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the Transformer and the scaled dot-product attention that Informer approximates.
- Zeng, A., Chen, M., Zhang, L. & Xu, Q. (2022). *Are Transformers Effective for Time Series Forecasting?* arXiv. https://arxiv.org/abs/2205.13504 — A critical study that compares Transformer forecasters with simple linear models on nine real-world datasets.

### Surveys and textbooks

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — Surveys the encoder and decoder designs, including attention-based ones, for multi-horizon forecasting.
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — Free textbook on the classical forecasting methods that attention-based models are compared with.
