---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - applications/law
tags:
  - fairness
  - bias
  - impossibility results
aliases:
  - 公平性定義
  - 公平性不可能性定理
  - Fairness definitions
  - Impossibility of fairness
---

# Fairness definitions and impossibility results

A fairness definition is a precise mathematical statement of what it means for a classifier or score to treat groups or individuals equitably. Several natural definitions exist, and for real-world data they generally cannot all be satisfied at once. This page compares the main definitions, explains the impossibility results that limit them, and describes how the choice between them is a question of values as much as of mathematics.

## Overview

Suppose a model predicts whether a loan will be repaid, whether a defendant will reoffend, or whether a patient needs extra care. The model's outputs can differ across groups defined by a protected attribute such as sex, race or age. Fairness definitions give a way to state, exactly, what "equal treatment" should mean in that setting. Each definition encodes a different intuition, and the impossibility results show that some intuitions conflict whenever the groups have different base rates of the outcome.

## Key concepts

- **Protected attribute** \(A\): the group membership a definition is meant to protect, such as sex or ethnicity.
- **Outcome** \(Y\) and **prediction** \(\hat{Y}\): the true label and the model's decision.
- **Score** \(S\): a predicted probability or risk value, before a threshold is applied.
- **Base rate**: the share of positive outcomes in a group, \(\Pr[Y=1 \mid A=a]\). Base rates often differ across groups because of differences in the underlying data-generating process.
- **Group versus individual fairness**: group definitions compare statistics across groups; individual definitions require that similar people receive similar outcomes.

## How it works

The table below gives the main criteria. Each one is a constraint on the joint distribution of \(A\), \(Y\), \(\hat{Y}\) or \(S\).

| Criterion | Condition | Intuition |
|---|---|---|
| Demographic parity | \(\Pr[\hat{Y}=1 \mid A=a]\) is equal for all groups \(a\) | Equal rates of positive decisions |
| Equal opportunity | \(\Pr[\hat{Y}=1 \mid Y=1, A=a]\) is equal for all \(a\) | Equal true-positive rates |
| Equalised odds | Equal true-positive and false-positive rates for all \(a\) | Equal error rates for both outcomes |
| Predictive parity | \(\Pr[Y=1 \mid \hat{Y}=1, A=a]\) is equal for all \(a\) | Equal precision of positive decisions |
| Calibration within groups | \(\Pr[Y=1 \mid S=s, A=a] = s\) for all \(a\) and \(s\) | A score of \(s\) means the same risk in every group |
| Individual fairness | Similar individuals receive similar outputs, under a task-specific similarity metric | Treat like cases alike |
| Counterfactual fairness | The prediction is unchanged in a model where \(A\) is set to another value, with the causal effects of \(A\) on other variables held fixed | Remove the causal influence of \(A\) |
| Fairness through unawareness | \(\hat{Y}\) does not use \(A\) directly | Drop the protected attribute |

**Individual fairness.** Dwork et al. (2012) require that the distance between two output distributions be at most the distance between the two individuals under a similarity metric. The metric must be chosen by someone, which is the hard part.

**Equalised odds and equal opportunity.** Hardt, Price and Srebro (2016) define equalised odds and its weaker form, equal opportunity, and show how to build post-processing rules that meet them, using group-specific thresholds applied to a fixed score.

**Fairness through unawareness.** Removing \(A\) from the inputs is the simplest policy, but other features (postcode, education, purchase history) can act as proxies. Hardt et al. (2016) and Dwork et al. (2012) both note that a model can discriminate without ever seeing the protected attribute.

### Impossibility results

Two results show that the main group criteria conflict when base rates differ and the predictor is not perfect.

- **Kleinberg, Mullainathan and Raghavan (2016)** show that three conditions cannot hold together: calibration within groups, balance for the positive class (equal average scores for true positives across groups), and balance for the negative class. Their abstract states that, except in highly constrained special cases, no method can satisfy the three conditions simultaneously.
- **Chouldechova (2017)** shows, for binary predictions, that predictive parity, equal false-positive rates and equal false-negative rates cannot all hold when base rates differ. She applies this result to the risk instruments studied in the COMPAS debate.

The practical consequence is that a model can be calibrated and still have unequal error rates, or it can have equal error rates and unequal precision. Choosing between these outcomes is a choice about which harm matters more.

### Costs of enforcing a criterion

Corbett-Davies et al. (2017) study the cost of imposing fairness constraints on a risk-based decision rule. They reformulate fairness as constrained optimisation, maximising public safety subject to fairness constraints, and show that for several past definitions of fairness the resulting algorithms come at a cost to public safety. The point for practitioners is that a fairness constraint is a policy with measurable side effects, not a free adjustment.

## Key methods

The criteria above are compared in the table. Each is a condition that a model is checked against, not an algorithm. The main ways of enforcing them are:

- **Pre-processing**: reweight or resample training data so that the base rates or feature distributions are more balanced.
- **In-processing**: add a fairness penalty or constraint to the training objective.
- **Post-processing**: adjust decisions after training, typically with group-specific thresholds, as in Hardt et al. (2016).

Each enforcement method trades one criterion against accuracy or against another criterion, so the choice of definition should come first.

## Connections

The definitions connect to the wider ethics discussion in [Ethics & Fairness](index.md), where the sources of bias are listed. They also connect to [Bias case studies](bias-case-studies.md), where the impossibility results explain why audits of the same system can reach opposite conclusions. Legal frameworks for non-discrimination define outcomes rather than mathematical criteria, so translating a legal test into one of these definitions requires judgement; see [Law, Policy & Governance](../governance/index.md).

On the machine-learning side, the definitions are the target of fairness toolkits such as Fairlearn and AIF360, which implement several criteria and mitigation methods.

## Applications

- **Credit and lending**: lenders compare error rates and approval rates across groups, which can involve several criteria at once.
- **Criminal justice risk assessment**: the COMPAS dispute is the standard example of calibration and error-rate criteria pointing in different directions.
- **Health risk scores**: differences in the target variable (costs rather than needs) can break equal-opportunity criteria even when the model is accurate for its stated target.

## Open questions

- **Which criterion should apply?** The impossibility results make this a value choice. Law and regulation often define discrimination by outcomes, which may not match any single statistical definition.
- **How to define the similarity metric** for individual fairness, and who should set it.
- **Intersectional groups**: a criterion satisfied for each attribute separately need not hold for their combinations.
- **Measurement error and label bias**: the criteria assume the labels are correct; when labels are themselves biased, equal error rates can hide unequal harm.

## References

### Seminal papers

- Dwork, C. et al. (2012). Fairness through awareness. *Proceedings of ITCS 2012*. https://doi.org/10.1145/2090236.2090255 — Introduces individual fairness as a Lipschitz condition on a task-specific similarity metric.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. *Advances in Neural Information Processing Systems 29*. https://arxiv.org/abs/1610.02413 — Defines equal opportunity and equalised odds and gives a post-processing method to achieve them.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2017). Inherent Trade-Offs in the Fair Determination of Risk Scores. *Proceedings of ITCS 2017*. https://arxiv.org/abs/1609.05807 — Proves that calibration and balance conditions cannot hold together when base rates differ.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that predictive parity and error-rate balance are incompatible under unequal base rates, using recidivism tools as the case.
- Corbett-Davies, S., Pierson, E., Feller, A. & Goel, S. (2017). Algorithmic Decision Making and the Cost of Fairness. *Proceedings of KDD 2017*. https://doi.org/10.1145/3097983.3098095 — Reformulates fairness as constrained optimisation of public safety, using pretrial detention decisions.

### Surveys and textbooks

- Verma, S. & Rubin, J. (2018). Fairness Definitions Explained. *Proceedings of the International Workshop on Software Fairness*. https://doi.org/10.1145/3194770.3194776 — Surveys and compares the main fairness definitions on one running example.
- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook covering these definitions, their trade-offs and their social context.

## Further learning

- [Fairlearn](https://fairlearn.org/) — open-source toolkit with fairness metrics and mitigation algorithms.
- [AI Fairness 360](https://aif360.res.ibm.com/) — IBM's open-source library of fairness metrics and algorithms.
