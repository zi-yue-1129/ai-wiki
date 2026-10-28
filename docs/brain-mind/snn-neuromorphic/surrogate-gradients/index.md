---
status: draft
last_reviewed: 2026-10-28
---

# Surrogate gradients (Neftci, Mostafa & Zenke, 2019)

Spiking networks are trained with backpropagation by replacing the threshold's derivative with a smooth surrogate.

## Problem

A spike is a step function, so its derivative is zero almost everywhere and backpropagation cannot train a spiking network directly.

## Core idea

Keep the hard threshold in the forward pass, and in the backward pass replace the threshold's derivative with a smooth surrogate. Then apply backpropagation through time.

## Equation or algorithm

In the forward pass a neuron emits a spike when its membrane potential crosses the threshold, and in the backward pass its derivative is replaced by a surrogate \(\sigma'\), a smooth function centred on the threshold.

## Results

The paper presents surrogate gradients as a flexible and efficient way to train spiking networks, rather than as a single benchmark result.

## Limitations

The choice of surrogate is a heuristic. Backpropagation through time stores the network's history, so memory cost grows with sequence length.

## Connections

- Parent topic: [Spiking Neural Networks & Neuromorphic Computing](../index.md)
- Other method on this topic: [Online Learning with Local Updates (e-prop)](../eprop/index.md)

## References

### Seminal papers

- Neftci, E. O., Mostafa, H. & Zenke, F. (2019). Surrogate Gradient Learning in Spiking Neural Networks. *IEEE Signal Processing Magazine*. https://doi.org/10.1109/MSP.2019.2931595 — Introduces surrogate gradients, which let spiking networks be trained with backpropagation through time.
- Bellec, G., et al. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — The e-prop learning rule, an online approximation to backpropagation through time for spiking networks.

### Surveys and textbooks

- Eshraghian, J. K., et al. (2023). Training Spiking Neural Networks Using Lessons From Deep Learning. *Proceedings of the IEEE*. https://doi.org/10.1109/JPROC.2023.3308088 — A tutorial on training spiking networks with deep-learning tools, with the snnTorch examples.
- Roy, K., Jaiswal, A. & Panda, P. (2019). Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — A review of spike-based computation and neuromorphic hardware.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics*. Cambridge University Press. https://neuronaldynamics.epfl.ch/ — Free online textbook on spiking neuron models and networks.
