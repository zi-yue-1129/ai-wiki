---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/rnn/index.md
tags:
  - time series
  - forecasting
  - sequence models
aliases:
  - Time-series forecasting
  - 時間序列預測
  - 時序預測
  - 時間序列
  - forecasting
---

# Time-Series Forecasting

Time-series forecasting predicts future values of a quantity from its past values and, often, from related variables. Electricity demand, sales, traffic, temperature, and the readings of a sensor are all sequences observed over time, and a good forecast lets a planner act before the event. The problem looks like language modelling, but the data are numbers measured at regular intervals, the cost of error is usually in the units of the quantity itself, and the uncertainty of the forecast often matters as much as its central value.

## Overview

A forecast is a function from a history of observations to a prediction for one or more future steps, the *horizon*. Forecasts can be point estimates, which give a single value, or probabilistic, which give a distribution or a set of quantiles. Probabilistic forecasts are needed when a decision depends on the risk of an extreme value, such as stocking enough of a product or reserving enough power.

Evaluation must respect time. A model is trained on the past and tested on a later period, and the test window is usually rolled forward over many origins, so that the result does not depend on one lucky split. Shuffling the data, as is standard in many machine-learning tasks, leaks future information into training and can overstate accuracy.

## Key concepts

- **Horizon**: how far ahead the model predicts. Multi-horizon forecasts predict several steps at once.
- **Stationarity**: a series whose statistical properties do not change over time. Many classical methods assume it, or assume that it can be made stationary by differencing.
- **Covariates**: variables known in the future, such as holidays or planned prices, that can improve the forecast.
- **Related series**: many series from the same domain, such as the sales of thousands of products. Models can learn across them.
- **Encoder and decoder**: the part of the model that reads the history and the part that produces the forecast.

## How it works

Classical methods, such as exponential smoothing and autoregressive models, fit a small number of parameters to one series at a time. They are fast, interpretable and hard to beat on short, simple series. Deep learning methods instead learn from many series at once, and they can use many covariates. Lim and Zohren (2020) survey the encoder and decoder designs used in one-step-ahead and multi-horizon forecasting, including recurrent, convolutional and attention-based models.

**Probabilistic autoregression.** DeepAR (Salinas et al., 2017) trains an autoregressive recurrent network on a large number of related time series. For each step, the network outputs the parameters of a probability distribution over the next value, and the forecast is a sampled trajectory. The model learns the scale and shape of each series from the group, so new series with little history can still be forecast.

**Basis expansion without recurrence.** N-BEATS (Oreshkin et al., 2019) uses a deep stack of fully connected residual blocks that predict a forecast as a combination of basis functions. The authors present a generic version and an interpretable version whose basis functions are trend and seasonality. The abstract reports that the design improves forecast accuracy over a statistical benchmark by 11% and over the previous year's winner of the M4 competition by 3%.

**Long sequences with attention.** Informer (Zhou et al., 2020) adapts the [Transformer](../transformer/index.md) to long-sequence forecasting. Its abstract frames the problem as one that demands high prediction capacity for long horizons, which motivates a more efficient attention mechanism. It is one of several Transformer variants proposed for forecasting.

## Key methods

Brief comparison. Each named method is a candidate for its own method page; those pages are not yet written, so the detail is given in this section for now.

- **DeepAR (probabilistic recurrent)**: autoregressive recurrent network trained on many series, with a distributional output. Natural for uncertainty, and sequential at inference.
- **N-BEATS (residual basis expansion)**: no recurrence or attention; interpretable or generic. Strong on univariate benchmarks.
- **Informer (efficient attention)**: a Transformer variant for long horizons, with a cheaper attention mechanism.

## Connections

The recurrent designs are described on the [Recurrent Networks](../rnn/index.md) page, and the attention designs on the [Transformer](../transformer/index.md) page. State-space models, which give long memory with linear-time updates, are on the [State-Space Models](../ssm/index.md) page. Forecasting also connects to probabilistic reasoning, since the output of a probabilistic forecast is a belief about the future, see [Probabilistic and Bayesian Methods](../../paradigms/probabilistic/index.md).

Neural recordings are time series too, so the same modelling questions arise in neuroscience. The connection is discussed in [NeuroAI](../../../brain-mind/neuroai/index.md).

## Applications

- **Energy.** Forecasting electricity demand and renewable generation to balance supply.
- **Retail and supply chains.** Forecasting demand for many products, where the decision is how much to stock.
- **Transport and weather.** Forecasting traffic flow and weather variables, where probabilistic forecasts support warnings and routing.

## Open questions

- Deep models are often evaluated on large collections of series, where they can benefit most. Their advantage on small or noisy series is less clear, so benchmark results need careful reading.
- Distribution shift breaks forecasts when the process changes, and detecting the change in time is hard.
- Fair evaluation needs held-out periods and baselines tuned as carefully as the new model, which is not always done.
- Combining forecasts with covariates that are themselves uncertain is an open modelling problem.

## References

### Seminal papers

- Salinas, D., Flunkert, V. & Gasthaus, J. (2017). *DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks*. arXiv. https://arxiv.org/abs/1704.04110 — Trains an autoregressive recurrent network on many related series to output probabilistic forecasts.
- Oreshkin, B. N., Carpov, D., Chapados, N. & Bengio, Y. (2019). *N-BEATS: Neural basis expansion analysis for interpretable time series forecasting*. arXiv. https://arxiv.org/abs/1905.10437 — A deep residual architecture for forecasting that reports gains on the M4 benchmark.
- Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H. & Zhang, W. (2020). *Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting*. arXiv. https://arxiv.org/abs/2012.07436 — A Transformer variant for long-horizon forecasting with a more efficient attention mechanism.

### Surveys and textbooks

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — Surveys encoder and decoder designs for one-step-ahead and multi-horizon forecasting.
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — A textbook on classical and modern forecasting methods, free to read online. The page does not state a year.
