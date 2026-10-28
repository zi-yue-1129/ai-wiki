---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- feature-based distillation
aliases:
  - Attention transfer
  - Attention maps distillation
  - 注意力轉移
---

# Attention Transfer

Attention transfer trains a student to match the teacher's attention maps, which summarise where a convolutional network responds spatially, rather than the full feature tensors. Zagoruyko and Komodakis showed that this cheaper target lets a smaller CNN gain accuracy from a stronger teacher. It is a [feature-based](../index.md) method that trades information for a simpler target.

## Problem

Matching full activations forces the student to copy features that it may not have the capacity to represent. A cheaper target that still carries the teacher's structure is needed.

## Core idea

Match the teacher's attention maps. An attention map is a spatial summary of the activations, so the student learns where to respond without copying every channel.

## Equation or algorithm

An attention map is computed from the squared activations, summed over channels, at each spatial position. The student is trained so that its attention maps are close to the teacher's, with a penalty added to the usual loss. Maps are compared after normalisation.

## Results

The authors argue that a smaller student CNN gains accuracy by mimicking the attention maps of a stronger teacher. The figures are in the paper's tables.

## Limitations

Attention maps exist only where the architecture has spatial structure, so the method was developed for convolutional networks. The summary discards channel information that full feature matching would keep.

## Open issues and related variants

- **Transformers.** Attention maps are a natural target for transformers, but how well the transfer works there needs study.
- **Related:** [FitNets](../fitnets/index.md) matches the full features, which carries more information at a higher cost.

## Connections

Attention maps are a spatial summary of where a network looks, which links the method to the attention mechanisms in [transformers](../../../../../theory/models/transformer/index.md). The focus on where a system responds has a counterpart in [neuroscience](../../../../../brain-mind/neuroscience/index.md).

## References

### Seminal papers

- Zagoruyko, S., Komodakis, N. (2016). *Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer*. arXiv:1612.03928. https://arxiv.org/abs/1612.03928 — Matches spatial attention maps between teacher and student to improve a smaller CNN.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Full-feature hints, the alternative this method simplifies.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The output loss that attention transfer is added to.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys feature-based knowledge, including attention-type targets.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Tung, F., Mori, G. (2019). *Similarity-Preserving Knowledge Distillation*. arXiv:1907.09682. https://arxiv.org/abs/1907.09682 — A different intermediate target, matching pairwise similarities, for comparison.
