---
status: draft
last_reviewed: 2026-10-28
tags:
  - sequence modelling
  - recurrent networks
  - density estimation
aliases:
  - DeepAR
  - 自回歸循環網路
  - 機率預測
---

# DeepAR (Salinas et al. 2020)

DeepAR is a recurrent forecasting model trained on many related time series at once. For each future value it outputs a probability distribution rather than a single number, which suits stocking decisions. It is one of the methods described on the parent page [Logistics and Supply Chain](../index.md).

## Overview

Classical methods such as exponential smoothing are usually fitted to one series at a time. A retailer has many items at many locations, many of them erratic or intermittent, and new products with little history. DeepAR asks whether one model trained jointly on all the series can learn their shared structure and produce accurate probabilistic forecasts. The paper reports that it does, and that the uncertainty growth over the horizon is learned from the data rather than assumed to be linear.

## Key concepts

- **Global model**: one set of parameters shared by all series.
- **Autoregression**: at each step the model takes the previous observation as input.
- **Recurrent state**: an [LSTM](../../../theory/models/rnn/gated-cells/lstm/index.md) hidden state carries the observed past into the forecast period.
- **Likelihood**: the distribution output for each step. The paper uses a Gaussian for real values and a negative binomial for counts.
- **Ancestral sampling**: drawing whole future paths by feeding each sampled value back into the network, so that quantiles can be estimated.
- **ρ-risk**: the quantile loss used for evaluation.

## How it works

Let $z_{i,t}$ be the value of series $i$ at time $t$ and $x_{i,t}$ its covariates. The future of the series, given its observed past, is factorised into likelihood terms:

$$
Q_\Theta(z_{i,t_0:T} \mid z_{i,1:t_0-1}, x_{i,1:T}) = \prod_{t=t_0}^{T} \ell\big(z_{i,t} \mid \theta(h_{i,t}, \Theta)\big), \qquad h_{i,t} = h(h_{i,t-1}, z_{i,t-1}, x_{i,t}, \Theta),
$$

where $h$ is a multi-layer LSTM and $\theta$ is produced from its output. For the Gaussian case the mean is affine in $h_{i,t}$ and the standard deviation passes through a softplus to stay positive. The encoder and decoder share weights.

1. **Scale.** Divide each series by its average over the observed range, so series of very different sizes can share one network. Multiply the outputs back.
2. **Train.** Cut each series into windows and maximise the log-likelihood of the observed values, feeding observed values back as inputs.
3. **Weight the sampling.** Choose windows with probability proportional to the series' scale. The paper's ablation shows that removing scaling and this weighted sampling reduces accuracy.
4. **Predict.** Run the observed range, draw many sample paths, and compute the quantiles or sums of interest.

## Results

On the parts dataset (monthly automobile-part sales) and on two Amazon weekly-sales datasets, the paper reports that DeepAR performs significantly better than the compared methods. The variant with a Gaussian likelihood is clearly worse on the count datasets, which supports the negative binomial choice (Salinas et al., 2020). On electricity and traffic data, the normalised deviation of DeepAR is 0.07 and 0.17, against 0.16 and 0.20 for matrix factorisation.[^1]

## Limitations

- **Dependence on pooling.** Gains come from learning across many series. A firm with few long series, or with new products, benefits less.
- **Noise model.** The forecast is only as good as the chosen likelihood, and other data types need other likelihoods.
- **Covariates.** Promotions, supplier failures and other causes of demand change must be supplied as covariates.
- **Sampling cost.** Quantiles come from many sample paths, although the paper reports prediction as fast.
- **Age.** The experiments predate transformer forecasters such as the Temporal Fusion Transformer (Lim et al., 2019).

## Open questions

- Does a better probabilistic score lower stock-out and holding costs? The paper measures forecast accuracy, not inventory outcomes.
- How do recurrent global models compare with transformer-based ones on the same retail data?
- Can the distributions be recalibrated with [conformal prediction](../../../theory/machine-learning/uncertainty-and-calibration/conformal-prediction/index.md) to guarantee coverage?

[^1]: Table 2 of Salinas et al. (2020). The arXiv abstract (arXiv:1704.04110) summarises the gain over state-of-the-art methods as around 15%.

## References

### Seminal papers

- Salinas, D. et al. (2020). DeepAR: probabilistic forecasting with autoregressive recurrent networks. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2019.07.001 — Trains one recurrent model across many related series to output full predictive distributions, tested on retail and public energy and traffic data.
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM cell used as DeepAR's recurrent state.
- Lim, B. et al. (2019). Temporal fusion transformers for interpretable multi-horizon time series forecasting. arXiv. https://arxiv.org/abs/1912.09363 — Transformer-based multi-horizon forecaster that combines static covariates, known future inputs and historical series.

### Surveys and textbooks

- Petropoulos, F. et al. (2020). Forecasting: theory and practice. arXiv. https://arxiv.org/abs/2012.03854 — Non-systematic review of forecasting methods across fields, from classical statistics to machine learning.
- Makridakis, S., Spiliotis, E. & Assimakopoulos, V. (2022). M5 accuracy competition: results, findings, and conclusions. *International Journal of Forecasting*. https://doi.org/10.1016/j.ijforecast.2021.11.013 — Reports a large benchmark of hierarchical retail forecasts that compared many methods.
