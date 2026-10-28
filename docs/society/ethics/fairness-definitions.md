---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/evaluation-and-validation
  - applications/law
  - applications/healthcare
tags:
  - fairness
  - evaluation
aliases:
  - 公平性定義
  - 公平性的不可能性結果
  - 人口統計均等
  - 機會均等化
  - 校準
  - Demographic parity
  - Equalised odds
  - Impossibility theorem
---

# Fairness Definitions and Impossibility Results

A fairness definition is a precise rule for when a classifier or score treats people equitably. Several natural definitions cannot all hold at once when the groups being compared have different base rates, so choosing one is a value judgement as well as a technical decision.

## Overview

Once bias has been diagnosed (see [Ethics & Fairness](index.md)), a developer still has to say what "fair" means in a formula. Proposed answers often disagree. Results from 2016 and 2017 showed that the disagreement is not only a matter of taste: under common conditions, the main criteria are mathematically incompatible.

The definitions build on the error rates and calibration measures in [Evaluation and Validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md). They matter most for risk scores in criminal justice, credit, health and hiring.

## Key concepts

- **Protected attribute** ($A$): a characteristic such as race or sex, on which decisions are restricted.
- **Outcome** ($Y$), **prediction** ($\hat{Y}$) and **score** ($S$): the true target, the decision, and the risk value it is based on.
- **Base rate**: the share of positive cases in a group, $P(Y=1 \mid A=a)$.
- **True and false positive rates**: the share of actual positives flagged, and of actual negatives wrongly flagged.
- **Calibration**: a score of $s$ corresponds to the same probability of a positive outcome whatever the person's group.

## How it works

Each definition is a constraint on the joint distribution of the protected attribute, the prediction or score, and the true outcome. Most describe statistics across groups, so a system can meet one and still treat particular people badly. That is why individual definitions also exist.

Constraints can often be imposed after training. Hardt, Price and Srebro (2016) show how to adjust a learned predictor to satisfy their criterion. Corbett-Davies et al. (2017) find that, for several definitions, the optimal rule uses a different threshold for each group, at a cost to public safety.

### Impossibility results

Kleinberg, Mullainathan and Raghavan (2016) formalise three conditions for a score: calibration within each group, and balance for the positive and negative classes. They prove that these cannot hold together except in highly constrained special cases, namely equal base rates or a perfect predictor. Chouldechova (2017) reaches a parallel result with false positive rate (FPR), false negative rate (FNR) and positive predictive value (PPV). For any group these are linked by an identity:

$$\mathrm{FPR} = \frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot(1-\mathrm{FNR})$$

where $p$ is the group's base rate. If two groups have equal PPV and equal FNR but different $p$, their false positive rates must differ. This is the formal core of the public debate over the COMPAS recidivism tool, where the same scores were defended and criticised by different criteria.

## Key methods

The table compares the main definitions. Each is a constraint, and each has a characteristic weakness.

| Definition | Requirement | Main weakness |
|---|---|---|
| Demographic parity | $P(\hat{Y}=1 \mid A=a)$ is equal for every group | Ignores the true outcome, so it may force extra false positives in one group |
| Equal opportunity (Hardt et al., 2016) | Equal true positive rates, $P(\hat{Y}=1 \mid Y=1, A=a)$ | Says nothing about false positives |
| Equalised odds (Hardt et al., 2016) | Equal true and false positive rates across groups | Incompatible with calibration when base rates differ |
| Calibration and predictive parity | $P(Y=1 \mid S=s, A=a) = s$, or equal PPV | Incompatible with equal error rates when base rates differ |
| Individual fairness (Dwork et al., 2012) | Similar individuals receive similar outcomes, under a similarity metric | The metric encodes a value choice |
| Counterfactual fairness (Kusner et al., 2017) | The decision is unchanged in a counterfactual world where $A$ differs | Depends on a causal model that must be argued for |

Demographic parity and equalised odds also conflict when a classifier has some skill and base rates differ: equal error rates then make the gap in positive-prediction rates proportional to the gap in base rates.

### Fairness through unawareness

Removing the protected attribute from the inputs is the simplest rule and the one most often proposed. It is often insufficient, because other features, such as postcode, can carry the same information. Lipton, Chouldechova and McAuley (2018) show that when other features correlate with group membership, a learning process that is blind to the attribute at test time can still implement treatment disparity. Counterfactual fairness tackles this by asking how the decision would change if the attribute were different.

### Choosing between definitions

No definition is neutral. The choice starts with what counts as the harm: a person wrongly denied, a person wrongly flagged, or a score that means different things for different groups. Where the base rates come from matters too. If they reflect past discrimination, equal outcomes and equal errors may pull apart. Friedler, Scheidegger and Venkatasubramanian (2021) argue that the appropriate mechanism depends on the value system behind it. Mitchell et al. (2021) list the assumptions that prediction-based decisions usually hide. A practical route is to name the harm, pick the matching criterion, measure the cost, and record the decision so it can be challenged.

## Connections

- **Evaluation.** The fairness criteria are conditions on the error rates and calibration measures in [Evaluation and Validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md), split by group.
- **Ethics.** The sources of bias, such as proxy targets and historical data, are described in [Ethics & Fairness](index.md). This page covers the formal side.
- **Privacy.** Auditing for fairness needs the protected attribute, but privacy rules may restrict its collection. See [Privacy and Data Protection](../privacy/index.md).
- **Brain and mind.** Base-rate neglect, underweighting how common a category is when judging a case, is a classic bias of human judgement, so human decision-makers face the same base-rate problem. See [heuristics and biases](../../brain-mind/cognitive-science/heuristics-and-biases/index.md).

## Applications

- **Criminal justice.** Risk assessment is the best-studied case: Chouldechova (2017) shows why the same scores can satisfy one criterion and fail another.
- **Health.** Obermeyer et al. (2019) found that a widely used algorithm gave Black patients the same risk level as sicker White patients. The fault lay in its proxy target, past health spending.
- **Law.** Several legal systems distinguish intentional treatment of a group from outcomes that fall unevenly under a neutral rule. The statistical definitions relate more closely to the second. See [Law](../../applications/law/index.md).

## Open questions

- Can one definition be justified across decisions, or should the criterion depend on the harm?
- How should base rates that reflect past injustice be treated: as facts to predict from, or as outcomes to correct?
- Auditing needs the protected attribute, yet privacy rules often limit its collection.

## References

### Seminal papers

- Dwork, C., Hardt, M., Pitassi, T., Reingold, O. & Zemel, R. (2012). *Fairness Through Awareness*. arXiv preprint. https://arxiv.org/abs/1104.3913 — Defines individual fairness via a task-specific similarity metric, and links statistical parity to affirmative action.
- Hardt, M., Price, E. & Srebro, N. (2016). *Equality of Opportunity in Supervised Learning*. arXiv preprint. https://arxiv.org/abs/1610.02413 — Introduces equal opportunity and equalised odds, and how to adjust predictors to meet them.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2016). *Inherent Trade-Offs in the Fair Determination of Risk Scores*. arXiv preprint. https://arxiv.org/abs/1609.05807 — Proves that calibration and two balance conditions cannot hold together except in special cases.
- Chouldechova, A. (2017). Fair prediction with disparate impact: A study of bias in recidivism prediction instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 — Shows that false positive rate, false negative rate and positive predictive value cannot all be equal when prevalence differs.
- Kusner, M. J., Loftus, J., Russell, C. & Silva, R. (2017). *Counterfactual Fairness*. arXiv preprint. https://arxiv.org/abs/1703.06856 — Defines counterfactual fairness using causal inference, comparing decisions in actual and counterfactual worlds.
- Lipton, Z. C., Chouldechova, A. & McAuley, J. (2018). *Does mitigating ML's impact disparity require treatment disparity?* arXiv preprint. https://arxiv.org/abs/1711.07076 — Shows that group-blind learning can still implement treatment disparity when other features correlate with group.
- Corbett-Davies, S., Pierson, E., Feller, A., Goel, S. & Huq, A. (2017). Algorithmic decision making and the cost of fairness. arXiv preprint. https://arxiv.org/abs/1701.08230 — Shows that several fairness constraints require race-specific thresholds and cost public safety.
- Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 — Traces racial bias in a health-management algorithm to its choice of proxy target.

### Surveys and textbooks

- Mitchell, S., Potash, E., Barocas, S., D'Amour, A. & Lum, K. (2021). Algorithmic Fairness: Choices, Assumptions, and Definitions. *Annual Review of Statistics and Its Application*. https://doi.org/10.1146/annurev-statistics-042720-125902 — Catalogues fairness definitions and the assumptions behind prediction-based decisions.
- Friedler, S. A., Scheidegger, C. & Venkatasubramanian, S. (2021). The (Im)possibility of fairness. *Communications of the ACM*. https://doi.org/10.1145/3433949 — Argues that the appropriate fairness mechanism depends on the value system adopted.
