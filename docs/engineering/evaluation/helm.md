---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/evaluation/benchmarks/language
tags:
  - evaluation
  - benchmarks
  - transparency
aliases:
  - HELM
  - Holistic Evaluation of Language Models
  - 語言模型整體評估
---

# HELM (Liang et al., 2022)

HELM, the Holistic Evaluation of Language Models, is a framework for evaluating language models across many scenarios and many metrics at once. It was introduced to make the capabilities, limitations and risks of models more transparent, and to show the trade-offs between metrics that a single accuracy number hides. Liang et al. (2022) describe the framework and its first large evaluation.

This page is part of [Benchmark suites](benchmark-suites.md), which also covers MMLU and its successors.

## Overview

Most leaderboards report one number per model. A model can score well on accuracy and still be poorly calibrated, unfair to some groups, or expensive to run. HELM addresses this by taxonomising the scenarios and metrics of interest, selecting a broad set of them, and reporting every metric for every scenario where possible. Its authors also record what is missing, such as question answering in neglected English dialects and metrics for trustworthiness.

## Key concepts

- **Scenario:** a use case, defined by a task, a dataset and a setting. HELM organises scenarios into a taxonomy of what models are used for.
- **Metric:** a measure of a desirable property. The framework uses seven: accuracy, calibration, robustness, fairness, bias, toxicity and efficiency.
- **Core scenario:** one of the 16 scenarios on which all metrics are reported when possible.
- **Trade-off view:** a presentation that lets readers see one metric against another for the same model.

## How it works

HELM proceeds in three steps. The authors first taxonomise scenarios and metrics. They then choose a subset based on coverage and feasibility, which means some gaps remain and are reported. Finally, they run each model on each core scenario and measure all seven metrics. The paper reports that the metrics were measured for most of the scenario-model pairs, about 87.5% of the time, so the results are a grid rather than a single ranking.

## Results

The abstract states that the framework measures seven metrics for each of 16 core scenarios when possible, which is about 87.5% of the time, and that this keeps metrics beyond accuracy from being neglected. The framework is designed to make trade-offs clear, so the main result is the comparison itself rather than a single winner.

## Limitations

- **Selection choices.** The scenario taxonomy and the selected subset reflect the authors' judgement, and other choices would give different grids.
- **Cost.** Running every model on every scenario and metric is expensive, which limits how often the suite can be refreshed.
- **Metrics are proxies.** Fairness, toxicity and robustness are measured by specific tests, which capture part of each property.
- **Versioning.** Results depend on the prompts, the models and the date of the run, so they age quickly.

## Connections

- The general suite landscape, including MMLU, is on [Benchmark suites](benchmark-suites.md).
- Evaluation practice for models and applications is on [Evaluation & Benchmarks](index.md).
- Metric definitions and statistical treatment are in the Theory section, on [Evaluation](../../theory/evaluation/index.md).
- Fairness and bias, which HELM measures, are discussed in [Society](../../society/index.md).

## Applications

- Comparing models on the trade-off between accuracy and calibration or fairness.
- Documenting a model's behaviour for a transparency report.

## Open questions

- Which scenarios should a holistic suite include as use cases change?
- How should metrics be weighted when a deployment needs one of them above the others?

## References

### Seminal papers

- Liang, P. et al. (2022). Holistic Evaluation of Language Models. arXiv. https://arxiv.org/abs/2211.09110 — Introduces HELM, the taxonomy of scenarios and metrics, and a grid of seven metrics across 16 core scenarios.
- Hendrycks, D. et al. (2021). Measuring Massive Multitask Language Understanding. ICLR. https://arxiv.org/abs/2009.03300 — The accuracy-based suite that HELM's accuracy metric is compared with.
- Srivastava, A. et al. (2022). Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models. arXiv. https://arxiv.org/abs/2206.04615 — A broad, collaboratively built task suite for measuring capabilities as models scale.
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. Proceedings of FAT* 2019. https://doi.org/10.1145/3287560.3287596 — Proposes model cards, short documents that report a model's intended use, evaluation conditions and performance across groups, a form of the transparency that HELM also aims at.

### Surveys and textbooks

- Wang, Y. et al. (2024). MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark. arXiv. https://arxiv.org/abs/2406.01574 — A harder successor to MMLU, for comparison with HELM's approach to measurement.
