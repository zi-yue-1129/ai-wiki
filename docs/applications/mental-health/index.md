---
related:
- brain-mind/psychology
- theory/probabilistic
- applications/healthcare
- society/ethics
---

# Mental Health

## Landscape

| Area | Examples |
|---|---|
| Computational psychiatry | Formal models (RL, Bayesian inference) of symptoms; parameters as biomarkers |
| Digital phenotyping | Smartphone sensors, typing, sleep, mobility and speech as signals of mood and relapse |
| Language-based assessment | Detecting depression, suicidality or psychosis risk from text and speech |
| Conversational support | Chatbots delivering CBT-style exercises; general LLMs used informally for emotional support |
| Clinician support | Session summarisation, therapist training simulations, measurement-based care |
| Crisis services | Triage and prioritisation of messages |
| Neuroimaging and neuromodulation | Predicting treatment response; personalising TMS targets |

## Computational psychiatry

Uses the models of [reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md) and [Bayesian inference](../../theory/probabilistic/index.md) to describe how cognition goes awry:

- **Depression**: reduced reward sensitivity or learning rate; pessimistic priors; altered exploration
- **Anxiety**: overestimating threat probability; intolerance of uncertainty
- **Addiction**: model-free (habitual) control overriding model-based control; aberrant dopamine prediction errors
- **Psychosis**: aberrant salience; imbalanced weighting of priors vs sensory evidence (predictive-processing accounts)
- **Autism**: proposals of attenuated priors or altered precision weighting (debated)
- **OCD**: imbalance between goal-directed and habitual control

Huys, Maia & Frank (2016), "Computational psychiatry as a bridge from neuroscience to clinical applications", *Nature Neuroscience*, is a standard review.

## Chatbots and LLMs

**Evidence:**

- Early rule-based CBT chatbots (Woebot, Wysa) showed modest short-term symptom reductions in small trials
- A randomised trial of a generative-AI therapy chatbot (Therabot) reported clinically meaningful symptom reductions for depression, anxiety and eating-disorder risk over 8 weeks (Heinz et al., 2025, *NEJM AI*)
- Large numbers of people use general-purpose chatbots for emotional support without clinical oversight

**Risks:**

- Inadequate responses to suicidal ideation or crisis; reinforcing delusions or harmful beliefs via sycophancy
- Emotional dependence on companion apps, especially among adolescents
- Privacy of highly sensitive data
- Lawsuits and regulatory action followed cases of harm linked to companion chatbots; several US states restricted AI "therapy" without licensed oversight (e.g. Illinois, 2025)

## Ethics

- Informed consent for passive sensing
- Risk of false positives (stigma) and false negatives (missed crises)
- Bias in language-based detection across cultures, dialects and languages
- Clear disclosure that the user is talking to AI; escalation to humans

## Resources

- Huys et al. (2016) and Montague et al. (2012), computational psychiatry reviews
- Torous et al. (2021), "The growing field of digital psychiatry", *World Psychiatry*
- Stade et al. (2024), "Large language models could change the future of behavioral healthcare", *npj Mental Health Research*
- Computational Psychiatry Course (Zurich, lectures online)
