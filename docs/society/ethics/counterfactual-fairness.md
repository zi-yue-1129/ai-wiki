---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - causal inference
  - counterfactuals
aliases:
  - 反事實公平
  - Counterfactual fairness
---

# Counterfactual fairness

!!! info "Part of Fairness definitions"
    This method page belongs to [Fairness definitions and impossibility results](fairness-definitions.md). It explains the criterion in detail; the parent page compares it with the others.

Counterfactual fairness asks whether a decision would be the same in a world where the individual had belonged to a different demographic group. It uses causal reasoning, so it requires a model of how the protected attribute influences the other variables. Kusner, Loftus, Russell and Silva (2017) introduced it using tools from causal inference.

## Problem

Group criteria compare statistics, and they do not say which features carry the influence of group membership. The problem is to define fairness for an individual decision, and to separate the effect of the protected attribute from the other causes of the outcome.

## Core idea

Build a causal model that describes how the protected attribute affects other variables. A decision is counterfactually fair if it is unchanged when the attribute is set to a different value in that model, while the variables not caused by the attribute keep their values. The criterion therefore depends on the causal model as well as on the data.

## Equation

With protected attribute \(A\), the predictor \(\hat{Y}\) is counterfactually fair if, for the actual value \(a\) and a counterfactual value \(a'\),

\[
\Pr\bigl[\hat{Y}_{A \leftarrow a}(U) = y \mid X = x, A = a\bigr] = \Pr\bigl[\hat{Y}_{A \leftarrow a'}(U) = y \mid X = x, A = a\bigr],
\]

where \(U\) denotes the unobserved background variables of the causal model.

## Results

The paper defines counterfactual fairness and presents it as a framework for modelling fairness with causal inference. Its claims concern what the definition captures. The practical result depends on the causal model used, so the conclusions hold only as far as that model is correct.

## Limitations

- **Causal model.** The criterion needs a causal graph, which is an assumption that data alone cannot verify.
- **Unobserved variables.** Counterfactual predictions depend on background variables that are not observed, so they must be inferred from the model.
- **Narrow scope.** The criterion addresses the causal effect of the protected attribute; it does not address the outcome's unfairness that comes from unmeasured factors outside the model.

## References

### Seminal papers

- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — Defines counterfactual fairness and presents it as a framework based on causal inference.
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — The individual-level criterion that counterfactual fairness is often compared with.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Group-based criteria, against which the causal approach is contrasted.

### Surveys and textbooks

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — A survey of fairness definitions, as its title states.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook covering fairness definitions and their assumptions.
