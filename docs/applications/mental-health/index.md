---
related:
- brain-mind/psychology
- theory/paradigms/probabilistic
- applications/healthcare
- society/ethics
aliases:
  - 心理健康
  - 精神健康
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

Uses the models of [reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md) and [Bayesian inference](../../theory/paradigms/probabilistic/index.md) to describe how cognition goes awry:

- **Depression**: reduced reward sensitivity or learning rate; pessimistic priors; altered exploration
- **Anxiety**: overestimating threat probability; intolerance of uncertainty
- **Addiction**: model-free (habitual) control overriding model-based control; aberrant dopamine prediction errors
- **Psychosis**: aberrant salience; imbalanced weighting of priors vs sensory evidence (predictive-processing accounts)
- **Autism**: proposals of attenuated priors or altered precision weighting (debated)
- **OCD**: imbalance between goal-directed and habitual control

Huys, Maia & Frank (2016), "Computational psychiatry as a bridge from neuroscience to clinical applications", *Nature Neuroscience*, is a standard review.

## Chatbots and LLMs

**Evidence:**

- A randomised trial of the rule-based CBT chatbot Woebot found reduced depression and anxiety symptoms in young adults over two weeks (Fitzpatrick et al., 2017)
- Large numbers of people use general-purpose chatbots for emotional support without clinical oversight

**Risks:**

- Inadequate responses to suicidal ideation or crisis; reinforcing delusions or harmful beliefs via sycophancy
- Emotional dependence on companion apps, especially among adolescents
- Privacy of highly sensitive data
- Policy on AI offered as therapy is changing quickly, and rules differ across jurisdictions

## Ethics

- Informed consent for passive sensing
- Risk of false positives (stigma) and false negatives (missed crises)
- Bias in language-based detection across cultures, dialects and languages
- Clear disclosure that the user is talking to AI; escalation to humans

## Key methods

Three methods are most relevant here. Each links to the page that explains it.

- [Reinforcement learning](../../theory/paradigms/reinforcement-learning/index.md): models of learning and reward that describe symptoms such as reduced reward sensitivity (Huys et al., 2016).
- [Probabilistic inference](../../theory/paradigms/probabilistic/index.md): Bayesian models of belief updating, used to describe pessimistic priors and intolerance of uncertainty (Huys et al., 2016).
- [InstructGPT and RLHF](../../theory/models/llm/instructgpt-rlhf/index.md): the training recipe behind the chat-style tools discussed above (Ouyang et al., 2022).

## References

### Seminal papers

- Fitzpatrick et al. (2017). Delivering Cognitive Behavior Therapy to Young Adults With Symptoms of Depression and Anxiety Using a Fully Automated Conversational Agent (Woebot). *JMIR Mental Health*. https://doi.org/10.2196/mental.7785 — Trial of a rule-based CBT chatbot with young adults.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. NeurIPS. https://arxiv.org/abs/1706.03762 — Introduces the Transformer, built on multi-head self-attention.
- Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. NeurIPS. https://arxiv.org/abs/2203.02155 — InstructGPT, instruction tuning from human preference feedback.

### Surveys and textbooks

- Huys, Maia & Frank (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — Review of how computational models can link neuroscience to psychiatric practice.
- Torous et al. (2021). The growing field of digital psychiatry: current evidence and the future of apps, social media, chatbots, and virtual reality. *World Psychiatry*. https://doi.org/10.1002/wps.20883 — Reviews evidence for digital tools in psychiatry, including chatbots.
- Stade et al. (2024). Large language models could change the future of behavioral healthcare: a proposal for responsible development and evaluation. *npj Mental Health Research*. https://doi.org/10.1038/s44184-024-00056-z — Proposes responsible development and evaluation of LLMs in behavioural healthcare.
