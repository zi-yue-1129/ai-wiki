---
status: draft
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

Feldman et al. (2015) link the legal notion of disparate impact to a measure of how much the classifier's output reveals the protected attribute, and they describe ways to make the data less biased.

## Limitations

- **Ignores accuracy.** Equal rates can be achieved by accepting less accurate predictions for some groups, and Corbett-Davies et al. (2017) show that constraints of this kind have a cost.
- **Base rates.** When the true outcome rates differ across groups, equal decision rates conflict with calibration and error-rate criteria (Kleinberg et al., 2017; Chouldechova, 2017).
- **Group choice.** The result depends on which groups are defined and how.

## References

### Seminal papers

- Feldman, M., Friedler, S. A., Moeller, J., Scheidegger, C. & Venkatasubramanian, S. (2015). Certifying and Removing Disparate Impact. *Proceedings of KDD 2015*. https://doi.org/10.1145/2783258.2783311 — Links disparate impact to the information a classifier reveals about the protected attribute, and describes ways to remove it.
- Dwork, C. et al. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — Introduces individual fairness, which is often contrasted with group criteria.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines a criterion based on the joint statistics of predictor, target and attribute, and a post-processing method.
- Corbett-Davies, S., Pierson, E., Feller, A. & Goel, S. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*. https://doi.org/10.1145/3097983.3098095 — Analyses the cost to public safety of imposing fairness constraints on a risk-based decision.
- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — A survey of fairness definitions, as its title states.

## Further learning

- [Fairlearn](https://fairlearn.org/) — open-source toolkit with the demographic parity metric and mitigation methods.
