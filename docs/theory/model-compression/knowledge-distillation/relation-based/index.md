---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/transformer
tags:
- model compression
- knowledge distillation
- relation-based distillation
aliases:
  - Relation-based distillation
  - Relational knowledge distillation
  - 關係式蒸餾
---

# Relation-Based Distillation

Relation-based distillation transfers the relations between examples, rather than the outputs or features of single examples. The student learns that certain pairs of inputs are close or far apart in the teacher's representation space, which carries structure that individual outputs and features do not.

## Overview

Output matching asks the student to reproduce the teacher's answer for each input. Feature matching asks it to reproduce the teacher's internal vector. Relation matching asks it to reproduce the geometry of a batch: distances between pairs, angles between triples, or the similarity between samples. This geometry is what downstream tasks often depend on, such as retrieval or clustering, so transferring it can help even when the individual outputs match well.

## Key concepts

- **Pairwise relation.** A quantity computed from two examples, such as their distance or similarity in the representation space.
- **Higher-order relation.** A quantity over three or more examples, such as the angle formed by a triple.
- **Batch-level loss.** Relation losses are computed over a batch, so the batch size affects the signal.
- **Geometry.** The arrangement of representations, which can be matched even when the coordinate systems of teacher and student differ.

## Comparison of methods

| Method | Relations matched | Cost driver | Page |
| --- | --- | --- | --- |
| RKD | Pairwise distances and triple angles | Batch size, through pairwise and triple terms | [RKD](rkd/index.md) |
| Similarity-preserving | Pairwise similarity of activations | Batch size, through the similarity matrix | [Similarity-preserving](similarity-preserving/index.md) |

RKD matches a richer set of relations, including angles over triples, and its results on metric learning are the strongest claim in the family. Similarity-preserving distillation keeps only the pairwise similarities, which is simpler to compute and to explain.

## Trade-offs

- **Flexibility versus information.** Relations allow the student to use a different representation geometry, but they carry less information per example than output or feature matching.
- **Batch dependence.** The loss depends on the batch composition, so training settings must be chosen with care.
- **Cost.** Pairwise computations add memory and time.

## More variants and open issues

- **Variant:** [feature-based distillation](../feature-based/index.md), which matches the vectors themselves.
- **Open issue:** which relations best transfer knowledge for language models, where representations are high-dimensional and batches are often composed of long sequences.
- **Open issue:** how relations transfer when the teacher and student are trained on different data.

## Connections

Relations between examples are the central object of metric learning and of [embedding](../../../../theory/models/transformer/index.md) geometry in transformers. The idea that similarity structure carries meaning is also an organising principle in [neuroscience](../../../../brain-mind/neuroscience/index.md), where population codes are studied through their geometry.

## References

### Seminal papers

- Park, W., et al. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — Matches distances and angles between examples, improving student models with a significant margin.
- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Trains the student to keep the pairwise similarities of the teacher's activations.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Feature-level distillation, the contrast to relation matching.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by knowledge type, including relations.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Output-level distillation, the baseline that relation methods extend.
