---
status: complete
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

Self-distillation trains a network to learn from its own outputs or features, either from an earlier copy of itself or from its own deeper layers. Unlike [teacher-student distillation](../index.md), no larger model is needed. The notable result of this family is that the student often ends up more accurate than the model that produced its targets.

## Overview

In classic distillation the teacher is a separate model that is larger or better trained. Self-distillation removes that requirement. A common setup trains generation \(t\) on the softened predictions of generation \(t-1\), with the same architecture each time. A second setup divides one network into sections and passes knowledge from the deepest section to the shallower ones within a single training run. Both approaches use the same kind of loss as classic distillation, with the teacher replaced by the network itself.

## Key concepts

- **Born-again network.** A student with the same architecture as its teacher, trained on the teacher's predictions.
- **Generation.** One round of self-distillation. Several generations can be chained.
- **Deep-layer teacher.** A variant in which the deepest part of a network supervises its shallower parts within one training run.
- **Why it helps.** Soft targets can act as a regulariser. The mechanism is still debated, and the papers offer different explanations.

## Key methods

Both landmark methods below use the network as its own teacher, but they differ in how many training runs they need.

- [Born-again networks (Furlanello et al., 2018)](born-again-networks/index.md): trains a sequence of generations, each with the same architecture as its teacher, so that every new student is distilled from the previous model.
- [Be Your Own Teacher (Zhang et al., 2019)](be-your-own-teacher/index.md): distills from the deepest part of a single network into its shallower parts, all within one run.

Born-again networks trade extra training runs for a clean teacher-student setup, and the effect can repeat over generations. Be Your Own Teacher reaches a similar effect inside one run, at the cost of auxiliary classifiers and extra loss terms.

## Trade-offs

- **Cost versus teacher-free design.** Born-again training needs repeated runs. Deep-layer self-distillation adds auxiliary heads within one run, but the reported gains depend on the architecture.
- **Evaluation.** A self-distilled model can match its teacher on accuracy while differing in calibration or robustness, which accuracy alone does not reveal.

## More variants and open issues

- **Variant:** [feature-based distillation](../feature-based/index.md), which can also be used between layers of one network.
- **Open issue:** why a network learns more from a copy of itself than from its labels alone. The regularisation account is plausible but not settled.
- **Open issue:** whether repeated generations keep improving or saturate for large models.
- **Related:** the [teacher assistant](../response-based/teacher-assistant/index.md) idea addresses large gaps between teacher and student, a different question from self-distillation's lack of a separate teacher.

## Connections

Self-distillation resembles the way learners review and consolidate their own earlier understanding. The idea that a system improves by re-learning its own predictions is also studied under [continual learning](../../../../theory/paradigms/continual/index.md), where a model's earlier state guides later training.

## References

### Seminal papers

- Furlanello, T., Lipton, Z. C., Tschannen, M., Itti, L. & Anandkumar, A. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — Trains students with the same architecture as their teachers; the abstract reports that these students outperform their teachers on vision and language tasks.
- Zhang, L., Song, J., Gao, A., Chen, J., Bao, C. & Ma, K. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Distils knowledge from the deeper sections of a network into its shallower sections; the abstract reports an average accuracy gain of 2.65%.
- Hinton, G., Vinyals, O. & Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation objective that self-distillation reuses with the network as its own teacher.
- Mirzadeh, S.-I., Farajtabar, M., Li, A., Levine, N., Matsukawa, A. & Ghasemzadeh, H. (2019). *Improved Knowledge Distillation via Teacher Assistant*. arXiv:1902.03393. https://arxiv.org/abs/1902.03393 — Shows that student performance degrades when the teacher-student gap is large, and proposes an intermediate teacher assistant to bridge it.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J. & Tao, D. (2021). *Knowledge Distillation: A Survey*. International Journal of Computer Vision, 129(6). https://doi.org/10.1007/s11263-021-01453-z — Surveys distillation methods, including the self-distillation variants discussed here.

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)
