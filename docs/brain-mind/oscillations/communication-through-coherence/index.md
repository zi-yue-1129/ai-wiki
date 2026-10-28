---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- neural oscillations
- synchrony
aliases:
  - 透過相干性的通訊
  - Communication through Coherence
  - CTC
  - Neuronal coherence
---

# Communication through coherence (Fries, 2005)

Communication through coherence is a hypothesis proposed by Pascal Fries in 2005. It holds that the effectiveness of signals sent from one group of neurons to another depends on whether their rhythmic activity is coherent, meaning that the phase relation between the two rhythms is stable over time. It is one of the main proposals linking neural oscillations to cognition. It is part of [Neural Oscillations and Synchrony](../index.md).

## Problem

Two brain areas can be densely connected, yet a receiving area is driven by many inputs at once. What decides which signals get through and which are ignored? Anatomical wiring is fixed on the timescale of learning, but selection has to change from moment to moment. The question is what dynamic mechanism can switch the effect of an existing connection on and off.

## Core idea

Fries (2005) proposed that neuronal communication is carried by neuronal coherence, so that a flexible pattern of coherence defines a flexible communication structure. The later review by the same author (Fries, 2015) states the mechanism more specifically. Gamma-band synchronisation modulates excitation so that it escapes the inhibition that follows and activates postsynaptic neurons effectively. It also makes a presynaptic activation pattern arrive at postsynaptic neurons in a temporally coordinated way. Because the phase relation can change, the same anatomical connection can carry different signals at different times.

## Equation or algorithm

The method is a measurement procedure rather than a single equation:

1. Record two signals, such as local field potentials from two sites or two electrodes.
2. Band-pass filter both signals to the frequency band of interest, and extract the phase of each at each time point.
3. Compute coherence from the phase difference: a normalised measure that is larger when the phase difference stays consistent across time or repeated trials.
4. Compare coherence between conditions, such as an attended and an unattended stimulus, to test whether the coupling changes with the task.

## Results

Womelsdorf et al. (2007) tested the account directly with neuronal recordings. They found that the mutual influence between neuronal groups depended on the phase relation between their rhythmic activities. The phase relations that supported an interaction came a few milliseconds before the interaction itself, which the authors read as consistent with a mechanistic role. The effects were specific in time, frequency and space. The authors concluded that the pattern of synchronisation flexibly determines the pattern of neuronal interactions.

Bosman et al. (2012) examined the attention side of the account in monkey visual cortex. When two stimuli drove separate sites in V1 and both drove the same V4 site equally strongly, primarily the behaviourally relevant stimulus became gamma-synchronised with V4. The authors propose that selective synchronisation makes the relevant input effective.

The evidence is largely correlational, which supports the hypothesis without establishing it fully.

## Limitations

- **Correlation is not causation.** Two groups can become coherent because they share a common input, without either one influencing the other. Showing that coherence changes communication requires manipulating the rhythm itself.
- **Analysis choices matter.** Coherence depends on the frequency band, the window length and the choice of reference signal. Reported effects can depend on these decisions, so comparisons between studies need care.
- **Which band?** The hypothesis is a framework, not a claim about one fixed frequency. In Bosman et al. (2012), the gamma activity of the different sites overlapped substantially in frequency, so the band that carries coherence is not sharply defined. Whether gamma is the right band for inter-area communication, and whether it differs between areas and tasks, is still debated.

## Connections

- **Theta–gamma coupling.** [Theta–gamma coupling](../theta-gamma-coupling/index.md) is the other rhythm-based method in this chapter. The two differ in scope: coherence concerns communication between groups, while theta–gamma coupling concerns how one circuit organises its own items.
- **Attention.** Coherence was proposed as a mechanism for selective attention (Fries, 2015). The topic is covered on the wiki's [Attention in Brains & Machines](../../attention-brain-machine/index.md) page.
- **Recording.** Coherence is computed from the local field potential, ECoG and EEG signals described on [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md).
- **Artificial networks.** Standard artificial networks have no phase, so the idea has no direct counterpart. The nearest analogy is gating in attention mechanisms, which select information by learned weights rather than by timing. That is a loose conceptual link, not evidence that the two work the same way.

## Applications

- **Research on neural communication.** The framework gives a testable prediction: changing the phase relation between two areas should change their interaction. This makes it a research tool for studies of attention and perception, using the signals listed above.

## Open questions

- Is phase alignment the mechanism of communication, or a readout of it that appears alongside communication?
- Which frequency bands carry communication between which areas, and how does this change with the task?
- Can coherence be estimated reliably from noisy human recordings, and how much do the estimates depend on analysis choices?

## References

### Seminal papers

- Fries, P. (2005). A mechanism for cognitive dynamics: neuronal communication through neuronal coherence. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2005.08.011 — The original proposal, which names neuronal coherence as the mechanism of communication between neuronal groups.
- Womelsdorf, T. et al. (2007). Modulation of neuronal interactions through neuronal synchronization. *Science*. https://doi.org/10.1126/science.1139597 — Recordings showing that interactions between neuronal groups depend on the phase relation of their rhythms, a few milliseconds ahead of the interaction.
- Bosman, C. et al. (2012). Attentional stimulus selection through selective synchronization between monkey visual areas. *Neuron*. https://doi.org/10.1016/j.neuron.2012.06.037 — Monkey recordings showing that, when two stimuli drive V1, the behaviourally relevant one becomes gamma-synchronised with V4.

### Surveys and textbooks

- Fries, P. (2015). Rhythms for cognition: communication through coherence. *Neuron*. https://doi.org/10.1016/j.neuron.2015.09.034 — Review by the author of the hypothesis, on how gamma-band synchronisation shapes communication between groups and how attention acts on it.
- Fries, P. (2009). Neuronal gamma-band synchronization as a fundamental process in cortical computation. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.051508.135603 — Review arguing that gamma-band synchronisation selects one of several converging inputs, a basic operation of cortical computation.
- Womelsdorf, T. & Fries, P. (2009). Selective attention through selective neuronal synchronization. In *The Cognitive Neurosciences*, MIT Press. https://doi.org/10.7551/mitpress/8029.003.0028 — Book chapter on selective attention through selective neuronal synchronisation, the subject given in its title.
