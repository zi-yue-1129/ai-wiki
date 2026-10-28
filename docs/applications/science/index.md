---
related:
- theory/models/agents
- theory/paradigms/symbolic-ai
- theory/paradigms/active
- applications/climate-energy
aliases:
  - 科學發現
  - 科學研究
---

# Scientific Discovery

AI is changing how science is done: as **surrogate simulator**, **pattern finder**, **hypothesis generator**, **experiment planner** and increasingly as **research agent**.

## By field

| Field | Examples |
|---|---|
| Weather and climate | GraphCast (GNN), Pangu-Weather, FourCastNet, GenCast (diffusion, probabilistic); AI forecasts that are competitive with numerical weather models on many metrics (Lam et al., 2023) |
| Materials science | GNoME predicted hundreds of thousands of stable crystals (Merchant et al., 2023); MatterGen generates materials with target properties; machine-learned interatomic potentials (MACE) speed up simulation |
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
- **Validation**: AI-generated hypotheses and claims need experimental confirmation before they are accepted
- **Understanding vs prediction**: accurate predictions without mechanistic insight
- **Monoculture**: over-reliance on the same tools and datasets narrows inquiry (Messeri & Crockett, 2024, *Nature*)

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Active learning](../../theory/paradigms/active/index.md): closed-loop discovery, in which a model chooses the next experiment, as in self-driving labs (Wang et al., 2023).
- [Symbolic AI](../../theory/paradigms/symbolic-ai/index.md): symbolic regression that recovers interpretable laws from data.
- [Agents](../../theory/models/agents/index.md): LLM agents that generate hypotheses and run experiments, as in AI scientists (Wang et al., 2023).

## References

### Seminal papers

- Lam et al. (2023). Learning skillful medium-range global weather forecasting. *Science*. https://doi.org/10.1126/science.adi2336 — GraphCast, a graph neural network that forecasts global weather.
- Merchant et al. (2023). Scaling deep learning for materials discovery. *Nature*. https://doi.org/10.1038/s41586-023-06735-9 — GNoME, which predicts large numbers of stable new crystals.
- Davies et al. (2021). Advancing mathematics by guiding human intuition with AI. *Nature*. https://doi.org/10.1038/s41586-021-04086-x — Uses machine learning to guide mathematicians toward conjectures in knot and representation theory.
- Kapoor & Narayanan (2023). Leakage and the reproducibility crisis in machine-learning-based science. *Patterns*. https://doi.org/10.1016/j.patter.2023.100804 — Documents data leakage in machine-learning-based science across fields.

### Surveys and textbooks

- Wang et al. (2023). Scientific discovery in the age of artificial intelligence. *Nature*. https://doi.org/10.1038/s41586-023-06221-2 — Review of AI across the stages of scientific discovery.
- Karniadakis et al. (2021). Physics-informed machine learning. *Nature Reviews Physics*. https://doi.org/10.1038/s42254-021-00314-5 — Review of embedding physical laws into machine learning models.
- Messeri & Crockett (2024). Artificial intelligence and illusions of understanding in scientific research. *Nature*. https://doi.org/10.1038/s41586-024-07146-0 — Argues that AI tools can create illusions of understanding in science.
