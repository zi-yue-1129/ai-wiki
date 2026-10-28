---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/gnn
tags:
  - environment
  - simulation
aliases:
  - GraphCast
  - 圖神經網路天氣預報
  - Lam et al. 2023
---

# GraphCast (Lam et al. 2023)

GraphCast is a graph neural network that predicts global weather six hours ahead. Run repeatedly, it produces forecasts up to 10 days long, and it is trained directly on decades of reanalysis data. It is one of the two landmark methods on the parent page [Weather Forecasting and Earth Observation](../index.md).

## Overview

Operational medium-range forecasts come from numerical weather prediction, which solves the physics of the atmosphere on a supercomputer. Lam et al. (2023) ask whether a model learned from historical data can match that accuracy at a fraction of the cost. GraphCast answers yes for deterministic forecasts. It predicts hundreds of weather variables, and the authors report that it outperforms ECMWF's High RESolution forecast (HRES), the most accurate operational deterministic system they compared against, on most of the targets they evaluated. Its architecture follows learned simulators in which graph networks model fluid and solid dynamics (Sanchez-Gonzalez et al., 2020).

## Key concepts

- **Grid and state**: the atmosphere is stored on a 0.25-degree latitude–longitude grid of 721 by 1,440 points. Each point holds 5 surface variables and 6 atmospheric variables on 37 pressure levels.
- **Multi-mesh**: a graph built by refining an icosahedron six times. Its 40,962 nodes spread almost evenly over the globe, and edges from every refinement level let information travel both locally and over long distances.
- **Encode, process, decode**: a learned encoder maps grid values onto the mesh, a processor passes messages across the mesh, and a decoder maps the result back to the grid.
- **Autoregressive rollout**: forecasts are made by feeding each prediction back in as the next input.

## How it works

GraphCast takes two consecutive states, the current one and the one six hours earlier, and predicts the next state. Its steps are:

1. **Encode.** A single graph-network layer maps the normalised input variables, with zero mean and unit variance, from the grid onto the multi-mesh.
2. **Process.** Sixteen graph-network layers, with unshared weights, pass learned messages across the mesh.
3. **Decode.** A single layer maps the features back to the grid and outputs a per-node prediction $\hat{Y}_t$.
4. **Update.** The next state is the current state plus that prediction:

$$\hat{X}_{t+1} = X_t + \hat{Y}_t$$

Training minimises the mean squared error, weighted by vertical level and averaged over $N$ autoregressive steps. The number of steps was raised during training from 1 to 12, that is from six hours to three days. The model was trained on 39 years (1979–2017) of ERA5 reanalysis, using gradient descent and backpropagation for about four weeks on 32 Cloud TPU v4 devices. It has 36.7 million parameters. A 10-day forecast is 40 six-hour steps, and it takes under a minute on a single TPU v4.

## Results

The main benchmark compares GraphCast with HRES on held-out data from 2018 onward. ERA5 serves as ground truth, and HRES is scored against its own analysis-based dataset so that its first step is not penalised. Skill is measured as root-mean-square error (RMSE) over 1,380 targets, which are variables at pressure levels across 10-day lead times. The arXiv preprint reports that GraphCast beats HRES on 90.3% of these targets, and significantly on 89.9%.[^1] The Science abstract gives the rounded figure of 90%. The authors also report that GraphCast beats Pangu-Weather on 99.2% of the 252 targets that Pangu-Weather presented, and that its median cyclone track error over 2018 to 2021 is lower than HRES.

## Limitations

- **Deterministic output.** GraphCast gives one forecast. Its mean-squared-error objective encourages spatially smoothed predictions at long lead times, so forecasts blur. The authors name ensemble prediction as a crucial next step.
- **Smaller than HRES.** GraphCast runs at 0.25 degrees, 37 pressure levels and 6-hour steps, while HRES uses 0.1 degrees, 137 levels and steps of up to one hour. The authors kept the largest model that they could practically fit.
- **Excluded variables.** Total precipitation is left out of the evaluation because ERA5's precipitation has known biases.
- **Reanalysis dependence.** Training and scoring both rely on ERA5, which is itself produced by a forecasting model.

## Open questions

- Can a learned model give calibrated probabilities without the blurring that a single mean-squared-error forecast produces? Later probabilistic models such as GenCast (Price et al., 2024) address this.
- Does the skill extend to precipitation and to rare, extreme events, which the evaluation treats only partly?
- The authors expect the approach to scale with compute and higher-resolution data. Whether accuracy keeps improving at finer resolution is not tested in the paper.

[^1]: The preprint numbers (arXiv:2212.12794) are the source for the 90.3% and 89.9% figures; the published abstract gives the rounded 90% figure.

## References

### Seminal papers

- Lam, R. et al. (2023). *Learning skillful medium-range global weather forecasting*. Science. https://doi.org/10.1126/science.adi2336 — The GraphCast paper, covering the model, its training and its comparison with ECMWF's HRES.
- Sanchez-Gonzalez, A. et al. (2020). *Learning to Simulate Complex Physics with Graph Networks*. arXiv. https://arxiv.org/abs/2002.09405 — Graph-network simulators that learn fluid and solid dynamics, the design lineage of GraphCast's encoder-processor-decoder.
- Keisler, R. (2022). *Forecasting Global Weather with Graph Neural Networks*. arXiv. https://arxiv.org/abs/2202.07575 — An earlier graph-network approach to global forecasting, trained on ERA5 and compared with operational models.

### Articles and documentation

- Hersbach, H. et al. (2020). *The ERA5 global reanalysis*. Quarterly Journal of the Royal Meteorological Society. https://doi.org/10.1002/qj.3803 — Describes ERA5, the reanalysis that GraphCast is trained and evaluated on.
- Rasp, S. et al. (2023). *WeatherBench 2: A benchmark for the next generation of data-driven global weather models*. arXiv. https://arxiv.org/abs/2308.15560 — Open evaluation framework and baselines for data-driven weather models.
- Bi, K. et al. (2023). *Accurate medium-range global weather forecasting with 3D neural networks*. Nature. https://doi.org/10.1038/s41586-023-06185-3 — The Pangu-Weather paper, a contemporary learned forecaster.
