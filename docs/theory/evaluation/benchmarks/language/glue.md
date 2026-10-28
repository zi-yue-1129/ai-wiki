---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# GLUE

GLUE (General Language Understanding Evaluation) is a benchmark that combines several natural language understanding tasks into one score, with a diagnostic suite for analysis (Wang et al., 2018). It was designed so that progress on one task would transfer to others.

## Task and data

GLUE contains nine tasks that cover sentence acceptability, sentiment, paraphrase, textual similarity and natural language inference. The tasks differ in size, and some have very little training data, which rewards models that share knowledge across tasks (Wang et al., 2018).

## Protocol and metric

Each task has its own metric, such as accuracy, F1 or correlation. The overall score is the average of the task scores. Test labels are hidden, so submissions go through a public leaderboard. The diagnostic suite is a hand-built set of examples for analysing linguistic phenomena.

## What it shows

At release, multi-task and transfer baselines did not give large gains over the best single-task models (Wang et al., 2018). Pre-trained encoders changed that picture: BERT reported its results on GLUE (Devlin et al., 2019), and GLUE became the main test bed for pre-trained language models.

## Limitations

- **Saturation.** SuperGLUE's authors note that models had surpassed non-expert humans on GLUE, which leaves little headroom (Wang et al., 2019).
- **Shortcuts.** Some tasks can be solved partly by exploiting patterns in the data. The diagnostic suite was designed to expose such failures.
- **English only.** The benchmark does not test other languages.

## Successors

[SuperGLUE](superglue.md) replaced the harder tasks. Later benchmarks, such as [MMLU](mmlu.md), test knowledge and reasoning rather than sentence-level understanding.

## Related

- [Language family overview](index.md) compares the language benchmarks.
- [Accuracy](../../metrics/classification/accuracy.md) and [F1](../../metrics/classification/f1.md) are the metrics most GLUE tasks use.

## References

### Seminal papers

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — Introduces the multi-task benchmark, its score and the diagnostic suite.
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL. https://arxiv.org/abs/1810.04805 — Reports pre-trained encoder results on GLUE that changed its role as a test bed.

### Articles and documentation

- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — The harder successor, with its own toolkit and leaderboard.
- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — Evaluates a unified text-to-text model on GLUE and SuperGLUE tasks.

### Additional sources

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — A later multi-task test that targets knowledge rather than sentence understanding.
