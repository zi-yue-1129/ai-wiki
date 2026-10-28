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

Luccioni, Viguier and Ligozat (2022) estimated the carbon footprint of training BLOOM, a 176-billion-parameter language model. They report two figures for the same training run, which differ by the boundary of what is counted. Their estimate shows that the choice of what to include can change the result by a large factor, and that precise carbon figures for ML models are hard to produce.

## Problem

A single number for a model's emissions hides the choices behind it. Counting only the electricity used during training gives a smaller figure than counting the manufacture of hardware and the rest of the system. The problem is to show how much the boundary matters and to give a transparent estimate for a real model.

## Core idea

Measure the energy the training actually drew, then extend the estimate outward in stages: from the power drawn by the processors, to the whole system, and finally to the emissions of making the equipment. Report the figures at each boundary so that readers can see what each one includes.

## How the estimate works

1. **Measure dynamic power.** Record the energy used by the processors during training.
2. **Add the system.** Include the wider system the processors ran in, such as cooling and other equipment.
3. **Add the life cycle.** Include the emissions from manufacturing the equipment and from the energy used outside training.
4. **Report each boundary.** Give the result for each boundary, so the reader can compare.

The abstract describes these boundaries and the two resulting figures. The factor-by-factor accounting is in the paper.

## Results

The abstract reports approximately 24.7 tonnes of CO2eq when only dynamic power consumption is counted, and 50.5 tonnes when all processes are included, from equipment manufacturing to operational energy. The gap is the boundary, and the authors stress that precise carbon estimates for ML models are difficult to produce.

## Limitations

- **One model.** The estimate describes one training run of one model, on one hardware setup. It does not give a general rate.
- **Assumed inputs.** Parts of the system boundary rely on assumptions about equipment and energy that cannot be fully measured from outside.
- **Training only.** The figures cover training, not the emissions of serving the model afterwards.

## Connections

- The simpler calculator that leaves out the wider boundary is on the [Emissions Calculator](emissions-calculator.md) page.
- Ways to lower the footprint of training are on the [Energy-Efficient Training](energy-efficient-training.md) page.
- The hardware whose manufacture is counted in the life-cycle figure is covered in [AI Hardware](../../engineering/hardware/index.md).

## Open questions

- How should the life-cycle boundary be standardised so that different models can be compared?
- How should the emissions of serving a model be counted against its training emissions?

## References

### Seminal papers

- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — The study described on this page, with two footprints for one training run that differ by boundary.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — The simpler calculator that counts only three inputs.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows how model, datacenter and processor choices change the footprint.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — Earlier estimate of training costs, which this kind of estimate extends.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Recommends reporting energy and emissions with the boundary stated.
