---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - applications/healthcare
  - applications/law
tags:
  - bias
  - fairness
  - audits
  - case studies
aliases:
  - 演算法偏見案例
  - 算法偏見案例研究
  - Algorithmic bias case studies
  - COMPAS
  - Gender Shades
---

# Case studies in algorithmic bias

Several deployed systems have been studied closely enough to show how bias arises, how it is measured, and how the measurement itself can be contested. This page reviews four well-documented cases, one of which concerns language models. For each, it asks what was measured, what the dispute was about, and what the case taught the field. The cases are useful because they are concrete; the mathematics of fairness is treated in [Fairness definitions](fairness-definitions.md).

## Overview

Bias cases share a common structure. A system is built to predict or rank something, the training data reflect past decisions or uneven sampling, and the system is then evaluated on a metric that does not capture the harm to some group. The disagreement afterwards is often about the metric, not only about the system. A case study therefore asks two questions: what did the system get wrong for whom, and by what standard was that judged?

## Key concepts

- **Disparate error rates**: a model makes more mistakes for one group than for another, which may or may not be the same as unequal treatment.
- **Proxy target**: a measurable variable that stands in for the quantity of interest. When the proxy differs in meaning across groups, the model inherits that difference.
- **Audit**: an evaluation of a deployed system by an outside party, using a defined set of groups and metrics. Audits depend on access and on the groups chosen.

## Case 1: Recidivism risk scores (COMPAS)

COMPAS is a commercial tool that estimates the risk that a defendant will be rearrested, and it was used in several US jurisdictions to inform bail and sentencing decisions. In 2016 journalists analysed its scores against two years of outcomes in Broward County, Florida, and reported higher false-positive rates for Black defendants than for white defendants. The developer disputed the analysis.

Chouldechova (2017) analysed this kind of instrument formally. She shows that these fairness criteria cannot all be satisfied simultaneously when recidivism prevalence differs across groups, and applies this to recidivism instruments of the kind at issue. The dispute was therefore not necessarily a simple error in either analysis. Each side had chosen a different fairness criterion, and the criteria cannot all hold. This is the main lesson of the case, and the reason [fairness definitions](fairness-definitions.md) matter in practice.

## Case 2: Gender classification (Gender Shades)

Buolamwini and Gebru (2018) built a benchmark balanced across skin type and gender, and tested three commercial gender classification systems on it. The abstract reports error rates of up to 34.7% for darker-skinned women, against a maximum error rate of 0.8% for lighter-skinned men.

Raji and Buolamwini (2019) study the impact of publicly naming biased performance results of commercial AI products, which is the follow-up question this case raises.

## Case 3: Health risk scores

Obermeyer et al. (2019) studied a widely used algorithm in the US health care system that identifies patients for extra care. The algorithm predicted future health costs, and used costs as a proxy for health need. Because less money had been spent on Black patients with the same level of illness, at a given risk score Black patients were considerably sicker than white patients. The authors report that reformulating the algorithm so that it no longer uses costs as a proxy for needs reduces the racial bias.

The case shows that a model can be accurate for its stated target and still be biased, because the target itself carries a history of unequal access to care. It is a measurement-bias case rather than a data-volume case.

## Case 4: Language-model stereotypes and dialect bias

Large language models reproduce stereotypes present in their training text. Bender et al. (2021) discuss the risks of very large language models, as the title states. Hofmann et al. (2024) study dialect. Their preprint reports that language models hold covert stereotypes about speakers of African American English that are more negative than any human stereotypes recorded experimentally, and links them to decisions about employability and criminality.

## What the cases taught

- **Measure per group, and say which groups.** Aggregate accuracy hides the failures that matter.
- **Check the target.** A proxy label can encode the inequality the model is supposed to avoid.
- **Expect conflicting metrics.** Different parties can be correct about different criteria.
- **Public naming is one accountability mechanism.** Whether publicly naming biased results changes products is the question Raji and Buolamwini (2019) investigate.

## Connections

The cases use the fairness criteria in [Fairness definitions](fairness-definitions.md) and the bias sources listed in [Ethics & Fairness](index.md). The audit side is discussed further in [Algorithmic auditing and impact assessment](algorithmic-auditing.md). Health and legal applications appear in [Healthcare](../../applications/healthcare/index.md) and [Law](../../applications/law/index.md).

## Applications

- Auditing commercial systems before and after deployment.
- Choosing evaluation groups and metrics when a system is procured.
- Designing benchmarks for dialect and language variety.

## Open questions

- **Who decides the target and the groups?** Most cases turn on choices made by the developer or the auditor, and these choices are not neutral.
- **Do language-model biases generalise?** Covert dialect bias has been shown for particular models and tasks; how far the result extends across systems is an active question.
- **How much does an audit change behaviour?** Raji and Buolamwini (2019) investigate the impact of publicly naming biased results, and the wider effect of audits is still an open question.

## References

### Seminal papers

- Buolamwini, J. & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency (PMLR 81)*. https://proceedings.mlr.press/v81/buolamwini18a.html — Audits three commercial gender classifiers across skin type and gender and reports large gaps in error rates.
- Raji, I. D. & Buolamwini, J. (2019). Actionable Auditing: Investigating the Impact of Publicly Naming Biased Performance Results of Commercial AI Products. *Proceedings of AIES 2019*. https://doi.org/10.1145/3306618.3314244 — Examines the impact of publicly naming biased performance results of commercial AI products.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*, 5(2), 153–163. https://doi.org/10.1089/big.2016.0047 — Shows that fairness criteria cannot all be satisfied when recidivism prevalence differs across groups.
- Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*, 366, 447–453. https://doi.org/10.1126/science.aax2342 — Shows that a cost-based proxy target produced racial bias in a widely used health-management algorithm, and that changing the target reduced it.
- Bender, E. M., Gebru, T., McMillan-Major, A. & Shmitchell, S. (2021). On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? *Proceedings of FAccT 2021*. https://doi.org/10.1145/3442188.3445922 — Discusses the risks of very large language models, as its title states.
- Hofmann, V., Kalluri, P. R., Jurafsky, D. & King, S. (2024). AI generates covertly racist decisions about people based on their dialect. *Nature*, 633, 147–154. https://doi.org/10.1038/s41586-024-07856-5 — Reports covert dialect prejudice in language models, with stereotypes more negative than recorded human stereotypes.

### Surveys and textbooks

- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Free textbook with worked examples of the cases above and the fairness criteria they illustrate.

## Further learning

- Angwin, J. et al. (2016). Machine Bias. *ProPublica*. https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing — Journalistic account of the COMPAS analysis and the company's response; read alongside Chouldechova (2017).
