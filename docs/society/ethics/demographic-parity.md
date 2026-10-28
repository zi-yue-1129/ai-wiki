---
status: complete
last_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - bias
aliases:
  - 人口統計均等
  - 統計均等
  - Demographic parity
  - Statistical parity
---

# Demographic parity

!!! info "Part of Fairness definitions"
    This method page belongs to [Fairness definitions and impossibility results](fairness-definitions.md). It explains the criterion in detail; the parent page compares it with the others.

Demographic parity requires that a classifier give positive decisions at the same rate in every group defined by a protected attribute. It is the simplest group criterion, and it is closely tied to the legal notion of disparate impact. Feldman et al. (2015) connected disparate impact to the information a classifier leaks about the protected attribute.

## Problem

A decision process can produce very different outcomes for different groups even if no one intends it. The problem is to define a measurable standard for those outcomes, and to say when a rate difference counts as disparate impact.

## Core idea

Choose a decision rule and compare its positive-decision rates across groups. If the rates are equal, demographic parity holds. The criterion ignores the true outcome, so it measures how decisions are distributed, not whether they are correct.

## Equation

With protected attribute \(A\) and prediction \(\hat{Y}\), demographic parity holds when

\[
\Pr[\hat{Y}=1 \mid A=a] = \Pr[\hat{Y}=1 \mid A=b] \quad \text{for all groups } a, b.
\]

## Results

- **Disparate impact and leakage.** Feldman et al. (2015) adopt a generalised four-fifths rule, under which a data set has disparate impact when the ratio of positive-decision rates is at most τ = 0.8. They show that a data set admits disparate impact if and only if the protected attribute can be predicted from the non-protected features with balanced error rate at most 1/2 − β/8, where β is the fraction of the protected group that is selected. They also give a repair that moves non-protected values toward a median distribution within each group, with a parameter λ controlling how much repair is applied.
- **Cost of the constraint.** Corbett-Davies et al. (2017) study pretrial detention decisions in Broward County, Florida, with 30% of defendants detained (100 random train–test splits). Enforcing statistical parity makes 17% of the detained defendants relatively low risk. The authors estimate that this leads to a 9% increase in violent recidivism among released defendants, compared with a rule that maximises public safety alone. The predictive-equality constraint gives 14% and 7%, and conditional statistical parity gives 10% and 4%.

## Limitations

- **Ignores accuracy.** Equal decision rates can be reached by accepting less accurate decisions for some groups. The Broward County figures above are the empirical version of this trade-off.
- **Base rates.** Kleinberg et al. (2017) and Chouldechova (2017) show that calibration and error-rate criteria cannot all hold together when base rates differ. Demographic parity is not one of the conditions in those theorems, so they do not settle its compatibility with them directly.
- **Group choice.** The result depends on which groups are defined and how they are defined.

## References

### Seminal papers

- Feldman, M., Friedler, S. A., Moeller, J., Scheidegger, C. & Venkatasubramanian, S. (2015). Certifying and Removing Disparate Impact. *Proceedings of KDD 2015*, 259–268. https://doi.org/10.1145/2783258.2783311 — Links disparate impact to the information a classifier reveals about the protected attribute, and describes a repair that removes it.
- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). Fairness through awareness. *Proceedings of ITCS 2012*, 214–226. https://doi.org/10.1145/2090236.2090255 — Introduces individual fairness, which is often contrasted with group criteria.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines equalised odds and equal opportunity from the joint statistics of predictor, target and attribute, and gives a post-processing method.
- Corbett-Davies, S., Pierson, E., Feller, A., Goel, S. & Huq, A. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*, 797–806. https://doi.org/10.1145/3097983.3098095 — Measures the cost to public safety of imposing fairness constraints on a risk-based decision.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — Shows that calibration within groups and two balance conditions can hold together only with perfect prediction or equal base rates.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that, when prevalence differs across groups, a score with equal precision cannot also have equal false-positive and false-negative rates.

### Surveys and textbooks

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — A survey of sources of bias and of the fairness definitions used to measure it.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free online textbook covering group criteria and their trade-offs.

## Further learning

- [Fairlearn](https://fairlearn.org/) — open-source toolkit with the demographic parity metric and mitigation methods.
