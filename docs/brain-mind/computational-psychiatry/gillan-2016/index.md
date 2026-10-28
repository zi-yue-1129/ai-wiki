---
status: draft
last_reviewed: 2026-10-28
related:
- applications/mental-health
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- psychology
- reinforcement learning
aliases:
  - Gillan et al. 2016
  - 兩步任務
  - 目標導向控制
  - Two-step task
  - Goal-directed control
---

# Gillan et al. 2016 (Goal-Directed Control and Compulsivity)

Gillan, Kosinski, Whelan, Phelps and Daw (2016) measured goal-directed control with a planning task and a fitted model, in large online samples. They found that deficits in goal-directed control were most strongly linked to a symptom dimension of compulsive behaviour and intrusive thought. This page is part of [Computational Psychiatry](../index.md). The parent page gives the overview; this page covers the method and the evidence.

## Overview

Obsessive-compulsive disorder and addiction both involve repetitive behaviour that continues despite its costs. One account holds that these problems share a deficit in goal-directed control, the ability to choose actions by reasoning about their outcomes, which leaves a person relying on habits. Goal-directed deficits, however, have also been reported in disorders with no obvious compulsive element. Gillan et al. suggested that this mismatch may reflect the way diagnostic categories are drawn. They tested it with a dimensional design, in which symptoms were measured as continuous traits in the general population and linked to task performance.

## Key concepts

- **Two-step task**: a sequential decision task in which the first choice leads probabilistically to one of two second-stage states, and the rewards in those states change over time. Because the transitions are known, the task can separate choices guided by a model from choices guided by past reward.
- **Model-free value**: a value learned from past rewards for each option, updated by a prediction error. See [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md).
- **Model-based value**: a value computed by planning with the known transition structure.
- **Hybrid model**: a model that combines the two values with a weight. The weight becomes the quantity of interest.
- **Symptom dimension**: a continuous trait derived from questionnaire scores, rather than a diagnostic category.

## How it works

Participants complete many trials. On each trial, a first-stage choice between two options is followed by a probabilistic transition to a second-stage state and a reward. The model keeps two value estimates for each first-stage option.

The model-free value is updated after each reward by a prediction error, $Q_{\text{MF}}(a) \leftarrow Q_{\text{MF}}(a) + \alpha\,\delta$. The model-based value looks ahead through the known transitions, $Q_{\text{MB}}(a) = \sum_{s} P(s \mid a)\,\max_{b} Q(s, b)$. A common hybrid form, following Daw et al. (2011), combines them as $Q_{\text{net}} = wQ_{\text{MB}} + (1-w)Q_{\text{MF}}$, and choices follow a softmax rule, $P(a) \propto \exp(\beta Q_{\text{net}}(a))$. Fitting this model to each participant's choices estimates $\alpha$, $\beta$ and the model-based weight $w$. A lower $w$ means that choices depend less on planning.

Gillan et al. collected these tasks in large online samples and related the estimated parameters to questionnaire-based symptom scores, rather than to clinical diagnoses.

## Results

The paper reports two independent general-population samples. Its main result, from the abstract, is that deficits in goal-directed control were most strongly associated with a symptom dimension combining compulsive behaviour and intrusive thought. The authors report that this association was specific when compared with other, non-compulsive aspects of psychopathology. This page does not quote effect sizes; they are in the paper and should be read there.

## Limitations

- The samples were recruited online from the general population. The result concerns a symptom dimension, not clinical diagnoses.
- The model is one of several possible models of the task. Its parameters can trade off against each other, so the estimates depend on the model being approximately right.
- The study rests on behaviour and questionnaires. The abstract does not establish a neural mechanism.
- An association between a symptom dimension and a model parameter does not show that the deficit causes the symptoms.

## Open questions

- Is the goal-directed deficit a stable trait that predicts who develops compulsive symptoms, or a state that changes with stress or treatment?
- Do the same deficits appear in clinical groups? The abstract notes that they accompany several disorders. Maia and Frank (2011) review how such models have been applied to psychiatric and neurological disorders.
- Can the parameter be estimated reliably enough for use in one person? This needs test-retest work.

## References

### Seminal papers

- Gillan, C. M., Kosinski, M., Whelan, R., Phelps, E. A. & Daw, N. D. (2016). Characterizing a psychiatric symptom dimension related to deficits in goal-directed control. *eLife*. https://doi.org/10.7554/eLife.11305 — Reports two general-population samples in which goal-directed control deficits track a dimension of compulsive behaviour and intrusive thought.
- Daw, N. D., Gershman, S. J., Seymour, B., Dayan, P. & Dolan, R. J. (2011). Model-Based Influences on Humans' Choices and Striatal Prediction Errors. *Neuron*. https://doi.org/10.1016/j.neuron.2011.02.027 — Shows that human choices carry model-based influences, and relates striatal prediction errors to the learning signal in the same task.

### Surveys and textbooks

- Maia, T. V. & Frank, M. J. (2011). From reinforcement learning models to psychiatric and neurological disorders. *Nature Neuroscience*. https://doi.org/10.1038/nn.2723 — Early review of how reinforcement learning models can describe symptoms in psychiatric and neurological disorders.
- Huys, Q. J. M., Maia, T. V. & Frank, M. J. (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — Review of how computational models can connect neuroscience with clinical practice in psychiatry.
- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P. (2012). Computational psychiatry. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2011.11.018 — Review that sets out computational psychiatry as an approach using models of learning and decision making to understand mental illness.

### Articles and documentation

- Insel, T. et al. (2010). Research Domain Criteria (RDoC): Toward a New Classification Framework for Research on Mental Disorders. *American Journal of Psychiatry*. https://doi.org/10.1176/appi.ajp.2010.09091379 — Proposes a research framework that organises mental disorders around dimensions of function, the framework behind dimensional studies such as this one.
