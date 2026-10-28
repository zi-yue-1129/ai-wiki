---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/neuroai
- brain-mind/neuroscience
tags:
- neuroscience
- neuromorphic
- learning
aliases:
  - Surrogate gradient learning
  - Neftci 2019
  - Surrogate gradients
---

# Surrogate Gradients (Neftci, Mostafa & Zenke, 2019)

Spiking networks communicate with discrete spikes, and the threshold that produces a spike has a derivative that is zero almost everywhere. Surrogate gradients keep the hard threshold in the forward pass and replace its derivative with a smooth function in the backward pass. This lets spiking networks be trained with backpropagation through time, the same family of methods used for ordinary recurrent networks.

This page is part of [Spiking Neural Networks & Neuromorphic Computing](../index.md). The parent page gives the overview; this page covers the method and its evidence.

## The problem

A spiking neuron emits a spike when its membrane potential crosses a threshold. Written as a function, a spike is a step: the output jumps from zero to one at the threshold and is flat everywhere else. Gradient-based learning needs a derivative, and the derivative of a step is zero almost everywhere, so the error signal cannot reach the weights.

## The approach

The method separates the forward and backward passes. The forward pass uses the true spiking nonlinearity, so the network computes with spikes. The backward pass uses a surrogate derivative, a smooth function centred on the threshold, so the error signal can flow back through time.

The steps were:

1. Simulate the spiking network forward in time, with each neuron emitting a spike when its membrane potential crosses the threshold.
2. In the backward pass, replace the derivative of the spike with a surrogate \(\sigma'\), a smooth function that is large near the threshold and small far from it.
3. Apply backpropagation through time to compute weight updates from the surrogate derivatives.

In equations, with membrane potential \(v_t\), threshold \(\vartheta\) and spike output \(s_t\), the forward pass is \(s_t = H(v_t - \vartheta)\), where \(H\) is the step function. The backward pass uses \(\partial s_t / \partial v_t \approx \sigma'(v_t - \vartheta)\) in place of the step's derivative. The paper treats the choice of \(\sigma'\) as a design decision, and several shapes are used in practice.

Step 3 is where the surrogate matters. Only the backward pass changes, so the network still computes with the same discrete spikes it is trained to produce.

## Results

The paper presents surrogate gradients as a flexible and efficient route to training spiking networks, and the evidence is that they can be applied across architectures and tasks rather than a single benchmark result. The summary used for this page gives this qualitatively. Check the paper and later benchmarks before quoting specific accuracies.

## Limitations

- The choice of surrogate is a heuristic. Different shapes can give different training behaviour, and there is no single principled choice.
- Backpropagation through time stores the network's history, so memory cost grows with the length of the sequence.
- The surrogate is an approximation to the true gradient, so the method does not optimise the exact objective for the spiking network.

## Connections

- **Online learning**: a local, online alternative that avoids storing the full history is on [Online Learning with Local Updates (e-prop)](../eprop/index.md).
- **Parent overview**: the wider field of spiking and neuromorphic computing, including hardware, is on [Spiking Neural Networks & Neuromorphic Computing](../index.md).
- **NeuroAI**: how gradient-based training of spiking networks relates to brain-inspired learning is on [NeuroAI](../../neuroai/index.md).

## Open questions

- **Which surrogate is best, and why?** The field uses several shapes, and a principled account of when each works is still missing.
- **Can surrogate-gradient training scale to the brain's learning rules?** Backpropagation through time is not obviously biological, and whether local approximations close the gap is an open question.

## References

### Seminal papers

- Neftci, E. O., Mostafa, H. & Zenke, F. (2019). Surrogate gradient learning in spiking neural networks. *arXiv*. https://arxiv.org/abs/1901.09948 — Introduces surrogate gradients, which let spiking networks be trained with backpropagation through time.
- Bellec, G., et al. (2020). A solution to the learning dilemma for recurrent networks of spiking neurons. *Nature Communications*. https://doi.org/10.1038/s41467-020-17236-y — The e-prop learning rule, an online approximation to backpropagation through time for spiking networks.

### Surveys and reviews

- Eshraghian, J. K., et al. (2023). Training spiking neural networks using lessons from deep learning. *Proceedings of the IEEE*. https://arxiv.org/abs/2109.12894 — A tutorial on training spiking networks with deep-learning tools, with the snnTorch examples.
- Roy, K., Jaiswal, A. & Panda, P. (2019). Towards spike-based machine intelligence with neuromorphic computing. *Nature*. https://doi.org/10.1038/s41586-019-1677-2 — A review of spike-based computation and neuromorphic hardware.
- Gerstner, W., Kistler, W. M., Naud, R. & Paninski, L. (2014). *Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition*. Cambridge University Press. https://neuronaldynamics.epfl.ch/book.html — Free online textbook on spiking neuron models and networks.
