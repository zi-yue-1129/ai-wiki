---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics
  - theory/paradigms/self-supervised/non-contrastive-methods
tags:
  - robotics
  - visual localisation
  - place recognition
  - visual representation
aliases:
  - Visual localisation
  - Visual place recognition
  - 視覺定位
---

# Visual Localisation

Visual localisation asks where a robot is by comparing its current camera view with images it has seen before. The most common form is place recognition: given a query image, retrieve the matching image from a database. Robots need this to recover from drift, to close loops and to relocalise in a map. This subtopic covers how the features are learned, how methods are evaluated under changes of viewpoint and appearance, and how frozen pretrained encoders have changed the field.

## Overview

A place recognition system has three parts: an encoder that turns an image into a descriptor, an aggregation step that combines local features into one vector, and a nearest-neighbour search over the database. Methods differ in how they train the encoder and whether they use a frozen foundation model or a network trained for place recognition.

Two kinds of change matter. Viewpoint change, such as a different heading or position, and appearance change, such as a shift in lighting, weather or season. A method can be strong against one and weak against the other, so evaluation needs both.

## Key methods

Each method has its own page. The overview and comparison here are brief.

| Method | Encoder | Training | What it changes |
|---|---|---|---|
| [AnyLoc](anyloc.md) (Keetha et al., 2023) | Frozen DINOv2 features, aggregated without training | None for the encoder | Shows that a general foundation model can match or beat task-trained place recognition encoders |
| [EigenPlaces](eigenplaces.md) (Berton et al., 2023) | Convolutional network | Trained on multiple views of each place | Makes viewpoint robustness a training target, not an accident of the data |

## Evaluation under change

Zaffar et al. (2021) build a benchmark that separates viewpoint change from appearance change by controlled amounts. Their results show that heading and three-dimensional offsets hurt matching more than a lateral shift, and that directional lighting hurts more than uniform brightness. The benchmark is useful because a single score on a mixed dataset hides which kind of change is failing.

## Pretrained representations in robotics

The same question appears in robotic manipulation and navigation. Burns et al. (2023) find that pretrained visual representations differ in robustness to lighting and texture changes, and that the choice of augmentations matters more than the choice of supervision. Silwal et al. (2024) report that pretrained encoders keep their performance on a real robot, while an encoder trained from scratch does not. These results support using frozen foundation features as the starting point for place recognition on robots, provided their robustness is measured on the target platform.

## Connections

- [Robotics](../index.md) places visual localisation among the robotic tasks in the wiki.
- [Navigation with visual goals](../navigation/index.md) uses the same retrieval idea to find the next waypoint in a graph of images.
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) describes the frozen encoder used by AnyLoc.

## Open questions

- How well descriptors trained on one season transfer to very different conditions over long periods.
- Whether viewpoint robustness from multi-view training can be obtained cheaply on a robot that only records one traversal.

## References

- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — a benchmark that separates viewpoint and appearance change.
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — frozen foundation features for place recognition across domains.
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — trains place recognition on multiple views of each place for viewpoint robustness.
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — pretrained representation robustness under visual shifts.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — sim-to-real transfer of pretrained encoders on a robot.
