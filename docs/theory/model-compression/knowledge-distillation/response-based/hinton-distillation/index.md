---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- response-based distillation
aliases:
  - Hinton distillation
  - Distilling the knowledge in a neural network
  - 欣頓蒸餾
---

# Hinton Distillation

Hinton, Vinyals and Dean's 2015 paper is the origin of modern knowledge distillation. It trains a small model on the softened outputs of a large teacher, so that the student learns the relative probabilities of wrong answers as well as the correct label. Their recipe is the standard objective that the other [response-based](../index.md) methods build on.

## Problem

Ensembles of networks are the most accurate models, but they are too expensive to deploy. A single model that captures the ensemble's knowledge is needed.

## Core idea

Train the small model on the teacher's softened outputs. A temperature spreads the teacher's probabilities, so the near-miss classes, which carry information about how classes relate, become visible to the student. The student is also trained on the true labels.

## Equation or algorithm

The combined loss is

\[
\mathcal{L} = (1-\alpha)\, \mathrm{CE}(y, \sigma(z_s)) + \alpha\, T^2\, \mathrm{KL}\!\left(\sigma(z_t/T)\,\Vert\,\sigma(z_s/T)\right)
\]

where \(z_s\) and \(z_t\) are the student and teacher logits, \(\sigma\) is the softmax, \(T\) is the temperature and \(\alpha\) weights the two terms. The factor \(T^2\) keeps the gradient sizes comparable across temperatures. The paper also proposes training specialist models on subsets of classes, which can be trained in parallel.

## Results

The abstract reports surprising results on MNIST and a significant improvement to the acoustic model of a commercial speech system. It gives no figures, so the full paper should be used for numbers.

## Limitations

The method needs the teacher's outputs on the training inputs, which is expensive for large teachers. The experiments are small by today's standards.

## Open issues and related variants

- **Temperature choice.** The best temperature depends on the task and is usually found by search.
- **Related:** [DistilBERT](../distilbert/index.md) applies the same objective to language-model pretraining, and [feature-based](../../feature-based/index.md) methods add intermediate targets.

## Connections

The objective is the basis of the distillation used across [training](../../../../../engineering/training/index.md) and deployment. The idea that a student learns from a teacher's graded beliefs has an analogy in how learners absorb the nuances of a teacher's answers; see [cognitive science](../../../../../brain-mind/cognitive-science/index.md).

## References

### Seminal papers

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The temperature-softened distillation objective with a combined task loss.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Adds intermediate hint targets to output distillation.
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Applies the same soft-target objective to language-model pretraining.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys output-based distillation as the starting point of the field.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Shows the student's performance degrades when the teacher is much larger than it.
