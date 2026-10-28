---
related:
- society/governance
- society/economics
- engineering/data
- applications/healthcare
- applications/law
---

# Ethics & Fairness

## Common principles

Most AI ethics frameworks (OECD AI Principles, UNESCO Recommendation on the Ethics of AI, IEEE, corporate principles) converge on: **beneficence, non-maleficence, autonomy, justice/fairness, explicability**, plus privacy, accountability and sustainability (Floridi & Cowls, 2019; Jobin et al., 2019). The hard part is turning principles into practice.

## Bias and fairness

### Where bias comes from

| Source | Example |
|---|---|
| Historical bias | Past hiring data reflect discrimination (Amazon's scrapped résumé screener, 2018) |
| Representation bias | Under-representation in training data (facial analysis error rates far higher for darker-skinned women — Buolamwini & Gebru, 2018, "Gender Shades") |
| Measurement bias | Proxy targets that differ across groups (health costs as a proxy for need — Obermeyer et al., 2019) |
| Aggregation bias | One model for groups with different relationships |
| Deployment bias | Using a model in a context it wasn't designed for |
| Feedback loops | Predictive policing sends patrols where past arrests were, generating more arrests there |

### Fairness definitions

| Criterion | Requirement |
|---|---|
| Demographic parity | Equal positive-prediction rates across groups |
| Equalised odds | Equal true- and false-positive rates |
| Equal opportunity | Equal true-positive rates |
| Predictive parity / calibration | Equal precision; scores mean the same across groups |
| Individual fairness | Similar individuals treated similarly |
| Counterfactual fairness | Prediction unchanged if the protected attribute had been different |

**Impossibility results**: when base rates differ, calibration and equal error rates cannot generally hold together (Kleinberg, Mullainathan & Raghavan, 2016; Chouldechova, 2017) — the heart of the COMPAS debate. Choosing a criterion is a value judgement, not a technical one.

Details, with the impossibility proofs, are in [Fairness definitions and impossibility results](fairness-definitions.md). Each criterion has its own page: [Demographic parity](demographic-parity.md), [Equalised odds](equalised-odds.md), [Calibration within groups](calibration-within-groups.md), [Individual fairness](individual-fairness.md) and [Counterfactual fairness](counterfactual-fairness.md).

### Mitigation

Pre-processing (reweighting, resampling), in-processing (fairness constraints), post-processing (group-specific thresholds), plus — most importantly — better problem formulation, data and stakeholder involvement. Tools: Fairlearn, AIF360.

### Bias in LLMs

Stereotypes in generated text and images, dialect bias (e.g. covert prejudice against African American English, Hofmann et al., 2024, *Nature*), unequal performance across languages, and cultural default to Western norms.

Concrete cases, including COMPAS, Gender Shades and a health-risk algorithm, are in [Case studies in algorithmic bias](bias-case-studies.md).

## Privacy

- Training on personal data scraped from the web; memorisation and extraction
- Inference of sensitive attributes from innocuous data
- Surveillance: facial recognition in public spaces (restricted under the EU AI Act)
- Rights: GDPR access, erasure and objection; the difficulty of "unlearning" from trained models
- Techniques: [federated learning, differential privacy](../../theory/paradigms/federated/index.md)

## Accountability and transparency

- Who is responsible when an AI-assisted decision harms someone? Developers, deployers, users?
- Documentation (model cards, datasheets, system cards), audits, impact assessments
- Contestability: people should be able to challenge automated decisions

Documentation and audit practice is covered in [Algorithmic auditing and impact assessment](algorithmic-auditing.md).

## Hidden labour and global justice

- Data labelling and content moderation are often outsourced to low-wage workers, sometimes exposed to traumatic content (e.g. reporting on Kenyan workers labelling toxic content, 2023)
- Benefits and harms are unevenly distributed across countries and languages
- Environmental costs (see [Climate & Energy](../../applications/climate-energy/index.md))

## Human autonomy and well-being

- Manipulative design and persuasive AI
- Emotional dependence on companion chatbots
- Children's interaction with AI
- De-skilling and cognitive offloading (see [Psychology & AI](../../brain-mind/psychology/index.md))

## References

- Barocas, S., Hardt, M. & Narayanan, A. (2023). *Fairness and Machine Learning: Limitations and Opportunities*. MIT Press. https://fairmlbook.org/ — Textbook on the fairness definitions used in this section and on the trade-offs between them.
- Buolamwini, J. & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *Proceedings of the 1st Conference on Fairness, Accountability and Transparency (PMLR 81)*. https://proceedings.mlr.press/v81/buolamwini18a.html — Audits commercial gender classifiers and finds much higher error rates for darker-skinned women.
- Obermeyer, Z. et al. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science*. https://doi.org/10.1126/science.aax2342 — Shows a health-risk algorithm underestimating the needs of Black patients because it used cost as a proxy for health.
- Mitchell, M. et al. (2019). Model Cards for Model Reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency*. https://arxiv.org/abs/1810.03993 — Proposes a standard documentation template covering intended use, evaluation across groups and known limitations.
- Bender, E. M. et al. (2021). On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*. https://doi.org/10.1145/3442188.3445922 — Discusses the risks of ever-larger language models, as its title states.

## Further learning

- [Stanford Encyclopedia of Philosophy: Ethics of AI and Robotics](https://plato.stanford.edu/entries/ethics-ai/) — peer-reviewed encyclopedia overview of the questions in this section.
