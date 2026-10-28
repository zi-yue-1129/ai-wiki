---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/neuroscience
tags:
- neuroscience
- learning
aliases:
  - Whittington & Bogacz 2017
  - Predictive coding approximates backpropagation
  - Local Hebbian learning in predictive coding
---

# Predictive Coding Approximates Backpropagation (Whittington & Bogacz 2017)

Whittington and Bogacz (2017) showed that a predictive coding network, with explicit prediction-error units, can approximate the error backpropagation algorithm using only local Hebbian plasticity. Each synaptic change depends only on the two neurons it connects and on the local prediction error, not on information from distant neurons. Under suitable parameter settings the weight updates match those of backpropagation, and the network performs much like a standard network on MNIST digit recognition.

This page is part of [Predictive Coding and the Free-Energy Principle](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

Backpropagation is an effective learning algorithm, but its weight updates depend on error signals that travel backward through the network. A real synapse cannot access the activity of distant neurons, so backpropagation is hard to reconcile with known cortical circuits. The question was whether a biologically plausible network with local learning can reach the same weight updates.

## The approach

The authors use a predictive coding network, in which each layer has prediction-error units that encode the mismatch between a layer's activity and its prediction from the layer above. Learning is driven by these errors, and the changes to each synapse use only the two neurons it connects.

The steps were:

1. Clamp the input and output layers, and let the hidden activity settle so that the prediction errors are minimised.
2. Update each synapse using only the activity of its two connected neurons and the local prediction error.
3. Repeat over training examples. For suitable parameter settings the weight changes match those of backpropagation.

Step 1 is what makes the scheme local. The hidden activity does the work that the backward pass does in backpropagation, and the error is available at each layer without being sent from elsewhere.

## Results

The authors show that, with suitable parameters, the weight updates converge to those of backpropagation. Under those conditions the network performs much like a standard network on MNIST digit recognition.

## Limitations

- The match depends on parameter choices. The approximation holds only under particular settings.
- The authors argue that the brain probably does not implement backpropagation exactly, because real signals are noisy at several levels. The result is an approximation of the algorithm, not evidence that the cortex implements it.
- The benchmark is small. Results on large deep networks are not established by this paper.

## Connections

- **Visual predictive coding**: the original predictive coding account of cortical responses is on [Rao and Ballard 1999](../rao-ballard-1999/index.md).
- **Review**: the case that predictive processing is a repeated cortical computation is in [Keller and Mrsic-Flogel 2018](../index.md) on the parent page.
- **NeuroAI**: biologically plausible alternatives to backpropagation, and how they are compared with deep networks, are on [NeuroAI](../../neuroai/index.md).
- **Neuroscience background**: the dopamine prediction-error signal, a different error-based learning rule in a different system, is in [Neuroscience Basics](../../neuroscience/index.md).

## Open questions

- **Does the cortex implement these error units?** The model is a candidate circuit, and the separate error and prediction populations need direct evidence.
- **Does the approximation hold at scale?** Results on small benchmarks are encouraging, but large networks have not been shown to match backpropagation under local learning.

## References

### Seminal papers

- Whittington, J. C. R. & Bogacz, R. (2017). An Approximation of the Error Backpropagation Algorithm in a Predictive Coding Network with Local Hebbian Synaptic Plasticity. *Neural Computation*. https://doi.org/10.1162/NECO_a_00949 — Shows that predictive coding with local plasticity can approximate backpropagation under suitable parameters.
- Rao, R. P. N. & Ballard, D. H. (1999). Predictive coding in the visual cortex: a functional interpretation of some extra-classical receptive-field effects. *Nature Neuroscience*. https://doi.org/10.1038/4580 — The hierarchical predictive coding model that this network extends, with feedback carrying predictions and feedforward connections carrying errors.

### Surveys and reviews

- Keller, G. B. & Mrsic-Flogel, T. D. (2018). Predictive Processing: A Canonical Cortical Computation. *Neuron*. https://doi.org/10.1016/j.neuron.2018.10.003 — A review arguing that predictive processing is a repeated circuit-level computation across cortex, and discussing how it could be tested.
- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*. https://doi.org/10.1038/nrn2787 — Proposes that brains minimise prediction error, a unifying framework for perception, action and learning. (Reference reused from the parent page; not re-checked for this page.)
- Clark, A. (2013). Whatever next? Predictive brains, situated agents, and the future of cognitive science. *Behavioral and Brain Sciences*. https://doi.org/10.1017/S0140525X12000477 — A review of predictive processing as a unifying framework for perception, action and cognition. (Reference reused from the parent page; not re-checked for this page.)
