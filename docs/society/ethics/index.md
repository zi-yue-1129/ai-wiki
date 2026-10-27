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

### Mitigation

Pre-processing (reweighting, resampling), in-processing (fairness constraints), post-processing (group-specific thresholds), plus — most importantly — better problem formulation, data and stakeholder involvement. Tools: Fairlearn, AIF360.

### Bias in LLMs

Stereotypes in generated text and images, dialect bias (e.g. covert prejudice against African American English, Hofmann et al., 2024, *Nature*), unequal performance across languages, and cultural default to Western norms.

## Privacy

- Training on personal data scraped from the web; memorisation and extraction
- Inference of sensitive attributes from innocuous data
- Surveillance: facial recognition in public spaces (restricted under the EU AI Act)
- Rights: GDPR access, erasure and objection; the difficulty of "unlearning" from trained models
- Techniques: [federated learning, differential privacy](../../foundations/paradigms/federated/index.md)

## Accountability and transparency

- Who is responsible when an AI-assisted decision harms someone? Developers, deployers, users?
- Documentation (model cards, datasheets, system cards), audits, impact assessments
- Contestability: people should be able to challenge automated decisions

## Hidden labour and global justice

- Data labelling and content moderation are often outsourced to low-wage workers, sometimes exposed to traumatic content (e.g. reporting on Kenyan workers labelling toxic content, 2023)
- Benefits and harms are unevenly distributed across countries and languages
- Environmental costs (see [Climate & Energy](../../applications/climate-energy/index.md))

## Human autonomy and well-being

- Manipulative design and persuasive AI
- Emotional dependence on companion chatbots
- Children's interaction with AI
- De-skilling and cognitive offloading (see [Psychology & AI](../../brain-mind/psychology/index.md))

## Resources

- Barocas, Hardt & Narayanan, *Fairness and Machine Learning* (free online)
- O'Neil, *Weapons of Math Destruction*; Benjamin, *Race After Technology*; Crawford, *Atlas of AI*
- Mitchell et al. (2019), "Model Cards for Model Reporting"
- [Stanford Encyclopedia of Philosophy: Ethics of AI and Robotics](https://plato.stanford.edu/entries/ethics-ai/)
