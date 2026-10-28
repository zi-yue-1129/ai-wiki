---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# Humanity's Last Exam

Humanity's Last Exam (HLE) is a benchmark of 2,500 questions across dozens of subjects, including mathematics, the humanities and the natural sciences. It is multimodal and was written by subject-matter experts to stay hard as models improve. Its authors describe it as the final closed-ended academic benchmark of its kind (Phan et al., 2025).

## Task and data

The questions are multiple-choice or short-answer. Each has a known solution that can be checked automatically, and each is meant to be unanswerable by a quick internet search. Some items include images, so the benchmark tests multimodal reasoning as well as text (Phan et al., 2025).

## Protocol and metric

The metric is **accuracy** against the reference answers, using automated grading. Short-answer grading depends on the matching rule, so the grader and any judge model must be reported. The metric is described in [accuracy](../../metrics/classification/accuracy.md).

## What it shows

The benchmark was built because models had passed 90% on MMLU (Phan et al., 2025). It asks how well models perform on questions at the edge of expert knowledge, and it is intended to track progress for longer than earlier benchmarks.

## Limitations

- **Contamination after release.** Once questions are public, they may enter training data, so later scores need a clear statement of when the model was trained relative to the release.
- **Automated grading.** Short-answer checking can reject a correct answer with different wording, and it can accept a wrong answer that matches the expected form.
- **Closed-ended format.** Real research questions are open-ended and cannot be checked against a fixed key, so HLE measures a narrower skill than research work.
- **Expert authorship.** Question quality depends on the contributors, and disagreement among experts is hard to resolve for a closed benchmark.

## Related

- [MMLU](mmlu.md) is the benchmark HLE was designed to succeed.
- [GPQA](gpqa.md) covers graduate-level science with a smaller set of questions.
- [Language family overview](index.md) compares the language benchmarks.

## References

### Seminal papers

- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — Introduces the 2,500-question benchmark, its construction and its grading.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — The benchmark whose saturation motivated HLE.

### Articles and documentation

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — A smaller expert-level benchmark, with a discussion of search-proof questions.
- Gema, A. P. et al. (2024). *Are We Done with MMLU?* arXiv. https://arxiv.org/abs/2406.04127 — Audits a saturated benchmark and reports errors that matter for successors.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes a broad approach to designing benchmarks that remain informative as models improve.
