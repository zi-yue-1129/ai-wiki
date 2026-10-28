---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - interpretability
  - dictionary learning
aliases:
  - Sparse autoencoders
  - SAE
  - Dictionary learning
  - 稀疏自編碼器
  - 字典學習
---

# Sparse autoencoders and feature dictionaries

A sparse autoencoder (SAE) is a small network trained to reconstruct a model's internal activations through a bottleneck, with a penalty that keeps most of the bottleneck units inactive for any given input. The active units then form a **feature dictionary**: each unit is a direction in activation space, and an input is described as a short combination of them. Researchers use SAEs to find features that are more interpretable than individual neurons, mostly in large language models.

## Overview

Neurons in large networks are often **polysemantic**, meaning they respond to several unrelated concepts (see [mechanistic interpretability](mechanistic-interpretability.md)). One explanation is superposition: a network packs more features into its neurons than it has dimensions, so each neuron mixes several features. If that is right, the features are directions in activation space, not single neurons, and a method that finds directions could recover them.

Sparse dictionary learning is the classic tool for this. Olshausen and Field (1996) showed that a sparse code trained on natural image patches produces filters resembling the receptive fields of cells in primary visual cortex. The same idea, applied to the activations of a language model, is the basis of SAE interpretability work.

## Key concepts

- **Encoder and decoder**: the encoder maps an activation to a sparse code, and the decoder maps the code back to an approximation of the activation.
- **Dictionary**: the decoder's columns, one per feature.
- **Sparsity**: the fraction of features active at once. Sparsity is enforced by an L1 penalty or by an explicit top-k rule, described in [k-sparse autoencoders](k-sparse-autoencoders.md).
- **Monosemantic feature**: a feature that responds to one concept in a human-recognisable way.

## How it works

An SAE is trained on a large set of activations collected from one layer of a model. The loss has two terms: reconstruction error, which keeps the features faithful to the activations, and a sparsity term, which keeps the code short. After training, each feature is examined by looking at the inputs that activate it most strongly. A feature is considered interpretable when those inputs share a clear concept. Interpretability is then checked by intervention: adding or removing a feature's direction should change the model's output in the predicted way.

Cunningham et al. (2023) train SAEs on activations from a small language model and report that many features are interpretable under this procedure, more so than the neurons they were derived from. Bricken et al. (2023) apply the method to a small transformer with a single layer and report many features that look monosemantic on inspection.

## Scaling

The main question is whether the method scales. Templeton et al. (2024) train SAEs on activations from a production-scale model and report millions of features, including features for concrete entities and some abstract concepts, along with features that can be used to steer behaviour. Gao et al. (2024) show that SAE size and sparsity can be scaled with predictable trade-offs between reconstruction quality and sparsity, and introduce a top-k architecture that makes training more stable. Lieberum et al. (2024) release a suite of SAEs for an open model family, which lets other researchers study the features without training their own. A [JumpReLU autoencoder](jumprelu-sae.md) gives each feature its own threshold to improve reconstruction.

Scaling introduces its own problems. An SAE that reconstructs activations well may still miss features, and a feature that is interpretable in one SAE may split into several in a larger one, so the features depend on the dictionary size.

## Steering and use

A feature can be used to steer the model: adding its direction to the residual stream changes what the model says about that concept. Templeton et al. (2024) present demonstrations of this kind. Steering is useful for checking that a feature is causal, but it is also a potential safety tool, since features linked to unwanted behaviour could in principle be suppressed. Whether that holds for real behaviours is open.

## Known failure modes

- **Reconstruction is not faithfulness.** An SAE can reconstruct activations well while learning features that the model does not use.
- **Feature splitting and absorption.** One concept can be split into several features, or a feature can absorb another when they co-occur.
- **Dependence on dictionary size.** The set of features changes with the size and sparsity of the SAE, so a feature is a property of a particular dictionary.
- **Interpretation by inspection.** Labelling a feature from its top activations is subjective, and automated labelling can be wrong.
- **Dead and dense features.** Some dictionary units never activate, and others activate on most inputs, which weakens their meaning.

## Connections

Sparse coding has a long history in neuroscience. The efficient-coding hypothesis, that sensory systems represent inputs with few active units, is a motivation for the image-coding results above, and the link is discussed in [sparse coding](../../brain-mind/computational-neuroscience/sparse-coding/index.md). The SAE approach differs in that it is applied to a trained artificial network and checked by intervention, which neuroscience cannot do as readily. For the architecture being analysed, see [transformers](../../theory/models/transformer/index.md).

## Applications

- Finding features for concepts, such as entities or safety-relevant topics, to use in audits.
- Steering model outputs by adding feature directions.
- Comparing models by the features they share or lack.

## Open questions

- Are SAE features the actual units a model computes with, or a useful but partial description?
- Can dictionaries be trained that avoid feature splitting without losing interpretability?
- Which features matter for safety, and can they be found reliably enough to audit a model?

## References

### Seminal papers

- Olshausen, B. A. & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*, 381, 607–609. https://doi.org/10.1038/381607a0 — Shows that a sparse coding objective trained on natural images produces receptive-field-like filters.
- Makhzani, A. & Frey, B. (2014). *k-Sparse Autoencoders*. ICLR 2014. https://arxiv.org/abs/1312.5663 — Enforces sparsity with a top-k rule in place of an L1 penalty.
- Cunningham, H. et al. (2023). *Sparse Autoencoders Find Highly Interpretable Features in Language Models*. arXiv:2309.08600. https://arxiv.org/abs/2309.08600 — Applies sparse autoencoders to language model activations and reports interpretable features.

### Surveys and textbooks

- Gao, L. et al. (2024). *Scaling and evaluating sparse autoencoders*. arXiv:2406.04093. https://arxiv.org/abs/2406.04093 — Studies how sparse autoencoders scale with dictionary size, and proposes a top-k architecture and evaluation metrics.

### Articles and documentation

- Bricken, T. et al. (2023). *Towards Monosemanticity: Decomposing Language Models With Dictionary Learning*. Transformer Circuits Thread. https://transformer-circuits.pub/2023/monosemantic-features/index.html — Applies dictionary learning to a small transformer and reports monosemantic features.
- Templeton, A. et al. (2024). *Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet*. Transformer Circuits Thread. https://transformer-circuits.pub/2024/scaling-monosemanticity/ — Scales sparse autoencoders to a production-scale model and reports features and steering demonstrations.
- Lieberum, T. et al. (2024). *Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2*. arXiv:2408.05147. https://arxiv.org/abs/2408.05147 — Releases a suite of sparse autoencoders for an open model family.
- Rajamanoharan, S. et al. (2024). *Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU Sparse Autoencoders*. arXiv:2407.14435. https://arxiv.org/abs/2407.14435 — Introduces a sparse autoencoder with a thresholded JumpReLU activation that improves reconstruction at a given sparsity.

## Further learning

- [SAELens](https://github.com/decoderesearch/SAELens) — Open-source library for training and analysing sparse autoencoders on language models.
