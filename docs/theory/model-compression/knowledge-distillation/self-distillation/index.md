---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - Self-distillation
  - 自我蒸餾
  - 自蒸餾
---

# Self-Distillation

Self-distillation trains a network to learn from its own outputs or features, either from an earlier copy of itself or from its own deeper layers. Unlike [teacher-student distillation](../index.md), no larger model is needed. The surprising result of this family is that the student often ends up more accurate than the model that produced its targets.

## Overview

In classic distillation the teacher is a separate model that is larger or better trained. Self-distillation removes that requirement. A common setup trains generation \(t\) on the softened predictions of generation \(t-1\), with the same architecture each time. A second setup adds auxiliary classifiers to the shallow layers of one network, and uses the deepest classifier as the teacher for the others. Both approaches use the same loss as classic distillation, with the teacher replaced by the network itself.

## Key concepts

- **Born-again network.** A student with the same architecture as its teacher, trained on the teacher's predictions.
- **Generation.** One round of self-distillation. Several generations can be chained.
- **Deep-layer teacher.** A variant where the deepest classifier of a network supervises its shallower classifiers within one training run.
- **Why it helps.** The soft targets act as a regulariser and reduce the variance of the final model, though the exact mechanism is still debated.

## Comparison of methods

| Method | Teacher | Training runs | Page |
| --- | --- | --- | --- |
| Born-again networks | Previous generation of the same architecture | One run per generation | [Born-again networks](born-again-networks/index.md) |
| Be Your Own Teacher | Deepest classifier of the same network | One run in total | [Be Your Own Teacher](be-your-own-teacher/index.md) |

Born-again networks trade extra training runs for a clean teacher-student setup, and the effect can repeat over generations. Be Your Own Teacher achieves a similar effect inside one run, at the cost of auxiliary classifiers and training terms.

## Trade-offs

- **Cost versus teacher-free design.** Born-again training needs repeated runs. Deep-layer self-distillation adds only auxiliary heads, but the gains are smaller.
- **Evaluation.** A self-distilled model can match its teacher on benchmarks while differing in calibration or robustness.

## More variants and open issues

- **Variant:** [feature-based distillation](../feature-based/index.md), which can also be used between layers of one network.
- **Open issue:** why a network learns more from a copy of itself than from its labels. The regularisation account is plausible but not settled.
- **Open issue:** whether repeated generations keep improving or saturate for large models.
- **Related:** the [teacher assistant](../response-based/teacher-assistant/index.md) idea, which bridges large gaps between teacher and student, shows that the size of the teacher also matters.

## Connections

Self-distillation resembles the way learners review and consolidate their own earlier understanding. The idea that a system improves by re-learning its own predictions is also studied under [continual learning](../../../../theory/paradigms/continual/index.md), where a model's earlier state is used to guide later training.

## References

### Seminal papers

- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — Students with the same architecture as their teachers outperform the teachers.
- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Deep-layer self-distillation, with an average accuracy gain of 2.65% over the baselines.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation loss that self-distillation reuses with the network as its own teacher.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation methods, including the self-distillation variants discussed here.
- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Shows that the student's performance degrades when the teacher-student gap is large.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
