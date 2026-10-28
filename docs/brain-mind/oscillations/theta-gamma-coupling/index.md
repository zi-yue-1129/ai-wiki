---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- neural oscillations
- memory
aliases:
  - θ–γ 耦合
  - Theta-gamma coupling
  - Theta–gamma neural code
  - Phase-amplitude coupling
  - PAC
---

# Theta–gamma coupling (Lisman & Jensen, 2013)

Theta–gamma coupling is a pattern in which the phase of a slow theta rhythm modulates the amplitude of a fast gamma rhythm. In human cortical recordings, theta is typically taken as about 4 to 8 Hz and high gamma as about 80 to 150 Hz. Lisman and Jensen (2013) proposed that this nesting forms a neural code, in which separate items occupy successive gamma bursts within each theta cycle. The idea is most closely tied to memory, especially in the hippocampus. It is part of [Neural Oscillations and Synchrony](../index.md).

## Problem

People can hold only a small number of items in short-term memory at once. Psychophysical measurements put this at about seven (Lisman & Idiart, 1995). The question is how a neural network can keep several items distinct at the same time, when each item is represented by activity in a shared population. A simple scheme in which every item keeps firing would make them interfere with one another.

## Core idea

Lisman and Idiart (1995) proposed that each item is assigned to a different fast gamma subcycle. The subcycles repeat inside each slow theta cycle, so the items form an ordered sequence within every theta cycle.

Later recordings in humans reported the coupling directly. Canolty et al. (2006) report that high-gamma power in human neocortex is phase-locked to theta, recorded with electrocorticography (ECoG). Lisman and Jensen (2013) develop the proposal into a broader theta–gamma neural code, in which the gamma subcycles within a theta cycle carry an ordered sequence of items, and they review the evidence for it, mainly from the hippocampus.

## Equation or algorithm

Measuring coupling is a procedure. Tort et al. (2010) describe one common version:

1. Filter the signal into a slow band (theta) and a fast band (gamma).
2. At each time point, take the phase of the slow band and the amplitude envelope of the fast band.
3. Sort the amplitude values into bins according to the slow-band phase, and average the amplitude within each bin.
4. Measure how far the resulting amplitude distribution departs from uniform, using a Kullback–Leibler-based index. A flat distribution means no coupling. A distribution with a clear peak means the amplitude depends on phase.
5. Compare the value with surrogate data, produced by a control analysis, to check that the coupling is greater than chance.

## Results

- **Model (Lisman & Idiart, 1995).** The model stores memories in oscillatory subcycles, with separate items in successive gamma subcycles within slow cycles, as the title states. The numerical settings of the simulation are not quoted on this page. This is a model result, not a recording.
- **Hippocampal coding (Lisman, 2005).** Lisman argues that the theta/gamma discrete phase code seen during hippocampal phase precession may be a more general brain coding scheme.
- **Human recordings (Canolty et al., 2006).** High-gamma power in human neocortex is phase-locked to theta, shown with ECoG.
- **Measure (Tort et al., 2010).** The authors introduce a Kullback–Leibler-based index of phase–amplitude coupling and compare it with other measures. This page does not quote the comparison results.

## Limitations

- **Model versus data.** The theory of items in gamma subcycles comes from a network model. Extending the code to other kinds of memory content is therefore an inference.
- **Coupling is not yet a code.** Showing that gamma amplitude depends on theta phase does not show that the phase carries specific item information. Decoding the content of each subcycle requires further analysis.
- **Measurement choices.** Coupling estimates depend on filter settings, epoch length and the controls used. Tort et al. (2010) discuss technical aspects such as epoch length and surrogate control analyses.
- **Sample.** The human evidence cited here comes from ECoG, which records the cortical surface. It samples only the areas where electrodes are placed, which limits how far the findings generalise across brain regions.

## Connections

- **Memory.** The hippocampus is the main region where theta–gamma coding has been proposed (Lisman & Jensen, 2013), as covered in [Memory & Learning](../../memory-learning/index.md).
- **Communication.** [Communication through coherence](../communication-through-coherence/index.md) is the other rhythm-based account in this chapter. Coherence concerns communication between groups, while theta–gamma coupling concerns how one circuit organises its own items.
- **Recording.** The ECoG and local field potential signals used in the human studies are described on [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md).
- **Artificial networks.** Phase-based coding is studied in spiking networks, where the timing of each spike relative to an oscillation carries information. See [Spiking Networks & Neuromorphic Computing](../../snn-neuromorphic/index.md). Standard artificial networks, which use continuous activations without spikes, have no direct counterpart to the subcycle code. The link is conceptual: both use the ordering of activity within a cycle to keep items apart.

## Applications

- **Human task studies.** Intracranial recordings can show how theta–gamma coupling changes across behavioural tasks, as Canolty et al. (2006) did.
- **Measuring coupling.** The Tort et al. (2010) index is one of the measures available for quantifying phase–amplitude coupling in recordings from different regions.

## Open questions

- Does the theta–gamma code carry specific content, and how does a downstream area read the phase of each subcycle?
- How many gamma subcycles fit in a theta cycle, and does this number vary across species and regions?
- Can the coupling be tested causally, by manipulating the theta rhythm and checking the effect on memory?

## References

### Seminal papers

- Lisman, J. E. & Idiart, M. A. P. (1995). Storage of 7 ± 2 short-term memories in oscillatory subcycles. *Science*, 267(5203), 1512–1515. https://doi.org/10.1126/science.7878473 — The original theta–gamma memory model: separate items in successive gamma subcycles within slow cycles.
- Lisman, J. (2005). The theta/gamma discrete phase code occurring during the hippocampal phase precession may be a more general brain coding scheme. *Hippocampus*, 15(7), 913–922. https://doi.org/10.1002/hipo.20121 — Argues that the theta/gamma phase code of hippocampal phase precession may be a more general coding scheme.
- Canolty, R. T. et al. (2006). High gamma power is phase-locked to theta oscillations in human neocortex. *Science*, 313(5793), 1626–1628. https://doi.org/10.1126/science.1128115 — ECoG evidence that the phase of theta modulates high-gamma power in humans.
- Tort, A. B. L., Komorowski, R., Eichenbaum, H. & Kopell, N. (2010). Measuring phase-amplitude coupling between neuronal oscillations of different frequencies. *Journal of Neurophysiology*, 104(2), 1195–1210. https://doi.org/10.1152/jn.00106.2010 — Introduces a Kullback–Leibler-based index of phase–amplitude coupling and compares it with other measures.

### Surveys and textbooks

- Lisman, J. E. & Jensen, O. (2013). The theta–gamma neural code. *Neuron*, 77(6), 1002–1016. https://doi.org/10.1016/j.neuron.2013.03.007 — Review that develops the theta–gamma coding proposal and the evidence for it.
- Lisman, J. & Buzsáki, G. (2008). A neural coding scheme formed by the combined function of gamma and theta oscillations. *Schizophrenia Bulletin*, 34(5), 974–980. https://doi.org/10.1093/schbul/sbn060 — Review of the evidence that theta and gamma oscillations work together as a neural code, with a discussion of a possible link to schizophrenia.
