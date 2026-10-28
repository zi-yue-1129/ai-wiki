---
related:
  - society/ethics
  - society/governance
  - theory/paradigms/supervised/evaluation-and-validation
aliases:
  - 人力資源
  - 招募
  - 人才招募
---

# Human Resources and Recruiting

AI now sits at many points in the employment cycle: writing job advertisements, screening applications, scheduling and analysing interviews, matching skills to roles and monitoring performance. Each of these uses can affect a person's livelihood, so employment is one of the areas where fairness rules are most explicit.

## Landscape

| Stage | Methods | Notes |
|---|---|---|
| Sourcing and job ads | Language models for drafting and targeting | Wording can change who applies |
| CV screening | Keyword rules, ranking models, language-model extraction | Most regulated use in several jurisdictions |
| Skills matching | Embedding-based matching of profiles to roles | Depends on how skills are represented |
| Interviews | Structured scoring, speech and video analysis, transcript summaries | Video-based scoring is contested and widely criticised |
| Assessment and workforce planning | Attrition models, performance prediction | Risk of using past outcomes that reflect past bias |
| Internal mobility and monitoring | Recommendation of training and roles; activity tracking | Surveillance concerns |

## Why it is hard

- **Biased labels**: a screening model trained on past hiring decisions learns the decisions made, including any bias in them.
- **Proxy variables**: features such as postcode, school or employment gaps can correlate with protected characteristics.
- **Opacity**: candidates rarely know that a model was used or why they were rejected.
- **Small samples**: for many roles, there are too few hires to measure outcomes reliably.

## Key methods

- [Supervised learning and evaluation](../../theory/paradigms/supervised/evaluation-and-validation/index.md): the basis for screening models, and for checking them with subgroup metrics.
- [Ethics & fairness](../../society/ethics/index.md): definitions of fairness, and the trade-offs between them.
- [Interpretability](../../society/interpretability/index.md): tools for explaining which inputs drove a score, which candidates and regulators both need.
- [Large Language Models](../../theory/models/llm/index.md): used for resume parsing, drafting and interview summaries, with new failure modes such as hallucinated qualifications.

## Connections

- The fairness trade-offs (equal opportunity, calibration and others) are on [Ethics & Fairness](../../society/ethics/index.md). This page applies them to hiring.
- Rules for automated decision tools are part of [Law, Policy & Governance](../../society/governance/index.md).
- How people form first impressions and how structured interviews change judgement is studied in [Cognitive Science](../../brain-mind/cognitive-science/index.md). Heuristics and biases in human judgement are the human baseline that algorithmic tools are compared with.

## Applications

- Resume screening and ranking
- Matching candidates to open roles
- Structured interview scoring and transcript analysis
- Workforce planning and internal mobility

## Risks and limits

- **Disparate impact**: a tool can reject a protected group at a higher rate even when it never uses the protected attribute. Raghavan et al. (2020) examine vendor claims of bias mitigation in algorithmic hiring and the evidence behind them.
- **Automation bias**: recruiters may defer to a score even when they are asked to review it.
- **Legal duties**: in some places, employers must audit automated tools before use. New York City's Local Law 144 requires a bias audit within one year before an automated employment decision tool is used, with enforcement from 5 July 2023 (NYC Department of Consumer and Worker Protection).
- **High-risk classification**: the EU AI Act lists AI systems used for recruitment and selection among its high-risk uses, which bring obligations for risk management, data governance and human oversight (Regulation (EU) 2024/1689).

## Open questions

- Which fairness metric should apply to hiring, given that the metrics conflict (Kleinberg et al., 2016; Chouldechova, 2017).
- Whether bias audits detect the problems that matter in practice, or only the ones they are designed to test.

## References

### Seminal papers

- Raghavan, M. et al. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. *FAT\* 2020*. https://doi.org/10.1145/3351095.3372828 — Examines vendor claims about bias mitigation in hiring tools and the evidence offered for them.
- Kleinberg, J., Mullainathan, S. & Raghavan, M. (2016). Inherent Trade-Offs in the Fair Determination of Risk Scores. arXiv. https://arxiv.org/abs/1609.05807 — Shows that several natural fairness criteria cannot all hold at once when base rates differ.
- Hardt, M., Price, E. & Srebro, N. (2016). Equality of Opportunity in Supervised Learning. arXiv. https://arxiv.org/abs/1610.02413 — Defines a fairness criterion based on equal true positive rates and shows how to enforce it with post-processing.
- Chouldechova, A. (2017). Fair Prediction with Disparate Impact: A Study of Bias in Recidivism Prediction Instruments. *Big Data*. https://doi.org/10.1089/big.2016.0047 — Shows that calibration and error-rate balance cannot both hold when group base rates differ.

### Surveys and textbooks

- Mehrabi, N. et al. (2021). A Survey on Bias and Fairness in Machine Learning. *ACM Computing Surveys*. https://doi.org/10.1145/3457607 — Survey of sources of bias and of the fairness definitions and mitigation methods used in machine learning.

### Articles and documentation

- European Union. Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (AI Act). *Official Journal of the European Union*. https://eur-lex.europa.eu/eli/reg/2024/1689/oj — The binding text that classifies recruitment and selection AI as high-risk.
- New York City Department of Consumer and Worker Protection. Automated employment decision tools. https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page — Official guidance on the bias audit requirement under Local Law 144.
