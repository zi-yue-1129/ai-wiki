---
status: draft
last_reviewed: 2026-10-28
related:
  - society/interpretability
  - theory/models/transformer
  - brain-mind/neuroai
tags:
  - interpretability
  - probing
  - representations
aliases:
  - 探測分類器
  - 表徵分析
  - Probing classifiers
  - Representation analysis
  - Linear probes
---

# Probing classifiers and representation analysis

A probing classifier is a simple model trained to read a property from the internal activations of a larger network. If a small classifier can recover the property from a layer's activations, the layer is said to encode it. Probing is one of the oldest and most widely used tools for asking what a network represents, and it has close parallels in neuroscience, where the same logic is applied to recordings from the brain.

## Overview

Trained networks are opaque, but their activations can be read. A probe asks a concrete question: does this layer contain information about part of speech, object identity, the position of a piece on a board, or whether a statement is true? The probe is trained on frozen activations, so the network itself is not changed. A high probe accuracy suggests that the information is present in a form the probe can use. The difficulty is that a sufficiently powerful probe can find information that the network never uses, so probes alone cannot say what the model relies on.

## Key concepts

- **Probe**: a classifier or regressor trained on a layer's activations \(h\) to predict an external label \(y\).
- **Linear probe**: a probe of the form \(\hat{y} = \mathrm{softmax}(Wh + b)\). Its simplicity is deliberate, because information that a linear map can read is easier to say the model is using.
- **Control task**: a probe trained on random labels that are assigned to the same inputs, used to measure how much a probe can memorise.
- **Selectivity**: the probe's accuracy on the real task minus its accuracy on the control task.
- **Representational similarity**: a comparison of two systems by the similarity structure of their responses to the same stimuli, rather than by matching individual units.

## How it works

The usual procedure has four steps:

1. Choose a trained model and a layer.
2. Collect activations \(h\) for inputs whose labels \(y\) are known, and split the data into training and test sets.
3. Train a probe on the training activations and measure accuracy on the test set.
4. Compare the result with a baseline, such as a probe on the raw input, a probe on a randomly initialised network, or a control task.

Comparing layers shows where information appears and where it disappears. Alain and Bengio (2016) used linear probes at each depth of a deep image network and found that linear separability of the class labels generally increased with depth. Their work made the probe a standard diagnostic.

## Key methods

- **[Linear probes](linear-probes.md) (Alain & Bengio, 2016).** Train one linear classifier per layer to show how class information develops through depth. The method is simple and fast; its weakness is that it reports decodability, not use.
- **Structural probes (Hewitt & Manning, 2019).** Learn a linear transformation of word representations under which squared distances approximate distances in the syntax tree. The probe recovers tree structure from contextual embeddings, which a label-classification probe would not show.
- **[Control tasks](control-tasks.md) (Hewitt & Liang, 2019).** Report selectivity, the gap between real-task and random-label accuracy, so that a high score means the representation encodes the property and the probe is not simply memorising.
- **[Representational similarity analysis](representational-similarity-analysis.md) (Kriegeskorte et al., 2008).** Compare two systems through the matrices of pairwise dissimilarities between their responses, which allows comparisons between a network layer and a brain region on the same stimuli.
- **Probes with causal interventions (Li et al., 2023).** Train a sequence model on Othello move sequences, probe its internal board state, and intervene on that representation to test whether the model's output changes. The intervention tests use, not just presence.

## Results

Hewitt and Liang (2019) argue that probes can memorise labels from word types, so accuracy alone overstates what a representation contains; selectivity measures the gap. Hewitt and Manning (2019) report that a linear transformation of ELMo and BERT embeddings makes squared distances track parse-tree distance and squared norms track depth, and that baselines lack this structure. Li et al. (2023) show that a model trained only on move sequences develops a nonlinear internal representation of the board state, and that interventions on this representation can control the model's output. Park et al. (2023) report linear representations of concepts in LLaMA-2 and show that these connect to linear probing and steering vectors.

## Limits

- **Presence is not use.** A probe shows that information is decodable, not that the model relies on it. Belinkov (2022) critically reviews the methodological limitations of probing classifiers.
- **Probe capacity.** The choice of probe architecture changes the conclusions. Linear probes are used to limit this, but nonlinear structure can still be missed.
- **Label quality.** Probes inherit the errors in their labels, and labels for abstract properties such as truth are hard to define.
- **Confounds.** A probe may pick up a correlated property. Balanced datasets and controls reduce this risk.

## Connections

Probing is the most direct shared tool between neural network interpretability and neuroscience. Representational similarity analysis, which originated in neuroscience, compares networks with brain recordings; see [NeuroAI](../../brain-mind/neuroai/index.md) for the wider programme. The architectures usually probed, Transformers and their residual streams, are described in [Transformers](../../theory/models/transformer/index.md). Probing is one of the methods listed in the [Interpretability](index.md) overview, next to [feature attribution](feature-attribution.md).

## Applications

- Checking whether a language model encodes syntax, semantics or world state before deciding where to intervene.
- Diagnosing which layers carry information useful for a downstream task.
- Comparing models and brain areas on shared stimuli.
- Auditing for sensitive attributes, to see whether a representation encodes them even when they are removed from the input.

## Open questions

- **Causal use.** How to link probe directions to the computation the model performs, not only to what it contains.
- **Non-linear and distributed codes.** Linear probes can miss information carried in complex ways; whether better probes reveal it without overfitting is unresolved.
- **Concept geometry.** Whether the linear representation hypothesis holds broadly across models and concepts is an active area of study.

## References

### Seminal papers

- Alain, G. & Bengio, Y. (2016). Understanding intermediate layers using linear classifier probes. *arXiv preprint*. https://arxiv.org/abs/1610.01644 — Introduces linear probes at each layer of a deep network to measure how class information develops with depth.
- Hewitt, J. & Manning, C. D. (2019). A Structural Probe for Finding Syntax in Word Representations. *Proceedings of NAACL-HLT 2019*. https://doi.org/10.18653/v1/N19-1419 — Shows that a linear transformation of contextual embeddings recovers syntax tree distances.
- Hewitt, J. & Liang, P. (2019). Designing and Interpreting Probes with Control Tasks. *Proceedings of EMNLP-IJCNLP 2019*. https://doi.org/10.18653/v1/D19-1275 — Introduces control tasks and selectivity to separate probe memorisation from encoded information.
- Kriegeskorte, N., Mur, M. & Bandettini, P. (2008). Representational similarity analysis – connecting the branches of systems neuroscience. *Frontiers in Systems Neuroscience*. https://doi.org/10.3389/neuro.06.004.2008 — Defines representational similarity analysis for comparing systems through their response geometry.
- Li, K., Hopkins, A. K., Bau, D., Viégas, F., Pfister, H. & Wattenberg, M. (2023). Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task. *Proceedings of ICLR 2023*. https://arxiv.org/abs/2210.13382 — Finds a nonlinear board-state representation in a model trained on Othello move sequences, and tests it with interventions.
- Park, K., Choe, Y. J. & Veitch, V. (2023). The Linear Representation Hypothesis and the Geometry of Large Language Models. *arXiv preprint*. https://arxiv.org/abs/2311.03658 — Formalises linear representations of concepts in language models and tests them.

### Surveys and textbooks

- Belinkov, Y. (2022). Probing Classifiers: Promises, Shortcomings, and Advances. *Computational Linguistics*, 48(1), 207–219. https://doi.org/10.1162/coli_a_00422 — Critically reviews the probing framework, its promises, shortcomings and advances.

## Further learning

- [Transformer Circuits Thread](https://transformer-circuits.pub/) — mechanistic interpretability research that extends probing to causal analysis.
