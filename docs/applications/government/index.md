---
status: draft
last_reviewed: 2026-10-28
related:
  - society/ethics
  - society/governance
  - society/interpretability
aliases:
  - 政府與公共服務
  - Government
  - Public sector AI
---

# Government and Public Services

Governments use AI to decide, plan and deliver public services, from benefit eligibility to tax audits. The stakes are high because decisions affect rights, and citizens often cannot choose another provider. This page covers AI used **by** public bodies. For laws that regulate AI, see [Law, Policy & Governance](../../society/governance/index.md).

## Landscape

| Area | Examples |
|---|---|
| Benefits and eligibility | Systems that flag cases for review or screen applications |
| Risk assessment | Tools that predict re-offending, child-welfare risk or fraud |
| Tax and enforcement | Audit selection and anomaly detection in returns |
| Service delivery | Chatbots for public information, translation and form filling |
| Planning and infrastructure | Traffic, transport and resource forecasting |
| Document processing | Classifying and summarising large volumes of correspondence |

## Where the risks concentrate

- **Errors with no easy appeal.** A wrong score can deny a benefit or trigger an investigation, so the right to contest a decision matters.
- **Bias.** Models trained on historical records can reproduce past discrimination, and a single accuracy figure can hide unequal error rates between groups.
- **Opacity.** Agencies often cannot explain how a system reached a decision, and the public cannot inspect it.

## Evidence on human and machine decisions

Whether machine learning can improve public decisions is an open empirical question. A widely cited study uses bail decisions as a test case for exactly that question, so claims about accuracy should be tested on real decisions and outcomes (see References).

## Key methods

Three methods underpin most public-sector tools. Each links to the page that explains it.

- [Evaluation and validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md): how to test a model on the population it will affect, not only on average accuracy.
- [Trees and ensembles](../../theory/paradigms/supervised/trees-and-ensembles/index.md): tabular models that are common in risk scoring and fraud detection.
- [Large language models](../../theory/models/llm/index.md): drafting and answering public correspondence, which needs human review.

## Connections

- The fairness trade-offs that appear in public tools are covered in [Ethics & Fairness](../../society/ethics/index.md).
- Explaining decisions to affected people is covered in [Interpretability](../../society/interpretability/index.md).

## Open questions

- What evidence should a public body need before deploying a model that affects benefits or liberty?
- How can people contest automated decisions when the reasons are not visible to them?
- Who is accountable when a system is built by a vendor but operated by a public agency?

## References

### Seminal papers

- Veale, M. & Binns, R. (2017). Fairer machine learning in the real world: Mitigating discrimination without collecting sensitive data. *Big Data & Society* 4(2). https://doi.org/10.1177/2053951717743530 — Examines how to reduce discrimination in machine learning without collecting sensitive attributes, a situation common to public agencies.
- Kleinberg, J. et al. (2018). Human Decisions and Machine Predictions. *The Quarterly Journal of Economics* 133(1). https://doi.org/10.1093/qje/qjx032 — Uses bail decisions as a test case for whether machine learning can improve human decision-making.
- Ananny, M. & Crawford, K. (2016). Seeing without knowing: Limitations of the transparency ideal and its application to algorithmic accountability. *New Media & Society* 20(3). https://doi.org/10.1177/1461444816676645 — Argues that transparency alone is a limited route to accountability for algorithmic systems.

### Surveys and textbooks

- OECD (2019). *Artificial Intelligence in Society*. OECD Publishing. https://www.oecd.org/en/publications/artificial-intelligence-in-society_eedfee77-en.html — A survey of AI's technical, economic and policy landscape, with public policy issues such as fairness, privacy, safety and accountability.

### Articles and documentation

- European Union (2024). Regulation (EU) 2024/1689 (Artificial Intelligence Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — Harmonised EU rules on artificial intelligence, adopted on 13 June 2024.
