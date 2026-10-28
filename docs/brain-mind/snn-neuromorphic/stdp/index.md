---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/neuroscience
- brain-mind/computational-neuroscience
tags:
- neuroscience
- learning rules
- spiking neural networks
aliases:
  - 脈衝時序依賴可塑性
  - Spike-timing-dependent plasticity
  - STDP
---

# Spike-timing-dependent plasticity (STDP)

Spike-timing-dependent plasticity (STDP) is a learning rule in which the change in a synapse depends on the relative timing of the spikes on either side of it. If the presynaptic neuron fires shortly before the postsynaptic neuron, the synapse strengthens; if the order is reversed, it weakens. It is the best-known biologically observed rule of this kind, and it is the basis of many learning rules in spiking networks.

This page is part of [Spiking Neural Networks & Neuromorphic Computing](../index.md). It covers one learning rule in detail.

## Overview

Donald Hebb proposed that neurons that fire together wire together. STDP makes that idea precise in time: what matters is not only that two neurons are active, but whether the input spike arrived before the output spike. A synapse that helps trigger a postsynaptic spike is strengthened, while one that arrives too late to contribute is weakened.

## Key concepts

- **Presynaptic and postsynaptic spike**: the spike arriving at the synapse, and the spike the receiving neuron fires.
- **Timing window**: the range of spike-time differences over which the synapse changes, typically tens of milliseconds.
- **Potentiation and depression**: strengthening when the presynaptic spike comes first, and weakening when it comes second.
- **Hebbian learning**: the broader principle that correlated activity strengthens connections, of which STDP is a timing-specific form.

## Problem

Hebb's principle leaves open when, within a short time, a synapse should change. Experiments on cortical and hippocampal neurons showed that the sign and size of the change depend on the order and interval of the spikes, and a model of learning in spiking networks needs a rule that captures this dependence.

## Core idea

The change in synaptic weight is a function of the time difference between the presynaptic and postsynaptic spikes, \(\Delta t = t_{post} - t_{pre}\). Pairs with \(\Delta t > 0\) (pre before post) produce potentiation, and pairs with \(\Delta t < 0\) produce depression. The effect falls off with the size of \(|\Delta t|\), so only near-coincident spikes change the synapse much.

## Equation or algorithm

A common form uses an exponential window for each sign of the time difference:

\[
\Delta w = \begin{cases} A_+ \, e^{-\Delta t / \tau_+} & \Delta t > 0 \\ -A_- \, e^{\Delta t / \tau_-} & \Delta t < 0 \end{cases}
\]

where \(A_+\) and \(A_-\) set the sizes of potentiation and depression, and \(\tau_+\) and \(\tau_-\) set the windows, typically in the range of tens of milliseconds. The rule is applied each time a spike pair occurs.

## Results

The original experiments on cultured hippocampal neurons (Bi & Poo, 1998) measured the change in synaptic strength as a function of the timing of paired spikes, and found the asymmetric window described above. Markram et al. (1997) reported a related dependence of synaptic efficacy on the timing of postsynaptic action potentials and synaptic inputs in cortical pyramidal neurons. The rule's form is taken from these measurements, and the numerical windows vary between preparations.

## Limitations

- **Pairwise rule.** The basic form considers only pairs of spikes. Triplet and other higher-order rules fit the data better in some preparations.
- **Unstable on its own.** Without a limit or a competing mechanism, STDP can drive weights to extremes, so practical models add normalisation or homeostasis.
- **Not a full learning rule for tasks.** STDP alone gives unsupervised feature learning. To learn a task, it needs a signal such as reward, which is the basis of reward-modulated STDP.

## Connections

- **Spiking neural networks**: STDP is one of the local learning rules for spiking networks, alongside [e-prop](../eprop/index.md), which uses an eligibility trace and a learning signal.
- **Neuromorphic hardware**: local, timing-based rules suit on-chip learning, because each synapse needs only the spike times of its two neurons.
- **Dopamine and reward**: reward-modulated STDP links the timing rule to the reward signal discussed on [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).
- **Parent topic**: [Spiking Neural Networks & Neuromorphic Computing](../index.md).

## Applications

- **Unsupervised feature learning**: networks trained with STDP can learn features from input spike trains without labels.
- **Neuromorphic chips**: on-chip learning with local timing rules is an active area of hardware design.

## Open questions

- **Does a pairwise rule capture the biology?** Higher-order interactions between spikes, and their dependence on dendritic position, are not fully captured by the simple form.
- **How does STDP combine with other plasticity?** Homeostatic and neuromodulatory mechanisms interact with STDP in ways the basic rule does not show.
- **Can STDP learn complex tasks at scale?** Most demonstrations are on small problems, so scaling to deep networks is unresolved.

## References

### Seminal papers

- Bi, G.-Q. & Poo, M.-M. (1998). Synaptic modifications in cultured hippocampal neurons: dependence on spike timing, synaptic strength, and postsynaptic cell type. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.18-24-10464.1998 — Measures how the sign and size of synaptic change depend on the timing of pre- and postsynaptic spikes.
- Markram, H., Lübke, J., Frotscher, M. & Sakmann, B. (1997). Regulation of Synaptic Efficacy by Coincidence of Postsynaptic APs and EPSPs. *Science*. https://doi.org/10.1126/science.275.5297.213 — Shows that the efficacy of cortical synapses depends on the timing of postsynaptic action potentials relative to synaptic input.
- Song, S., Miller, K. D. & Abbott, L. F. (2000). Competitive Hebbian learning through spike-timing-dependent synaptic plasticity. *Nature Neuroscience*. https://doi.org/10.1038/78829 — Shows that a timing-based rule produces competitive, Hebbian learning of input structure in a network model.

### Surveys and reviews

- Caporale, N. & Dan, Y. (2008). Spike timing-dependent plasticity: a Hebbian learning rule. *Annual Review of Neuroscience*. https://doi.org/10.1146/annurev.neuro.31.060407.125639 — A review of STDP as a Hebbian rule, covering its experimental basis and its role in circuit learning.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook with chapters on synaptic plasticity and learning rules in spiking networks.
