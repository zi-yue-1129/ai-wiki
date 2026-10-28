---
status: complete
last_reviewed: 2026-10-28
aliases:
  - 訓練能源成本
  - Training energy cost
---

# Training Energy Cost (Strubell et al., 2019)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one estimate in detail; the parent page compares it with others.

Strubell, Ganesh and McCallum (2019) estimated the approximate financial and environmental cost of training several NLP models. They used the estimates to argue that research should weigh energy use alongside accuracy. Their table is the reason the paper is cited: it puts figures in pounds of CO2 equivalent and in US dollars next to named models.

## Problem

Accuracy gains in NLP had come with rapidly growing computation, but most papers did not report what that computation cost in energy, money or emissions. Without those figures, readers cannot compare the cost of one approach with another, and the footprint of a model stays hidden.

## Core idea

Estimate the energy each model used from its hardware and training time, then convert that energy into an emissions figure and a cloud-compute price. The result is a rough, comparable price tag for each model.

## How the estimate works

1. **Count the hardware and time.** Take the processors used and the training time reported for each model.
2. **Estimate energy.** Convert hardware power and time into kilowatt-hours. The table's column is labelled kWh·PUE, so the energy is multiplied by a datacentre overhead factor.
3. **Convert to emissions.** Turn the energy into CO2 equivalent, in pounds, using an assumed grid intensity.
4. **Convert to money.** Price the same hours at cloud rates, given as a range in US dollars.

The table gives the inputs for each row, and the exact multipliers are in the paper.

## Results

The table in the paper reports estimated figures for several models. Some examples:

| Model | Hardware | Hours | CO2e (lbs) | Cloud cost (USD) |
|---|---|---|---|---|
| Transformer (base) | 8 × P100 | 12 | 26 | $41–$140 |
| Transformer (big) | 8 × P100 | 84 | 192 | $289–$981 |
| ELMo | 3 × P100 | 336 | 262 | $433–$1,472 |
| BERT (base) | 64 × V100 | 79 | 1,438 | $3,751–$12,571 |
| Neural architecture search (NAS) | 8 × P100 | 274,120 | 626,155 | $942,973–$3,201,722 |

The NAS row is the outlier. It is a search over architectures rather than a single training run, and the paper's point is that the cost of such searches can be very large. The table has no BERT (large) row, and it lists BERT (base) on two hardware setups. Power and emissions are blank for TPU runs because the authors had no public power data for TPUs.

## Limitations

- **Rough estimate.** The figures depend on assumed power draw, prices and grid intensity. They are useful for comparison, not as accounting figures.
- **Training only.** The estimate covers training, not the energy used by deployed models, which can be larger over a model's life.
- **Dated models.** The models and hardware of 2019 have since changed, so the numbers are a historical snapshot.
- **Hardware availability.** Several rows depend on cloud prices and hardware that most researchers cannot choose freely.

## Connections

- Later calculators refined the method. See the [Emissions Calculator](emissions-calculator.md) and the [BLOOM life-cycle estimate](life-cycle-estimate.md).
- Ways of reducing the cost are covered in [Energy-Efficient Training](energy-efficient-training.md).
- The argument for treating cost as a criterion is on the [Green AI](green-ai.md) page.

## Open questions

- How should the cost of a model be shared between its training and the many uses that follow?
- Can a comparable cost estimate be made for models whose hardware and training time are not published?

## References

### Seminal papers

- Strubell, E., Ganesh, A. & McCallum, A. (2019). *Energy and Policy Considerations for Deep Learning in NLP*. ACL 2019, pp. 3645–3650. doi:[10.18653/v1/P19-1355](https://doi.org/10.18653/v1/P19-1355) — The study described on this page. Preprint: https://arxiv.org/abs/1906.02243
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2020). Green AI. *Communications of the ACM*, 63(12), 54–63. doi:[10.1145/3381831](https://doi.org/10.1145/3381831) — Argues for reporting the price tag of training and for making efficiency an evaluation criterion. Preprint: https://arxiv.org/abs/1907.10597
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). *Quantifying the Carbon Emissions of Machine Learning*. arXiv preprint. https://arxiv.org/abs/1910.09700 — A calculator that refines the estimate with location and GPU type.
- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). *Towards the Systematic Reporting of the Energy and Carbon Footprints of Machine Learning*. JMLR 21(248). https://www.jmlr.org/papers/v21/20-312.html — Recommends reporting energy and carbon for ML experiments.
- Patterson, D., et al. (2021). *Carbon Emissions and Large Neural Network Training*. arXiv preprint. https://arxiv.org/abs/2104.10350 — Estimates the energy and emissions of several large models, and shows that model, datacentre and processor choices change the footprint.
