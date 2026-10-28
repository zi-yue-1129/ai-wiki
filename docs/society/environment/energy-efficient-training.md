---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 節能訓練
  - Energy-efficient training
---

# Energy-Efficient Training (Patterson et al., 2021)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one analysis in detail; the parent page compares it with others.

Patterson et al. (2021) analysed how the choice of model, datacenter and processor changes the carbon footprint of training large neural networks. Their main message is that these choices matter a great deal: combining them well can reduce the footprint by a large factor, with sparse models as one of the most important levers.

## Problem

Large models are often discussed as if their emissions were fixed by their size. If that were true, the only lever would be to train smaller models. The question is whether the same work can be done with much lower emissions by choosing the architecture, the place and the hardware more carefully.

## Core idea

Break the footprint into factors that a practitioner controls, and measure how much each factor can change it. The paper groups them into the model architecture, the datacenter and its energy mix, and the processor. It then looks at how the factors combine.

## How the analysis works

1. **Model architecture.** Compare dense models with sparsely activated ones that have a similar or larger number of parameters.
2. **Datacenter and location.** Compare the carbon-free share of electricity across places and times, and compare cloud datacenters with typical ones.
3. **Processor.** Compare machine-learning accelerators with off-the-shelf systems.
4. **Combine.** Estimate the effect of choosing the architecture, datacenter and processor together.

The abstract gives the ranges for each factor. The paper's detailed accounting is needed for any specific case.

## Results

The abstract reports that large but sparsely activated models can use less than a tenth of the energy of large dense models without sacrificing accuracy. It reports that the carbon-free energy share and the resulting emissions vary by roughly five to ten times, even within one country and organisation. It gives roughly 1.4 to 2 times greater efficiency for cloud datacenters, and roughly 2 to 5 times for ML-oriented accelerators. Combining the choices of model, datacenter and processor can cut the footprint by up to roughly 100 to 1000 times.

## Limitations

- **Depends on the baseline.** The reductions are relative to particular dense baselines and particular settings. Gains in one setting may be smaller in another.
- **Estimates of energy mix.** The effect of location depends on how carbon-free the local grid is at the time of training, which changes.
- **Accuracy and access.** The claim of no loss in accuracy applies to the models studied. Sparse models are also harder to serve and to run on some hardware.
- **Scope.** The analysis covers training, and it does not settle how much the total footprint falls once models are deployed at scale.

## Connections

- The estimate method this analysis relies on is discussed in [Training Energy Cost (Strubell et al., 2019)](training-energy-cost.md).
- Sparse architectures are one kind of efficient design. The model families are surveyed in [Models](../../theory/models/index.md).
- The hardware side of the factors is covered in [AI Hardware](../../engineering/hardware/index.md).

## Open questions

- How much do efficiency gains in models translate into lower total emissions once usage grows?
- How should the location and time of training be reported so that the emissions can be compared?
- Can efficiency gains be kept without making models harder to use for people with less compute?

## References

### Seminal papers

- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — The analysis described on this page, of how model, datacenter and processor choices change the footprint.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — Earlier estimate of the cost of training NLP models, which motivated this line of work.
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). Estimating the carbon footprint of BLOOM, a 176B parameter language model. arXiv:2211.02001. https://arxiv.org/abs/2211.02001 — A measured footprint for one large model, which shows how the choices in this analysis apply in practice.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — The calculator that uses hardware, duration and location as inputs.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Recommends reporting the factors this analysis depends on.
