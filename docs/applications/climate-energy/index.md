---
related:
- applications/science
- applications/agriculture
- engineering/hardware
- society/economics
aliases:
  - 氣候
  - 能源
---

# Climate & Energy

## AI for climate

| Area | Examples |
|---|---|
| Weather and climate modelling | AI weather models (GraphCast, GenCast, Pangu-Weather, ECMWF's AIFS); ML parameterisations in climate models; hybrid models such as NeuralGCM |
| Extreme events | Flood forecasting (Google Flood Hub), wildfire detection, cyclone tracking, heatwave prediction |
| Emissions monitoring | Satellite detection of methane plumes, power-plant emissions from imagery (Climate TRACE), deforestation alerts |
| Electricity grids | Load and renewable-output forecasting, grid balancing, fault detection, demand response |
| Buildings and industry | HVAC control, for example in data centres, and process efficiency |
| Materials for energy | Battery electrolytes, catalysts, solar materials, carbon capture sorbents (see [Scientific Discovery](../science/index.md)) |
| Fusion | RL control of tokamak plasmas; disruption prediction |
| Transport | Route optimisation, EV charging scheduling |
| Adaptation | Crop resilience, early-warning systems, insurance |

Rolnick et al. (2022), "Tackling Climate Change with Machine Learning", *ACM Computing Surveys*, maps this space comprehensively.

## AI's own footprint

| Issue | Notes |
|---|---|
| Electricity | Data-centre demand is growing rapidly, and projections of AI's share vary widely |
| Carbon | Depends on grid mix and timing; training a frontier model is significant but inference at scale now dominates many estimates |
| Water | Cooling consumes water; local stress matters |
| Hardware | Embodied emissions of chips and servers; e-waste |
| Transparency | Few providers disclose per-model energy use; estimates vary widely |

Mitigations: more efficient models (distillation, quantisation, MoE, sparsity), efficient hardware, scheduling to clean energy, siting near renewables, reporting standards. Neuromorphic computing promises large energy savings for certain workloads (see [Spiking Networks](../../brain-mind/snn-neuromorphic/index.md)).

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Graph neural networks](../../theory/models/gnn/message-passing/index.md): message passing over a graph of the atmosphere, as in GraphCast (Lam et al., 2023).
- [Denoising diffusion](../../theory/paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md): a diffusion model that generates an ensemble of forecasts, as in GenCast (Price et al., 2024).
- [Policy gradient and actor-critic](../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md): reinforcement learning for controlling physical systems, such as tokamak plasma shape (Degrave et al., 2022).

## References

### Seminal papers

- Lam et al. (2023). Learning skillful medium-range global weather forecasting. *Science*. https://doi.org/10.1126/science.adi2336 — GraphCast, a graph neural network that forecasts global weather.
- Price et al. (2024). Probabilistic weather forecasting with machine learning. *Nature*. https://doi.org/10.1038/s41586-024-08252-9 — GenCast, a diffusion-based model for probabilistic forecasts.
- Bi et al. (2023). Accurate medium-range global weather forecasting with 3D neural networks. *Nature*. https://doi.org/10.1038/s41586-023-06185-3 — Pangu-Weather, a 3D neural network for global forecasts.
- Degrave et al. (2022). Magnetic control of tokamak plasmas through deep reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-021-04301-9 — Reinforcement learning controls plasma shape in a tokamak.

### Surveys and textbooks

- Rolnick et al. (2022). Tackling Climate Change with Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3485128 — Comprehensive review of machine learning for climate mitigation and adaptation.
