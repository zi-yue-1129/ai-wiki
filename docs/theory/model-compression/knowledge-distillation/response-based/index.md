---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- response-based distillation
aliases:
  - Response-based distillation
  - Logit distillation
  - 響應式蒸餾
---

# Response-Based Distillation

Response-based distillation trains the student to match the teacher's output distribution, usually its softened logits for each example. It is the original form of [knowledge distillation](../index.md), and the methods in this family differ mainly in what the teacher's outputs are used for: a classifier's soft predictions, the masked-token predictions of a language model, or the teacher's own answers in a sequence.

## Overview

The standard recipe adds a KL divergence between the softened teacher and student distributions to the usual task loss. The teacher is frozen, so its outputs can be precomputed. Response-based methods need no access to the teacher's internal layers, which makes them the easiest form of distillation to apply to a model that is available only through its outputs.

## Comparison of methods

| Method | Setting | Extra signal beyond soft outputs | Page |
| --- | --- | --- | --- |
| Hinton distillation | Classification | None; temperature-softened targets with the true labels | [Hinton distillation](hinton-distillation/index.md) |
| DistilBERT | Language model pretraining | Masked language modelling loss and a hidden-state alignment loss | [DistilBERT](distilbert/index.md) |
| Teacher assistant (TAKD) | Any, when the gap is large | An intermediate-size teacher that bridges the gap | [Teacher assistant](teacher-assistant/index.md) |

The first method is the baseline. The second adds language-model objectives and hidden-state alignment to make pretraining cheaper. The third changes the teacher to make large gaps easier to close.

## Trade-offs

- **Simplicity versus signal.** Matching outputs alone is simple, but it gives one target per example and transfers less than feature-based methods do.
- **Temperature.** The temperature decides how much of the teacher's relative probabilities the student sees, and the best value depends on the task.
- **Teacher access.** Only outputs are needed, which suits models served behind an interface, subject to the provider's terms.

## Open issues

- **Gap size.** How large the teacher should be relative to the student, and whether an intermediate teacher is always needed, is not settled.
- **Output diversity.** When the teacher's outputs are nearly one-hot, the soft targets carry little information, and the best remedy is still debated.

## Connections

Response-based distillation is the most widely used form in practice, and the same objective underlies the [LLM distillation](../llm-distillation/index.md) methods. The hardware cost of running a teacher on each input is discussed in [AI hardware](../../../../engineering/hardware/index.md).

## References

### Seminal papers

- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — Introduces temperature-softened outputs as the distillation target.
- Sanh, V., et al. (2019). *DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter*. arXiv:1910.01108. https://arxiv.org/abs/1910.01108 — Distils BERT with output matching and hidden-state alignment.
- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Adds an intermediate teacher assistant to close large teacher-student gaps.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation by knowledge type, starting from output matching.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — The feature-level alternative that adds intermediate targets to output matching.
