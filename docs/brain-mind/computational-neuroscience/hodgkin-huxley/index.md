---
status: draft
last_reviewed: 2026-10-28
---

# Hodgkin–Huxley model (Hodgkin & Huxley, 1952)

A conductance-based model of the neuron's membrane voltage, built from ion channels and gating variables.

## Problem

How the action potential arises from ion movements across the membrane of the squid giant axon.

## Core idea

The membrane is a capacitor in parallel with voltage-gated sodium and potassium conductances and a leak. Three gating variables (m, h, n) each relax toward a voltage-dependent value, and they control the conductances.
- **Equations** (modern sign convention):

\[
C\frac{dV}{dt} = I - g_{Na}\,m^3 h\,(V - E_{Na}) - g_K\,n^4\,(V - E_K) - g_L\,(V - E_L)
\]

\[
\frac{dx}{dt} = \alpha_x(V)\,(1 - x) - \beta_x(V)\,x, \qquad x \in \{m, h, n\}
\]

## Results

The simulated action potential matches the shape of recordings from the squid axon, and the model reproduces how the spike propagates along the axon.

## Limitations

Fitted to one preparation at one temperature, with no dendritic structure. Four coupled equations per compartment are costly for large networks, which is why the simpler leaky integrate-and-fire and Izhikevich models in the table above are so common.

## Connections

- Parent topic: [Computational Neuroscience](../index.md)
- Other method on this topic: [Sparse Coding](../sparse-coding/index.md)

## References

### Seminal papers

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — Derives the four-variable conductance model of the action potential, the basis of most biophysical neuron models.
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — A two-variable model that reproduces many cortical firing patterns at low computational cost.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — Shows that a sparse code for natural images yields oriented, localised filters like V1 simple cells.
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.

### Surveys and textbooks

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook, from single neuron models to networks and learning rules.
