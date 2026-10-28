---
status: draft
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
  - 元學習與神經調節
  - Meta-parameters
---

# Metalearning and Neuromodulation (Doya, 2002)

Doya proposed that four neuromodulators, dopamine, serotonin, noradrenaline and acetylcholine, each regulate one of the meta-parameters of reinforcement learning. It is the classic computational account of why neuromodulators matter for learning, and it sits within the wider [Neuromodulation Beyond Dopamine](../index.md) topic.

## Overview

Reinforcement-learning algorithms have settings that are not learned from data. These include how quickly values change after each experience, how far into the future rewards are counted, and how strongly choices follow the current value estimates. Engineers choose these settings by hand, and a poor choice can make learning slow or unstable. Biological agents seem to adjust them as circumstances change, for example becoming more patient or more exploratory.

Doya asked whether the brain's neuromodulatory systems might be the machinery for this adjustment. Each of the four systems projects widely across the cortex and subcortex, which suits a signal that tunes many circuits at once. The paper proposes a specific assignment of functions. It is a theoretical proposal, and its value lies in making testable predictions about which system should change which parameter.

## Key concepts

- **Meta-parameter**: a setting of a learning algorithm that controls how it learns, rather than a quantity it learns. Doya considered the learning rate, the discount factor and the inverse temperature.
- **Learning rate ($\alpha$)**: how far a value estimate moves towards each new prediction error. A high learning rate tracks change quickly but is noisy.
- **Discount factor ($\gamma$)**: how much a reward is worth relative to the same reward one step later. A factor near 1 favours long-term outcomes, and a lower one favours immediate ones.
- **Inverse temperature ($\beta$)**: how strongly action choice favours the highest-valued option. A high value exploits current knowledge, and a low value explores.
- **Temporal-difference error**: the difference between the reward received and the reward predicted, adjusted for the value of the next state. It is the training signal of temporal-difference learning.

## How it works

In standard temporal-difference learning, the value of a state is updated by the error $\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)$, scaled by the learning rate: $V(s_t) \leftarrow V(s_t) + \alpha\,\delta_t$. Actions are chosen with a softmax policy, so that the probability of choosing action $a$ in state $s$ is $\exp(\beta Q(s,a))$ normalised over all actions. The three parameters $\alpha$, $\gamma$ and $\beta$ are fixed in the basic algorithm.

Doya's proposal assigns each neuromodulator to one of these quantities:

1. **Dopamine** carries the temporal-difference error $\delta_t$ itself. This follows the experimental work described in [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).
2. **Serotonin** regulates the discount factor $\gamma$, and so the time horizon over which rewards are weighed.
3. **Noradrenaline** regulates the inverse temperature $\beta$, and so the balance between exploitation and exploration.
4. **Acetylcholine** regulates the learning rate $\alpha$, and so how quickly memories are updated.

The mapping is a hypothesis about function. Each step can be read as an engineering statement: if the brain could change $\gamma$, $\beta$ or $\alpha$ in response to the situation, it would change how the agent plans, chooses and learns. The paper argues that the anatomy of each system is consistent with this role, though the projections are diffuse, so the mapping is an idealisation.

## Results

Doya's paper is primarily a theoretical proposal. It supports the mapping in two ways. First, it draws on anatomical and physiological findings about where each neuromodulator is released and what its receptors do. Second, it shows, in computational terms, what happens to learning and behaviour when each meta-parameter is changed. The paper's central result is the mapping itself, and this page quotes no numbers from it. Readers who need the details of any simulation should consult the paper directly.

## Limitations

- **The mapping is a hypothesis.** One neuromodulator controlling one parameter is an idealisation. Real systems interact, and each neuromodulator has several effects that do not fit a single parameter.
- **The serotonin assignment is contested.** Later reviews, including Dayan and Huys (2009), describe serotonin in terms of aversive processing and punishment, which is not the same as a discount factor.[^1]
- **The biological implementation is left open.** The paper does not specify how a neuromodulator level would be translated into the value of a parameter.
- **Meta-parameters may be represented elsewhere.** Some of the adjustment may happen in the cortex or the basal ganglia rather than through neuromodulators.

## Open questions

- **Causal tests.** Can changing one neuromodulator's activity change the corresponding parameter, and only that parameter, in a behavioural model? Pharmacology and optogenetics offer possible tests.
- **Can the agent learn its own meta-parameters?** Schweighofer and Doya (2003) examine adapting meta-parameters during learning. The question is whether the adjustment can be learned rather than set by hand, and how stable such learning is.
- **Does the mapping extend to model-based learning?** The proposal was framed around model-free learning. Whether the same parameters control planning and model-based control is less clear.

## References

### Seminal papers

- Doya, K. (2002). Metalearning and neuromodulation. *Neural Networks*. https://doi.org/10.1016/S0893-6080(02)00044-8 — The paper itself. It proposes that the four neuromodulators regulate the meta-parameters of reinforcement learning.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, the signal that Doya assigns to dopamine.
- Schweighofer, N. & Doya, K. (2003). Meta-learning in Reinforcement Learning. *Neural Networks*. https://doi.org/10.1016/S0893-6080(02)00228-9 — Studies how the meta-parameters of a reinforcement learner can be adapted during learning, building on the neuromodulatory view.

### Surveys and textbooks

- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*. https://doi.org/10.1038/nn2077 — Reviews how neuromodulators shape decisions and relates them to reinforcement-learning parameters.
- Dayan, P. & Huys, Q. J. M. (2009). Serotonin in Affective Control. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.051508.135607 — Reviews serotonin's role in appetitive and aversive control, and why it may only partly mirror dopamine.

### Articles and documentation

- Najarro, E. & Risi, S. (2020). Meta-Learning through Hebbian Plasticity in Random Networks. *arXiv*. https://arxiv.org/abs/2007.02686 — Searches for Hebbian learning rules that let agents adapt their own networks over their lifetime, a machine analogue of learned plasticity.

[^1]: Dayan and Huys (2009) argue that serotonin's computational role concerns aversive processing, and that its statistics differ from dopamine's because punishments and rewards are asymmetric in nature. This is a view that competes with Doya's discount-factor assignment.
