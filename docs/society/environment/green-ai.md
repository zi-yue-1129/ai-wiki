---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Green AI
  - 綠色 AI
  - Efficiency as an evaluation criterion
---

# Green AI (Schwartz et al., 2019)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one proposal in detail; the parent page compares it with others.

Schwartz, Dodge, Smith and Etzioni (2019) argue that efficiency should be treated as an evaluation criterion for AI research, alongside accuracy. They call this "Green AI", in contrast to research that pursues accuracy almost regardless of the computation it needs. Their argument is a position paper: it proposes a change in how research is reported and judged, rather than a new algorithm.

## Problem

The compute used in deep learning research has grown very quickly, and with it the carbon footprint and the financial cost of experiments. Most papers report accuracy but not the cost of producing it. A method that improves accuracy by spending far more computation looks like progress, and a cheaper method that matches it has no visible advantage. Researchers with limited budgets are also shut out of comparisons they cannot afford to run.

## Core idea

Make efficiency part of the evaluation, not a footnote. Report the price tag of developing, training and running a model, so that the cost of a result is visible next to its accuracy. Once cost is reported, efficient methods have baselines to be compared against, and they can be judged as improvements in their own right.

## How the proposal works

1. **Report the cost.** State the financial price tag of developing, training and running the model.
2. **Treat efficiency as a criterion.** Evaluate results on efficiency alongside accuracy and related measures.
3. **Set baselines by cost.** Compare methods at similar cost, so that a cheaper method can be shown to match an expensive one.
4. **Lower the barrier.** Make it possible for researchers with limited compute to take part in comparisons.

The abstract describes these elements. How a specific efficiency measure should be defined is left to the field.

## Results

As a position paper, Green AI has no experiment of its own. The abstract reports that compute used in deep learning research grew about 300,000 times between 2012 and 2018, and it cites that growth as the reason for the proposal. Its influence is best read through the reporting practices that followed, such as the estimates on the [Training Energy Cost](training-energy-cost.md) and [Emissions Calculator](emissions-calculator.md) pages.

## Limitations

- **No single measure.** Reporting cost is only useful if the measure is comparable across hardware, clouds and years. The paper does not settle which measure should be standard.
- **Reporting is not reduction.** Asking for efficiency to be reported does not, by itself, lower emissions. The effect depends on whether people use the numbers.
- **Incentives.** Evaluation criteria shape what researchers pursue, and a new criterion can be gamed or can crowd out other goals.

## Connections

- The estimates that make cost visible are on the [Training Energy Cost](training-energy-cost.md) page.
- A concrete way to report energy and carbon with each experiment is on the [Reporting Energy and Carbon](reporting-framework.md) page.
- Methods that reduce the cost of training are covered in [Energy-Efficient Training](energy-efficient-training.md).

## Open questions

- Which efficiency measure should a field adopt as a standard criterion?
- How should efficiency be compared between methods that run on different hardware?
- Will publication venues make efficiency a required part of evaluation?

## References

### Seminal papers

- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — The position paper described on this page, arguing for efficiency as an evaluation criterion alongside accuracy.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — Estimates the cost of training NLP models, which gives the argument concrete figures.
- Henderson, P. et al. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — Proposes a practical way to report energy and carbon with each experiment.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows how model, datacenter and processor choices change the footprint, which is the kind of comparison Green AI asks for.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — A calculator that makes emissions estimates available to any researcher.
