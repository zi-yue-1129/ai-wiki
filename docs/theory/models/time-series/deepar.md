---
status: draft
last_reviewed: 2026-11-06
related:
  - theory/models/rnn/index.md
tags:
  - time series
  - forecasting
  - probabilistic forecasting
aliases:
  - DeepAR
  - DeepAR 機率預測
---

# DeepAR

DeepAR is a probabilistic forecasting method that trains one autoregressive recurrent network on many related time series, and produces a full predictive distribution for each future step. It is one of the three landmark methods compared on the [Time-Series Forecasting](index.md) page.

## Problem

Classical forecasting fits one model to one series. That works for long, clean histories, but a retailer may need forecasts for thousands of products, many with short or intermittent sales records. A separate model for each product cannot borrow strength from the others. The decisions also need more than a single number: a stock plan depends on how likely demand is to exceed a level, so the forecast must describe its uncertainty.

## Core idea

DeepAR uses one recurrent network, shared by all series. At each time step the network reads the previous observed value, the covariates for that step (such as calendar features) and a learned embedding that identifies the series, updates its hidden state, and outputs the parameters of a probability distribution for the next value. Three details make this work on real data:

- **Scaling.** Each series is divided by a scale factor based on its average level before it enters the network, and the scale-dependent outputs are multiplied back afterwards. The network therefore learns patterns that are shared across series of very different sizes.
- **Training windows from short series.** Training windows may start before a series begins, with the unobserved values padded by zeros. The covariates and the embedding then let the model produce forecasts for a new series with little history.
- **Sampling of windows.** Training windows are drawn with probability proportional to the scale factor, so that large series are sampled often enough to be learned well.

## Equation and algorithm

With observations $z_{i,t}$ for series $i$ at time $t$, covariates $x_{i,t}$ and a shared parameter set $\Theta$, the hidden state follows

$$h_{i,t} = h\big(h_{i,t-1},\, z_{i,t-1},\, x_{i,t},\, \Theta\big),$$

and the output parameters are $\theta_{i,t} = \theta(h_{i,t}, \Theta)$. The likelihood is Gaussian for real-valued targets, and a negative binomial distribution for positive counts. Training maximises the summed log-likelihood over all series and all training time steps:

$$\mathcal{L}(\Theta) = \sum_{i}\sum_{t} \log \ell\big(z_{i,t} \mid \theta_{i,t}\big).$$

Because the hidden states are deterministic functions of the observed inputs, this objective can be optimised by ordinary stochastic gradient descent.

To forecast, DeepAR uses ancestral sampling. It draws the next value from the predicted distribution, feeds that sampled value back as the next input, and repeats up to the horizon. Each run gives one trajectory. The experiments in the paper draw 200 sample paths, and quantiles are read from the empirical distribution of the sampled paths.

## Results

The abstract reports accuracy improvements of around 15% over state-of-the-art methods on several real-world forecasting datasets. The paper scores the forecasts with a quantile-based risk measure, computed on the sum of each group of series over the forecast span. Readers should check the paper's tables for the per-dataset numbers rather than rely on the single headline figure.

## Limitations

- **Parametric uncertainty.** The predicted distribution is Gaussian or negative binomial. If the true error distribution has a different shape, for example heavy tails or multiple modes, the quantiles will be miscalibrated.
- **Cost of sampling.** Producing a distribution needs many sequential sample paths for each forecast, which is slower than a single deterministic pass.
- **Error feedback.** Feeding sampled values back as inputs lets errors accumulate over long horizons.
- **Dependence on related series.** The benefit comes from learning across many series. A single long series gains less from the shared model than from a well-tuned local model.

## Connections

DeepAR is an autoregressive [recurrent network](../rnn/index.md) that uses gated cells such as the LSTM. The non-recurrent alternative for point forecasts is [N-BEATS](n-beats.md), and the attention-based one is [Informer](informer.md). The idea of a predictive distribution as a belief about the future is discussed on the [Probabilistic and Bayesian Methods](../../paradigms/probabilistic/index.md) page.

## References

### Seminal papers

- Salinas, D., Flunkert, V. & Gasthaus, J. (2017). *DeepAR: Probabilistic Forecasting with Autoregressive Recurrent Networks*. arXiv. https://arxiv.org/abs/1704.04110 — The original paper: a global autoregressive recurrent network with distributional outputs and sampling-based forecasts.
- Hochreiter, S. & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*, 9(8), 1735–1780. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM cell, the recurrent unit used in the original DeepAR network.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2020). The M4 Competition: 100,000 time series and 61 forecasting methods. *International Journal of Forecasting*, 36(1), 54–74. https://doi.org/10.1016/j.ijforecast.2019.04.014 — Describes the large forecasting competition that set the benchmark for later methods, including this one.

### Surveys and textbooks

- Lim, B. & Zohren, S. (2020). *Time Series Forecasting With Deep Learning: A Survey*. arXiv. https://arxiv.org/abs/2004.13408 — Surveys encoder and decoder designs for one-step-ahead and multi-horizon forecasting.
- Gneiting, T. & Katzfuss, M. (2014). Probabilistic Forecasting. *Annual Review of Statistics and Its Application*, 1, 125–151. https://doi.org/10.1146/annurev-statistics-062713-085831 — Reviews what a probabilistic forecast should satisfy and how it is evaluated, which is the standard DeepAR is judged by.
- Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice*, 3rd ed. OTexts. https://otexts.com/fpp3/ — Free textbook on classical and modern forecasting, with worked examples.
