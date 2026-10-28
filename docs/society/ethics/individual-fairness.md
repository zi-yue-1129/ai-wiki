---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - individual fairness
  - similarity metrics
aliases:
  - 個體公平
  - Individual fairness
  - Fairness through awareness
---

# Individual fairness

!!! info "Part of Fairness definitions"
    This method page belongs to [Fairness definitions and impossibility results](fairness-definitions.md). It explains the criterion in detail; the parent page compares it with the others.

Individual fairness requires that similar individuals receive similar outcomes. Dwork, Hardt, Pitassi, Reingold and Zemel (2012) introduced it as an alternative to group criteria, with the similarity between individuals defined by a task-specific metric.

## Problem

Group criteria compare averages across groups, and they can be satisfied while similar people are still treated very differently. The problem is to state a fairness requirement at the level of the individual, and to make it an explicit, checkable condition on the classifier.

## Core idea

Define a metric \(d\) that measures how similar two individuals are for the task at hand. The classifier must map similar individuals to similar output distributions. The requirement is that similar individuals are treated similarly, and the metric is what makes "similar" precise.

## Equation

If \(M(x)\) is the output distribution for individual \(x\), and \(D\) measures distance between distributions, the Lipschitz condition is

\[
D\bigl(M(x), M(y)\bigr) \le d(x, y) \quad \text{for all individuals } x, y.
\]

## Results

The paper gives a framework for fair classification that combines the similarity metric with an algorithm for maximising utility subject to the fairness constraint. Its main contribution is the framework; it does not claim that a particular metric is right for a particular application.

## Limitations

- **Metric choice.** The criterion is only as fair as the metric, and the metric has to be designed by someone. The framework assumes that a task-specific similarity metric is available, which makes choosing it the central difficulty.
- **Scaling.** Checking the condition for every pair of individuals is hard for large datasets, so practical versions approximate it.
- **Proxies.** A metric that ignores sensitive attributes can still allow a classifier to discriminate through correlated features.

## References

### Seminal papers

- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — Introduces individual fairness as a Lipschitz condition on a task-specific similarity metric.
- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — An individual-level criterion based on causal reasoning, which addresses the metric choice differently.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — The group-based criteria that individual fairness is often contrasted with.

### Surveys and textbooks

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — A survey of fairness definitions, as its title states.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook covering individual and group fairness.
