---
status: draft
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

For an activation vector \(h\) from the chosen layer, the probe predicts

\[
\hat{y} = \mathrm{softmax}(W h + b),
\]

and only \(W\) and \(b\) are learned. Training minimises the cross-entropy between \(\hat{y}\) and the true labels.

## Results

The paper reports that linear separability of the features increases monotonically with depth, and it shows this experimentally for Inception v3 and ResNet-50. The conclusion is about how class information develops across layers, not about the network's final accuracy.

## Limitations

- **Presence, not use.** A decodable feature need not be one the model relies on. Belinkov (2022) reviews this limitation of probing in general.
- **Probe choice.** A linear probe reads only linear structure. Information that a nonlinear map could read is missed, and a more powerful probe risks reading information the model does not use.
- **Label quality.** The probe inherits any error in the labels, and labels for abstract properties are hard to define.

## References

### Seminal papers

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — Introduces linear probes at each depth to show how linear separability of class information grows with depth.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — Uses a linear probe on contextual embeddings to recover parse-tree structure.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Shows that probe accuracy must be read against control tasks.

### Surveys and textbooks

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Critically reviews the probing framework, its promises, shortcomings and advances.
- Li, K. et al. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Probes a model for board state and then tests the representation with interventions.
