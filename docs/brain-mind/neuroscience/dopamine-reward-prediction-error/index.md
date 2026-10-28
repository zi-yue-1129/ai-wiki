---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- theory/paradigms/reinforcement-learning
tags:
- neuroscience
- reinforcement learning
- decision making
aliases:
  - 多巴胺的獎勵預測誤差
  - Dopamine Reward Prediction Error
  - RPE
---

# Dopamine reward prediction error (Schultz, Dayan & Montague, 1997)

Dopamine neurons signal the difference between the reward expected and the reward received. This is the same quantity that drives learning in temporal-difference reinforcement learning, which is why this finding is one of the strongest links between AI and neuroscience.

This page is part of [Neuroscience Basics](../index.md). It covers one method in detail; the wider picture of how dopamine supports decisions is on [Decision Making, Dopamine & Reward](../../decision-reward/index.md).

## Overview

When you get a pleasant surprise, your brain learns that the cue leading to it is valuable. When the same reward becomes expected, the surprise disappears. Dopamine appears to carry the surprise, not the reward itself. That single signal can explain how behaviour is shaped by reward, and it gives a precise biological counterpart to a learning rule from AI.

## Key concepts

- **Reward prediction error**: the reward received minus the reward predicted. Positive means better than expected, negative means worse.
- **Phasic dopamine response**: a brief burst or dip of firing in dopamine neurons, as opposed to slower changes in tone.
- **Conditioned stimulus**: a cue, such as a light or tone, that reliably predicts reward.
- **Temporal-difference error**: the AI version of the prediction error, which also uses the predicted value of the next state.

## Problem

What do midbrain dopamine neurons signal while an animal learns about rewards? Earlier views linked dopamine mainly to reward itself or to movement. The question was whether its activity follows the reward directly, or follows the change between what was expected and what happened.

## Core idea

Dopamine neurons respond to unexpected rewards, and as learning proceeds the response moves to the earliest predictive cue. The pattern matches a temporal-difference error, the difference between the reward received and the reward predicted. Once a cue predicts reward well, the reward itself produces little response, and an expected reward that is omitted produces a dip below baseline.

The authors frame this as a link between reinforcement learning theory and the brain. Their key step is to compare recorded responses with what a learning algorithm would produce, rather than only describing the responses.

## Equation or algorithm

In modern notation, the temporal-difference error is

\(\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)\)

where \(r_t\) is the reward at time t, \(V\) is the learned value of a state, and \(\gamma\) is a discount factor. Learning then nudges the value estimates in the direction of \(\delta_t\). The temporal-difference form, in which predictions about successive states are compared, is due to Sutton (1988), and the mapping onto dopamine was proposed by Montague, Dayan & Sejnowski (1996).

## Results

The recordings were made in monkeys performing reward tasks. The main patterns reported by Schultz, Dayan and Montague (1997) are:

- Dopamine firing rose to unexpected rewards.
- After learning, the response shifted from the reward to the earliest reliable cue that predicted it.
- When an expected reward was omitted, firing dipped below baseline at the time the reward was due.

These three patterns match the prediction-error signal in the equation above. The reported findings come from a limited set of animals and tasks.

## Limitations

- **Sample and task.** The recordings came from a limited number of monkeys and reward tasks. Generalisation to other species, tasks and brain regions needed later work.
- **Prediction error is not the whole story.** Later work debated whether dopamine signals only prediction error, or also salience, novelty and information about the reward. Schultz (2016) reviews a two-component account in which an early, general response is followed by a later, error-specific one.

## Connections

- **Reinforcement learning**: the prediction error is the core update of temporal-difference learning, the basis of much AI research on agents. See [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Model-free control**: the model-free controller in [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md) is updated by this same signal.
- **Decision making**: how dopamine biases choices, and how it interacts with evidence accumulation, is on [Decision Making, Dopamine & Reward](../../decision-reward/index.md).

## Applications

- **Reinforcement learning in AI**: the temporal-difference update is used in game-playing and control agents, and the match to dopamine is a common example of how neuroscience inspires algorithms.
- **Computational psychiatry**: models that fit prediction-error learning to behaviour are used to study conditions such as addiction. These are research tools, not clinical diagnoses.

## Open questions

- **Does dopamine encode only the error?** Reports of salience and novelty signals keep the question open.
- **How is the error computed?** The circuit that calculates the expected value, and how it reaches dopamine neurons, is still under study.
- **How does this scale to human learning?** Human imaging studies support a similar role, but the signal measured is less direct than single-neuron recording.

## References

### Seminal papers

- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, linking reinforcement learning to the brain.
- Montague, P. R., Dayan, P. & Sejnowski, T. J. (1996). A framework for mesencephalic dopamine systems based on predictive Hebbian learning. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.16-05-01936.1996 — Proposes the predictive Hebbian framework that maps temporal-difference learning onto dopamine signals.
- Sutton, R. S. (1988). Learning to predict by the methods of temporal differences. *Machine Learning*. https://doi.org/10.1007/BF00115009 — Introduces temporal-difference learning, the algorithm whose error the dopamine signal is compared with.

### Surveys and reviews

- Schultz, W. (2016). Dopamine reward prediction-error signalling: a two-component response. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn.2015.26 — Reviews the evidence for an early, general response and a later, error-specific response in dopamine neurons.
- Dayan, P. & Daw, N. D. (2008). Decision theory, reinforcement learning, and the brain. *Cognitive, Affective, & Behavioral Neuroscience*. https://doi.org/10.3758/CABN.8.4.429 — Reviews how decision theory and reinforcement learning models relate to choice in the brain.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — The standard textbook on temporal-difference learning and the algorithm behind the prediction-error model.
