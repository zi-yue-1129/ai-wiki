---
status: complete
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

EigenPlaces, introduced by Berton, Trivigno, Caputo and Masone (2023), trains a place recognition network on several views of each place, so that the descriptor stays stable when the camera's viewpoint changes. The paper's argument is that viewpoint robustness has to be supervised during training: a model that sees each place from a single view does not learn it reliably. The parent subtopic is [Visual Localisation](index.md).

## Overview

EigenPlaces is a convolutional network trained as a classifier over places. Each place is represented by images taken from different viewpoints, and the groups are formed from the geometry of the scene, so that the same place appears with different headings and positions. The learned descriptor is then used for retrieval, as in other place recognition systems.

## Problem

A place recognition model trained on single views of each location learns features that depend on the viewpoint. When a robot returns to a place with a different heading, or from a slightly different position, the descriptor can change enough to miss the match. The paper asks whether training on explicit multi-view groups can make the descriptor robust to viewpoint without a large cost in training memory.

## Core idea

Organise the training data so that each place is seen from several viewpoints, and train the network to treat these views as one class. The grouping uses geometry, so the views within a group really do show the same place. This turns viewpoint robustness from a property the data may or may not have into a training objective.

## How it works

1. **Partition the map.** The training map, given as UTM coordinates, is split into 15 m by 15 m cells. Cells are grouped into subsets so that no two neighbouring cells share a subset, and the grid shifts after each epoch.
2. **Find a focal point per cell.** Within a cell, the method runs a principal component analysis on the centred coordinates. The first component approximates the road direction, and the second approximates the side of the road, where the facades are assumed to be. The focal point is

$$
c_i = \mathbb{E}[X_i] + D\, v_1,
$$

   where $\mathbb{E}[X_i]$ is the cell centre, $v_1$ is the first principal component and $D$ is the focal distance, set to 10 m in the main experiments.
3. **Form classes.** Images whose orientation points closest to the focal point are grouped into one class. Each cell gives a lateral class (focal point along the second component) and, for front-facing datasets, a frontal class. Each class therefore holds views of the same place from different positions and headings.
4. **Train and retrieve.** A convolutional backbone is trained on these classes, and the learned descriptor is stored for the database. For a query, the nearest stored descriptor gives the match.

The authors train on the San Francisco eXtra Large (SF-XL) dataset.

## Results

The paper compares against CosPlace, a classification-based place recognition model, using a ResNet-50 backbone. Recall at one (R@1) for the 2048-dimensional descriptors:

| Benchmark | CosPlace | EigenPlaces |
|---|---|---|
| Pitts30k | 90.9 | 92.5 |
| Tokyo 24/7 | 87.3 | 93.0 |
| SF-XL test v1 | 76.4 | 84.1 |
| MSLS Val | 87.4 | 89.1 |
| Nordland | 71.9 | 71.2 |
| SVOX Night | 50.7 | 58.9 |

EigenPlaces leads on most benchmarks, and CosPlace is slightly higher on Nordland. The memory and size claims in the paper are made against MixVPR, not CosPlace: the authors report under 7 GB of training GPU memory against more than 18 GB for MixVPR, and 2048-dimensional descriptors against MixVPR's 4096. The evaluation covers multi-view benchmarks (for example AmsterTime, Eynsham and Tokyo 24/7) and frontal-view benchmarks (MSLS, Nordland, St Lucia and SVOX).

## Limitations

- The evaluation sets are outdoor street and landscape imagery. The paper does not show transfer to indoor robotic settings.
- The method depends on geometric information, such as GPS-based coordinates, to form the training groups. This information must exist or be estimated for the training set.
- Night performance stays low: EigenPlaces reaches 58.9 on SVOX Night with 2048-dimensional descriptors, so viewpoint training does not solve appearance change. The VPR-Bench study treats appearance as a separate factor.

## Connections

- [Visual Localisation](index.md) places EigenPlaces next to the frozen-feature approach, AnyLoc.
- [AnyLoc](anyloc.md) represents the alternative that avoids training the encoder.
- [Navigation with visual goals](../navigation/index.md) uses place-level retrieval in a different way, to find the next waypoint.

## Open questions

- Whether multi-view training can be obtained for a robot that records only one traversal of a place.
- How much of the viewpoint robustness carries over when the same kind of network is run indoors.

## References

- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. https://openaccess.thecvf.com/content/ICCV2023/papers/Berton_EigenPlaces_Training_Viewpoint_Robust_Models_for_Visual_Place_Recognition_ICCV_2023_paper.pdf — The source of the geometric multi-view grouping, the SF-XL training and the benchmark tables quoted above. The arXiv version is [arXiv:2308.10832](https://arxiv.org/abs/2308.10832).
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — The frozen-feature alternative for place recognition, compared in the overview.
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision (2021). https://doi.org/10.1007/s11263-021-01469-5 — The benchmark that separates viewpoint from appearance change.
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — The self-supervised features used by the frozen alternative.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — Sim-to-real evidence for pretrained visual representations on a robot.
