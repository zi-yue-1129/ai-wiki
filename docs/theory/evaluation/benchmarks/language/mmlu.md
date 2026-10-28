---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# MMLU

MMLU (Massive Multitask Language Understanding) measures knowledge and problem solving with multiple-choice questions across 57 subjects, including elementary mathematics, US history, computer science and law (Hendrycks et al., 2021).

## Task and data

Each question has four answer options, and the model picks one. The subjects span STEM, the humanities, the social sciences and professional fields. Good performance requires extensive world knowledge as well as problem solving (Hendrycks et al., 2021).

## Protocol and metric

The metric is **accuracy** over all questions, often with the per-subject average reported as well. Results are usually obtained with a few worked examples in the prompt. Small changes in the prompt or in how the answer letter is extracted can change the score, so the protocol must be reported. The metric is described in [accuracy](../../metrics/classification/accuracy.md).

## What it shows

Most models at release scored close to chance. The largest GPT-3 model improved over chance by almost 20 percentage points on average, but it still fell well short of expert accuracy on every subject. The authors also found that models often did not know when they were wrong (Hendrycks et al., 2021).

## Limitations

- **Saturation.** Models now score above 90% on MMLU, which limits how well it measures progress at the frontier (Phan et al., 2025).
- **Label errors.** Gema et al. (2024) report that a portion of the questions are erroneous or ambiguous, so a ceiling below 100% does not always reflect the model.
- **Multiple choice.** Four options make guessing succeed a quarter of the time, and the format rewards recognition over generation.

## Successors

[Humanity's Last Exam](hle.md) was designed as a harder closed-ended successor. [GPQA](gpqa.md) targets graduate-level science with questions that are hard to answer by search.

## Related

- [Language family overview](index.md) compares the language benchmarks.
- [Accuracy](../../metrics/classification/accuracy.md) is the metric.

## References

### Seminal papers

- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — Introduces the 57-subject test and reports the first results on it.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Introduces the few-shot prompting setting used to evaluate large models on MMLU.

### Articles and documentation

- Gema, A. P. et al. (2024). *Are We Done with MMLU?* arXiv. https://arxiv.org/abs/2406.04127 — Audits the benchmark and reports errors and ambiguous questions in a portion of it.
- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — Notes that models already exceed 90% on MMLU, which motivates its successor.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — A broad benchmark collection that places MMLU among other language tasks.
