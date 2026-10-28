---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - Born-again networks
  - 重生網路
  - 再生網路
---

# Born-Again Neural Networks

Born-again networks are students with the same architecture as their teachers, trained on the teacher's predictions. Furlanello et al. showed that these students can outperform their teachers, which contradicted the assumption that distillation needs a larger teacher. The approach is a [self-distillation](../index.md) method, repeated over several generations if needed.

## Problem

Distillation was assumed to work only when the student is smaller than the teacher, so a larger teacher was thought necessary.

## Core idea

Train a student with the same architecture as its teacher, using the teacher's softened predictions as the target. The authors found that the resulting born-again networks outperform their teachers, and that the gain can be repeated over generations.

## Equation or algorithm

Each generation minimises the distillation loss against the previous generation's softened predictions, with the same architecture and no larger model. The first generation is trained on the labels. Each later generation uses the one before it as its teacher.

## Results

The abstract states that the born-again networks outperform their teachers significantly, in computer vision and in language modelling.

## Limitations

Each generation costs a full training run. The reported gains depend on the setting and on the number of generations.

## Open issues and related variants

- **Saturation.** Whether repeated generations keep improving, or saturate for large models, is open.
- **Related:** [Be Your Own Teacher](../be-your-own-teacher/index.md) achieves a similar effect inside a single training run.

## Connections

The method shows that a network can improve by relearning its own predictions. The same idea appears in [continual learning](../../../../../theory/paradigms/continual/index.md), where an earlier state of a model guides later training.

## References

### Seminal papers

- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — Students with the same architecture as their teachers outperform the teachers in vision and language.
- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Deep-layer self-distillation within one network, a related self-teaching method.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation loss that each generation reuses.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation methods across knowledge types and training schemes.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Shows that the gap between teacher and student affects the student, the question that self-distillation removes.
