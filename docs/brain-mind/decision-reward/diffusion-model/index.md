---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/cognitive-science
- brain-mind/psychology
tags:
- decision making
aliases:
  - 擴散決策模型
  - Diffusion Decision Model
  - DDM
---

# Diffusion Decision Model

The diffusion decision model (DDM) describes a two-choice decision as noisy evidence accumulating toward one of two boundaries. It explains both the choices people make and how long they take to make them, which is why it is the standard model for response-time data in psychology and neuroscience. It is a method for turning behaviour into mechanism: each parameter corresponds to a distinct cognitive process.

This page is part of [Decision Making, Dopamine & Reward](../index.md). The parent page gives the overview; this page covers the model itself.

## Overview

Two-choice tasks produce two kinds of data: the proportion of correct answers and the distribution of response times. A model that only predicts accuracy cannot tell apart a person who is careful from one who has good information. The DDM fits both, and separates the causes of a change in behaviour into parts that can be tested.

## Key concepts

- **Drift rate**: the average rate at which evidence accumulates toward the correct option. A clearer stimulus gives a larger drift rate.
- **Boundary separation**: the distance between the two decision boundaries. Wider boundaries mean more evidence is needed before responding, which is slower and more accurate.
- **Starting point**: where accumulation begins between the boundaries. A starting point closer to one boundary is a bias toward that option.
- **Non-decision time**: the time taken by processes outside the decision itself, such as perceiving the stimulus and moving the hand.
- **Noise**: random fluctuation in the evidence, which makes the same stimulus lead to different decision times and occasional errors.

## The model

Let evidence x start at a point z between boundaries at 0 and a. In standard notation, x changes as

dx = v dt + s dW

where v is the drift rate, s the scale of the noise, and dW a small increment of a Wiener process. The decision is made when x first reaches 0 or a. The response time is the time to reach a boundary plus the non-decision time. Choice and response time together then determine the predicted data, and fitting the parameters to the observed distribution of response times is what separates the components.

The model's form is a continuous version of sequential sampling, in which evidence is gathered one sample at a time until a threshold is reached. Its continuous form makes the predicted distributions of response times analytical, which is why it can be fitted to large datasets.

## Evidence from experiments

Ratcliff and McKoon (2008) review the model and illustrate its parameters with three experiments:

1. **Stimulus difficulty** changes the drift rate. Harder stimuli give less information per unit time, and the effect appears in both accuracy and the shape of response-time distributions.
2. **Speed-accuracy instructions** change boundary separation. Asking for speed narrows the boundaries, which shortens responses and increases errors, without changing the quality of information.
3. **Stimulus proportions** bias the starting point and drift. When one option is more frequent, responses shift toward it, and the model attributes this to a biased starting point.

The authors also argue that the model's constraints make it testable and potentially falsifiable, which distinguishes it from descriptive accounts of response times.

## Neural correspondence

The model describes behaviour, and its parameters are not directly neural quantities. Accumulation-to-bound ideas were motivated in large part by recordings from parietal cortex in monkeys performing motion discrimination, where firing rates rise toward a level before a choice. Gold and Shadlen (2007) review this line of work, which is the main reason the model is considered a candidate neural mechanism. Whether the fitted parameters map onto specific neurons is still an open research question.

## Connections

- **Decision making and reward**: the diffusion model covers evidence; learned values are a separate input. The parent page [Decision Making, Dopamine & Reward](../index.md) discusses how value can bias the starting point.
- **Model-based and model-free control**: a different question, about which controller chooses. See [Model-Based vs Model-Free Control](../model-based-vs-model-free/index.md).
- **Psychology**: the model is used in clinical and developmental research to compare groups by parameter rather than by accuracy alone. See [Psychology & AI](../../psychology/index.md).
- **Predictive coding**: accumulating evidence is one way a system could reach a decision from prediction errors. See [Predictive Coding & Free Energy](../../predictive-coding/index.md).

## Applications

- **Clinical and cognitive research**: comparing parameters between groups, such as older and younger adults, can separate slower processing from more cautious decision thresholds.
- **Human-AI interaction**: a possible use is modelling how quickly and accurately people respond to AI suggestions, to inform interfaces that avoid over-reliance. This is a proposed use, not a result from the sources cited here.

## Open questions

- **Are the parameters neural?** The fitted parameters are useful summaries, but their link to specific cortical populations is not settled.
- **How general is the model?** It was developed for two-choice tasks; extending it to many options and to value-based choice is an active area.
- **Is the boundary fixed?** Some tasks suggest the boundary changes over time or with reward, which the basic model does not capture.

## References

### Seminal papers

- Ratcliff, R. & McKoon, G. (2008). The Diffusion Decision Model: Theory and Data for Two-Choice Decision Tasks. *Neural Computation*. https://doi.org/10.1162/neco.2008.12-06-420 — Reviews the diffusion model and shows how its parameters separate the effects of difficulty, speed-accuracy instructions and bias.
- Ratcliff, R. (1978). A theory of memory retrieval. *Psychological Review*. https://princetonuniversity.github.io/NEU-PSY-502/_static/pdf/Class%205/Ratcliff1978.pdf — An early diffusion-style account of memory retrieval, from which the decision model was later developed.
- Ratcliff, R. & Smith, P. L. (2004). A comparison of sequential sampling models for two-choice reaction time. *Psychological Review*. https://pmc.ncbi.nlm.nih.gov/articles/PMC1440925 — Compares sequential-sampling models of two-choice reaction time, the family that includes the diffusion model.

### Surveys and reviews

- Gold, J. I. & Shadlen, M. N. (2007). The neural basis of decision making. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.29.051605.113038 — A review of how neurons accumulate evidence toward a decision, the neural background to the diffusion models.
- Dayan, P. & Daw, N. D. (2008). Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*. https://doi.org/10.3758/CABN.8.4.429 — Reviews how decision theory and reinforcement learning models relate to choice in the brain.
