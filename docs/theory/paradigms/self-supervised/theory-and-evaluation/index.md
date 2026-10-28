---
tags:
  - self-supervised learning
  - theory
  - evaluation
---

# Theory and Evaluation

Self-supervised learning is easy to run and hard to judge. This page covers why the objectives work, what they assume about the data, and how to measure whether the learned features are good.

## Overview

The loss used during pre-training is not the goal. What matters is how well the representation supports downstream tasks, and how cheaply it adapts to them. Theory explains which properties of the data make the pretext task useful, and evaluation protocols measure transfer.

## Theoretical views

- **Mutual information.** Contrastive losses such as InfoNCE maximise a lower bound on the mutual information between views, so the views should share the information needed downstream.
- **Alignment and uniformity.** Good embeddings place positive pairs close together and spread the embeddings uniformly on the hypersphere (Wang & Isola, 2020).
- **Latent classes.** Analyses show that if positive pairs share a latent class, minimising a contrastive loss yields features that separate the classes linearly (Saunshi et al., 2019).

## Evaluation protocols

- **Linear probing** freezes the encoder and trains a linear classifier on top. It measures how linearly separable the features are.
- **Fine-tuning** updates all weights on the downstream task, which measures initialisation quality under more training.
- **Few-shot and zero-shot** evaluation tests how much the representation supports learning from very few examples, or none.
- **Transfer across domains** checks whether features learned on one dataset help on another, a stricter test than in-domain accuracy.

Kolesnikov et al. (2019) show that rankings of methods can change with architecture and training budget, so comparisons need matched conditions.

## Failure modes

Collapse, where all embeddings become the same, and shortcut learning, where the model exploits cues in the augmentations, are the main failures. Both can give good pre-training loss with poor features, which is why evaluation on downstream tasks is necessary.

## Connections

The theory of alignment and uniformity links to [contrastive learning](../contrastive-learning/index.md). Collapse is discussed in [non-contrastive methods](../non-contrastive-methods/index.md). Evaluation practice follows [supervised evaluation](../../supervised/evaluation-and-validation/index.md), with extra attention to transfer.

## Applications

Choosing which pre-trained model to deploy, diagnosing failures of representation learning in new domains such as medical or scientific data, and designing benchmarks that reward transfer rather than pre-training loss.

## Open questions

A complete theory of why self-supervised features transfer is missing. Good benchmarks for non-vision domains are scarce, and it is unclear how to measure whether a representation captures causal or only correlational structure.

## References

### Seminal papers

- Wang & Isola (2020), "Understanding contrastive representation learning through alignment and uniformity on the hypersphere", ICML, [arXiv:2005.10242](https://arxiv.org/abs/2005.10242) — Defines alignment and uniformity as the two properties that contrastive losses optimise.
- Oord, Li & Vinyals (2018), "Representation learning with contrastive predictive coding", [arXiv:1807.03748](https://arxiv.org/abs/1807.03748) — Connects the InfoNCE loss to mutual information estimation.
- Saunshi, Plevrakis, Arora, Khodak & Khandeparkar (2019), "A theoretical analysis of contrastive unsupervised representation learning", ICML, [arXiv:1902.09229](https://arxiv.org/abs/1902.09229) — Gives guarantees that contrastive features support linear classification on latent classes.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Kolesnikov, Zhai & Beyer (2019), "Revisiting self-supervised visual representation learning", CVPR, [arXiv:1901.09005](https://arxiv.org/abs/1901.09005) — Shows that method rankings depend on architecture and budget, so comparisons must be matched.
- Chen, Kornblith, Norouzi & Hinton (2020), "A simple framework for contrastive learning of visual representations", ICML, [arXiv:2002.05709](https://arxiv.org/abs/2002.05709) — Includes an extensive linear-probing evaluation protocol that many later papers reuse.
