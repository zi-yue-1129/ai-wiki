---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - robotics
  - place recognition
  - viewpoint robustness
aliases:
  - EigenPlaces
  - 視角穩健的地點辨識
---

# EigenPlaces

EigenPlaces, introduced by Berton, Trivigno, Caputo and Masone (2023), trains a place recognition network on several views of each place, so that the descriptor stays stable when the camera's viewpoint changes. The paper's argument is that viewpoint robustness has to be supervised during training, because it does not appear reliably when a model sees each place from a single view. The parent subtopic is [Visual Localisation](index.md).

## Overview

EigenPlaces is a convolutional network trained as a classifier over places. Each place is represented by groups of images taken from different viewpoints, and the groups are formed from the geometry of the scene, so that the same place appears with different headings and positions. The learned descriptor is then used for retrieval as in other place recognition systems.

## Problem

A place recognition model trained on single views of each location learns features that depend on the viewpoint. When a robot returns to a place with a different heading or from a slightly different position, the descriptor can change enough to miss the match. The paper asks whether training on explicit multi-view groups can make the descriptor robust to viewpoint without a large memory cost.

## Core idea

Organise the training data so that each place appears from several viewpoints, and train the network to classify all of these views as one place. The grouping uses geometry, so that the views within a group really are of the same place. This turns viewpoint robustness from a property the data may or may not have into a training objective.

## How it works

1. Build training groups for each place from images taken at different viewpoints, using geometric information about the scene.
2. Train a convolutional backbone with a classification-style objective over the places, with each place represented by its multi-view group.
3. Use the learned descriptor for retrieval: store descriptors for the database, and find the nearest stored descriptor for each query.

## Results

The authors report state-of-the-art results on most of the place recognition benchmarks they test, and they report that the method uses less training memory and produces smaller descriptors than CosPlace, the earlier classification-based method. The experiments are outdoors, on large street-level datasets. The exact figures should be checked in the paper's tables, since they depend on the benchmark used.

## Limitations

- The results are on outdoor, street-level data, so their transfer to indoor robotic settings is not shown in the paper.
- The method depends on geometric information to form the multi-view groups, which must be available or estimated for the training set.
- Viewpoint training does not by itself address appearance change, which the benchmark of Zaffar et al. (2021) treats as a separate factor.

## Connections

- [Visual Localisation](index.md) places EigenPlaces next to the frozen-feature approach, AnyLoc.
- [AnyLoc](anyloc.md) represents the alternative that avoids training the encoder.
- [Navigation with visual goals](../navigation/index.md) uses place-level retrieval in a different way, to find the next waypoint.

## Open questions

- Whether multi-view training can be obtained for a robot that records only one traversal of a place.
- How much of the viewpoint robustness carries over when the same network is run indoors.

## References

- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — the source of the multi-view training and the outdoor results.
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — the frozen-feature alternative for place recognition.
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — the benchmark that separates viewpoint from appearance change.
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — the self-supervised features that the frozen alternative relies on.
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — the role of pretraining augmentations in visual robustness.
