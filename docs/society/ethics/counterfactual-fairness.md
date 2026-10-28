---
status: complete
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

Group criteria compare statistics, and they do not say which features carry the influence of group membership. Simply removing the protected attribute from the inputs does not solve this, because other features can act as proxies for it. The problem is to define fairness for an individual decision, and to separate the effect of the protected attribute from the other causes of the outcome.

## Core idea

Build a causal model that describes how the protected attribute affects other variables. A predictor is counterfactually fair if, given the individual's observed data, its distribution of predictions is the same whether the attribute keeps its actual value or is set to a different value in the causal model. A key lemma of the paper is that a predictor is counterfactually fair if it depends only on variables that are not descendants of the protected attribute in the causal graph. The criterion therefore depends on the causal model as well as on the data.

## Equation

With protected attribute \(A\), the predictor \(\hat{Y}\) is counterfactually fair if, for the actual value \(a\) and a counterfactual value \(a'\),

\[
\Pr\bigl[\hat{Y}_{A \leftarrow a}(U) = y \mid X = x, A = a\bigr] = \Pr\bigl[\hat{Y}_{A \leftarrow a'}(U) = y \mid X = x, A = a\bigr],
\]

where \(U\) denotes the unobserved background variables of the causal model, and \(\hat{Y}_{A \leftarrow a}\) is the prediction in the world where \(A\) is set to \(a\).

## Results

Kusner et al. (2017) fit law-school success predictors on a survey by the Law School Admission Council covering 163 schools and 21,790 students, with LSAT, GPA and first-year average as variables. The root-mean-square error of the models is:

| Model | RMSE |
|---|---|
| Full (uses race, sex and all other variables) | 0.873 |
| Unaware (drops the protected attributes) | 0.894 |
| Fair K (counterfactually fair, Level 2) | 0.929 |
| Fair Add (counterfactually fair, Level 3) | 0.918 |

The authors write that "we must sacrifice a small amount of accuracy to ensuring counterfactually fair prediction." The full model is counterfactually unfair for every protected attribute except sex, and the paper attributes the sex result to a very weak causal link between sex and GPA and LSAT, not to the method. The paper also gives three levels of causal assumption: Level 1 uses only observable non-descendants of the attribute, Level 2 posits latent background variables, and Level 3 posits a deterministic model with additive error terms.

## Limitations

- **Causal model.** The criterion needs a causal graph as input. The authors say that counterfactual claims "always require strong assumptions", and that such assumptions are in general unfalsifiable even with interventional data.
- **Unobserved variables.** Counterfactual predictions depend on background variables that are not observed, so they must be inferred from the model.
- **Synthetic evaluation.** The experiments assume that the true model matches the assumed model, so they do not test robustness to misspecification.
- **Level 1 is often impractical.** Few observed variables are typically non-descendants of a protected attribute.
- **Individual, not average, criterion.** Average causal effects can be non-zero even when a predictor is counterfactually fair.

## References

### Seminal papers

- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). Counterfactual Fairness. *Advances in Neural Information Processing Systems 30*. https://arxiv.org/abs/1703.06856 — Defines counterfactual fairness and presents it as a framework based on causal inference, with a law-school case study.
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*, 214–226. https://doi.org/10.1145/2090236.2090255 — The individual-level criterion that counterfactual fairness is often compared with.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Group-based criteria, against which the causal approach is contrasted.

### Surveys and textbooks

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — A survey of sources of bias and of the fairness definitions used to measure it.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free online textbook covering fairness definitions and their assumptions.
