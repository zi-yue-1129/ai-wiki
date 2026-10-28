---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - robotics
  - place recognition
  - foundation model
aliases:
  - AnyLoc
  - 通用視覺地點辨識
---

# AnyLoc

AnyLoc, introduced by Keetha, Mishra, Karhade, Jatavallabhula, Scherer, Krishna and Garg (2023), is a place recognition method built from a frozen foundation model. It takes intermediate DINOv2 features, aggregates them into a single descriptor without training, and retrieves matching places from a database. The paper's claim is that one general descriptor works across the different domains in its evaluation. The parent subtopic is [Visual Localisation](index.md).

## Overview

AnyLoc has no encoder training step. A frozen DINOv2 backbone produces dense local features, and a clustering-based aggregation, a form of vector of locally aggregated descriptors learned without labels, pools them into one vector per image. Retrieval is then a nearest-neighbour search. The method is a choice of features and of aggregation, not a new network.

## Problem

Place recognition methods are usually trained on one domain, such as city streets, and they lose accuracy elsewhere. Training a new encoder for each environment is costly, and the robot may not have the data to do so. The paper asks whether a general foundation model can serve as the single encoder across domains, and which layer and aggregation give the best results.

## Core idea

Use the features of a frozen self-supervised model, taken from an intermediate layer that the authors find works best, and aggregate them without labels. The aggregation step is what turns a rich feature map into a compact descriptor for retrieval.

## How it works

1. Pass the image through a frozen DINOv2 backbone, and keep the features of a chosen intermediate layer.
2. Cluster the local features with a vocabulary learned without labels, and aggregate them into a vector for the image.
3. Normalise the descriptor and store it in a database alongside the place it came from.
4. For a query image, compute its descriptor and retrieve the nearest stored descriptors.

## Results

The authors report that on indoor datasets AnyLoc gives recall at one above task-trained encoders. For example, on one indoor dataset they report recall of 75.2 against 64.4 for MixVPR. They also report that the gains level off at the larger backbone sizes. These figures should be checked in the paper's tables before reuse, since they depend on the evaluation protocol.

## Limitations

- Retrieval does not estimate geometry, so a match still needs verification before a robot relies on it.
- The largest backbone is expensive on embedded hardware, and the paper does not report latency for a robot-sized variant.
- The method is evaluated on retrieval benchmarks, and closed-loop robotic results are outside the paper's scope.

## Connections

- [Visual Localisation](index.md) places AnyLoc next to the trained alternative, EigenPlaces.
- [DINOv2](../../../theory/paradigms/self-supervised/non-contrastive-methods/dinov2.md) describes the frozen backbone that AnyLoc uses.
- [EigenPlaces](eigenplaces.md) represents the approach of training for viewpoint robustness.

## Open questions

- Whether the aggregation can be made cheaper for real-time use on small platforms without losing accuracy.
- How the frozen features handle the viewpoint changes that the benchmark of Zaffar et al. (2021) isolates.

## References

- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — the source of the frozen-feature method and the indoor results.
- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — the frozen backbone used by AnyLoc.
- Berton, G., Trivigno, G., Caputo, B., & Masone, C. (2023). *EigenPlaces: Training Viewpoint Robust Models for Visual Place Recognition*. ICCV 2023. arXiv:2308.10832. https://arxiv.org/abs/2308.10832 — the trained alternative for viewpoint robustness.
- Zaffar, M., Garg, S., Milford, M., et al. (2021). *VPR-Bench: An open-source visual place recognition evaluation framework with quantifiable viewpoint and appearance change*. International Journal of Computer Vision, 129(7), 2136–2174. arXiv:2005.08135. https://arxiv.org/abs/2005.08135 — the benchmark with controlled viewpoint and appearance change.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — evidence that pretrained encoders transfer better to real robots than encoders trained from scratch.
