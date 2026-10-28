---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# Language Benchmarks

Language benchmarks cover three different things: sentence-level understanding (GLUE and SuperGLUE), broad knowledge in multiple-choice form (MMLU), and expert-level reasoning (GPQA and Humanity's Last Exam). Scores from different groups are not interchangeable, because they test different skills.

| Benchmark | Task | Main metric |
|---|---|---|
| [GLUE](glue.md) | Nine understanding tasks | Per-task scores, averaged |
| [SuperGLUE](superglue.md) | Eight harder understanding tasks | Per-task scores, averaged |
| [MMLU](mmlu.md) | Knowledge across 57 subjects | Accuracy |
| [GPQA](gpqa.md) | Graduate-level science | Accuracy |
| [Humanity's Last Exam](hle.md) | Expert questions across subjects | Accuracy with automated grading |

## Common issues

- **Saturation.** Most of these benchmarks reach high scores within a few years of release.
- **Contamination.** Public questions can appear in pre-training data, so a score can partly reflect memory.
- **Prompt sensitivity.** Few-shot examples, answer extraction and the grader change results, so the protocol must be reported.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric for most of these.

## References

### Seminal papers

- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — Introduces the multi-task understanding benchmark.
- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — Introduces the harder successor and its human baseline.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — Introduces the 57-subject knowledge test.

### Articles and documentation

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — Introduces expert-written science questions with expert baselines.
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — Introduces a 2,500-question successor to saturated benchmarks.
