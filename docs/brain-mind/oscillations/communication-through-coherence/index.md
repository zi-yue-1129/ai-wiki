---
status: draft
last_reviewed: 2026-10-28
tags:
- neuroscience
- attention
aliases:
  - 相干性通訊
  - 透過相干性的通訊
  - Communication Through Coherence
  - Neuronal Coherence
  - Fries 2005
---

# Communication Through Coherence

Communication through coherence is Fries's (2005) proposal that the effect of one neuronal group on another depends on the rhythmic relation between them. When two groups oscillate coherently, the sender's signal reaches the receiver at a consistent phase, so it can arrive when the receiver is most excitable. This page is one of the methods on [Neural Oscillations and Synchrony](../index.md).

## Overview

Neurons in a cortical area send and receive signals constantly, yet only some of those signals seem to influence later processing. Fries asked what selects them. His answer was that neuronal groups communicate through their rhythms. The responsiveness of a receiving group changes over each oscillation cycle, and inputs have the most effect when they arrive during the high-responsiveness part of that cycle. Coherence between the two groups keeps this timing stable, so communication is selective rather than a fixed broadcast. The idea is closely related to attention, which is covered in [Attention in Brains & Machines](../../attention-brain-machine/index.md).

## Key concepts

- **Coherence**: a normalised measure of how consistent the phase relation between two signals is in a frequency band. Here it is used for the rhythms of two neuronal groups.
- **Phase of excitability**: the part of a cycle in which a group responds most strongly to input. Input that arrives in this part has more effect.
- **Gamma band**: the faster range of rhythms, roughly 30 Hz and above, which Fries's proposal emphasises. The exact band depends on the study.
- **Selective routing**: the idea that some connections between areas are effective and others are not, depending on the current pattern of coherence.

## How it works

The mechanism can be read as a sequence of steps.

1. A sender group and a receiver group each oscillate in some frequency band.
2. The receiver's responsiveness rises and falls with its own phase, so it responds more strongly to input that arrives in its high-responsiveness phase.
3. If the phase difference between sender and receiver is stable, the sender's rhythmic output arrives at a consistent phase of the receiver's cycle, and the connection is effective.
4. If the phase difference drifts, the sender's output arrives at random phases and its effect averages out.
5. Attention or other top-down influences can change coherence, and so change which connections are effective.

Coherence between two signals is usually measured with the magnitude-squared coherence:

$$C_{xy}(f) = \frac{|S_{xy}(f)|^2}{S_{xx}(f)\,S_{yy}(f)},$$

where $S_{xy}(f)$ is the cross-spectrum of the two signals and $S_{xx}(f)$ and $S_{yy}(f)$ are their auto-spectra. The value lies between 0 and 1 at each frequency $f$.

## Results

The most cited test of the attention side of the account is Fries and colleagues (2001). They recorded neurons in macaque area V4 while monkeys attended to one stimulus and ignored another. Neurons activated by the attended stimulus showed increased gamma-frequency synchronisation, from 35 to 90 Hz, and reduced low-frequency synchronisation, below 17 Hz, compared with nearby V4 sites activated by distracters. The authors suggest that these localised changes could amplify behaviourally relevant signals.

The 2005 proposal is a theoretical synthesis rather than a single experiment. Its support comes from many recordings. Fries's later review (2015) updates the argument, and it is a common starting point for the debate.

## Limitations

- **Correlation, not causation.** Coherence between two recorded signals shows that they are related, not that information passes between them. A shared input can make two areas coherent without any direct communication.
- **Recording limits.** Field potentials sum activity from many nearby neurons and can be affected by volume conduction, so coherence between electrodes may reflect a common source.
- **Conduction delays.** The phase-based account requires the phase relation to survive the delay between areas. That delay depends on distance and frequency, which makes the prediction hard to test across long distances.
- **Irregular firing.** Individual neurons fire irregularly, so the link between a population rhythm and the timing of single spikes has to be established. Wang (2010) reviews this problem.

## Open questions

- **Routing or readout?** Does coherence cause selective communication, or is it a readout of communication that happens for other reasons?
- **Which frequency?** The proposal emphasises gamma, but the relevant frequency may differ between areas, tasks and species.
- **How can it be tested causally?** Changing coherence without changing firing rates is difficult, and this is the main experimental gap.
- **Does the account scale?** The theory is usually tested with pairs of areas, but the same principle would have to hold across many areas at once.

## References

### Seminal papers

- Fries, P. (2005). A mechanism for cognitive dynamics: neuronal communication through neuronal coherence. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2005.08.011 — Proposes that neuronal groups communicate most effectively when their rhythms are coherent and the receiving group is in a favourable phase.
- Fries, P., Reynolds, J. H., Rorie, A. E. & Desimone, R. (2001). Modulation of oscillatory neuronal synchronization by selective visual attention. *Science*. https://doi.org/10.1126/science.1055465 — Recordings from macaque area V4 showing that attention changes gamma and low-frequency synchrony among neurons.

### Surveys and textbooks

- Fries, P. (2015). Rhythms for cognition: communication through coherence. *Neuron*. https://doi.org/10.1016/j.neuron.2015.09.034 — Later review by the same author that updates the communication-through-coherence argument and its evidence.
- Engel, A. K., Fries, P. & Singer, W. (2001). Dynamic predictions: oscillations and synchrony in top-down processing. *Nature Reviews Neuroscience*. https://doi.org/10.1038/35094565 — Review of how oscillations and synchrony may carry top-down predictions in the cortex.
- Wang, X.-J. (2010). Neurophysiological and computational principles of cortical rhythms in cognition. *Physiological Reviews*. https://doi.org/10.1152/physrev.00035.2008 — Review of cortical rhythms in cognition, including long-distance coherence in attention and working memory.
- Buzsáki, G. & Draguhn, A. (2004). Neuronal oscillations in cortical networks. *Science*. https://doi.org/10.1126/science.1099745 — Review of cortical network oscillations across frequencies and of their proposed functions.
