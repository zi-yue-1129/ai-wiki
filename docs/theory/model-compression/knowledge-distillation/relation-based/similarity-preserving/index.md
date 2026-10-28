---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- relation-based distillation
aliases:
  - Similarity-preserving distillation
  - 相似性保留蒸餾
---

# Similarity-Preserving Knowledge Distillation

Similarity-preserving distillation trains the student so that examples that produce similar activations in the teacher also produce similar activations in the student. It matches a pairwise similarity matrix over a batch, rather than the features themselves. The student keeps the teacher's similarities in its own representation space, so the two networks need not share a feature space. It is a simpler [relation-based](../index.md) method than [RKD](../rkd/index.md).

## Problem

Relational losses over whole batches can be expensive, and it is not clear which relations are most useful for transfer.

## Core idea

Semantically similar inputs tend to elicit similar activation patterns in a trained network. Use this as the target: compute the pairwise similarity of the teacher's activations over a batch, and train the student to produce the same similarity pattern.

## Equation or algorithm

For a batch, the similarity matrices of the teacher and the student are computed from their activations, with a normalised inner product for each pair. The student is trained to match the two matrices, and the loss is added to the usual task loss.

## Results

The abstract grounds the method in the observation that semantically similar inputs elicit similar activation patterns. The experimental figures are in the paper.

## Limitations

The similarity matrix grows with the square of the batch size, and the method was evaluated on classification tasks.

## Open issues and related variants

- **Batch size.** How to keep the cost of the similarity matrix low for large batches is a practical question.
- **Related:** [RKD](../rkd/index.md) adds angle relations over triples, which carry more structure.

## Connections

Pairwise similarity is the basis of metric learning, and the idea that similar inputs share a code connects to population coding in [neuroscience](../../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — Trains the student to keep the teacher's pairwise similarities in its own activations.
- Park, W., Kim, D., Lu, Y., Cho, M. (2019). *Relational Knowledge Distillation*. arXiv:1904.05068. https://arxiv.org/abs/1904.05068 — Matches distances and angles, a richer set of relations.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Feature-level distillation, the alternative that needs a shared feature space.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys relation-based knowledge among other types.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The output-level baseline that similarity matching complements.
