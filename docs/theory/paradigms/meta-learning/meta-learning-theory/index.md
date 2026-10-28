---
related:
- theory/paradigms/supervised/generalization-theory/index.md
- theory/paradigms/transfer/transfer-theory/index.md
tags:
  - meta-learning
  - learning theory
  - inductive bias
---

# Meta-learning Theory

Meta-learning theory asks why learning from many tasks should help a new task, and how much data is needed. The central idea is that learning across tasks reveals a shared inductive bias, such as a common representation or a common prior, and that this bias can be estimated from the tasks and then reused.

## Overview

Theory usually treats the tasks as drawn from an environment, and it bounds the expected error on a new task in terms of the number of tasks and the number of examples per task. The bounds show how a shared representation reduces the sample complexity of each new task, provided the tasks are related.

## Key results

- **Learning to learn**: Baxter's model formalises an inductive bias that is itself learned from a family of tasks, and it gives generalisation bounds for this setting.
- **Benefit of shared representations**: when tasks share a low-dimensional representation, the per-task error falls as the number of tasks grows, which justifies representation learning across tasks.
- **Hierarchical Bayes**: gradient-based meta-learning can be interpreted as inference in a hierarchical Bayesian model, which explains the role of the initialisation as a prior.
- **Biased regularisation**: learning-to-learn can be formulated as regularising each task toward a learned common parameter, with convergence and generalisation guarantees.

## Connections

The bounds use the same tools as [generalisation theory](../../supervised/generalization-theory/index.md). The same questions about when shared structure helps arise in [transfer theory](../../transfer/transfer-theory/index.md), and the optimisation-based methods in [optimisation-based meta-learning](../optimisation-based/index.md) can be read through the hierarchical Bayes view.

## Applications

Choosing how many tasks and examples to collect for a new domain, understanding why a pre-trained representation helps new tasks, and designing priors for personalised models.

## Open questions

Most theory assumes tasks are drawn from one environment with a simple structure, which rarely holds in practice. Bounds for deep networks and for the adaptation procedures actually used remain loose or missing.

## References

### Seminal papers

- Baxter (2000), "A model of inductive bias learning", Journal of Artificial Intelligence Research. https://jair.org/index.php/jair/article/download/10253/24418 — Formalises inductive bias as something that can be learned from a family of tasks, with generalisation bounds.
- Maurer, Pontil & Romera-Paredes (2016), "The benefit of multitask representation learning", JMLR, [arXiv:1505.06279](https://arxiv.org/abs/1505.06279) — Shows that learning a shared representation across tasks reduces the sample complexity of each new task.
- Grant, Finn, Levine, Darrell & Griffiths (2018), "Recasting gradient-based meta-learning as hierarchical Bayes", ICLR, [arXiv:1801.08930](https://arxiv.org/abs/1801.08930) — Interprets gradient-based meta-learning as inference in a hierarchical Bayesian model.
- Denevi, Ciliberto, Grazzi & Pontil (2019), "Learning-to-learn stochastic gradient descent with biased regularization", ICML, [arXiv:1903.10399](https://arxiv.org/abs/1903.10399) — Regularises each task toward a learned parameter and proves guarantees for this scheme.

### Surveys and textbooks

- Hospedales, Antoniou, Micaelli & Storkey (2021), "Meta-learning in neural networks: a survey", IEEE TPAMI, [arXiv:2004.05439](https://arxiv.org/abs/2004.05439) — Survey that summarises the theoretical framing of meta-learning and its open questions.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Thrun & Pratt (1998), *Learning to Learn*, Springer. https://link.springer.com/doi/10.1007/978-1-4615-5529-2 — Edited volume that sets out the foundations of learning to learn and inductive transfer.
