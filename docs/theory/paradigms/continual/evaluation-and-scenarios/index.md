---
related:
- theory/paradigms/supervised/evaluation-and-validation/index.md
tags:
  - continual learning
  - benchmarks
  - evaluation
---

# Evaluation and Scenarios

Continual learning results depend heavily on the setting. A method can look strong in one scenario and fail in another, so the scenario and the metrics must be stated clearly. This subtopic covers the main scenarios, the metrics used to measure forgetting and intransigence, and the common benchmark practices.

## Overview

Three scenarios are common. In task-incremental learning, the task identity is known at test time. In domain-incremental learning, the task changes the input distribution but not the label set. In class-incremental learning, new classes arrive and the model must choose among all classes seen so far, which is the hardest setting.

## Metrics

- **Forgetting**: the drop in accuracy on an earlier task after later training.
- **Intransigence**: the inability to learn a new task well because of constraints from earlier ones.
- **Forward and backward transfer**: how learning one task affects performance on future and past tasks.
- **Average accuracy**: the mean accuracy over all tasks after the whole sequence, a single summary that hides the trade-off above.

## Practical issues

Benchmarks often use permuted or split versions of standard datasets, and small differences in the protocol can change the ranking of methods. Good practice reports the scenario, the memory budget and the number of tasks, and it compares against simple baselines such as fine-tuning with a replay buffer.

## Connections

The metrics follow the standards of [supervised evaluation](../../supervised/evaluation-and-validation/index.md), extended to sequences of tasks. Scenarios that change the input distribution are the continual version of [domain adaptation](../../transfer/domain-adaptation/index.md).

## Applications

Comparing continual learning methods before deployment, choosing a memory budget for a production system, and designing a benchmark for a new domain such as medical imaging or robotics.

## Open questions

Standard benchmarks may not reflect the streams of data found in practice, where tasks are unlabelled and their boundaries are unknown. Metrics for plasticity, the ability to keep learning, are less developed than those for forgetting.

## References

### Seminal papers

- Van de Ven & Tolias (2019), "Three scenarios for continual learning", arXiv:1904.07734 — Defines the task-, domain- and class-incremental scenarios and compares methods within each.
- Kemker, McClure, Abitino, Hayes & Kanan (2018), "Measuring catastrophic forgetting in neural networks", AAAI, arXiv:1708.02072 — Proposes systematic measurements of forgetting across architectures and methods.
- Chaudhry, Dokania, Ajanthan & Torr (2018), "Riemannian walk for incremental learning: understanding forgetting and intransigence", ECCV, arXiv:1801.10112 — Defines forgetting and intransigence as separate measures and studies their trade-off.
- Lopez-Paz & Ranzato (2017), "Gradient episodic memory for continual learning", NeurIPS, arXiv:1706.08840 — Introduces backward and forward transfer metrics for sequences of tasks.

### Surveys and textbooks

- De Lange et al. (2021), "A continual learning survey: defying forgetting in classification tasks", IEEE TPAMI, arXiv:1909.08383 — Survey that proposes a common evaluation protocol for continual classification.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Hsu, Liu, Ramasamy & Kira (2018), "Re-evaluating continual learning scenarios: a categorization and case for strong baselines", NeurIPS continual learning workshop. No link checked.
