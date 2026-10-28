---
status: complete
last_reviewed: 2026-10-28
related:
- theory/models/rnn
tags:
- neuromorphic
- spiking neural networks
- learning rules
aliases:
  - e-prop
  - eligibility propagation
---

# Online learning with local updates: e-prop (Bellec et al., 2020)

Learning uses local eligibility traces and a learning signal, instead of backpropagation through time. This makes it possible to train recurrent spiking networks online, updating weights as the input arrives, with information that is available at each synapse.

This page is part of [Spiking Neural Networks & Neuromorphic Computing](../index.md). It covers one learning rule in detail.

## Overview

Training a recurrent network with backpropagation through time (BPTT) means storing the whole history of activity and then running the error backwards through it. That is practical on a computer, but it does not match what a synapse can know locally, and it is hard to run on energy-efficient neuromorphic hardware. e-prop is a learning rule that keeps only a short trace at each synapse and a learning signal at each neuron, and applies updates as it goes.

## Key concepts

- **Eligibility trace**: a per-synapse quantity that records, forward in time, how much a synapse's recent activity could have contributed to the neuron's output.
- **Learning signal**: a per-neuron error signal that reaches the neuron from outside the local circuit, such as a target or a reward.
- **Online learning**: updating the weights while the input is still arriving, rather than after a whole sequence.
- **Spiking neuron**: a neuron that communicates through discrete spikes, and whose state is typically a membrane potential.

## Problem

Backpropagation through time needs the whole history and is hard to reconcile with biology. Can recurrent spiking networks learn online with information that is available locally? The question is practical for neuromorphic hardware and also a model of how brains might learn.

## Core idea

Approximate the gradient with an eligibility trace for each synapse, which is computed forward in time. Combine it with a learning signal that reaches each neuron from outside. Updates can then happen at every time step. The authors show that this combination approximates the gradient that BPTT would compute, with some terms dropped.

## Equation or algorithm

The weight update sums, over time, the learning signal multiplied by the eligibility trace,

\[
\Delta W_{ji} = \sum_t L_j(t)\, e_{ji}(t)
\]

where \(L_j(t)\) is the learning signal for neuron j and \(e_{ji}(t)\) is the eligibility trace of the synapse from neuron i to neuron j. The trace is updated at each time step from local quantities, so the rule needs no stored history.

## Results

The authors report that the online rule performs close to backpropagation through time on the tasks they test, which include the spiking-network tasks described in the paper. The comparison is against BPTT on the same networks, so it measures how much accuracy the approximation costs.

## Limitations

- **An approximation.** The rule drops some gradient terms, so it does not compute the exact gradient, and performance can fall below BPTT on tasks where the dropped terms matter.
- **Chosen tasks.** The reported results cover the tasks the authors chose, so generalisation to other tasks and architectures needs separate testing.
- **Learning signal source.** The rule assumes a learning signal reaches each neuron, and how such a signal is provided in a biological or hardware system is a separate question.

## Connections

- **Surrogate gradients**: a different route to training spiking networks, which uses backpropagation with a smooth stand-in for the spike function. See [Surrogate Gradients](../surrogate-gradients/index.md).
- **Recurrent networks**: the rule is an online alternative to BPTT for recurrent models. The standard recurrent architecture is covered in [Recurrent Neural Networks](../../../theory/models/rnn/index.md).
- **Parent topic**: [Spiking Neural Networks & Neuromorphic Computing](../index.md).

## Applications

- **Neuromorphic hardware**: local updates suit chips that store weights and traces next to the neurons, avoiding the need to store a full history.
- **Models of learning in the brain**: local rules are a candidate for how cortical circuits learn, to be tested against data.

## Open questions

- **How close is the approximation on harder tasks?** The gap to BPTT is shown on the tasks reported, and larger problems may widen it.
- **Where does the learning signal come from?** The rule needs a per-neuron signal, and the biological or hardware source of that signal is still an open design question.
- **Do biological synapses follow the rule?** Testing eligibility-trace learning against synaptic recordings is an open experimental question.

## References

### Seminal papers

- Bellec, G., et al. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — The e-prop learning rule, an online approximation to backpropagation through time for spiking networks.
- Neftci, E. O., Mostafa, H. & Zenke, F. (2019). Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — Introduces surrogate gradients, which let spiking networks be trained with backpropagation through time.

### Surveys and textbooks

- Eshraghian, J. K., et al. (2023). Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — A tutorial on training spiking networks with deep-learning tools, with the snnTorch examples.
- Roy, K., Jaiswal, A. & Panda, P. (2019). Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — A review of spike-based computation and neuromorphic hardware.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook on spiking neuron models and networks.
