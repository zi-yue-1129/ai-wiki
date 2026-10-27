---
related:
- applications/science
- applications/agriculture
- engineering/hardware
- society/economics
---

# Climate & Energy

## AI for climate

| Area | Examples |
|---|---|
| Weather and climate modelling | AI weather models (GraphCast, GenCast, Pangu-Weather, ECMWF's AIFS); ML parameterisations in climate models; hybrid models such as NeuralGCM |
| Extreme events | Flood forecasting in 80+ countries (Google Flood Hub), wildfire detection, cyclone tracking, heatwave prediction |
| Emissions monitoring | Satellite detection of methane plumes, power-plant emissions from imagery (Climate TRACE), deforestation alerts |
| Electricity grids | Load and renewable-output forecasting, grid balancing, fault detection, demand response |
| Buildings and industry | HVAC control (DeepMind cut data-centre cooling energy by ~40% in 2016), process efficiency |
| Materials for energy | Battery electrolytes, catalysts, solar materials, carbon capture sorbents (see [Scientific Discovery](../science/index.md)) |
| Fusion | RL control of tokamak plasmas; disruption prediction |
| Transport | Route optimisation, EV charging scheduling |
| Adaptation | Crop resilience, early-warning systems, insurance |

Rolnick et al. (2022), "Tackling Climate Change with Machine Learning", *ACM Computing Surveys*, maps this space comprehensively.

## AI's own footprint

| Issue | Notes |
|---|---|
| Electricity | Data-centre demand is growing rapidly; the IEA (2025) projected global data-centre electricity use roughly doubling by 2030, with AI a major driver |
| Carbon | Depends on grid mix and timing; training a frontier model is significant but inference at scale now dominates many estimates |
| Water | Cooling consumes water; local stress matters |
| Hardware | Embodied emissions of chips and servers; e-waste |
| Transparency | Few providers disclose per-model energy use; estimates vary widely |

Mitigations: more efficient models (distillation, quantisation, MoE, sparsity), efficient hardware, scheduling to clean energy, siting near renewables, reporting standards. Neuromorphic computing promises large energy savings for certain workloads (see [Spiking Networks](../../brain-mind/snn-neuromorphic/index.md)).

## Resources

- [Climate Change AI](https://www.climatechange.ai/) — papers, summer school, tutorials
- IEA (2025), *Energy and AI*
- Luccioni et al., work on measuring AI's carbon footprint; [CodeCarbon](https://codecarbon.io/)
- [WeatherBench 2](https://sites.research.google/weatherbench/)
