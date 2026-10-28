---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - transformers
aliases:
  - Mechanistic interpretability
  - Circuits
  - 機械式可解釋性
  - 電路
---

# Mechanistic interpretability and circuits

Mechanistic interpretability tries to reverse-engineer the algorithms that a trained neural network has learned. Instead of asking which inputs drove an output, it asks which internal components compute which intermediate results, and how they combine. A **circuit** is a small subnetwork, made of neurons, attention heads and the connections between them, that implements an identifiable computation. The field's central bet is that trained networks are structured enough for such circuits to be found and checked.

## Overview

Post-hoc explanation methods such as LIME or SHAP (see [interpretability](index.md)) describe input-output behaviour, and their explanations can be unfaithful. Mechanistic interpretability aims at the mechanism itself. A good mechanistic claim is causal and testable: if a component is removed or altered, the behaviour it is said to support should change in the predicted way, and nothing else should change much.

The approach started with vision models. Olah et al. (2020) describe circuits in convolutional networks, such as curve detectors that combine edge detectors, and argue that features and their connections can be studied in the same way. The approach moved to language models after Elhage et al. (2021) gave a mathematical framework for transformer circuits.

## Key concepts

- **Residual stream**: the vector of activations that each layer reads from and writes to in a transformer. Components communicate by reading and writing to it.
- **Attention head**: a component that moves information between token positions. Heads can be studied by their attention patterns and by what they write to the residual stream.
- **Circuit**: a subgraph of components that performs a particular computation.
- **Causal intervention**: changing an activation, by ablation, patching or steering, to test whether the component carries the claimed information.

## Key findings

Several circuits are now well described.

**Induction heads.** Olsson et al. (2022) identify a two-head mechanism that completes repeated sequences: one head records which token preceded each token, and a second head attends to earlier occurrences of the current token and copies the token that followed. The mechanism appears during a sharp transition in training and is linked to in-context learning. The paper presents this as evidence for a general mechanism, but the link to all forms of in-context learning is a hypothesis.

**Factual recall.** Meng et al. (2022) use causal tracing to show that factual associations in GPT-style models are localised, mainly in mid-layer MLP modules at the final token of a subject. They then edit one association by changing those weights, in a method called ROME. The localisation claim is supported by intervention results, but the editing results describe the tested facts, not every fact.

**Indirect object identification.** Wang et al. (2022) reverse-engineer a circuit in GPT-2 small that completes sentences such as "When John and Mary went to the store, John gave a drink to ___". They identify groups of heads with distinct roles, such as detecting duplicated names and suppressing them, and check the proposed circuit with ablation experiments. This is one of the most complete circuit analyses for a language model, but it covers one small model and one task.

**Grokking.** Nanda et al. (2023) reverse-engineer how a small transformer learns modular addition after a long delay in generalisation, showing that the network gradually builds a periodic algorithm that can be measured with progress measures before test accuracy rises.

## Superposition

A network with $d$ neurons can represent many more than $d$ features if features are stored as nearly orthogonal directions that rarely co-occur. Elhage et al. (2022) study this in small toy models, showing that networks trade off how many features they represent against how much interference they accept, and that individual neurons can then respond to several unrelated features. This is **polysemanticity**. Superposition explains why neurons are often hard to interpret one at a time, and it motivates [sparse autoencoders](sparse-autoencoders.md), which try to recover the features as directions.

## Methods

- **Activation patching** (Meng et al., 2022; Wang et al., 2022): replace activations from one run with those from another to test which components carry a result.
- **Path patching and circuit discovery** (Conmy et al., 2023): search automatically for the edges of a circuit whose ablation changes the behaviour most, rather than inspecting components by hand.
- **Feature analysis**: decompose activations into features, usually with sparse autoencoders, and test whether the features are causally used.

## Connections

Neuroscience faces the same kind of question, how a distributed system computes, but neuroscientists cannot inspect every unit or set every weight. Jonas and Kording (2017) argue that standard neuroscience methods would struggle even on a microprocessor whose design is known, which is a caution for both fields. Interpretability is also a source of analogies for neuroscience, such as the idea of a unit tuned to a concept, discussed in [computational neuroscience](../../brain-mind/computational-neuroscience/index.md). For background on the transformer architecture, see [transformers](../../theory/models/transformer/index.md).

## Applications

- Debugging: finding circuits that cause a failure, such as a spurious correlation, and removing them.
- Auditing for hidden behaviour, which connects to [deceptive alignment](../safety-alignment/deceptive-alignment.md).
- Steering behaviour by adding or removing directions identified with a concept.

## Open questions

- Which circuits are general, and which are specific to one model or task?
- Do circuits found in small models persist in models many times larger?
- How much of a model's behaviour can be explained by a finite set of circuits at all?
- How faithful are interpretations to the actual computation, given that a circuit can be a useful story without being the full mechanism?

## References

### Seminal papers

- Olah, C. et al. (2020). *Zoom In: An Introduction to Circuits*. Distill. https://doi.org/10.23915/distill.00024.001 — Argues that features and the connections between them in vision networks can be studied as circuits.
- Elhage, N. et al. (2021). *A Mathematical Framework for Transformer Circuits*. Transformer Circuits Thread. https://transformer-circuits.pub/2021/framework/index.html — Frames the attention and MLP components of small transformers as linear algebra on the residual stream.
- Elhage, N. et al. (2022). *Toy Models of Superposition*. Transformer Circuits Thread. https://transformer-circuits.pub/2022/toy_model/index.html — Studies how networks represent more features than they have neurons, using toy models.
- Olsson, C. et al. (2022). *In-context Learning and Induction Heads*. Transformer Circuits Thread. https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html — Identifies induction heads as a mechanism for copying sequences and links them to in-context learning.
- Meng, K. et al. (2022). *Locating and Editing Factual Associations in GPT*. NeurIPS 2022. https://arxiv.org/abs/2202.05262 — Uses causal tracing to localise factual recall and edits it by changing mid-layer weights.
- Wang, K. et al. (2022). *Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small*. arXiv:2211.00593. https://arxiv.org/abs/2211.00593 — Reverse-engineers a complete circuit for a language-understanding task in GPT-2 small.
- Nanda, N. et al. (2023). *Progress Measures for Grokking via Mechanistic Interpretability*. ICLR 2023. https://arxiv.org/abs/2301.05217 — Reverse-engineers the algorithm a small transformer learns for modular addition.

### Surveys and textbooks

- Jonas, E. & Kording, K. P. (2017). *Could a Neuroscientist Understand a Microprocessor?* PLOS Computational Biology. https://doi.org/10.1371/journal.pcbi.1005268 — Shows that standard neuroscience analysis methods struggle to explain a microprocessor whose design is fully known.
- Conmy, A. et al. (2023). *Towards Automated Circuit Discovery for Mechanistic Interpretability*. NeurIPS 2023. https://arxiv.org/abs/2304.14997 — Automates the search for circuits by testing which edges matter for a behaviour.

### Articles and documentation

- Olah, C. et al. *Transformer Circuits Thread*. https://transformer-circuits.pub/ — Ongoing series of mechanistic interpretability papers, including the primary sources above.

## Further learning

- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens) — Open-source library for inspecting and intervening on transformer activations.
