---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 機器學習排放計算器
  - Machine Learning Emissions Calculator
---

# Machine Learning Emissions Calculator (Lacoste et al., 2019)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one calculator in detail; the parent page compares it with others.

Lacoste et al. (2019) introduced the Machine Learning Emissions Calculator, a tool that estimates the carbon emissions of training a machine-learning model. It turns a small number of inputs that a researcher can easily record into an emissions estimate, so that the figure can be reported with an experiment.

## Problem

Researchers rarely report how much carbon their experiments produced, partly because the number is hard to estimate without specialist data. A simple, transparent calculator would make the figure available to anyone who trains a model, and make it possible to compare experiments.

## Core idea

Estimate emissions from three inputs that are known or easy to record: the hardware used, how long it ran, and where the servers were located. The location sets the carbon intensity of the electricity, so the same training run has different emissions in different places.

## How the calculator works

1. **Hardware.** Record the make and model of the processors used.
2. **Duration.** Record how long the training ran.
3. **Location.** Record where the servers were, which sets the grid's carbon intensity.
4. **Estimate.** Combine these to give an emissions figure for the run.

The abstract names these factors as the inputs the calculator uses. The exact power assumptions and the emissions factors are documented with the tool.

## Results

The abstract introduces the calculator and describes it as estimating the carbon emissions of training ML models. It does not report a benchmark result, because the paper is about the tool. Its value is that the same run can be estimated consistently, and that location is a visible factor.

## Limitations

- **Three inputs only.** The estimate leaves out embodied emissions from making the hardware, cooling, and the energy used before and after training, so it understates the full footprint.
- **Assumed factors.** The result depends on power and grid assumptions that may not match the actual run.
- **Training only.** It estimates training, not the emissions of serving the model to users.

## Connections

- A fuller life-cycle estimate for a single large model is on the [BLOOM life-cycle estimate](life-cycle-estimate.md) page.
- Earlier cost estimates that the calculator refines are on the [Training Energy Cost](training-energy-cost.md) page.
- Location and energy mix are central to the analysis in [Energy-Efficient Training](energy-efficient-training.md).

## Open questions

- Should calculators include embodied emissions from hardware manufacture by default?
- How should a calculator handle grid intensity that changes during a training run?

## References

### Seminal papers

- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — The study described on this page, introducing the emissions calculator.
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — A fuller estimate for one model, which shows what the calculator leaves out.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — Earlier cost estimate that motivated transparent calculators.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Recommends that such figures be reported with experiments.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows that location and hardware choices change the figure a calculator reports.
