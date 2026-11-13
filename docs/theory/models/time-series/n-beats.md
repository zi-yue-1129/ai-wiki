---
status: draft
last_reviewed: 2026-11-13
tags:
  - time series
  - forecasting
  - interpretability
aliases:
  - N-BEATS
  - 神經基展開時序預測
  - 神經基底展開
---

# N-BEATS

N-BEATS is a deep network for univariate point forecasting that uses no recurrence and no attention. It stacks fully connected residual blocks, and each block predicts a forecast and a backcast as a weighted sum of basis functions. Two configurations are proposed: a generic one, which learns its bases, and an interpretable one, whose bases are a trend polynomial and a seasonal Fourier series. It is one of the landmark methods compared on the [time-series forecasting](index.md) overview.

## Problem

Univariate forecasting, where each series is predicted from its own past, was long dominated by statistical hybrids and by hand-crafted combinations of models. Neural networks had been tried, but they were usually not competitive on standard benchmarks, and their outputs could not be explained. The paper asks whether a pure deep network, without time-series-specific machinery or ensembling of statistical models, can beat the best statistical and hybrid methods while keeping an interpretable form.

## Core idea

The architecture is built from blocks, and each block does two jobs. It estimates the part of its input that it can explain, called the *backcast*, and it produces a partial *forecast*. The next block receives the input with the backcast removed, so it models only what the earlier blocks left unexplained. The final forecast is the sum of all partial forecasts. The authors call this doubly residual stacking.

Within a block, the forecast and backcast are not free outputs. They are expansions of learned coefficients over basis functions, which is why the family is called neural basis expansion. The choice of basis is what separates the two configurations.

## Equation or algorithm

Let $x_\ell$ be the input to block $\ell$, which is a lookback window of length $L$, and let $H$ be the forecast horizon. Each block passes its input through four fully connected ReLU layers, giving a hidden vector $h_\ell$, and then two linear heads produce forward and backward coefficients:

$$
\theta^b_\ell = W^b h_\ell, \qquad \theta^f_\ell = W^f h_\ell
$$

The basis layers $g^b$ and $g^f$ map the coefficients to the backcast and the forecast:

$$
\hat{x}_\ell = \sum_i \theta^b_{\ell,i}\, g^b_i, \qquad \hat{y}_\ell = \sum_i \theta^f_{\ell,i}\, g^f_i
$$

The residual link then passes the unexplained input onward, and the forecast is accumulated:

$$
x_{\ell+1} = x_\ell - \hat{x}_\ell, \qquad \hat{y} = \sum_\ell \hat{y}_\ell
$$

In the **generic** configuration, $g^b$ and $g^f$ are learned linear projections with no time-series structure. In the **interpretable** configuration, a trend stack uses a polynomial basis of low degree, $T(t) = (1, t, t^2, \dots)$, evaluated on a normalised time index over the horizon, and a seasonality stack uses a Fourier basis of cosine and sine terms. Each stack is removed from the input before the next stack is applied, so the trend is explained first and the seasonal pattern is fitted to what remains.

Training uses the symmetric mean absolute percentage error:

$$
\text{sMAPE} = \frac{200}{H}\sum_{t=1}^{H}\frac{|y_t - \hat{y}_t|}{|y_t| + |\hat{y}_t|}
$$

The M4 and M3 models were also trained with MAPE and MASE, and the paper reports results from an ensemble. The final forecast is the median of 180 models, formed from three losses, six lookback windows of between two and seven times the horizon, and several random initialisations.

## Results

On the M4 competition data, the paper's ensemble reaches an average sMAPE of 11.135, against 11.374 for the M4 winner, a hybrid of exponential smoothing and recurrent networks. The abstract states that the design improves accuracy by 11% over a statistical benchmark and by 3% over the M4 winner. The generic and interpretable configurations are close in accuracy. The paper also reports results on the M3 and tourism datasets, where the same architecture is used without changes.

## Limitations

- The paper treats univariate point forecasting only. It does not model covariates such as calendar features, and it does not produce probabilistic forecasts.
- The reported gains rely on ensembles of many networks, which makes training expensive compared with a single model.
- The generic outputs are not interpretable. The interpretable configuration reduces that cost but, on some subsets of M4, it scores slightly worse than the generic one.
- The M4 and M3 series contain no intermittent or lumpy demand, so the method is untested on that kind of data.
- The paper does not say when the architecture should not be used. Its meta-learning reading of the stacked blocks is offered as speculation.

## Connections

N-BEATS is a deep multilayer perceptron with residual links, so it sits close to the [multilayer perceptron](../mlp/index.md) and [residual network](../cnn/backbones-and-scaling/resnet/index.md) families. Its residual structure is a relative of the residual connections used in deep vision models. Its direct multi-horizon output contrasts with the step-by-step prediction of [DeepAR](deepar.md) and with the attention-based forecaster [Informer](informer.md). The choice of trend and seasonal bases is a use of prior knowledge about the data, the same idea that appears in classical decomposition methods covered in the [forecasting overview](index.md).

## References

### Seminal papers

- Oreshkin, B. N., Carpov, D., Chapados, N. & Bengio, Y. (2019). N-BEATS: Neural basis expansion analysis for interpretable time series forecasting. arXiv. https://arxiv.org/abs/1905.10437 — Defines the residual block, the generic and interpretable configurations, and the M4 results. Published at ICLR 2020.
- Smyl, S. (2020). A hybrid method of exponential smoothing and recurrent neural networks for time series forecasting. *International Journal of Forecasting*, 36, 75–85. doi:[10.1016/j.ijforecast.2019.03.017](https://doi.org/10.1016/j.ijforecast.2019.03.017) — The M4 winner, the hybrid method against which N-BEATS reports its 3% gain.

### Surveys and textbooks

- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36, 54–74. doi:[10.1016/j.ijforecast.2019.04.014](https://doi.org/10.1016/j.ijforecast.2019.04.014) — The benchmark, its metrics and the set of competing methods used in the N-BEATS evaluation.
- Lim, B. & Zohren, S. (2021). Time-series forecasting with deep learning: a survey. *Philosophical Transactions of the Royal Society A*, 379, 20200209. doi:[10.1098/rsta.2020.0209](https://doi.org/10.1098/rsta.2020.0209) — Places fully connected multi-horizon forecasters among the deep encoder and decoder designs.
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — Describes the classical decomposition and smoothing methods that the interpretable configuration resembles.
