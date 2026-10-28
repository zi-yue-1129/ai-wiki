---
related:
- theory/paradigms/active/index.md
- theory/paradigms/meta-learning/memory-and-model-based/index.md
tags:
  - continual learning
  - experience replay
  - episodic memory
---

# Replay and Memory-based Continual Learning

Replay methods keep some information about earlier tasks and mix it into training on new tasks. The stored information can be a small set of real past examples, a learned generator that produces pseudo-examples, or constraints derived from past gradients. Replay is among the most effective ways to reduce forgetting, but it needs memory or a generator.

## Overview

A typical replay learner holds a memory buffer, fills it with examples from earlier tasks, and trains on a mixture of the current data and the buffer. Choices that matter include how examples are selected for the buffer, how many are stored, and whether the stored examples are used as training data or as constraints.

## Main approaches

- **Exemplar replay**: store a fixed number of real examples per class and use them with a distillation loss, as in iCaRL.
- **Gradient constraints**: store examples and use them to check that an update does not increase their loss, as in gradient episodic memory.
- **Tiny episodic memory**: use only a few stored examples per task with simple experience replay, which often matches more complicated methods.
- **Generative replay**: train a generative model to produce pseudo-examples of earlier tasks, which avoids storing real data.

## Connections

Replay resembles the sampling used in [active learning](../../active/index.md), where the choice of which examples to keep matters. Episodic memory also appears in [memory-based meta-learning](../../meta-learning/memory-and-model-based/index.md). The same stored-data idea underlies the generalisation discussion in [supervised learning](../../supervised/index.md).

## Applications

Keeping a recognition system current as new product categories are added, updating a speech model for new speakers without losing old ones, and personal assistants that retain earlier user information.

## Open questions

Storing real data raises privacy and storage concerns, and generative replay can drift when the generator forgets. The best selection rule for the memory is still debated, and small memories may not cover the diversity of old tasks.

## References

### Seminal papers

- Rebuffi, Kolesnikov, Sperl & Lampert (2017), "iCaRL: incremental classifier and representation learning", CVPR, arXiv:1611.07725 — Exemplar replay combined with distillation for class-incremental learning.
- Lopez-Paz & Ranzato (2017), "Gradient episodic memory for continual learning", NeurIPS, arXiv:1706.08840 — Uses stored examples to constrain updates so that past losses do not increase.
- Chaudhry et al. (2019), "On tiny episodic memories in continual learning", ICLR, arXiv:1902.10486 — Shows that very small episodic memories with simple replay are strong baselines.
- Shin, Lee, Kim & Kim (2017), "Continual learning with deep generative replay", NeurIPS, arXiv:1705.08690 — Generates pseudo-examples of earlier tasks with a generative model instead of storing data.

### Surveys and textbooks

- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, arXiv:1909.08383 — Survey and comparison that includes replay methods under a common protocol.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Robins (1995), "Catastrophic forgetting, rehearsal and pseudorehearsal", Connection Science. No link checked.
