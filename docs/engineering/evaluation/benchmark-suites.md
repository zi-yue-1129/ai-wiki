---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/evaluation/benchmarks
tags:
  - evaluation
  - benchmarks
  - language models
aliases:
  - Benchmark Suites
  - MMLU
  - HELM
  - 基準套件
  - 基準測試套件
---

# Benchmark suites: MMLU, HELM and successors

A benchmark suite bundles many tasks, often across subjects or scenarios, into one evaluation. Suites let a model be compared across a wide range of abilities rather than one, and they have become the common reference points for language models. Their results are only as informative as their coverage, their metrics and the care with which they are reported.

This page is part of [Evaluation & Benchmarks](index.md). The general definition of each benchmark is on [Language benchmarks](../../theory/evaluation/benchmarks/language/index.md).

## Overview

Early language benchmarks measured one task each, such as sentiment or entailment. Large models made single tasks easy, so attention moved to suites that test knowledge and reasoning across many subjects. Two suites show the range. MMLU (Hendrycks et al., 2021) tests multitask accuracy over 57 subjects, including mathematics, history, computer science and law. HELM (Liang et al., 2022) evaluates models across scenarios and several metrics at once, so that accuracy is not reported alone.

## Key concepts

- **Scenario:** a use case, such as question answering or summarisation, defined by its data and task.
- **Metric:** a measure of quality, such as accuracy, calibration, robustness, fairness, bias, toxicity or efficiency.
- **Coverage:** how many subjects, languages or scenarios the suite includes, and what it leaves out.
- **Successor suite:** a later benchmark built because an earlier one is saturated or contaminated.

## Key methods

- [MMLU](../../theory/evaluation/benchmarks/language/mmlu.md): a multiple-choice suite across 57 subjects. It is the most common single number in model comparisons, and its limits are the same as any single-format test.
- [HELM](helm.md): a holistic framework that reports seven metrics for each of 16 core scenarios, so that trade-offs between metrics are visible.
- Successors: later suites raise difficulty or remove weak questions. MMLU-Pro (Wang et al., 2024) is a more robust and challenging version of MMLU. BIG-bench (Srivastava et al., 2022) collects a broad set of tasks contributed by many researchers, to measure capabilities as models scale.

## How to read a suite score

- **Check the version and protocol.** Few-shot prompting, answer parsing and the choice of subset all change a score.
- **Check for contamination.** A suite that is public may appear in training data. See [Benchmark contamination](../evaluation/index.md) for the general treatment.
- **Read metrics beyond the headline.** A model that is accurate but poorly calibrated or unfair in some scenario is a different system from one that is only accurate.
- **Compare like with like.** Scores from different protocols are not comparable.

## Connections

- The general practice of evaluation, including LLM-as-judge and human review, is on [Evaluation & Benchmarks](index.md).
- Benchmarks for reasoning and agents are on [Reasoning and Agent Benchmarks](../../theory/evaluation/benchmarks/reasoning-agents/index.md).
- Evaluation design and metric definitions are in the Theory section, on [Evaluation](../../theory/evaluation/index.md).

## Applications

- Choosing a model for a general-purpose assistant by comparing multiple suites.
- Tracking a model across versions with a fixed suite and protocol.

## Open questions

- Which mix of scenarios and metrics best reflects use in practice?
- How long can a public suite remain useful before contamination makes it unreliable?

## References

### Seminal papers

- Hendrycks, D. et al. (2021). Measuring Massive Multitask Language Understanding. ICLR. https://arxiv.org/abs/2009.03300 — Introduces MMLU, a test of multitask accuracy across 57 subjects.
- Liang, P. et al. (2022). Holistic Evaluation of Language Models. arXiv. https://arxiv.org/abs/2211.09110 — Introduces HELM, which measures seven metrics across 16 core scenarios.
- Srivastava, A. et al. (2022). Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models. arXiv. https://arxiv.org/abs/2206.04615 — Introduces BIG-bench, a broad, collaboratively built set of tasks for measuring capabilities as models scale.
- Wang, Y. et al. (2024). MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark. arXiv. https://arxiv.org/abs/2406.01574 — A more robust and challenging successor to MMLU.

### Surveys and textbooks

- Liang, P. et al. (2022). Holistic Evaluation of Language Models. arXiv. https://arxiv.org/abs/2211.09110 — Cited above for the metric framework and its scope of scenarios.
