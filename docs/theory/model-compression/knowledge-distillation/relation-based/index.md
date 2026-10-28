---
status: complete
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

Output matching asks the student to reproduce the teacher's answer for each input. Feature matching asks it to reproduce the teacher's internal vector. Relation matching asks it to reproduce the geometry of a batch: distances between pairs, angles between triples, or the similarity between samples. This geometry often matters for downstream tasks such as retrieval or clustering, so transferring it can help even when individual outputs already match well.

## Key concepts

- **Pairwise relation.** A quantity computed from two examples, such as their distance or similarity in the representation space.
- **Higher-order relation.** A quantity over three or more examples, such as the angle formed by a triple.
- **Batch-level loss.** Relation losses are computed over a batch, so the batch composition and size shape the training signal.
- **Geometry.** The arrangement of representations. It can be matched even when the coordinate systems of teacher and student differ.

## Key methods

Both landmark methods below match relations within a batch. They differ in which relations they keep.

- [RKD (Park et al., 2019)](rkd/index.md): matches distance-wise and angle-wise relations between examples, so it captures both pairwise and higher-order structure.
- [Similarity-preserving distillation (Tung & Mori, 2019)](similarity-preserving/index.md): asks the student to keep the pairwise similarities of the teacher's activations, a narrower target that is simpler to state.

RKD uses a richer set of relations, including angles over triples. Similarity-preserving distillation keeps only pairwise similarities, which makes the objective easier to explain.

## Trade-offs

- **Flexibility versus information.** Relations let the student use a different representation geometry, but each example carries less information than with output or feature matching.
- **Batch dependence.** The loss depends on which examples share a batch, so batch size and sampling must be chosen with care.
- **Cost.** Pairwise terms grow with the square of the batch size, which adds memory and time.

## More variants and open issues

- **Variant:** [feature-based distillation](../feature-based/index.md), which matches the vectors themselves.
- **Open issue:** which relations best transfer knowledge for language models, where representations are high-dimensional and batches often consist of long sequences.
- **Open issue:** how relations transfer when the teacher and student are trained on different data.

## Connections

Relations between examples are the central object of metric learning and of the embedding geometry studied in [transformer models](../../../../theory/models/transformer/index.md). The idea that similarity structure carries meaning is also an organising principle in [neuroscience](../../../../brain-mind/neuroscience/index.md), where population codes are studied through their geometry.

## References

### Seminal papers

- Park, W., Kim, D., Lu, Y. & Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — Proposes distance-wise and angle-wise distillation losses that transfer the mutual relations of examples; the abstract reports significant student gains and, for metric learning, students that match or exceed their teachers.
- Tung, F. & Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Trains the student so that pairs of inputs that are similar or dissimilar in the teacher's activations are also similar or dissimilar in the student's.
- Romero, A., Ballas, N., Ebrahimi Kahou, S., Chassang, A., Gatta, C. & Bengio, Y. (2015). *FitNets: Hints for Thin Deep Nets*. ICLR 2015. https://arxiv.org/abs/1412.6550 — Feature-level distillation, the contrast to relation matching.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by type of knowledge, including relation-based knowledge.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The output-level distillation baseline that relation methods extend.
