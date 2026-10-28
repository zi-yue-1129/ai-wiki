---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - Be your own teacher
  - Deep-layer self-distillation
  - 自己當老師
---

# Be Your Own Teacher

Be Your Own Teacher is a self-distillation method that improves a single network within one training run. Auxiliary classifiers are attached to shallow layers, and each is trained to match the deepest classifier, so knowledge flows downwards inside the network. Zhang et al. reported an average accuracy gain of 2.65% over the baselines. It is a [self-distillation](../index.md) method that needs no separate teacher run.

## Problem

Self-distillation with separate teacher and student runs is expensive. A single network should be able to improve itself within one training run.

## Core idea

Attach auxiliary classifiers to the shallow layers of a network, and train each classifier on the labels and on the output of the deepest classifier. The deepest classifier acts as the teacher for everything below it.

## Equation or algorithm

The loss sums the cross-entropy of every classifier with the labels, plus a distillation term that pulls each shallow classifier towards the deepest one. The auxiliary classifiers are removed at test time, so inference cost is unchanged.

## Results

The abstract reports an average accuracy improvement of 2.65%, from 0.61% for ResNeXt to 4.07% for VGG19.

## Limitations

The method adds classifiers and training terms during training. The gains are for convolutional networks on image classification, and the paper does not test language models.

## Open issues and related variants

- **Architectures.** Whether the same downward flow helps transformers, where layers differ more, is open.
- **Related:** [born-again networks](../born-again-networks/index.md) use a full extra training run to achieve a similar effect.

## Connections

The method is a form of deep supervision, in which intermediate layers receive their own training signal. The downward flow of a deep classifier to shallow ones is also a question of [deep learning theory](../../../../../theory/deep-learning/index.md).

## References

### Seminal papers

- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Deep-layer self-distillation with auxiliary classifiers, an average 2.65% accuracy gain.
- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — The full-generation alternative to self-teaching within one run.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation loss that the shallow classifiers use.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys self-distillation variants.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Intermediate hints, the feature-level counterpart of deep-layer self-teaching.
