---
related:
  - engineering/evaluation
  - theory/models/llm
tags:
  - evaluation
  - benchmarks
  - language
  - scaling
last_reviewed: 2026-11-01
aliases:
  - BIG-bench
  - Beyond the Imitation Game
  - 超越模仿遊戲基準
  - 大型基準
---

# BIG-bench

BIG-bench (Beyond the Imitation Game benchmark) is a collection of 204 tasks written to measure what language models can do and how their performance changes with scale. The tasks were contributed by 450 authors from 132 institutions. The authors built it to probe abilities that they believed lay beyond the language models of the time (Srivastava et al., 2022).

## Task and data

Most language benchmarks come from one source, such as a set of exam questions or a set of sentence pairs. BIG-bench instead gathers many separate tasks into one suite, each written by a contributor who had a specific capability in mind. The tasks cover a wide range of topics, and the paper's abstract notes that they were chosen to target abilities thought to be out of reach for current models (Srivastava et al., 2022).

Because the tasks are heterogeneous, the suite is not summarised by a single score in the same way as GLUE or MMLU. Each task keeps its own metric, and results are reported task by task and in aggregate.

## Protocol and metric

The authors evaluated three families of models: the OpenAI GPT models, dense transformers built inside Google, and sparse Switch-style transformers. Their sizes ranged from millions to hundreds of billions of parameters. Expert human raters also performed all the tasks, which gave a human reference point for each one (Srivastava et al., 2022).

Each task keeps the metric its author chose, so a single headline number from the suite should be read with care. The per-task results carry most of the information.

## What it shows

The main finding is that performance and calibration improve with scale, but the absolute scores remain poor, and they stay well below the level of the expert raters. Performance is remarkably similar across the three model classes, with a small benefit from sparsity (Srivastava et al., 2022).

The paper separates two kinds of scaling behaviour:

- **Smooth and predictable tasks.** Scores rise gradually with model size. These tasks tend to involve a large knowledge or memorisation component.
- **Breakthrough tasks.** Scores stay near chance over a range of sizes and then rise sharply at a critical scale. These tasks often involve several steps or components, or metrics that are brittle.

The authors also report that bias typically increases with scale in ambiguous contexts, and that prompting can reduce it (Srivastava et al., 2022).

The breakthrough pattern was later studied as a general phenomenon. Wei et al. (2022) define an emergent ability as one that is absent in smaller models and present in larger ones, so that it cannot be predicted by extrapolating from small models.

## Limitations

- **Heterogeneous metrics.** Tasks do not share a scale, so averaging them hides large differences between tasks.
- **Brittle breakthroughs.** The paper notes that breakthrough behaviour often comes with brittle metrics. A sharp jump may therefore partly reflect how a task is scored rather than a change in the model.
- **Human baseline.** Expert raters are a strong reference, but the baseline reflects the skill of the particular raters who performed the tasks.
- **Protocol sensitivity.** As with other prompt-based benchmarks, the prompt format and answer extraction change the scores, so the protocol must be reported with each result.

## Connections

- [GPT-3](../../../models/llm/gpt-3-few-shot/index.md) is one of the model families evaluated on the suite, and its few-shot results motivated much of the later benchmarking.
- [Scaling laws](../../../models/llm/scaling-laws/index.md) describe how loss falls with compute, while BIG-bench asks how task scores change with scale. Loss and task scores are different quantities, so the two views answer different questions.
- [Compute-optimal training](../../../models/llm/compute-optimal-training/index.md) shows how the model size and data budget affect the same benchmark scores.
- [MMLU](mmlu.md) is a fixed multiple-choice benchmark, a contrast to the open collection of BIG-bench tasks.
- [HELM](../../../../engineering/evaluation/helm.md) evaluates language models across many scenarios and metrics at once, which addresses the heterogeneous-metric problem in a different way.

## Applications

BIG-bench is used as a broad test bed when a new model family is introduced. It shows where a model gains abilities as it grows and where it does not.

## Open questions

- Whether breakthrough behaviour reflects a real change in model capability or a change in the metric. The paper points to brittle metrics as one cause, but the question is not settled.
- How to aggregate heterogeneous tasks into one measure that does not hide important differences.
- How much of the benchmark's content has entered pre-training data, since a public suite can be memorised.

## References

### Seminal papers

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Introduces the 204-task suite, the expert human baseline and the scaling results summarised on this page.
- Wei, J. et al. (2022). *Emergent Abilities of Large Language Models*. arXiv. https://arxiv.org/abs/2206.07682 — Defines emergent abilities as those present in larger models but not in smaller ones, and argues that they cannot be predicted by extrapolation.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 model family, one of the three families evaluated on BIG-bench.

### Surveys and benchmarks

- Liang, P. et al. (2022). *Holistic Evaluation of Language Models*. arXiv. https://arxiv.org/abs/2211.09110 — Measures seven metrics across 16 core scenarios, a multi-metric design that contrasts with BIG-bench's per-task scoring.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — A fixed multiple-choice benchmark across 57 subjects, a contrast to an open task collection.
