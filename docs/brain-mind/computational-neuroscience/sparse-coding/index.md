---
status: draft
last_reviewed: 2026-10-28
---

# Sparse coding (Olshausen & Field, 1996)

Natural image patches are described as sparse combinations of learned basis functions.

## Problem

Why neurons in primary visual cortex (V1) respond to oriented edges at particular positions.

## Core idea

A natural image patch is described as a weighted sum of a few basis functions with sparse coefficients. The basis functions are learned from unlabelled images.

## Equation or algorithm

For each patch, find coefficients \(a_i\) and basis functions \(\phi_i\) that minimise

\[
E = \Big\| I - \sum_i a_i \phi_i \Big\|^2 + \lambda \sum_i S(a_i)
\]

where \(S\) is a sparseness penalty that favours few active coefficients.

## Results

The learned basis functions are localised, oriented and band-pass, resembling the simple-cell receptive fields of V1.

## Limitations

A linear generative model that leaves out complex cells, temporal dynamics and top-down influences. Sparse coding is one normative account among several, not a full model of V1.

## Connections

- Parent topic: [Computational Neuroscience](../index.md)
- Other method on this topic: [Hodgkin–Huxley Model](../hodgkin-huxley/index.md)

## References

### Seminal papers

- Hodgkin, A. L. & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*. https://doi.org/10.1113/jphysiol.1952.sp004764 — Derives the four-variable conductance model of the action potential, the basis of most biophysical neuron models.
- Izhikevich, E. M. (2003). Simple model of spiking neurons. *IEEE Transactions on Neural Networks*. https://doi.org/10.1109/TNN.2003.820440 — A two-variable model that reproduces many cortical firing patterns at low computational cost.
- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*. https://doi.org/10.1038/381607a0 — Shows that a sparse code for natural images yields oriented, localised filters like V1 simple cells.
- Richards, B. A. et al. (2019). A deep learning framework for neuroscience. *Nature Neuroscience*. https://doi.org/10.1038/s41593-019-0520-2 — Argues for studying the brain through objective functions, learning rules and architectures.

### Surveys and textbooks

- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook, from single neuron models to networks and learning rules.
