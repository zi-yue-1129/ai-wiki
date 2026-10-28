---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# Multimodal Benchmarks

Multimodal benchmarks test whether a model can combine what it sees with what it knows. The two benchmarks here differ in what they stress: VQA v2 checks whether the image is used at all, and MMMU checks expert reasoning over images.

| Benchmark | Task | Main metric |
|---|---|---|
| [VQA v2](vqa-v2.md) | Short open-ended answers about an image | Consensus accuracy against ten human answers |
| [MMMU](mmmu.md) | College-level questions with images | Accuracy, overall and per discipline |

## Common issues

- **Language priors.** A model can answer from the question text, which inflates scores. Balanced data counters this (Goyal et al., 2016).
- **Mixed signal.** Scores on expert questions combine perception with knowledge, so errors are hard to attribute (Yue et al., 2023).
- **Saturation.** Recent systems score high on the older sets, which pushes new benchmarks toward harder questions.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Vision](../vision/index.md) covers image-only benchmarks.
- [Language](../language/index.md) covers the text-only counterparts.

## References

### Seminal papers

- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — Defines the open-ended visual question answering task.
- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — Shows language priors inflate scores and introduces balanced data.

### Articles and documentation

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — Introduces the college-level multimodal benchmark.
- Srivastava, A. et al. (2022). *Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models*. arXiv. https://arxiv.org/abs/2206.04615 — Describes broad benchmark design, including multimodal tasks.
- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows how a re-collected test set can reveal fit to the original data.
