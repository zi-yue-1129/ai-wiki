---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - Self-distillation
  - Born-again networks
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

## Key methods

### Born Again Neural Networks (Furlanello et al., 2018)

- **Problem:** Distillation was assumed to work only when the student is smaller than the teacher, so the teacher must be larger.
- **Core idea:** Train a student with the same architecture as its teacher on the teacher's predictions. The authors find that the resulting born-again networks outperform their teachers.
- **Equation or algorithm:** Each generation minimises the distillation loss against the previous generation's softened predictions, with the same architecture and no larger model.
- **Results:** The abstract states that the born-again networks outperform their teachers significantly, in computer vision and in language modelling.
- **Limitations:** Each generation costs a full training run, and the reported gains depend on the setting and the number of generations.

### Be Your Own Teacher (Zhang et al., 2019)

- **Problem:** Self-distillation with separate teacher and student runs is expensive, and a single network should be able to improve itself within one training run.
- **Core idea:** Attach auxiliary classifiers to shallow layers and train each classifier to match the deepest one, so that knowledge flows downwards inside one network.
- **Equation or algorithm:** The loss sums the cross-entropy of every classifier with the labels and a distillation term that pulls each shallow classifier toward the deepest one.
- **Results:** The abstract reports an average accuracy improvement of 2.65%, from 0.61% for ResNeXt to 4.07% for VGG19.
- **Limitations:** The method adds classifiers and training terms. The gains are for convolutional networks on image classification.

## Trade-offs

- **Cost versus teacher-free design.** Born-again training needs repeated runs. Deep-layer self-distillation adds only auxiliary heads, but the gains are smaller.
- **Evaluation.** A self-distilled model can match its teacher on benchmarks while differing in calibration or robustness.

## More variants and open issues

- **Variant:** [feature-based distillation](../feature-based/index.md), which can also be used between layers of one network.
- **Open issue:** why a network learns more from a copy of itself than from its labels. The regularisation account is plausible but not settled.
- **Open issue:** whether repeated generations keep improving or saturate for large models.
- **Related:** the [teacher assistant](../index.md) idea, which bridges large gaps between teacher and student, shows that the size of the teacher also matters.

## Connections

Self-distillation resembles the way learners review and consolidate their own earlier understanding. The idea that a system improves by re-learning its own predictions is also studied under [continual learning](../../../../theory/paradigms/continual/index.md), where a model's earlier state is used to guide later training.

## References

### Seminal papers

- Furlanello, T., et al. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — Students with the same architecture as their teachers outperform the teachers.
- Zhang, L., et al. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Deep-layer self-distillation, with an average accuracy gain of 2.65% over the baselines.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation loss that self-distillation reuses with the network as its own teacher.

### Surveys and textbooks

- Gou, J., et al. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation, including self-distillation variants.
- Mirzadeh, S.-I., et al. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Shows that the student's performance degrades when the teacher-student gap is large.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
