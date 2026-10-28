---
status: complete
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

Partition people by their score and check, within each group, how often the outcome occurs at each score level. Calibration within groups holds when, for every group and every score bin, the share of the group's members in the bin who belong to the positive class matches the bin's score. Kleinberg et al. state this as one of three conditions, the other two being balance for the positive class and balance for the negative class.

## Equation

For score \(S\) and protected attribute \(A\), calibration within groups holds when

\[
\Pr[Y=1 \mid S=s, A=a] = s \quad \text{for all scores } s \text{ and all groups } a.
\]

## Results

Kleinberg et al. (2017) prove that if a risk assignment satisfies all three conditions, then the instance must allow perfect prediction or the two groups must have the same base rate. Calibration within groups therefore cannot hold together with both balance conditions when base rates differ, except in these special cases.

Chouldechova (2017) studies recidivism prediction instruments, including COMPAS. When prevalence differs across groups, a score with equal positive predictive value (predictive parity) cannot also have equal false-positive and false-negative rates. Her result is about error rates and precision, so it does not state the calibration condition above directly.

## Limitations

- **Score balance versus error rates.** The impossibility result concerns the two score-balance conditions, not the error rates of a thresholded decision. Calibrated scores can still produce unequal false-positive and false-negative rates when base rates differ, so equal error rates need a separate check.
- **Score meaning.** Calibration says nothing about the decisions taken at a threshold; a calibrated score can still lead to unequal decisions.
- **Data needs.** Checking calibration within small groups needs enough outcome data at each score level.

## References

### Seminal papers

- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — Proves that calibration within groups and two balance conditions cannot hold together under unequal base rates, except with perfect prediction.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that, when prevalence differs across groups, a score with equal precision cannot also have equal false-positive and false-negative rates.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines error-based criteria that contrast with calibration.

### Surveys and textbooks

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — A survey of sources of bias and of the fairness definitions used to measure it.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free online textbook covering calibration and its trade-offs with other criteria.
