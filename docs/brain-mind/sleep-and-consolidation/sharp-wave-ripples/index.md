---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- memory
- sleep
aliases:
  - Sharp-Wave Ripples
  - SWR
  - SWRs
  - Hippocampal Ripples
  - 尖波漣波
  - 海馬迴漣波
---

# Sharp-wave ripples (Buzsáki et al., 1992)

Sharp-wave ripples are brief, highly synchronous events in the hippocampus. A sharp wave is a large, slow deflection of the local field potential, and the ripple is a fast oscillation, near 200 Hz in the CA1 region, that rides on it. These events carry hippocampal replay to the rest of the brain.

This page is part of [Sleep, Replay and Memory Consolidation](../index.md). The sequences these events carry are covered on [Hippocampal replay](../hippocampal-replay/index.md).

## Overview

A replay of a route needs many neurons to fire together in a short, ordered burst. Something in the circuit has to package that burst into one event, and the event has to be recognisable to the rest of the brain. Sharp-wave ripples are the best-studied candidate. They are visible as a distinct signal in the local field potential, which makes them easy to record and to detect in real time. For background on the hippocampus and memory, see [Memory & Learning in the Brain](../../memory-learning/index.md).

## Problem

Replay is observed as sequences of spikes, but which circuit event organises those spikes, and whether that event is needed for memory, were open questions. Recordings of the hippocampus during rest had shown rhythmic activity, but the link between that activity and memory had to be tested directly.

## Core idea

Ripples arise in the CA3 region, whose recurrent excitatory connections produce a burst of activity, the sharp wave. That burst drives a fast oscillation in CA1, the ripple. During each ripple, the spikes of CA1 neurons are coordinated so that they replay fragments of waking sequences in a compressed time frame. The ripple is thought to pass this representation to cortical and subcortical circuits, supporting consolidation. Buzsáki (2015) also argues that replay during ripples can combine recent and existing information, which may support decisions and planning.

## Equation or algorithm

Ripple detection follows a common procedure:

1. Filter the local field potential in the ripple band, usually a range around 150 to 250 Hz.
2. Compute the envelope of the filtered signal and mark periods where it exceeds a threshold, often set in standard deviations above the mean.
3. Keep events that last a minimum time, and check that they coincide with the sharp wave in the broader signal.
4. Use the detected events to trigger analyses of spiking, such as replay decoding, or to trigger stimulation in closed-loop experiments.

Thresholds and band limits vary between labs, so results from different studies are not always directly comparable.

## Results

- Buzsáki et al. (1992) reported transient CA1 network oscillations, near 200 Hz, during behavioural immobility, consummatory behaviour and slow-wave sleep. The pyramidal cells in the recordings fired at a lower rate than the oscillation, and their spikes were phase-locked to it.
- Girardeau et al. (2009) reported that selectively suppressing hippocampal ripples impairs spatial memory.
- Ego-Stengel and Wilson (2010) reported that disrupting ripple-associated hippocampal activity during rest impairs spatial learning in rats.
- Buzsáki (2015), a review, summarises that ripples occur during offline states linked to consummatory behaviour and non-REM sleep, and that disrupting them interferes with memory.

## Limitations

- **Suppression is not perfectly specific.** Methods that detect and disrupt ripples can also affect other activity. Conclusions depend on the controls used to rule this out.
- **Not every ripple replays.** Ripples vary in content and in the spiking they contain. Replay is a property of some ripples, not all of them.
- **The function is debated.** Consolidation, planning and creative thought are all proposed roles for ripple-linked replay, and the evidence for each is at different strengths.
- **Mostly rodent data.** Most detailed recordings come from rats and mice during spatial tasks and sleep.

## Connections

- **Replay.** Ripples carry the sequences described on [Hippocampal replay](../hippocampal-replay/index.md), so the two pages should be read together.
- **Complementary learning systems.** The proposal that ripples transfer information to the cortex is the mechanism that [Complementary Learning Systems](../../memory-learning/complementary-learning-systems/index.md) requires for interleaved training.
- **Sleep.** Ripples are linked to non-REM sleep and to the slow oscillations and spindles of that stage. The stage-level evidence is on the [chapter overview](../index.md).
- **Neuromodulation.** Buzsáki (2015) notes that neurotransmitters and neuromodulators influence ripple occurrence, which links ripples to the broader modulatory systems described on [Decision Making, Dopamine & Reward](../../decision-reward/index.md).

## Applications

- **Closed-loop neuroscience.** Systems that detect ripples in real time and switch them off or change them are used to test whether ripples are needed for memory. These are research tools, not clinical treatments.
- **Biomarkers.** Buzsáki (2015) proposes ripple activity as a cognitive biomarker for episodic memory and planning. The proposal is a research hypothesis that has not been validated for clinical use.

## Open questions

- **Are ripples needed for consolidation, planning or both?** Suppression studies support a role for memory, but planning and decision effects are still being separated from memory effects.
- **What decides which content is replayed in a ripple?** Models of prioritisation are candidates, but the rules are not established.
- **How do ripples relate to other sleep rhythms?** The timing of ripples relative to spindles and slow oscillations is still being mapped.
- **Do the same ripple mechanisms operate across mammals, including humans?** Comparative evidence is incomplete.

## References

### Seminal papers

- Buzsáki, G. et al. (1992). High-frequency network oscillation in the hippocampus. *Science* 256, 1025–1027. https://doi.org/10.1126/science.1589772 — Original description of the roughly 200 Hz CA1 oscillations during immobility, consummatory behaviour and slow-wave sleep, the events later identified as sharp-wave ripples.
- Girardeau, G., Benchenane, K., Wiener, S. I., Buzsáki, G. & Zugaro, M. B. (2009). Selective suppression of hippocampal ripples impairs spatial memory. *Nature Neuroscience* 12, 1222–1223. https://doi.org/10.1038/nn.2384 — Reports that suppressing ripples selectively impairs spatial memory, a key test of their function.
- Ego-Stengel, V. & Wilson, M. A. (2010). Disruption of ripple-associated hippocampal activity during rest impairs spatial learning in the rat. *Hippocampus* 20, 1–10. https://doi.org/10.1002/hipo.20707 — Reports that disrupting ripple-associated activity during rest impairs spatial learning in rats.

### Surveys and textbooks

- Buzsáki, G. (2015). Hippocampal sharp wave-ripple: A cognitive biomarker for episodic memory and planning. *Hippocampus* 25, 1073–1188. https://doi.org/10.1002/hipo.22488 — Long review of sharp-wave ripples, their circuit origin, and their roles in replay, memory consolidation and planning.
