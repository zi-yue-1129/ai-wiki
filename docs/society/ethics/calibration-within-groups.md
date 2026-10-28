---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
tags:
  - fairness
  - calibration
  - risk scores
aliases:
  - 群體內校準
  - Calibration within groups
  - Calibration
---

# Calibration within groups

!!! info "Part of Fairness definitions"
    This method page belongs to [Fairness definitions and impossibility results](fairness-definitions.md). It explains the criterion in detail; the parent page compares it with the others.

Calibration within groups requires that a risk score mean the same thing in every group: among people given a score of \(s\), the same proportion should have the outcome whatever their group. It is one of the three conditions in Kleinberg, Mullainathan and Raghavan's impossibility result.

## Problem

A score that is well calibrated overall can still be systematically too high for one group and too low for another. The problem is to state precisely what it means for a score to be equally trustworthy for every group, and to know when that property can be met together with other fairness criteria.

## Core idea

Partition people by their score and check, within each group, how often the outcome occurs at each score level. Calibration within groups holds when the observed rate at each score matches the score itself for every group.

## Equation

For score \(S\) and protected attribute \(A\), calibration within groups holds when

\[
\Pr[Y=1 \mid S=s, A=a] = s \quad \text{for all scores } s \text{ and all groups } a.
\]

## Results

Kleinberg et al. (2017) show that calibration within groups cannot hold together with balance for the positive and the negative class, except in highly constrained special cases. Chouldechova (2017) shows, for binary predictions, that calibration-type criteria conflict with error-rate balance when recidivism prevalence differs across groups.

## Limitations

- **Error-rate conflict.** Calibration within groups cannot be combined with equal error rates when base rates differ, so a calibrated tool can still produce unequal false-positive rates.
- **Score meaning.** Calibration says nothing about the decisions taken at a threshold; a calibrated score can still lead to unequal decisions.
- **Data needs.** Checking calibration within small groups needs enough outcome data at each score level.

## References

### Seminal papers

- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — Proves that calibration within groups and two balance conditions cannot hold together under unequal base rates.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that fairness criteria, including predictive parity, cannot all hold when prevalence differs.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines error-based criteria that contrast with calibration.

### Surveys and textbooks

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — A survey of fairness definitions, as its title states.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook covering calibration and its trade-offs with other criteria.
