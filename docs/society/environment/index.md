---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/climate-energy
  - engineering/hardware
  - society/governance
tags:
  - environment
  - energy
  - carbon emissions
aliases:
  - 環境影響
  - 碳足跡
  - Carbon footprint
  - Green AI
---

# Environmental Impact of AI

Training and running large models uses a great deal of electricity, and the hardware that does the work is manufactured with energy and materials. This page covers how the environmental cost of AI is estimated, why different estimates disagree, and what can reduce it.

## Overview

The environmental cost of a model is hard to pin down because it depends on what is counted. An estimate might include only the electricity used by the processors during training, or it might also include cooling, the wider datacenter, the manufacture of the hardware, and the energy used to serve the model afterwards. Each choice gives a different number, and the same training run can produce figures that differ by a large factor.

Early work in the field made the cost visible. Strubell et al. (2019) estimated the price tag of training several NLP models, and argued that energy should be reported alongside accuracy. Later work refined the estimates and made the boundaries explicit.

## Key concepts

- **Energy use**: the electricity drawn by processors and the datacenter that houses them.
- **Carbon intensity**: emissions per unit of electricity, which depends on the local energy mix and therefore on where a model is trained.
- **Embodied emissions**: the emissions from manufacturing hardware, which a life-cycle estimate adds to the operational figure.
- **System boundary**: what an estimate includes. Two estimates that differ only in their boundary can give very different results.

## How it works

Three steps produce most estimates.

1. **Measure or estimate the energy.** Use the hardware, the training time and the power drawn by the processors to estimate the energy used.
2. **Convert to emissions.** Multiply the energy by the carbon intensity of the electricity where the run took place.
3. **Extend the boundary.** Add cooling, the wider system, and the manufacture of hardware, if the estimate is meant to be a full footprint.

Serving a model to many users adds a recurring cost that a training estimate does not cover. The methods below focus mainly on training, and they make clear which part of the cost they include.

## Key methods

Each method has its own page with the problem, method, results and limitations. The table compares them briefly.

| Method | Question | Main result (per abstract) | Read more |
|---|---|---|---|
| Training energy cost (Strubell et al., 2019) | What does training several NLP models cost in money and emissions? | Approximate cost estimates for several recent NLP models; the per-model figures are in the paper's tables | [Training Energy Cost](training-energy-cost.md) |
| Machine learning emissions calculator (Lacoste et al., 2019) | Can training emissions be estimated from a few easily recorded inputs? | A calculator that uses hardware, duration and location; the abstract reports no benchmark result | [Emissions Calculator](emissions-calculator.md) |
| Energy-efficient training (Patterson et al., 2021) | How much can choices of model, datacenter and processor change the footprint? | Sparse models can use under a tenth of the energy of dense models; combined choices can cut the footprint by roughly 100 to 1000 times | [Energy-Efficient Training](energy-efficient-training.md) |
| Life-cycle estimate for BLOOM (Luccioni et al., 2022) | How much does the system boundary change one model's footprint? | About 24.7 tonnes CO2eq counting dynamic power only, and 50.5 tonnes counting the full life cycle | [BLOOM Life-Cycle Estimate](life-cycle-estimate.md) |
| Green AI (Schwartz et al., 2019) | Should efficiency be judged alongside accuracy? | A position paper proposing that cost be reported and treated as an evaluation criterion; no experiment of its own | [Green AI](green-ai.md) |
| Reporting energy and carbon (Henderson et al., 2020) | How can energy and emissions be tracked and reported consistently for each experiment? | A framework for tracking during a run, standardised online appendices, and a leaderboard for energy-efficient reinforcement learning | [Reporting Energy and Carbon](reporting-framework.md) |

## Responses

| Approach | What it does | Limits |
|---|---|---|
| Report energy and emissions with each experiment | Makes figures comparable across papers, as proposed in [Reporting Energy and Carbon](reporting-framework.md) | Needs tracking tools and an agreed boundary |
| Treat efficiency as an evaluation criterion | Makes cost a factor alongside accuracy, as argued in [Green AI](green-ai.md) | Depends on how the research community judges work |
| Prefer efficient architectures and hardware | Lowers energy per unit of work, as shown by Patterson et al. (2021) | Gains depend on the baseline and may complicate serving |
| Train on low-carbon electricity | Lowers emissions for the same energy use | Depends on local grid data and on where compute is available |

## Connections

- The energy use of AI sits within the wider energy and climate picture (see [Climate & Energy](../../applications/climate-energy/index.md)).
- The hardware whose energy use and manufacture are counted here is covered in [AI Hardware](../../engineering/hardware/index.md).
- The model families whose architecture affects efficiency are surveyed in [Models](../../theory/models/index.md).
- Reporting requirements for energy and emissions in other fields are a governance question (see [Law, Policy & Governance](../governance/index.md)).

## Applications

- **Reporting in research papers**: recording energy and emissions for each experiment, so readers can compare cost with accuracy.
- **Choice of hardware and location** when planning training runs, with emissions as one input.
- **Efficiency work in practice**, such as sparse models and efficient accelerators, where the energy saving is the goal.

## Open questions

- How should the life-cycle boundary be standardised so that different models can be compared?
- Do efficiency gains lower total emissions once usage grows, or do they make AI cheaper to use more?
- How should the emissions of serving a model be counted against the emissions of training it?
- Can comparable estimates be made for models whose hardware and training time are not published?

## References

### Seminal papers

- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — Estimates the financial and environmental cost of training several NLP models, and started the discussion of energy in ML research.
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — Argues for reporting the cost of training and for treating efficiency as an evaluation criterion.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — Introduces a calculator that estimates emissions from hardware, duration and location.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Recommends systematic reporting of energy and emissions, and proposes a tracking framework.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows how model, datacenter and processor choices change the footprint, and how much they can reduce it.
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — Gives two footprints for one training run, differing by system boundary.
