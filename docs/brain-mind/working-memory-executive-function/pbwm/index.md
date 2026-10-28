---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
tags:
- working memory
- gating
- basal ganglia
- reinforcement learning
aliases:
  - PBWM
  - Prefrontal basal ganglia working memory
  - 前額葉基底核工作記憶
  - O'Reilly and Frank 2006
---

# Prefrontal basal ganglia working memory (PBWM)

PBWM is a computational model in which the prefrontal cortex (PFC) holds task information, while the basal ganglia decide when that information is allowed to change. The gate is learned from a reinforcement signal modelled on dopamine, so the system learns both what to store and when to store it. O'Reilly and Frank (2006) introduced the model.

This page is one method within [Working Memory and Executive Function](../index.md). For the wider picture of how persistent activity and synaptic states compare, see that overview.

## Overview

Consider a task in which a cue must be remembered across a delay, and an unrelated distractor appears in the middle. Useful memory has to protect the cue from the distractor, but still let relevant new information replace old information. PBWM handles this by dividing the job. The prefrontal cortex is the store, and the basal ganglia act as a gate in front of it.

O'Reilly and Frank describe their aim as deconstructing the "homunculus" of executive function: the idea that some inner agent decides what to hold, without any mechanism that explains how. PBWM gives that agent a mechanism that can be learned.

## Problem

Executive control is often described as if a controller inside the brain decides what to hold and what to do with it. The mechanism behind that controller has been hard to specify. The question is how a system can learn to control its own working memory: which information to keep, when to overwrite it, and when to ignore input.

The learning problem is hard for two reasons. First, the consequence of a gating decision may appear only after a long delay, so the credit must be assigned across time. Second, many prefrontal units could have changed, so the credit must also be assigned across units.

## Core idea

PBWM has three parts that work together.

- **Prefrontal cortex.** Maintains task representations and updates them only when a gate allows it.
- **Basal ganglia.** Provide a dynamic gate that decides whether the current input updates a prefrontal representation.
- **Dopamine-like learning.** The midbrain, basal ganglia and amygdala form an actor–critic architecture. The critic learns which prefrontal representations are task relevant and trains the actor, which supplies the gate.

The authors say the learning mechanism is designed to solve both credit assignment problems at once.

## Equation or algorithm

The paper gives the full learning rule. This page gives the outline as numbered steps rather than a single equation.

1. An input arrives. Gate units in the basal ganglia decide whether it should update a set of prefrontal units or be ignored.
2. If the gate opens, the prefrontal representation is overwritten. If it stays closed, the previous contents are kept, so information survives distractors.
3. The task produces an outcome. The critic compares its prediction with what happened. The difference is a prediction error of the kind described in the [dopamine reward prediction error](../../neuroscience/dopamine-reward-prediction-error/index.md) page, and it plays the same role as in the actor–critic methods covered in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
4. The prediction error trains the critic and the actor. Future gating decisions then favour updates that proved useful.

## Results

On the 1-2-AX working memory task and other benchmark working memory tasks, the authors report that PBWM performs favourably compared with standard backpropagation-based temporal learning mechanisms. The comparison is the paper's main evidence for the learning rule.

## Limitations

- **Benchmark scope.** The advantage is shown on the authors' chosen working memory tasks against chosen baselines. It is not evidence of general superiority.
- **Anatomical simplification.** The model assigns roles to basal ganglia and prefrontal circuits at a level that simplifies real anatomy and cell types.
- **Biological plausibility.** The model is argued to fit known circuits, but the specific learning rule is a hypothesis to test rather than a measured mechanism.
- **Earlier work.** An earlier computational model of frontal cortex and basal ganglia interaction in working memory (Frank, Loughry & O'Reilly, 2001) addresses a closely related question. PBWM's contribution is its learning mechanism.

## Connections

- **Executive control theory.** PBWM is consistent with the bias-signal account of prefrontal control proposed by Miller and Cohen (2001), and offers a learning mechanism for it.
- **Dopamine and reinforcement learning.** The learning signal is the same family as the prediction error that [Decision Making, Dopamine & Reward](../../decision-reward/index.md) discusses in the context of choice.
- **Related prefrontal models.** Rougier et al. (2005) show how a related PFC model can self-organise abstract, rule-like representations through experience.
- **AI: gated memory.** The LSTM uses learned gates that decide what enters and leaves a memory cell ([LSTM](../../../theory/models/rnn/gated-cells/lstm/index.md)). The functional resemblance to PBWM is clear, though the two systems are built differently.

## Applications

- **Modelling prefrontal tasks.** PBWM was tested on working memory benchmarks such as the 1-2-AX task. Related frontal models have been used to simulate performance on Stroop and Wisconsin card sorting, in both intact and frontally damaged people (Rougier et al., 2005).
- **Designing gated memory in AI.** Learned gates that protect a memory store are a core design in recurrent networks, as in the LSTM.

## Open questions

- **Which signals train the gate in a real brain, and when?** The model assumes a dopamine-like teaching signal, but the exact timing and targets of that signal in gating are still under study.
- **Does gating scale beyond benchmarks?** It is unclear how far a learned gate of this kind extends to richer, real-world tasks with many interacting goals.
- **How does gating relate to attention?** Gating decides what enters memory, and attention decides what is selected for processing. How the two are coupled is not settled.

## References

### Seminal papers

- O'Reilly, R. C. & Frank, M. J. (2006). Making working memory work: a computational model of learning in the prefrontal cortex and basal ganglia. *Neural Computation*. https://doi.org/10.1162/089976606775093909 — The original PBWM paper, which introduces the learned gate and the actor–critic learning rule.
- Frank, M. J., Loughry, B. & O'Reilly, R. C. (2001). Interactions between frontal cortex and basal ganglia in working memory: a computational model. *Cognitive, Affective, & Behavioral Neuroscience*. https://doi.org/10.3758/CABN.1.2.137 — An earlier computational model of interactions between frontal cortex and basal ganglia in working memory, the same interaction that PBWM models.
- Rougier, N. P., Noelle, D. C., Braver, T. S., Cohen, J. D. & O'Reilly, R. C. (2005). Prefrontal cortex and flexible cognitive control: rules without symbols. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.0502455102 — Shows how a related PFC model forms abstract rule-like representations and simulates Stroop and card-sorting behaviour.
- Hochreiter, S. & Schmidhuber, J. (1997). Long short-term memory. *Neural Computation*. https://doi.org/10.1162/neco.1997.9.8.1735 — Introduces the LSTM, whose multiplicative gate units learn to open and close access to a memory cell.

### Surveys and textbooks

- Miller, E. K. & Cohen, J. D. (2001). An integrative theory of prefrontal cortex function. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.24.1.167 — Reviews evidence for the PFC as a source of goal-directed bias signals, a framework that PBWM is consistent with.
