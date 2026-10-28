---
status: complete
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

Require that the decision's error rates, both the rate of correctly flagged positives and the rate of incorrectly flagged negatives, do not depend on group membership. Hardt et al. show that a learned predictor can be adjusted after training to meet this condition. The adjusted decision is a function of the prediction and the protected attribute only, and finding the best such decision is a linear program when the prediction is binary. When the prediction is a real-valued score, equalised odds can require randomised group-specific thresholds, which the authors optimise numerically. Equal opportunity needs only deterministic group-specific thresholds.

## Equation

With protected attribute \(A\), true outcome \(Y\), and prediction \(\hat{Y}\), equalised odds holds when

\[
\Pr[\hat{Y}=1 \mid Y=y, A=a] = \Pr[\hat{Y}=1 \mid Y=y, A=b] \quad \text{for } y \in \{0,1\} \text{ and all groups } a, b.
\]

Equal opportunity is the weaker requirement that only the true-positive rate, for \(y=1\), be equal.

## Results

Hardt et al. (2016) use a credit-default case study with a sample of 301,536 TransUnion TransRisk scores from 2003, a fixed 82/18 cost ratio and a 620 cutoff. They report the fraction of maximum profit that each rule attains at an 82% non-default threshold:

| Rule | Fraction of maximum profit |
|---|---|
| Race blind | 99.3% |
| Equal opportunity | 92.8% |
| Equalised odds | 80.2% |
| Demographic parity | 69.8% |

The authors conclude that equal opportunity costs less than a quarter of what demographic parity costs. The comparison is one case study with a single score and a single cost ratio.

## Limitations

- **Base rates.** When base rates differ, equalised odds cannot hold together with calibration within groups (Chouldechova, 2017; Kleinberg et al., 2017).
- **Post-processing cost.** Group-specific thresholds lower the profit or accuracy of the decision, and the adjusted rule needs the protected attribute at decision time.
- **Not proof of fairness.** The paper states that satisfying the criterion, or any other criterion that uses only the joint statistics, "should not be considered a conclusive proof of fairness". Two causal scenarios with identical joint statistics cannot be told apart by such a test.
- **Labels.** The criterion assumes the true outcome is measured correctly. The authors note that the target may itself be unreliable or biased, so equal error rates against a biased label are a weaker guarantee.
- **Finite samples.** The analysis assumes the joint distribution is known. Estimation from finite samples is not covered.

## References

### Seminal papers

- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines equalised odds and equal opportunity and gives a post-processing method to achieve them.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that, when prevalence differs across groups, a score with equal precision cannot also have equal false-positive and false-negative rates. The paper's example is the COMPAS recidivism score.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://doi.org/10.4230/LIPIcs.ITCS.2017.43 — Proves that calibration within groups and the two balance conditions cannot hold together, except with perfect prediction or equal base rates.

### Surveys and textbooks

- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. & Galstyan, A. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*, 54(6), 1–35. https://doi.org/10.1145/3457607 — A survey of sources of bias and of the fairness definitions used to measure it.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free online textbook covering error-rate criteria and their trade-offs.
