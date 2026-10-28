---
status: draft
last_reviewed: 2026-10-28
aliases:
  - 訓練能源成本
  - Training energy cost
---

# Training Energy Cost (Strubell et al., 2019)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one estimate in detail; the parent page compares it with others.

Strubell, Ganesh and McCallum (2019) estimated the approximate financial and environmental cost of training several recent NLP models, and used those estimates to argue that research should weigh energy use alongside accuracy. The paper is one of the first to put a cost estimate on the training of large language models, and it framed the problem for a field that had mostly reported accuracy.

## Problem

Accuracy gains in NLP had come with rapidly growing computation, but most papers did not report what that computation cost in energy, money or emissions. Without those figures, readers cannot compare the cost of one approach with another, and the carbon footprint of a model stays hidden.

## Core idea

Estimate the energy used to train each model from its hardware and training time, then convert that energy into a financial cost and an emissions figure. The result is a rough but comparable price tag for each model.

## How the estimate works

1. **Count the hardware and time.** Take the processors used and the training duration reported for each model.
2. **Estimate energy.** Convert hardware power and time into energy, using typical power draw for the processors.
3. **Convert to money and emissions.** Apply cloud prices to get a financial cost, and apply a grid carbon intensity to get emissions.
4. **Compare.** Set the costs of different models side by side.

The abstract describes the approach as an estimate of approximate costs, and the exact multipliers are in the paper.

## Results

The abstract says that large NLP models have produced notable accuracy gains that depend on "exceptionally large computational resources", and it cites "the carbon footprint required to fuel modern tensor processing hardware". It states that the paper estimates the financial and environmental costs of training several recent models, and proposes recommendations to reduce costs and improve equity. The abstract does not give the per-model figures, so they should be read from the paper's tables.

## Limitations

- **Rough estimate.** The figures depend on assumed power draw, prices and grid intensity. They are useful for comparison rather than as accounting figures.
- **Training only.** The estimate covers training, not the energy used by deployed models every day, which can be larger over a model's lifetime.
- **Older models.** The models and hardware of 2019 have since changed, so the numbers are a historical snapshot.

## Connections

- The estimate method was refined by later calculators and life-cycle estimates. See [Emissions Calculator (Lacoste et al., 2019)](emissions-calculator.md) and [BLOOM life-cycle estimate](life-cycle-estimate.md).
- Ways of reducing the cost are covered in [Energy-Efficient Training (Patterson et al., 2021)](energy-efficient-training.md).
- The wider climate context for energy use is covered in [Climate & Energy](../../applications/climate-energy/index.md).

## Open questions

- How should the cost of a model be shared between its training and the many uses that follow?
- Can a comparable cost estimate be made for models whose hardware and training time are not published?

## References

### Seminal papers

- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — The study described on this page, estimating the cost of training several NLP models.
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — Argues for reporting the price tag of training and for making efficiency an evaluation criterion.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — Introduces a calculator for the emissions of training, which refines the estimate on this page.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Recommends reporting energy and emissions for ML experiments, and proposes a tracking framework.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows that model, datacenter and processor choices change the footprint substantially.
