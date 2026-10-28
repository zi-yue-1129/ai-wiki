---
related:
- theory/models/agents
- theory/paradigms/symbolic-ai
- theory/paradigms/active
- applications/climate-energy
---

# Scientific Discovery

AI is changing how science is done: as **surrogate simulator**, **pattern finder**, **hypothesis generator**, **experiment planner** and increasingly as **research agent**.

## By field

| Field | Examples |
|---|---|
| Weather and climate | GraphCast (GNN), Pangu-Weather, FourCastNet, GenCast (diffusion, probabilistic), and AI forecasts adopted operationally by ECMWF (AIFS, 2025) — often more accurate than traditional numerical models at a fraction of the compute |
| Materials science | GNoME predicted hundreds of thousands of new stable crystals; MatterGen generates materials with target properties; machine-learned interatomic potentials (MACE) speed up simulation |
| Chemistry | Retrosynthesis planning, reaction prediction, autonomous chemistry labs (Coscientist, ChemCrow) |
| Physics | Jet tagging and anomaly detection at the LHC; controlling tokamak plasma with RL (Degrave et al., 2022); neural-network quantum states; symbolic regression to rediscover laws |
| Astronomy | Exoplanet detection, galaxy morphology, gravitational-wave detection, imaging the black-hole shadow with learned priors |
| Mathematics | Guiding intuition in knot theory and representation theory (Davies et al., 2021); FunSearch for combinatorics; AlphaProof and AlphaGeometry for olympiad problems; LLM + Lean formalisation |
| Biology | See [Life Sciences](../life-science/index.md) |
| Earth observation | Flood forecasting (Google Flood Hub), deforestation monitoring, crop mapping |
| Neuroscience | Connectome reconstruction, spike sorting, behaviour tracking — see [Neuroscience Basics](../../brain-mind/neuroscience/index.md) |

## Paradigms

- **Surrogate models / emulators**: train a network to approximate an expensive simulation (CFD, climate, molecular dynamics) — orders of magnitude faster
- **Physics-informed ML**: embed differential equations or symmetries into models (PINNs, neural operators like FNO, equivariant networks)
- **Inverse problems**: infer causes from observations (imaging, tomography) with learned priors
- **Closed-loop discovery**: Bayesian optimisation + robotics = self-driving labs (e.g. A-Lab for materials synthesis)
- **Literature-based discovery**: LLMs mining millions of papers for connections
- **AI scientists**: agents that generate hypotheses, run computational experiments and write papers (Sakana's AI Scientist, Google's AI co-scientist, FutureHouse's agents); outputs still need careful human vetting

## Concerns

- **Reproducibility**: data leakage in ML-based science is widespread (Kapoor & Narayanan, 2023, found leakage across many fields)
- **Validation**: AI-generated hypotheses and claims (e.g. "millions of new materials") need experimental confirmation; some claims were later critiqued
- **Understanding vs prediction**: accurate predictions without mechanistic insight
- **Monoculture**: over-reliance on the same tools and datasets narrows inquiry (Messeri & Crockett, 2024, *Nature*)

## Resources

- Wang et al. (2023), "Scientific discovery in the age of artificial intelligence", *Nature*
- [AI for Science](https://ai4sciencecommunity.github.io/) community; Microsoft Research AI for Science; DeepMind science blog
- Karniadakis et al. (2021), "Physics-informed machine learning", *Nature Reviews Physics*
- [WeatherBench 2](https://sites.research.google/weatherbench/)
