---
status: complete
last_reviewed: 2026-10-28
related:
- theory/paradigms/meta-learning
tags:
- neuroscience
- reinforcement learning
- meta-learning
aliases:
  - Doya 2002
  - Metalearning and neuromodulation
  - 以神經調節實現的元學習
  - Neuromodulators as meta-parameters
  - 神經調節的元參數假說
---

# Meta-learning with neuromodulation (Doya, 2002)

Doya proposes that four neuromodulators each control one part of a reinforcement-learning algorithm. Dopamine carries the prediction error. Serotonin, noradrenaline and acetylcholine set three meta-parameters: the time scale of prediction, the randomness of action choice, and the speed of learning. The paper treats neuromodulation as a way for the brain to adjust how it learns, not only what it learns.

This page is part of [Neuromodulators beyond Dopamine](../index.md). The prediction error itself is covered on [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md), and is not repeated here.

## Overview

A reinforcement-learning agent has settings beyond its value rule. Its learning rate controls how far each outcome moves its estimates. Its discount factor controls how much future reward counts relative to immediate reward. Its choice rule controls how strictly it picks the best-valued option, which sets the balance between exploiting and exploring. These settings are meta-parameters, because they govern the learning process rather than being learned from data. A fixed setting suits only some environments. Doya asks whether the brain could change these settings as the environment changes, and whether neuromodulators are the mechanism.

## Key concepts

- **Discount factor** (γ): the weight given to future rewards relative to immediate ones. A value near 1 looks far ahead.
- **Inverse temperature** (β): the sharpness of a softmax choice rule. A high value makes the agent almost always pick the best-valued option, and a low value makes choice more random.
- **Learning rate** (α): the fraction of the prediction error used to update a value estimate.

## Problem

Reinforcement learning explains how dopamine might carry a prediction error, but it leaves open how the other settings are chosen. Several circuits could adjust them. Doya asks which neuromodulator might control each setting, and whether the choice follows from what the algorithm needs.

## Core idea

Doya links each neuromodulator to one component of the algorithm:

- **Dopamine** carries the temporal-difference error, the learning signal itself.
- **Serotonin** controls the discount factor, and so the time scale over which rewards are predicted.
- **Noradrenaline** controls the inverse temperature of the choice rule, and so the randomness of action selection and exploration.
- **Acetylcholine** controls the learning rate, the speed at which memory is updated.

The paper frames neuromodulators as global signals that regulate the distributed learning mechanisms of the brain. This gives the brain a route to adjust its own learning. The mapping is a proposal, but it gives each neuromodulator a precise computational job that can be tested against behaviour.

## Equation or algorithm

The standard algorithm, with $Q(s, a)$ the learned value of action $a$ in state $s$, is:

- Prediction error (SARSA form): $\delta_t = r_t + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t)$, with discount factor $\gamma$.
- Value update: $Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \, \delta_t$, with learning rate $\alpha$.
- Choice rule: $P(a \mid s) = \dfrac{\exp(\beta \, Q(s, a))}{\sum_{b} \exp(\beta \, Q(s, b))}$, with inverse temperature $\beta$.

In Doya's mapping, $\delta_t$ corresponds to dopamine, $\gamma$ to serotonin, $\beta$ to noradrenaline and $\alpha$ to acetylcholine. The update and choice rules are standard. The mapping is the paper's contribution.

## Results

The paper is a theoretical proposal and does not report a new experimental dataset. It states the mapping as a hypothesis: serotonin for the discount factor γ, noradrenaline for the inverse temperature β and acetylcholine for the learning rate α. This page does not summarise further experimental results from the paper.

## Limitations

- **A hypothesis, not a demonstration.** The paper presents the mapping as a proposal, based on a review of experimental data and theoretical models.
- **Several roles per system.** Neuromodulators act across many circuits and have several effects. A one-to-one mapping to a single parameter simplifies this.
- **Scalar settings.** The model treats each meta-parameter as one number. Neural control may vary across regions and over time.
- **How settings are chosen.** The proposal says which signal sets which parameter, but not how the values change over time. That needs an additional learning mechanism.

## Connections

- **Reinforcement learning.** The three meta-parameters and the prediction error are components of the algorithm covered on [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md).
- **Model-based and model-free control.** The discount factor and inverse temperature affect how an agent trades off cached values against planning. See [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md).
- **Decision making.** How noradrenaline and dopamine affect choice is covered on [Decision Making, Dopamine & Reward](../../decision-reward/index.md).
- **Meta-learning in AI.** Adjusting the learning algorithm itself is the central concern of [Meta-Learning](../../../theory/paradigms/meta-learning/index.md).
- **Adaptive optimisers.** Per-parameter learning-rate control, such as [Adam](../../../theory/optimization/adaptive/adam.md), solves a related practical problem. It is not a neuromodulatory model.

## Applications

- **Adaptive reinforcement learning.** Reinforcement-learning systems often tune the discount factor, learning rate and exploration temperature by hand. Doya's mapping gives each a biological interpretation and suggests they could adapt as the environment changes.
- **Computational psychiatry.** Fitting learning-rate and choice-sharpness parameters to behaviour is a standard way to study individual differences in choice. These are the kinds of parameters Doya's mapping assigns to neuromodulators. See [Decision Making, Dopamine & Reward](../../decision-reward/index.md) for context.

## Open questions

- **Which neuromodulator controls which setting?** The mapping is a proposal, and each assignment needs its own test.
- **How are the settings learned?** The proposal needs a rule for changing them over time, and the neural mechanism for that rule is not yet clear.
- **Are neuromodulators the only controllers?** Changes in cortical connectivity or in other areas could also set these parameters, and their relative roles are unknown.

## References

### Seminal papers

- Doya, K. (2002). Metalearning and neuromodulation. *Neural Networks*, 15(4–6), 495–506. https://doi.org/10.1016/s0893-6080(02)00044-8 — The original paper. Proposes that dopamine, serotonin, noradrenaline and acetylcholine correspond to the prediction error and three reinforcement-learning meta-parameters.

- Yu, A. J. & Dayan, P. (2005). Uncertainty, Neuromodulation, and Attention. *Neuron*, 46(4), 681–692. https://doi.org/10.1016/j.neuron.2005.04.026 — Proposes that acetylcholine and noradrenaline signal expected and unexpected uncertainty, an alternative account of the same two neuromodulators.

### Surveys and textbooks

- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*, 11(4), 410–416. https://doi.org/10.1038/nn2077 — Review of neuromodulators and decision making.
- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — Reviews the noradrenaline system and its tonic and phasic modes, which relate to the proposal's role for noradrenaline in action selection.
- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*, 16(6), 710–715. https://doi.org/10.1016/j.conb.2006.09.002 — Reviews acetylcholine's role in learning and memory, relevant to the learning-rate mapping on this page.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — Standard introduction to reinforcement learning, which covers the discount factor, learning rate and softmax choice rule used on this page.
