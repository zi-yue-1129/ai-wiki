---
status: draft
last_reviewed: 2026-10-28
related:
- theory/models/rnn
tags:
- neuroscience
- neural oscillations
- synchrony
aliases:
  - 神經振盪與同步
  - 神經振盪
  - 腦波振盪
  - Neural Oscillations
  - Brain Oscillations
  - Neural Synchrony
---

# Neural Oscillations and Synchrony

Groups of neurons in the brain often produce rhythms: their collective activity rises and falls at regular frequencies. Synchrony is the matching of timing across neurons or brain areas. Together they have been proposed as a way for the brain to organise timing, communication and memory. Their counterpart in artificial networks is much less direct than in other areas of neuroscience and AI.

## Overview

A neural oscillation is a rhythmic change in the activity of a population of neurons. Researchers see it in group-level signals such as the [local field potential](../neuroimaging-methods/index.md), which reflects the synaptic activity of many cells, and in scalp EEG. A single neuron's spikes are not themselves a rhythm, but when many neurons fire at similar phases, the group signal oscillates.

Oscillations occur across a very wide range of frequencies. Buzsáki and Draguhn (2004) describe them as spanning five orders of magnitude, and argue that their preservation across species suggests they are functionally relevant rather than a by-product of network activity. They link recent findings to three roles: biasing which inputs are selected, temporally linking neurons into assemblies, and facilitating synaptic plasticity.

## Core ideas

- **Frequency bands.** Oscillations are grouped into bands. The usual labels are delta, theta, alpha, beta and gamma, but the boundaries differ from study to study. Two ranges used in this chapter come from specific studies: theta at 4 to 8 Hz and high gamma at 80 to 150 Hz, in human cortical recordings (Canolty et al., 2006).
- **Phase.** Phase is where a signal sits within its cycle. Information can be carried by when a spike occurs within a cycle, not only by how many spikes occur. Lisman and Idiart (1995) proposed that the items of a short-term memory each occupy a different fast subcycle nested inside a slow cycle, so that the phase of the fast rhythm separates them.
- **Coherence.** Coherence describes a stable phase relation between two rhythms over time. Womelsdorf et al. (2007) found that how strongly two neuronal groups influenced each other depended on the phase relation between their rhythms, and that these phase relations preceded the interaction by a few milliseconds.
- **Cross-frequency coupling.** The amplitude of a fast rhythm can depend on the phase of a slow one. This is the basis of theta–gamma coupling, which is linked to memory.

## Key methods

- [Communication through coherence (Fries, 2005)](communication-through-coherence/index.md): proposes that rhythmic synchrony between areas sets when their signals are effective, so that coherence controls which interactions get through. It is about communication between areas.
- [Theta–gamma coupling (Lisman & Jensen, 2013)](theta-gamma-coupling/index.md): proposes that the phase of a slow theta rhythm organises fast gamma bursts into a coding scheme within a circuit. It is about how one circuit organises items, with memory as the main application.

## Connections

- **Memory.** Theta and gamma rhythms in the hippocampus are central to the memory-related ideas in [Memory & Learning](../memory-learning/index.md). The sleep rhythms there, such as slow oscillations, spindles and ripples, belong to the same family of ideas.
- **Recording.** Group rhythms are measured with [LFP, ECoG and EEG](../neuroimaging-methods/index.md), which see populations rather than single cells. Interpreting them requires care, since a rhythm in a summed signal does not reveal which neurons produced it.
- **Computational models.** Models of coupled oscillators and of spiking networks study how such rhythms arise. See [Computational Neuroscience](../computational-neuroscience/index.md) and [Spiking Networks & Neuromorphic Computing](../snn-neuromorphic/index.md), where phase coding is one of the listed coding schemes.
- **Artificial networks.** Standard artificial networks have no membrane potentials, spikes or rhythms of their own, so oscillations have no direct counterpart in them. One architecture applies the idea directly. The coupled oscillatory recurrent neural network (coRNN) treats its hidden state as the output of a system of coupled nonlinear oscillators, discretised over time (Rusch & Mishra, 2020). The authors report that this keeps gradients bounded, which helps learning over long sequences, and reports results comparable to the state of the art on several benchmarks. The analogy is architectural: it shows that oscillator dynamics can serve as a recurrent computation. It does not show that trained networks develop brain-like theta or gamma rhythms, or that such rhythms do the same job in both systems. See [Recurrent Neural Networks](../../theory/models/rnn/index.md).

## Applications

- **Brain–computer interfaces.** Decoding brain signals for control of devices is covered on the [brain–computer interfaces](../bci/index.md) page. Group-level recordings of the kind described above are one of its input signals.
- **Sleep and memory.** The sleep rhythms mentioned under Connections (slow oscillations, spindles and ripples) are discussed in the context of memory on the [Memory & Learning](../memory-learning/index.md) page.
- **Sequence modelling.** The coRNN architecture is an example of using oscillator equations to build a sequence model, with benchmark results reported in its paper.

## Open questions

- **Causality.** Do oscillations cause communication between areas, or do they only accompany it? Answering this needs experiments that manipulate rhythms directly, which are harder in humans.
- **Band specificity.** Are the frequency bands functionally distinct, or do they form a continuum? The boundaries between bands are set by convention in many studies.
- **Reading the code.** Phase coding has been shown in models and in some recordings. Whether downstream areas actually decode phase is less clear.
- **Use in AI.** Whether oscillator-based architectures offer benefits beyond the benchmarks they have been tested on is still open.

## References

### Seminal papers

- Singer, W. & Gray, C. M. (1995). Visual feature integration and the temporal correlation hypothesis. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.ne.18.030195.003011 — Proposes that temporal correlation between neurons may bind visual features into objects.
- Lisman, J. E. & Idiart, M. A. P. (1995). Storage of 7 ± 2 short-term memories in oscillatory subcycles. *Science*. https://doi.org/10.1126/science.7878473 — A network model in which memory items occupy different gamma subcycles within slow theta cycles.
- Fries, P. (2005). A mechanism for cognitive dynamics: neuronal communication through neuronal coherence. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2005.08.011 — Proposes that coherence between neuronal groups controls their communication.

### Surveys and reviews

- Buzsáki, G. & Draguhn, A. (2004). Neuronal oscillations in cortical networks. *Science*. https://doi.org/10.1126/science.1099745 — Survey of the oscillations in cortical networks, their frequency span and their proposed functions.
- Fries, P. (2015). Rhythms for cognition: communication through coherence. *Neuron*. https://doi.org/10.1016/j.neuron.2015.09.034 — Review of the coherence hypothesis and the evidence for it, written by the author who proposed it.
- Buzsáki, G. (2006). *Rhythms of the Brain*. Oxford University Press. https://doi.org/10.1093/acprof:oso/9780195301069.001.0001 — Book-length treatment of brain rhythms, for readers who want more depth than the survey above.

### Articles and documentation

- Rusch, T. K. & Mishra, S. (2020). Coupled Oscillatory Recurrent Neural Network (coRNN): An accurate and (gradient) stable architecture for learning long time dependencies. arXiv:2010.00951. https://arxiv.org/abs/2010.00951 — A recurrent architecture built from coupled nonlinear oscillators, with bounded hidden-state gradients and benchmark results.
