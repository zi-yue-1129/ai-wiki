---
status: draft
last_reviewed: 2026-11-13
tags:
  - time series
  - forecasting
  - transformers
  - long sequences
aliases:
  - Informer
  - 長序列時間序列預測
  - 高效 Transformer 時序預測
---

# Informer

Informer is a Transformer for long-sequence time-series forecasting, the task of predicting hundreds of future steps at once. It keeps the encoder-decoder shape of the [Transformer](../transformer/index.md) but changes three parts: a sparse attention mechanism called ProbSparse, a distilling operation that shortens the encoder's sequence between layers, and a generative decoder that produces the whole horizon in one forward pass. It is one of the landmark methods compared on the [time-series forecasting](index.md) overview.

## Problem

Forecasting a long horizon, such as a week of hourly electricity load, needs a model that can connect output steps to input steps far apart in time. Transformers do this well, but their self-attention compares every query with every key, so cost grows quadratically with the sequence length. Their usual decoder also generates one step at a time, which is slow and lets errors accumulate. The paper asks whether a Transformer can be made efficient enough for these long horizons.

## Core idea

The authors observe that in a trained attention layer only a few queries have a sharply peaked attention distribution. Those queries carry most of the information, while the rest produce an almost uniform average. ProbSparse attention spends full computation only on the queries that matter. The distilling operation halves the length of the encoder's representation after each attention block, and the generative decoder fills in the whole target window in a single pass, using a block of known history as the starting context.

## Equation or algorithm

**ProbSparse attention.** For query $\mathbf{q}_i$ and keys $K$ with dimension $d$, the paper scores how far the attention distribution of a query is from uniform with a max-mean measure:

$$
M(\mathbf{q}_i, K) = \max_j \frac{\mathbf{q}_i \mathbf{k}_j^\top}{\sqrt{d}} - \frac{1}{L_K}\sum_{j=1}^{L_K}\frac{\mathbf{q}_i \mathbf{k}_j^\top}{\sqrt{d}}
$$

The paper avoids computing this exactly. It estimates the scores from a random sample of about $L_K \ln L_Q$ key products, keeps the top $u = c \ln L_Q$ queries with full attention, with $c$ set to 5 in practice, and gives the other queries the mean of the values. The authors state the cost as $O(L \ln L)$ in time and memory.

**Self-attention distilling.** Between attention blocks, a one-dimensional convolution with kernel width 3, an ELU activation and a max-pooling step with stride 2 halve the time dimension. Several stacks receive progressively shorter inputs, and their outputs are concatenated, so the memory of the encoder is reduced.

**Generative decoder.** The decoder input concatenates a start-token segment, taken from the known history just before the target, with zero placeholders for the target window. Masked attention and a fully connected layer then produce every future step together. Because no prediction is fed back as input, the decoder avoids the error accumulation of step-by-step inference.

## Results

The paper evaluates on electricity transformer temperature datasets (ETTh1, ETTh2, ETTm1), electricity consumption (ECL) and weather data. Its univariate tables report mean squared error and mean absolute error averaged over the forecast window. At the longest univariate horizon for ETTh1, which is 720 steps, Informer reports an MSE of 0.269, against 0.658 for DeepAR on the same cell. The canonical-attention variant, labelled Informer† in the paper, reports 0.257 there, so the efficient mechanism does not win every cell. Across its univariate and multivariate tables, the authors count Informer as the best method in most settings, and they report large MSE reductions against LSTMa and against DeepAR, ARIMA and Prophet at several horizons.

## Limitations

- The authors say the gains in the multivariate setting are smaller than in the univariate one, and they leave the cause for future work.
- DeepAR is better than Informer at shorter horizons on the ECL dataset. The authors attribute Informer's advantage at longer horizons to better scaling.
- The experiments were set up to run on one GPU, and the memory ablation reduced batch size, heads and model dimension. Results at larger scale are not shown.
- The theory behind the top-$u$ selection relies on approximations. The authors justify them with a numerical example, and they note that one condition can be relaxed.
- Later work questions whether attention is needed at all. A critique by Zeng et al. (2023) reports that simple linear models match or beat several Transformer forecasters, Informer among them, on common benchmarks. The result depends on the datasets and horizons used, so the Transformer's value for forecasting remains debated.

## Connections

Informer is a [Transformer](../transformer/index.md) with a cheaper attention, so the [attention variants](../transformer/attention-variants/index.md) page is the place to compare it with other efficient attention designs. Its direct multi-horizon output contrasts with the autoregressive sampling of [DeepAR](deepar.md) and with the fully connected basis expansion of [N-BEATS](n-beats.md). Its encoder-decoder layout follows the sequence-to-sequence setting described on the [recurrent networks](../rnn/index.md) page, with attention replacing the recurrent state.

## References

### Seminal papers

- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2021). Informer: Beyond efficient Transformer for long sequence time-series forecasting. *Proceedings of the AAAI Conference on Artificial Intelligence*, 35(12), 11106–11115. doi:[10.1609/aaai.v35i12.17325](https://doi.org/10.1609/aaai.v35i12.17325) — Introduces ProbSparse attention, self-attention distilling and the generative decoder, with the long-horizon experiments.
- Zhou, H. et al. (2020). Informer: Beyond efficient Transformer for long sequence time-series forecasting. arXiv. https://arxiv.org/abs/2012.07436 — The preprint version of the same paper.
- Vaswani, A. et al. (2017). Attention is all you need. arXiv. https://arxiv.org/abs/1706.03762 — The Transformer whose attention Informer modifies.
- Lim, B., Arık, S. Ö., Loeff, N. & Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. *International Journal of Forecasting*, 37, 1748–1764. doi:[10.1016/j.ijforecast.2021.03.012](https://doi.org/10.1016/j.ijforecast.2021.03.012) — Another attention-based multi-horizon forecaster, which uses attention to explain its predictions.

### Surveys and textbooks

- Lim, B. & Zohren, S. (2021). Time-series forecasting with deep learning: a survey. *Philosophical Transactions of the Royal Society A*, 379, 20200209. doi:[10.1098/rsta.2020.0209](https://doi.org/10.1098/rsta.2020.0209) — Surveys the encoder and decoder designs of deep forecasters, including attention-based models.
- Zeng, A., Chen, M., Zhang, L. & Xu, Q. (2023). Are Transformers effective for time series forecasting? *Proceedings of the AAAI Conference on Artificial Intelligence*, 37(9), 11121–11128. doi:[10.1609/aaai.v37i9.26317](https://doi.org/10.1609/aaai.v37i9.26317) — A critique showing that simple linear models match or beat several Transformer forecasters, Informer included, on common benchmarks.
