---
status: draft
last_reviewed: 2026-11-06
related:
  - theory/models/mlp/index.md
tags:
  - time series
  - forecasting
  - interpretability
aliases:
  - N-BEATS
  - 神經基底展開
---

# N-BEATS

N-BEATS is a deep, purely fully connected architecture for univariate point forecasting. It uses stacks of residual blocks, each of which produces a backcast of its input and a forecast of the future. An interpretable variant constrains the forecast to a trend and a seasonal component. It is one of the three landmark methods compared on the [Time-Series Forecasting](index.md) page.

## Problem

In the M-competitions, the most accurate methods for univariate forecasting were statistical methods and hybrids that combined statistical and neural components with hand-designed features. Plain deep networks did not win. N-BEATS asks whether a generic deep network, with no time-series-specific components, can match or beat these methods, and whether a deep model can also be interpretable, since the forecast of a trend and a seasonal pattern should be readable by a planner.

## Core idea

The network is a stack of blocks. Each block takes a window of the recent past, passes it through four or more fully connected layers, and produces two outputs:

- a **backcast**, its estimate of the part of the input window it can explain, and
- a **forecast**, its prediction for the next part of the series.

Blocks are chained as residuals. Each block subtracts its backcast from its input before the next block sees it, so each block models what the earlier blocks left unexplained. The final forecast is the sum of all the block forecasts.

The interpretable version changes what the blocks can output. It uses two stacks. The trend stack's forecast is a low-degree polynomial in time, and the seasonality stack's forecast is a sum of sine and cosine terms (a Fourier basis). The authors report that this version loses little accuracy compared with the generic one.

## Equation and algorithm

For block $\ell$ with input $x_\ell$, a fully connected network produces parameters $\theta^b_\ell$ and $\theta^f_\ell$. The backcast and forecast are linear projections onto basis matrices $V^b_\ell$ and $V^f_\ell$:

$$\hat{x}_\ell = V^b_\ell\, \theta^b_\ell, \qquad \hat{y}_\ell = V^f_\ell\, \theta^f_\ell.$$

The next block receives $x_{\ell+1} = x_\ell - \hat{x}_\ell$, and the forecast is $\hat{y} = \sum_\ell \hat{y}_\ell$. In the generic version the basis matrices are learned. In the interpretable version they are fixed: polynomial powers of a normalised time index for the trend stack, and sine and cosine functions for the seasonality stack.

The authors train ensembles of such models with different lookback lengths and losses. The losses are sMAPE, MASE and MAPE, and the paper states that TOURISM uses MAPE alone.

## Results

The abstract reports that N-BEATS improves forecast accuracy by 11% over a statistical benchmark, and by 3% over the winner of the previous M4 competition. On M4, the paper's generic model reaches an overall weighted accuracy (OWA) of 0.797, against 0.821 for the M4 winner and 0.861 for the best statistical entry. The paper also reports state-of-the-art results on M3 and TOURISM. These numbers come from the paper's own tables and should be checked there before reuse.

## Limitations

- **Univariate scope.** The method forecasts one series from its own past. The base design takes no covariates, so it cannot use holidays or planned prices directly.
- **Point forecasts.** The output is a single value per step. Uncertainty needs a separate method, such as an ensemble or a quantile extension.
- **Cost.** The best results use ensembles of many trained models, which costs much more than one model.
- **Benchmark dependence.** The strongest evidence comes from M-competition data. Performance on industrial data with intermittent demand or many covariates is less well established by the paper.

## Connections

N-BEATS is a deep [multilayer perceptron](../mlp/index.md) with residual connections, and it shows that recurrence and attention are not required for forecasting. Its probabilistic counterpart is [DeepAR](deepar.md), and the attention-based alternative is [Informer](informer.md).

## References

### Seminal papers

- Oreshkin, B. N., Carpov, D., Chapados, N. & Bengio, Y. (2019). *N-BEATS: Neural basis expansion analysis for interpretable time series forecasting*. arXiv. https://arxiv.org/abs/1905.10437 — The original paper: a residual stack of fully connected blocks with generic and interpretable variants, evaluated on M3, M4 and TOURISM.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014 — The competition whose winner N-BEATS is compared against, and the source of the benchmark.
- Hyndman, R. J. & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting*, 22(4), 679–688. https://doi.org/10.1016/j.ijforecast.2006.03.001 — Discusses scale-free error measures for comparing forecasts across series, including the scaled errors used in MASE.

### Surveys and textbooks

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — Surveys deep forecasting architectures, including the non-recurrent designs that N-BEATS belongs to.
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — Free textbook covering the classical trend and seasonal methods that the interpretable version re-creates in neural form.
- Gneiting, T. & Katzfuss, M. (2014). Probabilistic Forecasting. *Annual Review of Statistics and Its Application*, 1, 125–151. https://doi.org/10.1146/annurev-statistics-062713-085831 — Reviews how point and probabilistic forecasts are evaluated, which is the context for the point-forecast results here.
