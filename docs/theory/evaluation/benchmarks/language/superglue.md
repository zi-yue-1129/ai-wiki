---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - language
---

# SuperGLUE

SuperGLUE is the successor to [GLUE](glue.md). It keeps the same idea of one score over many language understanding tasks, but uses harder tasks, a software toolkit and a public leaderboard (Wang et al., 2019).

## Task and data

SuperGLUE contains eight tasks, including reading comprehension, question answering, word sense disambiguation, coreference and textual entailment. Several tasks need reasoning beyond surface overlap between sentences (Wang et al., 2019).

## Protocol and metric

Each task has its own metric, and the overall score is their average. The authors report a human baseline, which makes it possible to say how far models are from people on the same tasks. The test labels are hidden and results are submitted to a leaderboard.

## What it shows

The benchmark was built after models had passed non-expert human scores on GLUE, so its aim was to restore headroom (Wang et al., 2019). Pre-trained text-to-text models reported results on it (Raffel et al., 2019), and it became the standard test for transfer learning in English.

## Limitations

- **Contamination.** Pre-training corpora built from web text may include task data or near-duplicates, so a high score can partly reflect memorisation.
- **Saturation.** Top systems have approached the human baseline, so the benchmark now distinguishes fewer systems than it did at release.
- **English only.** The tasks do not test other languages.
- **Leaderboard use.** Repeated submissions to a hidden test set risk fitting the leaderboard rather than the task. Protocol rules should be read before comparing scores.

## Related

- [GLUE](glue.md) is the benchmark this one replaces.
- [MMLU](mmlu.md) and [GPQA](gpqa.md) test knowledge and expert reasoning rather than sentence-level understanding.
- [Language family overview](index.md) compares the language benchmarks.

## References

### Seminal papers

- Wang, A. et al. (2019). *SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems*. arXiv. https://arxiv.org/abs/1905.00537 — Introduces the benchmark, its tasks, its toolkit and the human baseline.
- Wang, A. et al. (2018). *GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding*. arXiv. https://arxiv.org/abs/1804.07461 — The benchmark that SuperGLUE was built to succeed.

### Articles and documentation

- Raffel, C. et al. (2019). *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer*. arXiv. https://arxiv.org/abs/1910.10683 — Reports results of a text-to-text model on SuperGLUE tasks.
- Devlin, J. et al. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL. https://arxiv.org/abs/1810.04805 — Pre-trained encoder whose transfer results motivated harder benchmarks.

### Additional sources

- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Evaluates large models with in-context examples on benchmarks of this kind.
