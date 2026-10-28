---
status: draft
last_reviewed: 2026-10-28
---

# Online learning with local updates: e-prop (Bellec et al., 2020)

Learning uses local eligibility traces and a learning signal, instead of backpropagation through time.

## Problem

Backpropagation through time needs the whole history and is hard to reconcile with biology. Can recurrent spiking networks learn online with information that is available locally?

## Core idea

Approximate the gradient with an eligibility trace for each synapse, which is computed forward in time, and combine it with a learning signal that reaches the neuron from outside. Updates can then happen at every time step.

## Equation or algorithm

The weight update sums, over time, the learning signal multiplied by the eligibility trace,

\[
\Delta W_{ji} = \sum_t L_j(t)\, e_{ji}(t)
\]

## Results

The authors report that the online rule performs close to backpropagation through time on the tasks they test.

## Limitations

The rule drops some gradient terms, so it is an approximation. The reported results cover the tasks the authors chose.

## Connections

- Parent topic: [Spiking Neural Networks & Neuromorphic Computing](../index.md)
- Other method on this topic: [Surrogate Gradients](../surrogate-gradients/index.md)

## References

### Seminal papers

- Neftci, E. O., Mostafa, H. & Zenke, F. (2019). Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — Introduces surrogate gradients, which let spiking networks be trained with backpropagation through time.
- Bellec, G., et al. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — The e-prop learning rule, an online approximation to backpropagation through time for spiking networks.

### Surveys and textbooks

- Eshraghian, J. K., et al. (2023). Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — A tutorial on training spiking networks with deep-learning tools, with the snnTorch examples.
- Roy, K., Jaiswal, A. & Panda, P. (2019). Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — A review of spike-based computation and neuromorphic hardware.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook on spiking neuron models and networks.
