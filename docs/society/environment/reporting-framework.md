---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Reporting energy and carbon
  - Experiment Impact Tracker
  - Systematic reporting of ML footprints
---

# Reporting Energy and Carbon (Henderson et al., 2020)

!!! info "Part of Environmental Impact of AI"
    This method page belongs to [Environmental Impact of AI](index.md). It explains one framework in detail; the parent page compares it with others.

Henderson, Hu, Romoff, Brunskill, Jurafsky and Pineau (2020) present a framework for tracking the energy use and carbon emissions of machine-learning experiments while they run, and for publishing the results in a standard form. They use it to build a leaderboard for energy-efficient reinforcement learning, and they offer it as a model for other fields.

## Problem

Accurate reporting of energy and carbon use is needed to understand the climate impact of machine learning, but it is rarely done. Estimates made after the fact depend on details that are easy to lose, and figures reported in different ways cannot be compared. Without a common format, a researcher who wants to report energy use has to build the measurement from scratch.

## Core idea

Measure energy and estimate emissions during the experiment, not afterwards, and publish the figures in a standardised online appendix. The same format for every experiment makes results comparable, and collecting them in one place makes it possible to build a leaderboard.

## How the framework works

1. **Track while running.** Record the energy used and estimate the carbon emitted as the experiment executes.
2. **Standardise the output.** Publish the figures in a standard online appendix, so that the reporting format is the same across papers.
3. **Collect the results.** Gather the reports into a leaderboard, which lets readers compare methods on energy as well as performance.
4. **Learn from case studies.** Use case studies to suggest ways of reducing energy use and emissions.

The abstract describes the tracking, the standardised appendices and the leaderboard. The details of how energy is measured and converted to emissions are in the paper.

## Results

The abstract reports the framework, the leaderboard for energy-efficient reinforcement learning, and case studies that suggest reductions. It is a reporting framework, so its results are the practice it sets up rather than a single number that can be compared with the estimates on other pages.

## Limitations

- **Depends on measurement.** Energy readings depend on the hardware and tools available, and carbon figures depend on estimates of local grid intensity.
- **Narrow first case.** The leaderboard was built for reinforcement learning. Other fields may need different measures and different formats.
- **Adoption.** A standard appendix is only useful if researchers fill it in, and the figures can only be checked as far as the reporting allows.

## Connections

- The earlier calculator that estimates from three inputs, without tracking the run, is on the [Emissions Calculator](emissions-calculator.md) page.
- The argument for reporting cost alongside accuracy is on the [Green AI](green-ai.md) page.
- Ways of reducing the energy use that such reports reveal are covered in [Energy-Efficient Training](energy-efficient-training.md).

## Open questions

- How should energy and carbon be measured consistently across different hardware and cloud providers?
- Who should check the figures that researchers report?
- How can a reporting format be extended to fields beyond reinforcement learning?

## References

### Seminal papers

- Henderson, P., Hu, J., Romoff, J., Brunskill, E., Jurafsky, D. & Pineau, J. (2020). Towards the systematic reporting of the energy and carbon footprints of machine learning. *Journal of Machine Learning Research*. https://arxiv.org/abs/2002.05651 — The framework described on this page, for tracking and standardised reporting of energy and carbon.
- Schwartz, R., Dodge, J., Smith, N. A. & Etzioni, O. (2019). Green AI. arXiv:1907.10597. https://arxiv.org/abs/1907.10597 — Argues that the cost of research should be reported and treated as a criterion, which this framework makes practical.
- Lacoste, A., Luccioni, A., Schmidt, V. & Dandres, T. (2019). Quantifying the carbon emissions of machine learning. arXiv:1910.09700. https://arxiv.org/abs/1910.09700 — Estimates emissions from three inputs, without tracking the run during training.
- Strubell, E., Ganesh, A. & McCallum, A. (2019). Energy and policy considerations for deep learning in NLP. arXiv:1906.02243. https://arxiv.org/abs/1906.02243 — An earlier cost estimate made after the fact, which shows why in-run measurement matters.
- Patterson, D. et al. (2021). Carbon emissions and large neural network training. arXiv:2104.10350. https://arxiv.org/abs/2104.10350 — Shows how much the factors that such reports record can change the footprint.
