---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- data-free distillation
aliases:
  - Zero-shot knowledge distillation
  - ZSKD
  - 零樣本知識蒸餾
---

# Zero-Shot Knowledge Distillation

Zero-shot knowledge distillation (ZSKD) distils a network without any training data. Nayak et al. synthesise surrogate samples from the teacher alone, by optimising inputs so that the teacher is confident and the samples are diverse, and then train the student on those samples. It is a [data-free](../index.md) method, and the authors report performance competitive with distillation on the real training data.

## Problem

Distillation requires training data, which may be unavailable for a released model, or may be private.

## Core idea

Generate surrogate samples from the teacher. Start from random noise and optimise the input so that the teacher assigns it confidently to a chosen class, with terms that encourage diversity across classes. The student then learns from these samples with the usual distillation loss.

## Equation or algorithm

Inputs are optimised from noise to maximise the teacher's confidence in sampled classes, with a term that keeps the samples diverse. The student is trained on the synthetic samples with the soft-target objective of [Hinton distillation](../../response-based/hinton-distillation/index.md).

## Results

The authors state that the framework results in competitive generalisation performance compared with distillation on the actual training data, on several benchmarks.

## Limitations

Synthesis is expensive, and the quality depends on how well the teacher's outputs characterise the data. The paper's benchmarks are image classification.

## Open issues and related variants

- **Language models.** Discrete tokens are harder to optimise than continuous images, so synthesis for language is an open problem.
- **Related:** [sequence-level distillation](../../llm-distillation/sequence-level/index.md) is a partial data-free method for sequence models, which still uses source sentences.

## Connections

Data-free distillation touches privacy, discussed in [ethics](../../../../../society/ethics/index.md) and [governance](../../../../../society/governance/index.md). The training pipelines it sits in are described under [training](../../../../../engineering/training/index.md).

## References

### Seminal papers

- Nayak, G. K., Mopuri, K. R., Shaj, V., Babu, R. V., Chakraborty, A. (2019). *Zero-Shot Knowledge Distillation in Deep Networks*. arXiv:1905.08114. https://arxiv.org/abs/1905.08114 — Distils a network from synthetic samples optimised from the teacher alone.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The standard objective that assumes training data.
- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — A partial data-free approach for translation models.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation settings, including those without data.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — A distilled language model that uses real data, for contrast with synthetic-data methods.
