---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 全生命週期估算
  - BLOOM carbon footprint
  - Life-cycle estimate
---

# Life-Cycle Carbon Estimate (BLOOM, 2022)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one estimate in detail; the parent page compares it with others.

Luccioni, Viguier and Ligozat (2022) estimated the carbon footprint of training BLOOM, a 176-billion-parameter language model. They report two figures for the same training run, which differ in what is counted. The gap shows that the choice of boundary can change the result by a large factor, and that precise carbon figures for ML models are hard to produce.

## Problem

A single number for a model's emissions hides the choices behind it. Counting only the electricity used by the processors during training gives a smaller figure than counting the manufacture of the hardware and the power that idle machines draw. The problem is to show how much the boundary matters and to give a transparent estimate for a real model.

## Core idea

Measure the energy that the processors drew during training, convert it with the grid's carbon intensity, and then extend the estimate outward in stages. Report the figure at each boundary so that readers can see what each one includes.

## How the estimate works

1. **Dynamic power.** Multiply the GPU power drawn during training by the carbon intensity of the grid. The authors exclude CPU power, and they do not count offsets or heat recycling.
2. **Idle power.** Add the power drawn by the cluster while it is idle, which is the cost of keeping the hardware available.
3. **Embodied emissions.** Add the emissions from manufacturing the servers and GPUs, which the authors estimate from proxies rather than exact hardware data.
4. **Report each boundary.** Give the total for each stage, so that the reader can compare the dynamic-only figure with the full life-cycle figure.

The paper does not attempt a cradle-to-grave assessment. Network switches and cooling equipment are left out of the embodied figure.

## Results

The training run used about 433 MWh of dynamic energy on about 1.08 million GPU hours, over 118 days. The hardware was Nvidia A100 GPUs in a French national cluster, where the grid's carbon intensity was about 57 gCO2eq/kWh. The two headline figures are:

- **Dynamic power only:** about 24.7 tonnes CO2eq.
- **Full life cycle:** about 50.5 tonnes CO2eq. This adds about 11.2 tonnes of embodied emissions for servers and GPUs, and about 14.6 tonnes from idle cluster power.

The authors also measure a serving deployment: 16 A100 GPUs on a cloud instance that handled about 230,000 requests over about 18 days, using 914 kWh, with a grid intensity of 394 gCO2eq/kWh. This gives roughly 340 kg CO2eq over the tracking period. The authors describe all of these as estimates.

## Limitations

- **One model and one cluster.** The estimate describes one training run on one hardware setup. It does not give a general rate for ML.
- **Proxy inputs.** Training power was not tracked in real time, so the rated power of the GPUs is used as a proxy, and the embodied figures rely on proxies.
- **Excluded parts.** CPU power, network switches and cooling equipment are not in the figures, so the totals are not complete.
- **Serving is a separate case.** The inference figures come from a single deployment and may not represent other setups.

## Connections

- The simpler calculator that counts only three inputs is on the [Emissions Calculator](emissions-calculator.md) page.
- Ways to lower the footprint of training are on the [Energy-Efficient Training](energy-efficient-training.md) page.
- The hardware whose manufacture is counted in the life-cycle figure is covered in [AI Hardware](../../engineering/hardware/index.md).
- The argument for reporting figures such as these with each paper is on the [Reporting Energy and Carbon](reporting-framework.md) page.

## Open questions

- How should the life-cycle boundary be standardised so that different models can be compared?
- How should the emissions of serving a model be counted against its training emissions?

## References

### Seminal papers

- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv preprint. https://arxiv.org/abs/2211.02001 — The study described on this page, with two footprints for one training run and the boundary between them.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv preprint. https://arxiv.org/abs/1910.09700 — The simpler calculator that counts only three inputs.
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv preprint. https://arxiv.org/abs/2104.10350 — Shows how model, datacentre and processor choices change the footprint.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — Earlier estimate of training costs, which this kind of estimate extends.
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248). https://www.jmlr.org/papers/v21/20-312.html — Recommends reporting energy and emissions with the boundary stated.
