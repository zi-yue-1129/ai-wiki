---
status: complete
last_reviewed: 2026-10-28
related:
  - society/interpretability
tags:
  - interpretability
  - probing
  - representations
aliases:
  - 線性探測器
  - Linear probes
  - Linear classifier probes
---

# Linear probes

!!! info "Part of Probing classifiers"
    This method page belongs to [Probing classifiers and representation analysis](probing.md). It explains the method in detail; the parent page compares it with the other probing methods.

A linear probe is a linear classifier trained on the frozen activations of one layer of a network to predict an external label. If it succeeds, the information is linearly decodable from that layer. Alain and Bengio (2016) introduced the approach as a way to track how class information develops with depth.

## Problem

A deep network's intermediate layers are hard to read directly. The question is how information about the output class is organised as the representation passes through the layers. The problem is to measure this without changing the network, and in a way that is easy to compare across layers.

## Core idea

Freeze the trained network. For each layer of interest, train a linear classifier on that layer's activations, using labelled examples. The probe is trained independently of the model, so its accuracy reflects what the layer contains rather than what the network was trained to do.

## Equation

For an activation vector $h$ from the chosen layer, the probe predicts

$$
\hat{y} = \mathrm{softmax}(W h + b),
$$

and only $W$ and $b$ are learned. Training minimises the cross-entropy between $\hat{y}$ and the true labels.

## Results

Alain and Bengio report that the linear separability of features increases monotonically with depth. They observe this for ResNet-50 and Inception v3, and also for a small convolutional network trained on MNIST. The conclusion is about how class information develops across layers, not about the network's final accuracy. Later work shows the other side of the same measurement: Li et al. (2023) find that a linear probe does not recover a board state from a sequence model trained on Othello moves, while a nonlinear probe does.

## Limitations

- **Presence, not use.** A decodable feature need not be one the model relies on. Belinkov (2022) reviews this limitation of probing in general, and interventions are needed to test use.
- **Probe choice.** A linear probe reads only linear structure. Information that a nonlinear map could read is missed, and a more powerful probe risks reading information the model does not use.
- **Label quality.** The probe inherits any error in the labels, and labels for abstract properties are hard to define.

## Connections

Linear probes are the simplest member of the [probing](probing.md) family. [Representational similarity analysis](representational-similarity-analysis.md) compares whole representations rather than predicting one label, and [control tasks](control-tasks.md) were introduced to tell whether a probe's accuracy reflects the representation or the probe's own capacity. Causal tests of what a representation is used for connect to [mechanistic interpretability](mechanistic-interpretability.md). For the broader comparison of explanation methods, see the [interpretability overview](index.md).

## Applications

- Tracking where a language model first represents syntactic or semantic properties across its layers.
- Checking whether a vision model's intermediate layers contain a concept before the final layer, for debugging.
- Measuring whether a fine-tuned model has retained or lost information from its pretrained layers.

## Open questions

- Which probe capacity is enough to say a property is represented, without reading information the model never uses?
- How well do probe results predict whether an intervention on the representation changes behaviour?
- Can probes be trained in a way that avoids reading spurious correlations in the labels?

## References

### Seminal papers

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. arXiv:1610.01644. https://arxiv.org/abs/1610.01644 — Introduces linear probes at each depth and shows that linear separability of class information grows with depth.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — Uses a linear probe on contextual embeddings to recover parse-tree structure.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Shows that probe accuracy must be read against control tasks.

### Surveys and textbooks

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Critically reviews the probing framework, its promises, shortcomings and advances.
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Probes a model for board state, finds that nonlinear probes recover it, and tests the representation with interventions.
