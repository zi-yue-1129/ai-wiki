---
status: complete
last_reviewed: 2026-10-28
---

# Hodgkin–Huxley model (Hodgkin & Huxley, 1952)

A conductance-based model of the neuron's membrane voltage: ion channels whose conductances are controlled by gating variables generate the action potential.

## Overview

Neurons communicate with brief electrical pulses called action potentials, or spikes. In the early 1950s, Alan Hodgkin and Andrew Huxley measured the ionic currents across the membrane of the giant axon of the squid and wrote down a set of equations that reproduce the spike. Their 1952 paper is the basis of most biophysically detailed neuron models. It links the behaviour of individual ion channels to the voltage of the whole cell, and it is the reference point for the simpler spiking models used in neuroscience and in [spiking neural networks](../../snn-neuromorphic/index.md).

## Key concepts

- **Membrane potential (V)**: the voltage difference across the cell membrane.
- **Ion channel**: a pore in the membrane that lets specific ions, such as sodium (Na⁺) or potassium (K⁺), cross. Many channels open or close depending on the voltage.
- **Conductance (g)**: how easily current passes through a set of channels. The maximal conductance $\bar g$ multiplied by the fraction of open channels gives the conductance at a given moment.
- **Gating variables (m, h, n)**: quantities between 0 and 1 that describe the fraction of channel gates that are open. Each relaxes toward a voltage-dependent value.
- **Reversal potential (E)**: the voltage at which the current through one type of channel is zero. It is set by the ion concentrations on each side of the membrane.
- **Action potential**: a rapid, stereotyped rise and fall of the membrane voltage, which carries the signal along the axon.

## Problem

How does an action potential arise from the movement of ions across the membrane of a nerve cell? Before this work, the ionic currents had been measured only roughly. The question was whether a quantitative model, built from measured currents, could account for the observed shape of the spike and for its propagation along the axon.

## Core idea

The membrane is modelled as a capacitor in parallel with three conductance paths: one for sodium, one for potassium and a leak. When the membrane depolarises, the sodium conductance rises quickly, which drives the voltage further up. The sodium conductance then inactivates, and the potassium conductance rises more slowly, which brings the voltage back down. Each gating variable follows its own first-order dynamics, with rates that depend on voltage. The model fits the measured currents at a fixed temperature, and the paper scales the rates to other temperatures.

## Equation or algorithm

In the convention the paper uses, $V$ is the displacement of the membrane potential from rest, and depolarisation makes $V$ negative. Many modern texts flip this sign. The membrane equation is

$$C_M \frac{dV}{dt} = I - \bar g_{Na}\, m^3 h\,(V - V_{Na}) - \bar g_K\, n^4\,(V - V_K) - \bar g_L\,(V - V_L)$$

where $C_M$ is the membrane capacitance, $I$ is the injected current, $\bar g$ are the maximal conductances and $V_{Na}$, $V_K$, $V_L$ are the reversal potentials. Each gating variable $x \in \{m, h, n\}$ obeys

$$\frac{dx}{dt} = \alpha_x(V)\,(1 - x) - \beta_x(V)\,x$$

The rate functions, in the paper's units (V in mV, rates in ms⁻¹, at 6.3 °C), are

$$\alpha_n = \frac{0.01\,(V+10)}{e^{(V+10)/10}-1}, \qquad \beta_n = 0.125\, e^{V/80}$$

$$\alpha_m = \frac{0.1\,(V+25)}{e^{(V+25)/10}-1}, \qquad \beta_m = 4\, e^{V/18}$$

$$\alpha_h = 0.07\, e^{V/20}, \qquad \beta_h = \frac{1}{e^{(V+30)/10}+1}$$

The paper scales these rates to other temperatures with a temperature coefficient (Q10) of 3. Simulating the model follows these steps:

1. Set $V$ to the resting value, and set each gating variable to its steady-state value at that voltage.
2. At each time step, compute $\alpha$ and $\beta$ for every gate from the current $V$.
3. Update $m$, $h$ and $n$ with the gating equation.
4. Compute the sodium, potassium and leak currents from the conductances.
5. Update $V$ from the membrane equation, including any injected current $I$, and repeat.

## Results

The paper compares calculated action potentials with recorded ones from the squid axon. In its comparison, the calculated threshold is about 6 mV, against about 8 mV measured experimentally.

For propagation, the paper combines the model with cable theory. At 18.5 °C, the calculated conduction velocity is 18.8 m/s, against an observed velocity of 21.2 m/s in the same fibre, so the calculation is about 11 per cent below the measurement in this preparation.

## Limitations

The model was fitted to one preparation, the squid giant axon, and to a limited set of temperatures. The rates at other temperatures are scaled rather than measured. The model has no spatial structure beyond the cable, so dendrites and the many other channel types found in later neurons are absent. Four coupled equations per compartment are costly to simulate across large networks, which is why simpler spiking models such as Izhikevich's (2003) are common. The rate functions describe one axon at one temperature range, and the same framework has since been applied to other channel types. The 1952 rates should therefore be read as a model of one preparation, not as a general law.

## Key methods

A brief comparison of three landmark spiking-neuron models:

- **Hodgkin–Huxley** (this page): four state variables, with each term tied to a measured ion current. It is biophysically interpretable but expensive to simulate.
- [**Izhikevich model** (2003)](../../snn-neuromorphic/index.md): two variables and a reset rule. It reproduces several cortical firing and bursting patterns at low computational cost, and is used where large networks matter more than the detailed channel mechanisms.
- **Leaky integrate-and-fire**: one variable that integrates input and emits a spike with a reset when a threshold is crossed. It is the cheapest of the three, but it has no spike shape and no ion channels.

## Connections

- Parent topic: [Computational Neuroscience](../index.md)
- Companion method: [Sparse Coding](../sparse-coding/index.md), a normative account of how cortex represents images. It works at a different level from the biophysics on this page.
- [Spiking Neural Networks and Neuromorphic Computing](../../snn-neuromorphic/index.md) uses simplified spiking neurons of the kind this model motivates.
- [Neuroscience Basics](../../neuroscience/index.md) introduces neurons, synapses and ion channels for readers new to the subject.

## Applications

- **Research simulation.** Conductance-based models of the Hodgkin–Huxley type are used to test how changes in channel conductance alter a neuron's excitability. Gerstner et al. (2014) include the Hodgkin–Huxley equations among the single-neuron models in their textbook.
- **Designing simpler models.** Izhikevich (2003) combines the biological realism of Hodgkin–Huxley-style dynamics with the efficiency of integrate-and-fire models, so that very large spiking networks can be simulated.
- **Teaching.** The model is the standard worked example of how a physical mechanism, ion flow through gated channels, becomes an equation for a signal that can be simulated and tested.

## Open questions

- How well do the parameters fitted to the squid axon describe neurons in other species and cell types?
- How can conductance models be extended to dendritic trees and large networks without losing the biophysical meaning of their parameters?
- Which reduced models keep the functional behaviour of the full model while remaining cheap to simulate?
- How does the diversity of ion channels shape learning and computation in cortex?

## References

### Seminal papers

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — Derives the four-variable conductance model of the action potential, and its calculated conduction velocity, from measured squid axon currents.
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — A two-variable model that reproduces several cortical firing and burst patterns at low computational cost.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — Shows that a sparse code for natural images yields localised, oriented, bandpass filters like those of V1 simple cells.
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures, the framework in which biophysical models sit.

### Surveys and textbooks

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://doi.org/10.1017/CBO9781107447615 — Textbook from single-neuron models, including the Hodgkin–Huxley equations, through networks and learning rules. A free online version is available at https://neuronaldynamics.epfl.ch/.
