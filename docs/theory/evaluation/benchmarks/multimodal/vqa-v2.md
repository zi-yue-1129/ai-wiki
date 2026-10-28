---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - multimodal
---

# VQA v2

VQA v2 is the balanced version of the Visual Question Answering benchmark. Visual question answering asks an open-ended question about an image and expects a short answer (Antol et al., 2015). VQA v2 was built after it was found that models could score well by answering from the question text alone (Goyal et al., 2016).

## Task and data

Given an image and a question such as "what colour is the bus?", the system returns an answer. In VQA v2 each question is paired with two images that give different answers, which removes the shortcut of answering from the most common response to that question (Goyal et al., 2016).

## Protocol and metric

Each question has ten human answers. The accuracy for a predicted answer is the number of matching human answers divided by three, capped at one, which gives partial credit when annotators disagree (Antol et al., 2015). Answers are normalised before matching, so the normalisation rules must be stated.

## What it shows

Balancing the data lowered the scores of models that relied on language priors, and it made image understanding necessary for good performance (Goyal et al., 2016). It is the standard test for showing whether a model uses the image at all.

## Limitations

- **Short answers.** Responses are one or a few words, so the benchmark does not test explanation or multi-step reasoning.
- **Annotator agreement.** Where human answers disagree, the score reflects the consensus rule as much as the model.
- **Saturation.** Recent multimodal systems score well, so differences need intervals.

## Related

- [MMMU](mmmu.md) tests college-level reasoning over images rather than short factual answers.
- [ImageNet](../vision/imagenet.md) is the classification benchmark that visual encoders are usually evaluated on first.
- [Multimodal family overview](index.md) compares the benchmarks in this area.

## References

### Seminal papers

- Goyal, Y. et al. (2016). *Making the V in VQA Matter: Elevating the Role of Image Understanding in Visual Question Answering*. arXiv. https://arxiv.org/abs/1612.00837 — Introduces the balanced dataset and the evidence that language priors inflated scores.
- Antol, S. et al. (2015). *VQA: Visual Question Answering*. arXiv. https://arxiv.org/abs/1505.00468 — Defines the open-ended task, the dataset and the consensus-based accuracy.

### Articles and documentation

- Yue, X. et al. (2023). *MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI*. arXiv. https://arxiv.org/abs/2311.16502 — A harder multimodal benchmark that follows VQA in testing reasoning.
- He, K. et al. (2015). *Deep Residual Learning for Image Recognition*. arXiv. https://arxiv.org/abs/1512.03385 — Residual networks, a common image encoder in visual question answering.

### Additional sources

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
