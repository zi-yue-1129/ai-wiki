---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- relation-based distillation
aliases:
  - Relational knowledge distillation
  - RKD
  - 關係式知識蒸餾
---

# Relational Knowledge Distillation

Relational knowledge distillation (RKD) trains a student to reproduce the geometry of the teacher's representations over a batch: the distances between pairs of examples and the angles formed by triples. The student does not need to share the teacher's coordinates, only its structure. It is a [relation-based](../index.md) method, and it was shown to improve student models and, in metric learning, to let students outperform their teachers.

## Problem

Matching individual features forces the student's representation to share the teacher's coordinates, which is unnecessary when only the structure matters, for example in retrieval or clustering.

## Core idea

Compare the relations between examples in the teacher and the student, instead of the examples themselves. Pairwise relations use distances, and higher-order relations use angles over triples, so the student reproduces the teacher's geometry.

## Equation or algorithm

A distance loss compares normalised pairwise distances between the examples of a batch in teacher and student spaces. An angle loss compares the angles formed by triples of examples. Both are added to the usual task loss, with the distances normalised by their mean so that the scale of the two spaces does not matter.

## Results

The abstract says the method improves student models with a significant margin, and that students can outperform their teachers in metric learning. It gives no single headline figure.

## Limitations

The batch-level computation adds cost, and the choice of relation affects the outcome. Results depend on the batch size, because the relations are computed within each batch.

## Open issues and related variants

- **Which relations.** The best set of relations for a given task is not known in advance.
- **Related:** [similarity-preserving distillation](../similarity-preserving/index.md) matches a simpler pairwise similarity matrix.

## Connections

Relations between examples are the central object of metric learning, and of the embedding geometry of [transformers](../../../../../theory/models/transformer/index.md). Similarity structure as a carrier of meaning is also studied in [neuroscience](../../../../../brain-mind/neuroscience/index.md), through population codes.

## References

### Seminal papers

- Park, W., Kim, D., Lu, Y., Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — Matches distances and angles between examples, improving student models with a significant margin.
- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Matches the pairwise similarities of activations, a simpler relation loss.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Feature-level distillation, the contrast to relation matching.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by knowledge type, including relations.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Output-level distillation, the baseline that relation methods extend.
