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

Lacoste et al. (2019) introduced the Machine Learning Emissions Calculator, a tool that estimates the carbon emissions of a training run from three inputs: the zone where the server is, the type of GPU, and the training time. The aim is a figure simple enough that any researcher can record it and report it with an experiment.

## Problem

Researchers rarely report how much carbon their experiments produce. The figure is hard to estimate without specialist data about hardware, power and electricity supply, so it is usually left out. A transparent calculator that needs only a few facts would make the figure available to anyone who trains a model, and make experiments comparable.

## Core idea

Estimate the energy a run uses from the GPU type and the training time, then convert that energy into emissions with the carbon intensity of the electricity where the server runs. The location matters because the same run drawn from a clean grid emits far less than one drawn from a coal-heavy grid.

## How the calculator works

1. **Location.** Record the geographic zone of the server. The authors assume each cloud region draws from its local grid, and they match public grid data to the regions of major cloud providers.
2. **Hardware.** Record the GPU type. The energy estimate uses the GPU's rated power and its performance figures.
3. **Duration.** Record the training time.
4. **Estimate.** Combine these into an approximate energy figure and multiply by the grid's carbon intensity to give CO2 equivalent.

The paper lists provider offsets among the variables but does not explain how they enter the calculation, so the tool's main output depends on the three inputs above.

## Results

The paper is about the tool, and it reports no benchmark. Its illustrative figures show how much location matters. Carbon intensity ranges from about 20 gCO2eq/kWh for Quebec to about 737 gCO2eq/kWh for Iowa, a spread of roughly 40 times across the regions it considers. For models such as VGG or BERT trained on several GPUs for weeks, the authors say that choosing a low-carbon location could avoid several hundred kilograms of CO2 equivalent.

## Limitations

- **Approximation.** The authors call the calculator an approximation, with a large margin of error in both energy and carbon figures, partly because organisations share little data.
- **Theoretical power.** The energy estimate relies on rated power and theoretical peak performance rather than measured draw, which the authors say would be more accurate.
- **Training only.** Inference is excluded, so the figure does not cover serving a model.
- **Missing factors.** Power usage effectiveness (PUE) is discussed but is not an input, and embodied carbon from manufacturing is not included.
- **Global load balancing.** If cloud jobs are moved between regions, the benefit of choosing a low-carbon zone can shrink.

## Connections

- The fuller estimate for one large model, which adds embodied emissions and idle power, is on the [BLOOM life-cycle estimate](life-cycle-estimate.md) page.
- Earlier cost estimates for NLP training are on the [Training Energy Cost](training-energy-cost.md) page.
- A tool that measures energy during the run, rather than estimating it beforehand, is described in [Reporting Energy and Carbon](reporting-framework.md).
- Location and energy mix are central to [Energy-Efficient Training](energy-efficient-training.md).

## Open questions

- Should calculators include embodied emissions from hardware manufacture by default?
- How should a calculator handle grid intensity that changes during a training run?
- How accurate must a calculator be before its figures are used for decisions about where to train?

## References

### Seminal papers

- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv preprint. https://arxiv.org/abs/1910.09700 — The paper described on this page, introducing the calculator and its three inputs.
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv preprint. https://arxiv.org/abs/2211.02001 — A measured footprint for one model, which shows what a simple calculator leaves out.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — Earlier estimate of the cost of training NLP models, which motivated transparent calculators.
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248). https://www.jmlr.org/papers/v21/20-312.html — Recommends that energy and carbon be reported with experiments, using measured rather than estimated figures.
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv preprint. https://arxiv.org/abs/2104.10350 — Shows that location and hardware choices change the figure a calculator reports.
