---
status: draft
last_reviewed: 2026-10-28
related:
- theory/paradigms/reinforcement-learning/exploration
tags:
- neuroscience
- reinforcement learning
- exploration
aliases:
  - Aston-Jones and Cohen 2005
  - Adaptive gain
  - 適應性增益
  - 藍斑去甲腎上腺素
  - Locus coeruleus
---

# Locus Coeruleus Adaptive Gain (Aston-Jones and Cohen, 2005)

Aston-Jones and Cohen proposed that the noradrenergic locus coeruleus works in two modes, phasic and tonic. Phasic bursts favour exploiting the current task, and sustained tonic activity favours disengaging and searching for alternatives. The theory is one of the three method accounts in [Neuromodulation Beyond Dopamine](../index.md).

## Overview

The locus coeruleus is a small nucleus in the brainstem that sends noradrenaline to almost the entire brain. For decades it was linked mainly to arousal and stress. Aston-Jones and Cohen argued that a more specific role emerges when its activity is studied during behaviour. Recordings in monkeys showed that its neurons change their firing in a task-dependent way, and that these changes relate to how well the animal is doing.

The paper's theory is called adaptive gain. The locus coeruleus is proposed to change how strongly the brain's target circuits respond to their inputs, so that the same stimulus has more or less effect depending on the animal's current state. The theory explains how this change can help performance on the current task and how it can prompt a switch to another task.

## Key concepts

- **Phasic mode**: brief bursts of locus coeruleus firing, tied to task-relevant events such as the outcome of a decision.
- **Tonic mode**: a sustained, background level of firing. In the theory it is associated with lower task utility and with searching for alternatives.
- **Adaptive gain**: the proposal that noradrenaline sets the sensitivity of target neurons, so that responses to task-relevant stimuli are sharpened or flattened.
- **Utility**: how valuable the current task is, relative to what else the animal could do. The theory proposes that frontal cortex estimates utility and drives the locus coeruleus.
- **Exploitation and exploration**: staying with the current best option versus trying others. The two modes are proposed to implement a trade-off between them.

## How it works

The theory describes a loop between the frontal cortex and the locus coeruleus. In a numbered summary, in our own words and not as an equation from the paper:

1. Frontal areas, including the anterior cingulate and orbitofrontal cortices, monitor how useful the current task is.
2. When the task is useful, the locus coeruleus produces phasic bursts after task-relevant outcomes. Target circuits respond more sharply to task-relevant inputs, which favours continuing with the task.
3. When the utility of the task falls, the locus coeruleus shifts to a tonic mode. Its target circuits respond less selectively, which favours disengaging from the task and searching for alternatives.
4. Over short and long timescales, the balance between these modes is proposed to keep performance close to the best achievable.

The theory is a systems-level account. It does not specify the neuron-level computation inside the target circuits, and it links the modes to behaviour through the frontal inputs rather than through a formal learning rule.

## Results

The evidence comes from neurophysiological recordings in monkeys and from modelling studies, as the paper's abstract describes. The main finding is that locus coeruleus neurons show phasic responses tied to task outcomes and tonic changes that accompany shifts in behaviour, including disengagement from a task. The paper argues that these patterns support the proposed trade-off between exploitation and exploration. It is a review and synthesis, and this page quotes no numbers from it.

## Limitations

- **The evidence is mostly from monkeys.** The theory extends to other species and to humans by inference, and the mapping of the two modes onto human behaviour is not established.
- **The link to behaviour is partly correlational.** Showing that tonic activity accompanies disengagement is not the same as showing that it causes it.
- **The source of the utility signal is itself a hypothesis.** The theory relies on frontal areas computing task utility, which is supported by connections but not fully tested.
- **Other accounts emphasise different roles.** Bouret and Sara (2005) propose that phasic bursts reset cortical networks, which is a related but distinct view.

## Open questions

- **How heterogeneous is the locus coeruleus?** Its neurons may not all follow the same pattern, and different projections may serve different functions.
- **How is utility computed?** The theory requires a precise estimate of task value. How the frontal cortex computes it, and how that estimate is passed to the locus coeruleus, remains open.
- **Does the trade-off hold in humans?** Human studies of exploration, such as those that examine random and directed exploration, could test the predictions more directly.
- **How do noradrenaline and dopamine interact?** Both are linked to exploration and to reward, and their combined effect is not yet clear.

## References

### Seminal papers

- Aston-Jones, G. & Cohen, J. D. (2005). An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.28.061604.135709 — The paper itself. It proposes that the phasic and tonic modes of the locus coeruleus implement a trade-off between exploitation and exploration.
- Yu, A. J. & Dayan, P. (2005). Uncertainty, neuromodulation, and attention. *Neuron*. https://doi.org/10.1016/j.neuron.2005.04.026 — Proposes a complementary account of noradrenaline, in which unexpected uncertainty drives its release.
- Schultz, W., Dayan, P. & Montague, P. R. (1997). A Neural Substrate of Prediction and Reward. *Science*. https://doi.org/10.1126/science.275.5306.1593 — Shows that dopamine neurons signal reward prediction errors, the reward-learning signal the locus coeruleus account complements.

### Surveys and textbooks

- Sara, S. J. (2009). The locus coeruleus and noradrenergic modulation of cognition. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2573 — Reviews how the locus coeruleus and noradrenaline influence attention, memory and cognitive control.
- Bouret, S. & Sara, S. J. (2005). Network reset: a simplified overarching theory of locus coeruleus noradrenaline function. *Trends in Neurosciences*. https://doi.org/10.1016/j.tins.2005.09.002 — Proposes that bursts of locus coeruleus activity reset cortical networks after salient events.
- Doya, K. (2008). Modulators of decision making. *Nature Neuroscience*. https://doi.org/10.1038/nn2077 — Reviews how neuromodulators shape decisions and relates them to reinforcement-learning parameters.
- Hasselmo, M. E. (2006). The role of acetylcholine in learning and memory. *Current Opinion in Neurobiology*. https://doi.org/10.1016/j.conb.2006.09.002 — Reviews acetylcholine's proposed effects on encoding and retrieval, for comparison with noradrenaline's role.
