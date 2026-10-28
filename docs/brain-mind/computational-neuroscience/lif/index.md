---
status: complete
last_reviewed: 2026-10-28
related:
- brain-mind/snn-neuromorphic
- brain-mind/neuroscience
tags:
- neuroscience
- spiking neural networks
- neuron models
aliases:
  - 漏電積分發放模型
  - Leaky integrate-and-fire
  - LIF
---

# Leaky integrate-and-fire (LIF)

The leaky integrate-and-fire (LIF) neuron is the simplest spiking model that still captures the core of how a neuron fires. The membrane voltage integrates input current, slowly leaks back toward rest, and emits a spike and resets when it reaches a threshold. It is the workhorse model of spiking networks, because it is simple enough to simulate at scale and still reproduces the timing of spikes.

This page is part of [Computational Neuroscience](../index.md). It covers one neuron model in detail.

## Overview

Real neurons generate action potentials through ion-channel dynamics, which the [Hodgkin–Huxley model](../hodgkin-huxley/index.md) describes in detail. Most network studies do not need that level of detail. The LIF model keeps only the voltage, the leak and the threshold, and treats the spike as an event. That makes it fast enough for large networks and for neuromorphic hardware, at the cost of the spike's shape.

## Key concepts

- **Membrane voltage**: the potential across the neuron's membrane, which rises with input and decays toward rest.
- **Leak**: the decay of the voltage back toward its resting value between inputs.
- **Threshold**: the voltage at which the neuron emits a spike.
- **Reset**: the return of the voltage to a lower value after a spike, after which the neuron can fire again.
- **Refractory period**: a short interval after a spike during which the neuron does not respond, often added to the basic model.

## Problem

Neurons respond to input by spiking, and the timing of those spikes carries information. A model of this process needs to capture the threshold and the leak without the cost of a full ion-channel model, so that networks of many neurons can be simulated.

## Core idea

Treat the neuron as a leaky capacitor. Input current charges it, the leak discharges it, and when the voltage reaches the threshold the model records a spike and resets the voltage. The model is a simplification of the Hodgkin–Huxley picture: it omits the ionic currents that shape the spike, and keeps the integration and threshold that determine when the spike happens.

## Equation or algorithm

The membrane voltage \(V\) follows

\[
\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R\,I(t), \qquad V \geq V_{th} \;\Rightarrow\; \text{spike},\; V \leftarrow V_{reset}
\]

where \(\tau_m\) is the membrane time constant, \(R\) the membrane resistance, \(I(t)\) the input current, and \(V_{rest}\), \(V_{th}\) and \(V_{reset}\) the resting, threshold and reset voltages. In simulation, the equation is integrated in small time steps, and a spike is recorded whenever the threshold is crossed.

## Results

The model's firing behaviour is well established. With constant input, it fires at a rate that increases with input strength above threshold, which captures the basic firing-rate behaviour of neurons. Its spike times are a useful, if simplified, description of how neurons encode input in timing. The benefit is computational: LIF networks can be simulated at large scale, which is why they underlie most spiking-network studies.

## Limitations

- **No spike shape.** The spike is an event, so the model does not describe ion channels, spike width or the after-hyperpolarisation.
- **Simplified dendrites.** Each neuron is a single point, so the model cannot represent the nonlinear dendritic computations found in detailed models.
- **Fixed parameters.** Standard LIF neurons do not adapt their threshold or leak, so variants such as adaptive LIF are needed for some tasks.

## Connections

- **Hodgkin–Huxley model**: the detailed model that LIF simplifies. See [Hodgkin–Huxley](../hodgkin-huxley/index.md).
- **Spiking neural networks**: LIF neurons are the usual units of spiking networks, and the learning rules that train them are on [Spiking Neural Networks & Neuromorphic Computing](../../snn-neuromorphic/index.md), including [spike-timing-dependent plasticity](../../snn-neuromorphic/stdp/index.md).
- **Parent topic**: [Computational Neuroscience](../index.md).

## Applications

- **Neuromorphic hardware**: many chips implement LIF-type neurons, because the model is cheap to compute and naturally event-driven.
- **Network models**: large simulations of cortical circuits commonly use LIF neurons as their units.

## Open questions

- **How much detail does a network need?** The question of which features of detailed neurons matter for network function is open, and it determines when LIF is adequate.
- **How should adaptation be added?** Adaptive variants improve temporal processing, but the best way to combine adaptation with learning is still being explored.

## References

### Seminal papers

- Abbott, L. F. (1999). Lapicque's introduction of the integrate-and-fire model neuron (1907). *Brain Research Bulletin*. https://doi.org/10.1016/S0361-9230(99)00161-6 — A historical account of Lapicque's 1907 integrate-and-fire model, the origin of the LIF neuron.
- Burkitt, A. N. (2006). A review of the integrate-and-fire neuron model: I. Homogeneous synaptic input. *Biological Cybernetics*. https://doi.org/10.1007/s00422-006-0082-8 — A review of the integrate-and-fire model's behaviour under constant and fluctuating synaptic input.

### Surveys and textbooks

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook with a chapter on integrate-and-fire neurons and their variants.
- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — The detailed conductance model that the LIF neuron simplifies.
