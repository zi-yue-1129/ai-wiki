---
related:
  - applications/science
  - applications/climate-energy
  - theory/models/gnn
aliases:
  - 天氣預報
  - 地球觀測
  - 遙測
---

# Weather Forecasting and Earth Observation

Weather forecasting is one of the clearest successes of machine learning in science. Learned models now match or beat physics-based forecasts on many medium-range metrics, at a fraction of the compute. Earth observation applies similar models to satellite and other remote-sensing data to map land, disasters and economic activity.

## Landscape

| Area | Methods | Notes |
|---|---|---|
| Medium-range global forecasting | GraphCast (graph neural network); Pangu-Weather (3D transformer with Earth-specific priors); FourCastNet (adaptive Fourier neural operators) | Forecasts take seconds to minutes on a GPU; numerical models remain the physics baseline |
| Foundation models for the Earth system | Aurora (Bodnar et al., 2025) | Pretrained on diverse Earth data, then adapted to several forecasting tasks |
| Evaluation | WeatherBench 2 (Rasp et al., 2023) | Common scores for learned and numerical models |
| Satellite and remote sensing | Convolutional and transformer segmentation of imagery | Land cover, flood and fire mapping |
| Socioeconomic mapping from imagery | Transfer of imagery features to predict asset wealth | Jean et al. (2016) |
| Climate-relevant ML | Surveys of applications across forecasting and monitoring | Rolnick et al. (2022) |

## How it works

Numerical weather prediction solves the equations of atmospheric physics on a grid, starting from an estimate of the current state. Learned models are usually trained on decades of reanalysis data, a reconstruction of past weather that combines observations with a numerical model. Given the current state, the model predicts the state a few hours later, and it is rolled out autoregressively to reach days ahead.

## Why it is hard

- **Extremes**: hurricanes, heat waves and atmospheric rivers are rare in the training record, so models can under-predict them.
- **Inherited bias**: reanalysis data is produced by numerical models, so a learned model can absorb their errors.
- **Physical consistency**: a model can be accurate on average yet violate conservation laws, which matters for downstream use.
- **Sparse observations**: many regions and sensors have few measurements, which limits both training and checking.

## Key methods

- [Graph neural networks](../../theory/models/gnn/index.md): GraphCast operates on a mesh of the globe, passing messages between neighbouring grid points. See [Message passing](../../theory/models/gnn/message-passing/index.md) for the general form.
- [Convolutional networks and U-Net](../../theory/models/cnn/unet/index.md): the standard architecture for segmenting satellite imagery, such as flood or burn-scar maps.
- [Computer vision](../../theory/models/computer-vision/index.md): the image tasks behind remote sensing, from classification to detection.
- [Domain adaptation](../../theory/paradigms/transfer/domain-adaptation/index.md): needed when a model trained on one sensor, region or climate must work on another.

## Connections

- Climate mitigation and energy are covered in [Climate & Energy](../climate-energy/index.md). This page concerns forecasting and observation, which that page also uses.
- The broader role of AI in scientific prediction, including surrogate models of physical simulators, is on [Scientific Discovery](../science/index.md).

## Applications

- Operational medium-range and nowcasting forecasts
- Monitoring floods, wildfires, droughts and crop conditions from satellites (see [Agriculture & Food](../agriculture/index.md))
- Estimating poverty and infrastructure from imagery
- Early warning and disaster response

## Risks and limits

- **Verification gaps**: benchmark scores can hide poor performance on rare, high-impact events.
- **Operational trust**: forecasters need to know when a learned model is likely to fail.
- **Data access and equity**: observation coverage is uneven across countries.
- **Dependence**: if forecasts come from a few learned models, errors can be correlated.

## Open questions

- Whether learned models can reliably forecast extremes they have never seen.
- How to combine data-driven and physics-based forecasts in operational systems.

## References

### Seminal papers

- Lam, R. et al. (2023). Learning skillful medium-range global weather forecasting. *Science*. https://doi.org/10.1126/science.adi2336 — Introduces GraphCast, a graph neural network that outperforms the leading numerical forecast on many medium-range scores.
- Bi, K. et al. (2023). Accurate medium-range global weather forecasting with 3D neural networks. *Nature*. https://doi.org/10.1038/s41586-023-06185-3 — Introduces Pangu-Weather, a 3D network with Earth-specific priors for medium-range forecasts.
- Pathak, J. et al. (2022). FourCastNet: A Global Data-driven High-resolution Weather Model using Adaptive Fourier Neural Operators. arXiv. https://arxiv.org/abs/2202.11214 — Global forecasting model using Fourier neural operators at high spatial resolution.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). U-Net: Convolutional Networks for Biomedical Image Segmentation. arXiv. https://arxiv.org/abs/1505.04597 — The encoder-decoder architecture widely used for dense segmentation, including of satellite images.
- Jean, N. et al. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*. https://doi.org/10.1126/science.aaf7894 — Uses features learned from daytime satellite imagery to predict household wealth in several African countries.

### Surveys and textbooks

- Schultz, M. G. et al. (2021). Can deep learning beat numerical weather prediction? *Philosophical Transactions of the Royal Society A*. https://doi.org/10.1098/rsta.2020.0097 — Reviews what learned models can and cannot yet do relative to numerical forecasting.
- Rolnick, D. et al. (2022). Tackling Climate Change with Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3485128 — Survey of ML applications to forecasting, monitoring and mitigation, with a discussion of their limits.
- Rasp, S. et al. (2023). WeatherBench 2: A benchmark for the next generation of data-driven global weather models. arXiv. https://arxiv.org/abs/2308.15560 — Common evaluation framework for comparing learned and numerical weather models.

### Articles and documentation

- Bodnar, C. et al. (2025). A foundation model for the Earth system. *Nature*. https://doi.org/10.1038/s41586-025-09005-y — Aurora, a model pretrained on diverse Earth-system data and adapted to several forecasting tasks.
