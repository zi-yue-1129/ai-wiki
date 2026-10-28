---
tags:
  - self-supervised learning
  - pretext tasks
---

# Pretext Tasks

Pretext tasks are hand-designed prediction problems, such as predicting the relative position of two patches or the rotation of an image. Solving them requires understanding the data, and the learned features are then reused on real tasks. Early self-supervised vision relied on these tasks, and their limits motivated the later methods.

## Overview

A pretext task is defined by a transformation of the input and a target that the model must recover. Because the target is created from the data, no human labels are needed. The usefulness of the features depends on whether solving the task requires semantic understanding rather than shortcuts.

## Common pretext tasks

- **Context prediction** (Doersch et al., 2015) gives the network two patches from one image and asks for their relative position. It was an early demonstration that spatial structure can be learned without labels.
- **Rotation prediction** (Gidaris et al., 2018) rotates an image by 0, 90, 180 or 270 degrees and asks which rotation was applied. The task is simple, yet it produces useful features.
- **Colourisation** predicts colour channels from greyscale images, which requires recognising objects and their typical colours.
- **Jigsaw puzzles** shuffle patches and ask for the permutation, forcing the model to learn parts and their arrangement.
- **Temporal order** asks whether frames or audio segments are in the correct order, which uses the arrow of time in video.

## Shortcuts

Many pretext tasks can be solved by shortcuts. Context prediction can be solved by matching chromatic aberration at patch edges, and rotation prediction can exploit image borders. Good pretext design removes these cues, which is hard in practice.

## Connections

Predictive pretext tasks share the goal of [masked prediction](../masked-prediction/index.md) and [contrastive learning](../contrastive-learning/index.md): all turn unlabelled data into a supervised-looking problem. Contrastive predictive coding is a general pretext task for sequences, see [contrastive learning](../contrastive-learning/index.md).

## Applications

Early unsupervised pre-training for object detection, learning features from video and audio without labels, and as baselines that show how much a representation depends on the choice of task.

## Open questions

Which pretext task produces the most transferable representation is largely an empirical question. Pretext tasks tend to be replaced by more general objectives when enough data and compute are available, and it is unclear what the best hand-designed task would be.

## References

### Seminal papers

- Doersch, Gupta & Efros (2015), "Unsupervised visual representation learning by context prediction", ICCV, arXiv:1505.05192 — Learns features by predicting the relative position of image patches.
- Gidaris, Singh & Komodakis (2018), "Unsupervised representation learning by predicting image rotations", ICLR, arXiv:1803.07728 — Rotation prediction, a simple pretext task with strong transfer results.
- Oord, Li & Vinyals (2018), "Representation learning with contrastive predictive coding", arXiv:1807.03748 — Predicts future latent states of sequences, a general pretext task.

### Surveys and textbooks

- Bengio, Courville & Vincent (2013), "Representation learning: a review and new perspectives", *IEEE TPAMI* 35(8), arXiv:1206.5538 — Survey placing pretext tasks among representation-learning methods.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Kolesnikov, Zhai & Beyer (2019), "Revisiting self-supervised visual representation learning", CVPR, arXiv:1901.09005 — Careful comparison of pretext tasks under the same architecture and training budget.

## Further reading

- Noroozi & Favaro (2016), on jigsaw puzzles, and Zhang, Isola & Efros (2016), on colourisation. Both at ECCV. No link checked.
