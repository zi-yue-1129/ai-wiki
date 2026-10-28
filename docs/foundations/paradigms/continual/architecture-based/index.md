---
related:
- foundations/paradigms/transfer/fine-tuning-and-adaptation/index.md
- foundations/paradigms/meta-learning/index.md
tags:
  - continual learning
  - progressive networks
  - network expansion
---

# Architecture-based Continual Learning

Architecture-based methods change the network itself as tasks arrive. They can add new capacity for new tasks, dedicate parts of a fixed network to each task, or grow the network only when needed. Because old parameters are frozen or protected, forgetting is avoided by design rather than by penalty or replay.

## Overview

There are two broad options. Fixed-capacity methods assign subsets of parameters to tasks, for example by pruning and reusing the freed weights. Expanding methods add new units or whole columns for each task and connect them to the old ones, with the old parameters left unchanged. Both need a way to decide which task a given input belongs to, unless tasks are known at test time.

## Main methods

- **Progressive networks**: add a new column for each task and connect it to the frozen earlier columns through lateral connections, which allows transfer without forgetting.
- **PackNet**: iteratively prunes a single network and freezes the important weights for each task, so that many tasks share one architecture.
- **Dynamically expandable networks**: add neurons only when the current capacity is not enough, which keeps the network compact.

## Connections

Expanding networks reuse the representation transfer of [fine-tuning](../../transfer/fine-tuning-and-adaptation/index.md), and they are related to the modular ideas in [meta-learning](../../meta-learning/index.md). Unlike [regularisation-based](../regularisation-based/index.md) methods, they do not trade plasticity for stability.

## Applications

Multi-task robot controllers that add skills over time, mobile apps that add features without retraining old ones, and vision systems that must support new object categories without losing old accuracy.

## Open questions

Models grow over time, which raises memory and inference costs. Task identity is often needed at test time, and it is unclear how to route inputs to the right part of a shared network when it is not given.

## References

### Seminal papers

- Rusu et al. (2016), "Progressive neural networks", arXiv:1606.04671 — Adds a new column for each task with lateral connections to frozen earlier columns.
- Mallya & Lazebnik (2018), "PackNet: adding multiple tasks to a single network by iterative pruning", CVPR, arXiv:1711.05769 — Prunes and freezes weights per task, so that many tasks share one network.
- Yoon, Yang, Lee & Hwang (2018), "Lifelong learning with dynamically expandable networks", ICLR, arXiv:1708.01547 — Adds neurons only when the current capacity is insufficient for a new task.

### Surveys and textbooks

- Parisi, Kemker, Part, Kanan & Wermter (2019), "Continual lifelong learning with neural networks: a review", Neural Networks, arXiv:1802.07569 — Review that groups architecture-based methods with the other families.
- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, arXiv:1909.08383 — Survey that compares architecture-based methods under a common protocol.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Serra, Suris, Miron & Karatzoglou (2018), "Overcoming catastrophic forgetting with hard attention to the task", ICML. No link checked.
