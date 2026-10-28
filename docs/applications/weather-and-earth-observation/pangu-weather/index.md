---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer/vision-transformer
tags:
  - environment
  - simulation
aliases:
  - Pangu-Weather
  - 盤古天氣
  - 盤古天氣預報
  - Bi et al. 2023
---

# Pangu-Weather (Bi et al. 2023)

Pangu-Weather is a deep learning system for global medium-range weather forecasting. It treats the atmosphere as a three-dimensional cube, processes it with a transformer adapted to the Earth's geometry, and trains a separate model for each of several lead times. It is one of the two landmark methods on the parent page [Weather Forecasting and Earth Observation](../index.md).

## Overview

Numerical weather prediction solves discretised physical equations, which is accurate but expensive. Bi et al. (2023) identify two problems with earlier AI forecasters. Treating the atmosphere as a stack of two-dimensional maps discards the vertical structure, and calling one model many times lets errors accumulate. Pangu-Weather addresses both. It uses a three-dimensional network over pressure levels, and it trains models for several lead times so that fewer model calls are needed. The Nature paper reports stronger deterministic results than the operational ECMWF Integrated Forecasting System (IFS) on reanalysis data in all tested variables.

## Key concepts

- **3D Earth-Specific Transformer (3DEST)**: a variant of the vision transformer that works on cubes of pressure level, latitude and longitude, with an Earth-specific positional bias. See [Vision Transformer](../../../theory/models/transformer/vision-transformer/index.md).
- **Shifted windows**: attention is computed within local windows that shift between layers, the mechanism of the Swin Transformer (Liu et al., 2021). The authors adapt this mechanism to weather data.
- **Hierarchical temporal aggregation**: training models for lead times of 1, 3, 6 and 24 hours. A 24-hour model covers a day in one call, so a five-day forecast needs five calls rather than 120 calls to a one-hour model.
- **Pressure levels**: the vertical dimension of the atmosphere, with data on fixed pressure surfaces from the ground upward.

## How it works

The input is ERA5 reanalysis on a grid of 1440 by 721 points at 0.25 degrees. The preprint uses 13 pressure levels with five upper-air variables (geopotential, specific humidity, temperature, and the two wind components), four surface variables (2-metre temperature, 10-metre winds and mean sea level pressure), and three constant masks for topography, land–sea and soil type.

A model $f$ with parameters $\theta$ maps the state at time $t$ to the state a fixed lead time $\Delta t$ later:

$$\hat{A}_{t+\Delta t} = f(A_t;\, \theta)$$

The network is an encoder–decoder. The upper-air and surface data are embedded into two cubes and concatenated along the height dimension. Encoder blocks reduce resolution and the decoder mirrors them. Each block is a 3DEST block, a vision-transformer block whose shifted-window mechanism and positional bias respect the Earth's geometry. Training used ERA5 data from 1979 onward, about 39 years, and each model ran for 100 epochs on 192 GPUs, roughly 15 days per model.

## Results

The benchmark is ERA5 as ground truth, with comparisons against the operational IFS and FourCastNet, using latitude-weighted root-mean-square error (RMSE) and anomaly correlation coefficient (ACC) across variables and lead times. The arXiv preprint reports that for a single-member forecast, the RMSE of the 5-day 500 hPa geopotential (Z500) is 296.7, against 333.7 for the IFS and 462.5 for FourCastNet.[^1] The preprint also reports an inference time of 1,400 ms for a forecast on one GPU, more than 10,000 times faster than the operational IFS. The Nature abstract adds that the model tracks tropical cyclones more accurately than ECMWF's high-resolution forecast when started from reanalysis, and that it works with ensemble forecasts.

## Limitations

- **Cyclone intensity.** Predicted minimum pressure is often about 50 hPa higher than the ERA5 value, while track errors are reasonable. The preprint attributes this partly to the lack of unbiased intensity data in the training archive.
- **Training not converged.** The authors note that 100 epochs was the largest budget they could use, and that more data or time would likely improve accuracy.
- **Limited variables.** Precipitation is not among the predicted variables, and the authors list adding more observed variables as future work.
- **Several models.** Hierarchical aggregation needs a separate trained model for each lead time, which multiplies the training and storage cost.

## Open questions

- Would the gain over NWP hold with real-time observations, rather than reanalysis initial conditions used in these comparisons?
- The authors propose three directions: more observation variables, a fourth (time) dimension, and deeper or wider networks. Which of these yields the most accuracy per unit of compute is untested.
- Better intensity forecasts may need higher-resolution training data that include unbiased cyclone observations.

## References

### Seminal papers

- Bi, K. et al. (2023). *Accurate medium-range global weather forecasting with 3D neural networks*. Nature. https://doi.org/10.1038/s41586-023-06185-3 — The published Pangu-Weather paper on 3D Earth-specific transformers and hierarchical temporal aggregation.
- Bi, K. et al. (2022). *Pangu-Weather: A 3D High-Resolution Model for Fast and Accurate Global Weather Forecast*. arXiv. https://arxiv.org/abs/2211.02556 — The preprint, which reports the detailed RMSE and timing figures quoted on this page.
- Pathak, J. et al. (2022). *FourCastNet: A Global Data-driven High-resolution Weather Model using Adaptive Fourier Neural Operators*. arXiv. https://arxiv.org/abs/2202.11214 — The main AI baseline in Pangu-Weather's comparisons, using Fourier neural operators.

### Articles and documentation

- Liu, Z. et al. (2021). *Swin Transformer: Hierarchical Vision Transformer using Shifted Windows*. arXiv. https://arxiv.org/abs/2103.14030 — The shifted-window transformer whose mechanism the 3DEST block adapts.
- Hersbach, H. et al. (2020). *The ERA5 global reanalysis*. Quarterly Journal of the Royal Meteorological Society. https://doi.org/10.1002/qj.3803 — Describes ERA5, the reanalysis used for training and evaluation.
- Rasp, S. et al. (2023). *WeatherBench 2: A benchmark for the next generation of data-driven global weather models*. arXiv. https://arxiv.org/abs/2308.15560 — Open evaluation framework and baselines for data-driven weather models.

[^1]: These figures are from the arXiv preprint (arXiv:2211.02556). The published version may report different numbers, so check it before quoting them.
