---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- episodic memory
aliases:
  - 相位-振幅耦合
  - 跨頻耦合
  - 調變指數
  - Phase-Amplitude Coupling
  - Cross-Frequency Coupling
  - Modulation Index
  - Tort 2010
---

# Phase-Amplitude Coupling and the Modulation Index

Phase-amplitude coupling is the dependence of a fast oscillation's amplitude on the phase of a slower one. Tort and colleagues (2010) introduced a measure for it, the modulation index, which reduces the strength of coupling to a single number. This page is one of the methods on [Neural Oscillations and Synchrony](../index.md).

## Overview

Brain rhythms do not only run side by side. In the hippocampus and neocortex, the amplitude of fast gamma oscillations often rises and falls with the phase of a slower theta rhythm. Canolty and colleagues (2006) reported this in human cortex. The phenomenon is called cross-frequency coupling. The most studied case is theta–gamma coupling, which is linked to memory (see the Connections section of the [topic page](../index.md)).

Measuring coupling is harder than describing it, because a measure must be compared with chance. The index of Tort and colleagues was built with this in mind.

## Key concepts

- **Cross-frequency coupling (CFC)**: an interaction in which the phase of a slow oscillation modulates the amplitude of a fast one.
- **Phase**: the position of the slow oscillation within its cycle, obtained from the band-pass-filtered signal, usually with the Hilbert transform.
- **Amplitude envelope**: the smoothly varying strength of the fast oscillation, also obtained with the Hilbert transform.
- **Phase bin**: a slice of the slow cycle, for example 20 degrees wide.
- **Surrogate data**: shuffled or time-shifted versions of the recording, used to estimate chance coupling.

## How it works

The analysis follows a fixed sequence of steps.

1. Band-pass filter the recording in a slow band (the phase band) and in a faster band (the amplitude band).
2. Use the Hilbert transform to obtain the instantaneous phase $\phi(t)$ of the slow signal and the amplitude envelope $A(t)$ of the fast one.
3. Divide the phase range into $N$ bins.
4. In each bin $j$, average the fast amplitude to get $A_j$, and normalise to a distribution, $p_j = A_j / \sum_k A_k$.
5. Compute the entropy of this distribution, $H = -\sum_{j=1}^{N} p_j \log p_j$, and the modulation index

$$\mathrm{MI} = \frac{\log N - H}{\log N}.$$

If amplitude is the same in every bin, then $p_j = 1/N$, $H = \log N$ and MI is 0. If all the amplitude falls in one bin, then $H = 0$ and MI is 1. Tort and colleagues describe the index as an adaptation of the Kullback–Leibler distance, which measures how far the empirical phase–amplitude distribution is from uniform. The normalised form above is that distance divided by its maximum value.

6. Compare the value with a surrogate distribution, for example one built from amplitude series shifted in time, to decide whether the coupling exceeds chance.


## Results

- **Human cortex (Canolty et al., 2006).** Electrocorticogram recordings showed that the phase of theta, 4 to 8 Hz, modulated the power of high gamma, 80 to 150 Hz, more strongly at higher theta amplitudes.
- **Comparison and rat hippocampus (Tort et al., 2010).** The authors compared it with seven other coupling measures and found it especially suited to the task. They then applied it to recordings from freely moving rats and reported that regions CA3 and CA1 show different coupling characteristics.
- **Memory (Tort et al., 2009).** While rats learned to associate items with their spatial context, theta–gamma coupling in CA3 strengthened. The low-gamma band, 30 to 60 Hz, became more strongly modulated by theta phase, and the strength of coupling correlated with gains in accuracy. The authors suggest a role in memory recall.

## Limitations

- **Strength, not mechanism.** The index measures how strongly amplitude depends on phase. It does not show causation or the direction of influence.
- **Sensitivity to analysis choices.** Results depend on filters, phase-bin number and data length. Tort and colleagues discuss these and recommend surrogate controls.
- **Artefacts.** Coupling can appear in a filtered signal because of the shape of the slow waveform, or because neighbouring frequency bands overlap. Careful filter choice and surrogate tests are needed to tell real coupling from these effects.

## Open questions

- **Is coupling necessary for memory?** A correlation with learning does not show whether the rhythm is needed or simply accompanies a useful brain state.
- **What does the coupling carry?** Lisman and Jensen (2013) propose that theta–gamma coupling organises a sequence of items, one per gamma subcycle. Testing this requires recordings that resolve individual items.
- **Which frequency pairs matter?** Coupling has been reported across many frequency pairs. It is unclear which reflect general mechanisms and which are specific to a task.

## References

### Seminal papers

- Tort, A. B. L., Komorowski, R., Eichenbaum, H. & Kopell, N. (2010). Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. *Journal of Neurophysiology*. https://doi.org/10.1152/jn.00106.2010 — Introduces the modulation index and compares it with other coupling measures.
- Canolty, R. T. et al. (2006). High gamma power is phase-locked to theta oscillations in human neocortex. *Science*. https://doi.org/10.1126/science.1128115 — Human recordings in which theta phase modulates high-gamma power.
- Tort, A. B. L., Komorowski, R. W., Manns, J. R., Kopell, N. J. & Eichenbaum, H. (2009). Theta–gamma coupling increases during the learning of item–context associations. *Proceedings of the National Academy of Sciences*. https://doi.org/10.1073/pnas.0911331106 — Rat CA3 recordings in which theta–gamma coupling strengthens during learning.
- Lisman, J. E. & Jensen, O. (2013). The theta-gamma neural code. *Neuron*. https://doi.org/10.1016/j.neuron.2013.03.007 — Proposes gamma subcycles within each theta cycle as a code for sequences.

### Surveys and textbooks

- Canolty, R. T. & Knight, R. T. (2010). The functional role of cross-frequency coupling. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2010.09.001 — Review of proposed functional roles for cross-frequency coupling.
- Colgin, L. L. (2016). Rhythms of the hippocampal network. *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn.2016.21 — Reviews theta and gamma rhythms in hippocampal circuits and memory.
