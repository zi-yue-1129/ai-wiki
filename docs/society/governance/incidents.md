---
status: draft
last_reviewed: 2026-10-28
related:
  - society/governance
  - society/safety-alignment
  - society/ethics
tags:
  - incidents
  - AI failures
  - reporting
aliases:
  - AI 事故
  - 事件資料庫
  - AI 事件
  - Incident database
---

# AI incident databases and case studies

An AI incident database is a structured record of real cases in which AI systems caused or nearly caused harm. Such records help researchers, regulators and companies see recurring failure patterns, which the scattered news coverage of single failures does not reveal. This page covers the main databases, how incidents are classified, what case studies have taught, and how regulation is starting to require incident reporting.

## Overview

Aviation and medicine learned long ago to record accidents and near misses, so that the same failure is not repeated in each new setting. AI has lacked a comparable habit. McGregor describes the AI Incident Database as an incident collection started by an industrial and non-profit cooperative, with the aim of preventing repeated real-world AI failures by cataloguing them [(McGregor, 2020)](https://arxiv.org/abs/2011.08512).

## Key concepts

- **Incident**: a real event in which an AI system contributed to harm, or to a near miss.
- **Hazard**: a situation that could plausibly lead to an incident, even if none has occurred yet.
- **Taxonomy**: a shared classification of incidents, for example by harm type, affected party, sector and cause. Taxonomies make records comparable.
- **Functionality gap**: the difference between what a system is claimed to do and what it does in practice.

## How it works

A database collects reports from news, public filings and submissions, and each entry is tagged with a taxonomy. Good entries record the system, the deployment context, the harm, and what was done in response. Incomplete entries are common, so most databases list sources and mark uncertain fields. The OECD AI Incidents and Hazards Monitor, for example, is an automated media monitor. It labels its summaries and classifications as AI-generated, and it states that the results are not the official views of the OECD or its member countries [(OECD AI Incidents Monitor)](https://oecd.ai/en/incidents).

The OECD has also published a definition of AI incidents and related terms, so that databases and regulators can agree on what counts as an incident and what counts as a hazard [(OECD, 2024)](https://doi.org/10.1787/d1a8d965-en).

## Case studies

Case studies show failure patterns that a single test does not reveal. Raji and colleagues argue that many deployed AI systems do not deliver the functions claimed for them, and that this functionality gap is a recurring source of harm. They call for audits that test the claims themselves [(Raji et al., 2022)](https://doi.org/10.1145/3531146.3533158). Failures that occur after deployment, such as systems that perform well on benchmarks but poorly in a new population, are a common theme in incident collections.

## Connections

Incidents feed the safety questions discussed in [AI safety and alignment](../safety-alignment/index.md), including specification gaming and reward hacking. Many incidents involve fairness failures covered in [Ethics and fairness](../ethics/index.md). The evaluation of AI systems before deployment is described in [Evaluation](../../theory/evaluation/index.md).

## Applications

Companies use incident records in risk management and product reviews. Regulators and standards bodies use them to decide which harms to prioritise. Researchers mine them to build taxonomies and to test whether a new risk has occurred before.

## Reporting duties

The EU AI Act requires providers of high-risk AI systems to report serious incidents to the market surveillance authorities of the Member States where the incident occurred, and sets timelines for doing so [(Regulation (EU) 2024/1689)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj). Reporting duties make incident data more complete, but they can also be limited to providers that fall under the Act, so public databases will still depend on news and voluntary reports.

## Open questions

- How should incident databases handle uncertain or disputed facts, and how should they weigh news reports against company disclosures?
- Which taxonomy should be used across jurisdictions, and can it be kept stable as systems change?
- Do incident records reduce repeated failures, or do they mainly inform risk assessment?
- How can reporting cover near misses and hazards without exposing sensitive commercial information?

## References

### Seminal papers

- McGregor, *Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database* (2020). https://arxiv.org/abs/2011.08512 — Describes the design and purpose of the AI Incident Database.
- Raji, Kumar, Horowitz and Selbst, *The Fallacy of AI Functionality*, ACM Conference on Fairness, Accountability, and Transparency (2022). https://doi.org/10.1145/3531146.3533158 — Argues that failures to deliver claimed functionality are a recurring source of AI harm and calls for audits.

### Surveys and textbooks

- OECD, *Defining AI incidents and related terms*, OECD Artificial Intelligence Papers (2024). https://doi.org/10.1787/d1a8d965-en — Sets out shared definitions of AI incidents and hazards.

### Articles and documentation

- OECD, *AI Incidents and Hazards Monitor (AIM)*, OECD.AI. https://oecd.ai/en/incidents — Automated monitor of AI incidents and hazards, with its own disclaimers about the status of its data.
- European Union, *Regulation (EU) 2024/1689 (Artificial Intelligence Act)*, Official Journal of the European Union (2024). https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Sets serious-incident reporting duties for providers of high-risk AI systems.
