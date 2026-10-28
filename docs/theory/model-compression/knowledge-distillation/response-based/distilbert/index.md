---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- language models
aliases:
  - DistilBERT
  - 精簡 BERT
---

# DistilBERT

DistilBERT is a distilled version of BERT with half the layers. It is trained during pretraining with three losses: the soft-target distillation loss from the teacher, the masked language modelling loss, and a cosine loss that aligns the student's hidden states with the teacher's. It is the standard reference for distilling a language model at pretraining time, and a [response-based](../index.md) method that adds hidden-state alignment.

## Problem

BERT is accurate but large and slow for many production uses, and fine-tuning a smaller model from scratch loses much of the accuracy that pretraining gives.

## Core idea

Initialise the student from the teacher's weights, with half of the layers removed, and train it during pretraining with the teacher's soft predictions as one target. The student is also aligned with the teacher's hidden states, so it keeps the teacher's internal structure.

## Equation or algorithm

The student is trained on three objectives together. A temperature-scaled distillation loss matches the teacher's soft predictions over the vocabulary. The masked language modelling loss is the usual pretraining objective. A cosine embedding loss aligns the student's hidden-state vectors with the teacher's at each token.

## Results

The abstract reports that DistilBERT reduces the size of a BERT model by 40% while retaining 97% of its language understanding capabilities, and that it is 60% faster.

## Limitations

The student is still bounded by the teacher's knowledge, and the reported results are on language understanding benchmarks, which do not cover every use. The pretraining distillation needs a large corpus and substantial compute.

## Open issues and related variants

- **Alignment choice.** Which hidden states to align, and how, is a design choice that the paper makes but does not fully explore.
- **Related:** [Hinton distillation](../hinton-distillation/index.md) is the output-only objective that DistilBERT extends.

## Connections

DistilBERT is the language-model form of the distillation that [LLM methods](../../llm-distillation/index.md) use today. The pretraining cost it saves matters most for [training](../../../../../engineering/training/index.md) at scale.

## References

### Seminal papers

- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Halves BERT's layers with output distillation and hidden-state alignment, keeping 97% of its language understanding.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The soft-target objective that DistilBERT uses.
- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Intermediate-layer hints, the same idea behind the hidden-state alignment.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation methods across knowledge types and training schemes.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation*. arXiv:1606.07947. https://arxiv.org/abs/1606.07947 — Distils sequence models by training on the teacher's outputs, the earlier language-model setting.
