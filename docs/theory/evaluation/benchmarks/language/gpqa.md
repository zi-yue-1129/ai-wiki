---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# GPQA

GPQA is a set of 448 graduate-level multiple-choice questions in biology, physics and chemistry. The questions were written by experts and designed to be hard to answer by searching the web, hence the name "Google-proof" (Rein et al., 2023).

## Task and data

Each question has four options. Questions were written by people with PhDs or PhD training in the relevant field. The benchmark is organised by three sciences, and its size is deliberately small so that each question can be validated carefully.

## Protocol and metric

The metric is **accuracy**. The paper also reports how people perform. Experts with PhDs reached 65% accuracy, or 74% when clear mistakes they identified in retrospect are discounted. Skilled non-expert validators reached 34% even though they spent over 30 minutes with unrestricted web access. A GPT-4-based baseline scored 39% (Rein et al., 2023).

## What it shows

The benchmark gives a difficulty scale anchored to human experts rather than to the general public. It was built to ask whether a system can answer questions that require expert knowledge and careful reasoning, not simple recall.

## Limitations

- **Small sample.** With 448 questions, a few percentage points can be sampling noise. Report a confidence interval, which the [protocols](../../protocols/index.md) section describes.
- **Narrow coverage.** The benchmark covers three sciences and not the other fields where expert reasoning matters.
- **Search access.** The "Google-proof" property was checked against people with web access at writing time. Models with browsing tools can be evaluated differently, so the evaluation setup must be stated.

## Related

- [MMLU](mmlu.md) covers broader knowledge at a lower difficulty.
- [Humanity's Last Exam](hle.md) is a larger and harder successor.
- [Language family overview](index.md) compares the language benchmarks.

## References

### Seminal papers

- Rein, D. et al. (2023). *GPQA: A Graduate-Level Google-Proof Q&A Benchmark*. arXiv. https://arxiv.org/abs/2311.12022 — Introduces the 448 expert-written questions and the expert and non-expert baselines.
- Hendrycks, D. et al. (2021). *Measuring Massive Multitask Language Understanding*. ICLR. https://arxiv.org/abs/2009.03300 — Earlier multiple-choice knowledge benchmark that GPQA targets above.

### Articles and documentation

- Phan, L. et al. (2025). *Humanity's Last Exam*. arXiv. https://arxiv.org/abs/2501.14249 — Larger successor with questions designed to stay hard.
- Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. arXiv. https://arxiv.org/abs/2201.11903 — Shows that intermediate reasoning steps change scores on reasoning benchmarks.

### Additional sources

- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Broad benchmark collection that places expert-level questions among other tasks.
