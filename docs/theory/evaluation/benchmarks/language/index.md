---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
aliases:
  - Language benchmarks
  - 語言基準
---

# Language Benchmarks

Language benchmarks cover three different things: sentence-level understanding (GLUE and SuperGLUE), broad knowledge in multiple-choice form (MMLU), and expert-level questions that resist search (GPQA and Humanity's Last Exam). Scores from different groups are not interchangeable, because they test different skills and use different answer formats.

## Overview

The first generation of language benchmarks asked whether a model understands sentences: whether two sentences entail each other, whether a pronoun refers to a given noun, and similar tasks. GLUE combined several such tasks into one score and added a diagnostic suite for linguistic analysis. Its authors found that multi-task and transfer baselines did not immediately beat training a separate model for each task (Wang et al., 2018).

Performance on GLUE rose quickly, and SuperGLUE was introduced with harder tasks, a toolkit and a public leaderboard, because the older benchmark had surpassed the level of non-expert humans (Wang et al., 2019). The later generation moved to knowledge and reasoning. MMLU covers 57 subjects, from elementary mathematics to law, and was designed so that models must have broad world knowledge to score well (Hendrycks et al., 2021). When the authors published it, most models were near random chance, and the largest GPT-3 model was about 20 percentage points above chance on average.

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [GLUE](glue.md) | Sentence and sentence-pair understanding tasks, scored together | Per-task scores, combined into one number |
| [SuperGLUE](superglue.md) | Harder understanding tasks, with a human baseline | Per-task scores, combined into one number |
| [MMLU](mmlu.md) | Multiple-choice knowledge across 57 subjects | Accuracy |
| [GPQA](gpqa.md) | Graduate-level multiple-choice questions written by experts | Accuracy |
| [Humanity's Last Exam](hle.md) | 2,700 expert questions, multiple-choice and short-answer | Accuracy with automated grading |

GPQA was built to be hard to answer with search. Its 448 multiple-choice questions were written by experts, and PhD-level experts reached 65% accuracy, while skilled non-experts with web access reached 34%. The strongest GPT-4 based baseline in the paper reached 39% (Rein et al., 2023). Humanity's Last Exam extends the idea to 2,700 questions across many subjects, with answers that are unambiguous but cannot be found quickly on the internet (Phan et al., 2025).

## Key concepts

- **Saturation**: a benchmark is saturated when most systems score near its ceiling, so it no longer separates them. The HLE paper notes that models already score over 90% on MMLU.
- **Human baseline**: a score from people, used to show headroom. SuperGLUE was motivated by GLUE scores passing non-expert humans.
- **Multiple-choice versus open answer**: multiple-choice items can be scored automatically but allow guessing; short answers need a grader.

## How it works

A typical evaluation prompts the model with the question and its options, or with examples of the task, then extracts an answer and compares it with the key. Accuracy is the share of correct answers. For understanding tasks, the score is computed per task and then averaged, so one large task does not dominate the result unless the aggregation says so.

## Common issues

- **Saturation.** Most of these benchmarks reach high scores within a few years of release, after which they stop separating systems.
- **Contamination.** Public questions can appear in pre-training data, so a score can partly reflect memory rather than reasoning.
- **Prompt and extraction sensitivity.** Few-shot examples, answer extraction and the grader change results, so the protocol must be reported with the score.

## Connections

- [Language models](../../../models/llm/index.md) are the systems these benchmarks are used to evaluate.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric behind most of the scores here.
- [Language in the brain](../../../../brain-mind/language-in-brain/index.md) describes how human language understanding is studied, a different question from benchmark accuracy.

## Open questions

- Whether a single knowledge score measures understanding or mostly reflects how much text a model has seen.
- How to keep expert benchmarks useful once frontier systems approach the expert baseline.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Evaluation & Benchmarks](../../../../engineering/evaluation/index.md) gives practical guidance for language models.
- [Math and code](../math-and-code/index.md) covers the reasoning-heavy benchmarks that share many of these issues.

## References

### Seminal papers

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — Introduces the multi-task understanding benchmark, its diagnostic suite, and the finding that multi-task baselines do not yet beat per-task models.
- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — Explains why GLUE had lost headroom after surpassing non-expert humans, and introduces harder tasks.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. arXiv (2020). https://arxiv.org/abs/2009.03300 — Introduces the 57-task knowledge test and reports that most models were near chance at release.

### Articles and documentation

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — Introduces 448 expert-written science questions, with expert and non-expert accuracy reported.
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — Introduces 2,700 expert questions designed to remain hard for frontier models.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — The GPT-3 paper, whose prompting setup is the usual way these benchmarks are run on large models.
