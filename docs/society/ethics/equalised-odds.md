---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - bias
  - error rates
aliases:
  - 機會均衡
  - 等化勝算
  - Equalised odds
  - Equalized odds
---

# Equalised odds

!!! info "Part of Fairness definitions"
    This method page belongs to [Fairness definitions and impossibility results](fairness-definitions.md). It explains the criterion in detail; the parent page compares it with the others.

Equalised odds requires that a classifier have the same true-positive rate and the same false-positive rate in every group. It conditions on the true outcome, so it asks whether a model makes the same kinds of mistakes for different groups. Hardt, Price and Srebro (2016) defined it and gave a method for achieving it after training.

## Problem

Decision rules can look fair on average while giving some groups more false accusations or more missed cases. The problem is to define fairness in terms of errors, not just decision rates, and to show that a predictor can be adjusted to meet it.

## Core idea

Require that the decision's error rates, both the rate of correctly flagged positives and the rate of incorrectly flagged negatives, do not depend on group membership. The paper shows that one can adjust any learned predictor, using group-specific thresholds, so that it satisfies this criterion.

## Equation

With protected attribute \(A\), true outcome \(Y\), and prediction \(\hat{Y}\), equalised odds holds when

\[
\Pr[\hat{Y}=1 \mid Y=y, A=a] = \Pr[\hat{Y}=1 \mid Y=y, A=b] \quad \text{for } y \in \{0,1\} \text{ and all groups } a, b.
\]

Equal opportunity is the weaker requirement that only the true-positive rate, for \(y=1\), be equal.

## Results

Hardt et al. (2016) show how to optimally adjust a learned predictor to remove discrimination according to their definition, and they note that the criterion depends only on the joint statistics of the predictor, the target and the protected attribute.

## Limitations

- **Base rates.** When base rates differ, equalised odds cannot hold together with calibration within groups (Chouldechova, 2017; Kleinberg et al., 2017).
- **Post-processing cost.** Group-specific thresholds lower accuracy for some groups and require the protected attribute at decision time.
- **Labels.** The criterion assumes the true outcome is measured correctly; biased labels make equal error rates a weaker guarantee.

## References

### Seminal papers

- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines equalised odds and equal opportunity and gives a post-processing method to achieve them.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that equal error rates cannot hold together with predictive parity when prevalence differs across groups.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — Proves that the three fairness conditions cannot be satisfied together, except in special cases.

### Surveys and textbooks

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — A survey of fairness definitions, as its title states.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook covering error-rate criteria and their trade-offs.
