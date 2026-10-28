---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - society/human-ai-interaction
tags:
  - auditing
  - documentation
  - accountability
  - regulation
aliases:
  - 演算法稽核
  - 演算法審計
  - 影響評估
  - Algorithmic auditing
  - Model cards
  - Datasheets
---

# Algorithmic auditing and impact assessment

Algorithmic auditing is the systematic evaluation of an AI system, or of the organisation that builds and deploys it, against defined criteria such as accuracy across groups, safety, or legal compliance. Impact assessment is the related practice of anticipating who a system will affect and how, before or during deployment. Both depend on documentation, because an auditor can only test what is described and can only check what is accessible. This page covers the main kinds of audit, the documentation artefacts that support them, and the regulatory duties that now require some of them.

## Overview

A model that performs well on a benchmark can still fail for particular users, in particular settings, or after it is put into a new use. Audits try to answer whether the system does what its providers say, for whom it does so, and what can go wrong. Impact assessments ask the same questions earlier, with a wider view that includes the people affected and the institutions that will use the output.

## Key concepts

- **Internal audit**: an evaluation run by the developing organisation, usually with teams separate from the product group.
- **External audit**: an evaluation by a party outside the organisation, which can be a regulator, a researcher or an accredited body. External audits depend on what access the auditor is given.
- **Black-box and white-box access**: a black-box audit tests inputs and outputs only; a white-box audit can inspect data, code or weights.
- **Model card**: a standardised document describing a model's intended use, evaluation results across groups, and limitations.
- **Datasheet**: a document describing a dataset's collection, composition, uses and known gaps.
- **Impact assessment**: a structured review of the likely benefits and harms of a system to affected people.

## How it works

### Audit stages

Raji et al. (2020) introduce a framework for algorithmic auditing that supports AI system development end to end, applied throughout the internal organisation's development lifecycle. Its aim is to identify harms before deployment and to trace issues that emerge after it back to their source. Audits in practice vary widely in scope and rigour.

### Documentation artefacts

- **Model cards.** Mitchell et al. (2019) propose model cards: short documents that accompany a trained model and provide benchmarked evaluation across conditions such as cultural and demographic groups. The purpose is to make the model's intended use and limits visible to people who did not train it.
- **Datasheets for datasets.** Gebru et al. (2021) propose that every dataset be accompanied by a datasheet documenting its motivation, composition, collection process and recommended uses.

Both artefacts are self-reported. They make audits possible but do not replace them.

### Impact assessment

An impact assessment identifies the affected groups, the decisions the system influences, the likely failure modes, and the mitigations that are planned. Some regulatory frameworks ask for such assessments, and the procedures differ by jurisdiction.

## Regulatory context

The EU Artificial Intelligence Act, Regulation (EU) 2024/1689, sets out harmonised rules for AI in the Union. It includes obligations for systems it classifies as high-risk. The classification and conformity rules are in the Act's text, which is the primary source for these duties; interpretation and enforcement guidance continue to develop.

Other regimes take different routes. Some jurisdictions rely on sector regulators, on procurement rules for public bodies, or on voluntary standards. Law and policy are covered in [Law, Policy & Governance](../governance/index.md).

## Auditing large language models

Auditing general-purpose models is harder than auditing narrow classifiers, because the set of tasks and users is open-ended. Common approaches include benchmark evaluation across groups, adversarial testing or red-teaming to find harmful outputs, and documentation of training data and safety measures. Metaxa et al. (2021) survey methods for auditing algorithmic systems from the outside in, which is the setting that black-box access imposes.

## Connections

Auditing puts into practice the fairness criteria discussed in [Fairness definitions](fairness-definitions.md), and it is how the failures in [Bias case studies](bias-case-studies.md) were found and checked. The human side of audits, including how people use the outputs of an audited system, is in [Human-AI interaction](../human-ai-interaction/index.md).

## Applications

- Pre-deployment testing of hiring, credit and health tools.
- Public-sector procurement, where agencies require documentation and evaluation results before adopting a system.
- Research audits of platform recommendation and search systems through controlled accounts.

## Open questions

- **Access.** External auditors often need data, code or model access that developers do not want to share. How to provide it safely is unresolved.
- **Standards.** Without shared metrics and procedures, two audits of the same system can disagree.
- **Accountability for failures.** When an audit passes and the system later harms someone, the allocation of responsibility is not settled.
- **Auditing general-purpose models.** Testing an open-ended system across all of its uses is not yet feasible, and the scope of audits for these systems is still being defined.

## References

### Seminal papers

- Raji, I. D. et al. (2020). Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing. *Proceedings of FAT\* 2020*. https://doi.org/10.1145/3351095.3372873 — Proposes an internal audit framework applied across the development lifecycle.
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. *Proceedings of FAT\* 2019*. https://doi.org/10.1145/3287560.3287596 — Proposes model cards with benchmarked evaluation across cultural and demographic groups.
- Gebru, T. et al. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92. https://doi.org/10.1145/3458723 — Proposes datasheets that document each dataset's motivation, composition, collection process and recommended uses.

### Surveys and textbooks

- Metaxa, D. et al. (2021). Auditing Algorithms: Understanding Algorithmic Systems from the Outside In. *Foundations and Trends in Human–Computer Interaction*, 14(4), 272–344. https://doi.org/10.1561/1100000083 — Surveys methods for auditing algorithmic systems from the outside in.
- Regulation (EU) 2024/1689 of the European Parliament and of the Council (Artificial Intelligence Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — The primary legal text for AI Act obligations, including for high-risk systems.
