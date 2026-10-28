---
status: complete
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
| [AnyLoc](anyloc.md) (Keetha et al., 2023) | Frozen DINOv2 features, aggregated without training | None for the encoder | Shows that a general foundation model can outperform task-trained place recognition encoders on several benchmarks |
| [EigenPlaces](eigenplaces.md) (Berton et al., 2023) | Convolutional network | Trained on multiple views of each place, grouped by scene geometry | Makes viewpoint robustness a training target, not an accident of the data |

## Evaluation under change

Zaffar et al. (2021) build VPR-Bench, a framework with a dataset whose viewpoint and illumination changes are quantified, and evaluate ten place recognition techniques on twelve datasets. Their main findings are that all techniques suffer from viewpoint variance, and that lateral change has less effect than three-dimensional change. Directional illumination change also has more adverse effects on matching confidence than uniform illumination change. The benchmark is useful because a single score on a mixed dataset hides which kind of change is causing failure.

## Pretrained representations in robotics

The same question appears in robotic manipulation and navigation. Burns et al. (2023) compare fifteen pretrained vision models under changes of lighting and scene texture. They find that the choice of augmentations outweighs the importance of the supervision signal, and that emergent segmentation ability is the strongest predictor of out-of-distribution success among vision transformers. Silwal et al. (2024) evaluate five pretrained visual representations in simulation and on real robots. Their simulation trends largely match the real-world trends, and a randomly initialised ViT-Base baseline, fine-tuned with the same augmentations, does poorly on real-robot image navigation, at 10% success against 90% for VC-1 Large. These results support using frozen foundation features as the starting point for place recognition on robots, provided their robustness is measured on the target platform.

## Connections

- [Robotics](../index.md) places visual localisation among the robotic tasks in the wiki.
- [Navigation with visual goals](../navigation/index.md) uses the same retrieval idea to find the next waypoint in a graph of images.
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) describes the frozen encoder used by AnyLoc.

## Open questions

- How well descriptors trained on one season transfer to very different conditions over long periods.
- Whether viewpoint robustness from multi-view training can be obtained cheaply on a robot that only records one traversal.

## References

- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision (2021). https://doi.org/10.1007/s11263-021-01469-5 — A benchmark that separates viewpoint and appearance change and quantifies each.
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — Frozen foundation features for place recognition across domains.
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. https://openaccess.thecvf.com/content/ICCV2023/papers/Berton_EigenPlaces_Training_Viewpoint_Robust_Models_for_Visual_Place_Recognition_ICCV_2023_paper.pdf — Trains place recognition on geometry-grouped multiple views of each place for viewpoint robustness.
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — Compares fifteen pretrained models under visual shifts and finds that augmentations matter more than supervision.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — Studies pretrained visual representations across simulation and real robots, with a from-scratch baseline.
