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

Patterson et al. (2021) analysed how the choice of model, datacentre and processor changes the carbon footprint of training large neural networks. Their main message is that these choices matter a great deal. Combined well, they can reduce the footprint by a large factor, and sparsely activated models are one of the strongest levers.

## Problem

Large models are often discussed as if their emissions were fixed by their size. If that were true, the only lever would be to train smaller models. The question is whether comparable work can be done with much lower emissions by choosing the architecture, the place and the hardware more carefully.

## Core idea

Split the footprint into factors that a practitioner controls, and measure how much each can change it. The paper groups them into the model architecture, the datacentre and its energy mix, and the processor, and then looks at how they combine.

## How the analysis works

1. **Model architecture.** Compare large dense models with large sparsely activated models that have as many or more parameters.
2. **Datacentre and location.** Compare the share of carbon-free energy across places, and compare cloud datacentres with typical ones.
3. **Processor.** Compare machine-learning accelerators with off-the-shelf systems.
4. **Estimate totals.** Estimate the energy and CO2e of recent large models, including T5, Meena, GShard, Switch Transformer and GPT-3, and refine an earlier estimate for the architecture search behind the Evolved Transformer.

## Results

The abstract reports the following ranges:

- Large sparsely activated models can use less than one-tenth of the energy of large dense models, without a loss of accuracy.
- The carbon-free share of energy, and so the CO2e, varies by roughly 5 to 10 times depending on location, even within one country and organisation.
- Cloud datacentres are roughly 1.4 to 2 times more energy-efficient than typical datacentres.
- ML-oriented accelerators are roughly 2 to 5 times more effective than off-the-shelf systems.
- The choice of model, datacentre and processor together can reduce the footprint by up to roughly 100 to 1000 times.

The paper also argues that energy use and CO2e should be reported in ML papers and treated as key evaluation metrics, a point that links to [Green AI](green-ai.md).

## Limitations

- **Relative to a baseline.** The reductions are measured against particular dense models and settings. Gains in one setting may be smaller in another.
- **Moving energy mix.** The effect of location depends on how carbon-free the local grid is at the time of training, and that changes.
- **Training only.** The analysis covers training. It does not show how much total emissions fall once a model is deployed at scale.
- **Estimated figures.** Totals for the recent models are estimates from public information, not measurements of each run.

## Connections

- The estimate method used for the cost of NLP training is discussed in [Training Energy Cost (Strubell et al., 2019)](training-energy-cost.md).
- A fuller life-cycle estimate for one large model, including embodied emissions, is on the [BLOOM life-cycle estimate](life-cycle-estimate.md) page.
- Sparse architectures are one kind of efficient design. The model families are surveyed in [Models](../../theory/models/index.md).
- The hardware side of the factors is covered in [AI Hardware](../../engineering/hardware/index.md).

## Open questions

- How much do efficiency gains in models translate into lower total emissions once usage grows?
- How should the location and time of training be reported so that the emissions can be compared?
- Can efficiency gains be kept without making models harder for groups with less compute to use?

## References

### Seminal papers

- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv preprint. https://arxiv.org/abs/2104.10350 — The analysis described on this page, of how model, datacentre and processor choices change the footprint. Its abstract gives the ranges quoted above.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — Earlier estimate of the cost of training NLP models, which motivated this line of work.
- Luccioni, A. S., Viguier, S. & Ligozat, A.-L. (2022). *Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model*. arXiv preprint. https://arxiv.org/abs/2211.02001 — A measured footprint for one large model, with the boundaries that a total depends on.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv preprint. https://arxiv.org/abs/1910.09700 — A calculator whose inputs are the server's location, the GPU and the training time.
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248). https://www.jmlr.org/papers/v21/20-312.html — Recommends reporting the factors on which the footprint depends.
