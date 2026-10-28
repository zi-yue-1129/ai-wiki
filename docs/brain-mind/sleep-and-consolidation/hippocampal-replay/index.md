---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- memory
- sleep
aliases:
  - Hippocampal Replay
  - Reverse Replay
  - 海馬迴重播
  - 反向重播
  - 序列重播
---

# Hippocampal replay (Foster & Wilson, 2006)

Hippocampal replay is the reactivation of neuron firing sequences that were recorded during an experience, seen again later while an animal rests or sleeps. Foster and Wilson (2006) showed that awake rats replay these sequences in reverse order, immediately after running.

This page is part of [Sleep, Replay and Memory Consolidation](../index.md). The network event that carries replay is covered on [Sharp-wave ripples](../sharp-wave-ripples/index.md).

## Overview

Place cells are hippocampal neurons that fire when an animal is in a particular location. As an animal runs a route, place cells fire in a fixed order, so their sequence traces the path. Replay means that the same order appears again later, outside the experience itself and often at a faster speed. Replay therefore carries information about the past in a compressed form. This is useful if the brain has to store or evaluate that past without running it again.

## Problem

The hippocampus is needed to form new episodic memories, as patient H.M. showed (see [Memory & Learning in the Brain](../../memory-learning/index.md)). The open question was how information leaves the hippocampus. Replay offered one answer: if the hippocampus repeats recent sequences, the neocortex can learn from them. That answer depends on whether replay happens at all, and whether it happens while the animal is awake as well as asleep.

## Core idea

Wilson and McNaughton (1994) recorded many place cells at once. They found that the patterns that represented a rat's path during running were reactivated in later sleep. Skaggs and McNaughton (1996) reported replay of firing sequences during sleep after spatial experience. Foster and Wilson (2006) then recorded awake rats. Immediately after running, the sequences of place cells replayed in the reverse order of the run. Diba and Buzsáki (2007) found that sequences run both forward and in reverse during the ripple events described on the [sharp-wave ripples](../sharp-wave-ripples/index.md) page.

Reverse order matters because it links an outcome back to the states that led to it. Foster and Wilson suggested that this could support the evaluation of event sequences, as in reinforcement-learning models.

## Equation or algorithm

Replay has no single equation. The measure is a procedure for detecting it:

1. Record the spiking of many place cells during a run, and estimate for each cell the location where it fires most.
2. In a later rest or sleep period, find bursts of population activity.
3. For each burst, decode the location each active cell represents, and order the cells by when they fire.
4. Compare that order with the order of the run. A close forward or reverse match is evidence of replay, and it is judged against shuffled controls that break the sequence.

## Results

- Replay of waking place-cell patterns has been observed during sleep (Wilson & McNaughton, 1994; Skaggs & McNaughton, 1996).
- Awake replay after running has been observed, and in the Foster and Wilson (2006) study the sequences ran in reverse order.
- Sequences run forward and in reverse during sharp-wave ripples (Diba & Buzsáki, 2007).
- Mattar and Daw (2018) built a normative model in which each candidate memory is ranked by its utility, defined as the gain in future reward from updating it multiplied by the discounted number of future visits the agent is expected to make to the state it concerns. The model explains both forward replay, which helps plan ahead, and reverse replay, which links outcomes back to earlier actions.

## Limitations

- **Observation is not causation.** Replay shows that a sequence is reactivated, but not that the reactivation is what makes the memory last. Causal tests have mostly come from disrupting the ripples that carry replay (see [Sharp-wave ripples](../sharp-wave-ripples/index.md)).
- **Decoding depends on choices.** Reconstructing the order of cells depends on how place fields are estimated and on the statistical controls used. Conclusions depend on these choices.
- **Evidence is mostly from rodents in spatial tasks.** Replay in other species and tasks is less well characterised.
- **The function of reverse replay is contested.** Foster and Wilson linked it to evaluation of event sequences, while Mattar and Daw linked it to planning. Later work has not settled which account is right.

## Connections

- **Brain.** Replay is carried by [sharp-wave ripples](../sharp-wave-ripples/index.md). The idea that replay trains the neocortex is the core of [Complementary Learning Systems](../../memory-learning/complementary-learning-systems/index.md), and the broader memory picture is on [Memory & Learning in the Brain](../../memory-learning/index.md).
- **Reward and value.** The evaluation idea links replay to the prediction-error signal in [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).
- **Planning.** If replay simulates future routes or outcomes, it is related to the model-based control described on [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md).
- **AI.** The machine counterpart is [experience replay](../experience-replay/index.md). Both reuse stored experience in a different order from the one in which it happened.

## Applications

- **Neuroscience research.** Replay is read out from recordings of place cells during rest and sleep, and used as a measure of memory processing in experiments that change sleep or rest. These are research tools.

## Open questions

- **Which events are replayed, and why?** Mattar and Daw's utility account is one candidate. Its predictions for specific events are still being tested.
- **Do sleep and waking replay have the same function?** Their roles in consolidation and planning may differ.
- **How does replay change cortex?** The route from hippocampal replay to lasting cortical change is still under study.
- **Does replay in humans look like replay in rodents?** Evidence is growing, but it is harder to obtain.

## References

### Seminal papers

- Foster, D. J. & Wilson, M. A. (2006). Reverse replay of behavioural sequences in hippocampal place cells during the awake state. *Nature* 440, 680–683. https://doi.org/10.1038/nature04587 — Shows that place-cell sequences replay in reverse order during waking rest after running in rats, and suggests a link to reinforcement-learning evaluation.
- Wilson, M. A. & McNaughton, B. L. (1994). Reactivation of hippocampal ensemble memories during sleep. *Science* 265, 676–679. https://doi.org/10.1126/science.8036517 — Reports that patterns of hippocampal place-cell activity from waking experience reactivate during sleep.
- Skaggs, W. E. & McNaughton, B. L. (1996). Replay of neuronal firing sequences in rat hippocampus during sleep following spatial experience. *Science* 271, 1870–1873. https://doi.org/10.1126/science.271.5257.1870 — Reports replay of place-cell firing sequences during sleep after spatial experience.
- Diba, K. & Buzsáki, G. (2007). Forward and reverse hippocampal place-cell sequences during ripples. *Nature Neuroscience* 10, 1241–1242. https://doi.org/10.1038/nn1961 — Reports that place-cell sequences run both forward and in reverse during sharp-wave ripples.
- Mattar, M. G. & Daw, N. D. (2018). Prioritized memory access explains planning and hippocampal replay. *Nature Neuroscience* 21, 1609–1617. https://doi.org/10.1038/s41593-018-0232-z — Proposes that replay is ranked by utility, explaining forward planning and reverse replay in simulated navigation.

### Surveys and textbooks

- Davidson, T. J., Kloosterman, F. & Wilson, M. A. (2009). Hippocampal replay of extended experience. *Neuron* 63, 497–507. https://doi.org/10.1016/j.neuron.2009.07.027 — Reports hippocampal replay of extended spatial experience, beyond the short sequences of earlier studies.
- Wittkuhn, L. et al. (2021). Replay in minds and machines. *Neuroscience & Biobehavioral Reviews* 129, 367–388. https://doi.org/10.1016/j.neubiorev.2021.08.002 — Reviews the computational functions of replay in neuroscience and machine learning, with the two fields compared.
