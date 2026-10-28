---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/robotics/visual-localisation
tags:
  - self-supervised learning
  - vision transformer
  - visual representation
aliases:
  - DINOv2
  - 自監督視覺特徵
---

# DINOv2

DINOv2, introduced by Oquab et al. (2023), is a self-supervised vision transformer whose frozen features are useful across many tasks without fine-tuning. It extends the DINO family of self-distillation methods with patch-level objectives and trains on a curated image collection. The parent subtopic is [Non-Contrastive Methods](index.md), and the earlier method it builds on is [DINO](index.md).

## Overview

A frozen DINOv2 backbone produces a feature for each image and for each patch. Downstream systems can use these features directly, with a light head or a retrieval step, instead of training the backbone for each task. The paper's main claim is that a self-supervised model trained at scale on curated data gives features that match or exceed those from weakly supervised pretraining across a range of benchmarks.

## Problem

Supervised pretraining needs labels that are expensive to collect and that bias the features toward the chosen classes. Earlier self-supervised methods reached useful features but usually on smaller data, and their features were less reliable across tasks. The paper asks whether self-supervised learning can produce general visual features at a scale comparable to weakly supervised models.

## Core idea

Combine two self-supervised objectives. An image-level objective uses self-distillation between a teacher and a student on different views of the same image. A patch-level objective predicts masked patches from the rest of the image, so that local features are also trained. The data is curated to reduce duplicates and to balance concepts, which the authors identify as important for feature quality.

## How it works

1. Build a large, curated image collection, using a retrieval step to find images similar to a set of seed datasets.
2. Train a vision transformer with an image-level self-distillation loss on global crops.
3. Add a patch-level loss on masked patches, so that dense features are learned as well as global ones.
4. Freeze the trained backbone and use its image and patch features for downstream tasks, such as classification, segmentation and retrieval.

## Results

The paper reports that frozen DINOv2 features perform strongly on image classification, segmentation and depth estimation, often without task-specific training of the backbone. Studies in robotics and place recognition use the frozen features as a drop-in encoder. For example, the AnyLoc work reports that frozen DINOv2 features outperform task-trained place-recognition encoders on indoor datasets. The benchmark numbers should be taken from the paper's tables.

## Limitations

- The largest backbones are expensive to run on embedded hardware, so smaller variants or distilled versions are often used on robots.
- Frozen features do not adapt to a domain, and their robustness to lighting and viewpoint must be measured for each application.
- The curation step that gives the best features depends on the reference datasets chosen, which limits the reproducibility of the exact data mixture.

## Connections

- [Non-Contrastive Methods](index.md) places DINOv2 among the self-distillation methods.
- [Visual localisation](../../../../applications/robotics/visual-localisation/index.md) shows DINOv2 features in a robotic setting.
- [Masked prediction](../../self-supervised/masked-prediction/index.md) describes the patch-level objective's family.

## Open questions

- Whether curated data can be replaced by a principled selection rule that works for new domains with little data.
- How the frozen features behave under the strong photometric changes that matter in outdoor robotics.

## References

- Oquab, M., Darcet, T., Moutakanni, T., et al. (2023). *DINOv2: Learning Robust Visual Features without Supervision*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — the source of the self-supervised objectives, the curated data and the frozen-feature results.
- Caron, M., Touvron, H., Misra, I., et al. (2021). *Emerging Properties in Self-Supervised Vision Transformers*. ICCV 2021. arXiv:2104.14294. https://arxiv.org/abs/2104.14294 — the DINO self-distillation method that DINOv2 extends.
- Keetha, N., Mishra, A., Karhade, J., et al. (2023). *AnyLoc: Towards Universal Visual Place Recognition*. arXiv:2308.00688. https://arxiv.org/abs/2308.00688 — uses frozen DINOv2 features for place recognition.
- Burns, K., Witzel, Z., Hamid, J. I., et al. (2023). *What makes pre-trained visual representations successful for robust manipulation?* arXiv:2312.12444. https://arxiv.org/abs/2312.12444 — compares pretrained visual representations under visual shifts, including DINO-style models.
- Silwal, S., Yadav, K., Wu, T., et al. (2024). *What do we learn from a large-scale study of pre-trained visual representations in sim and real environments?* ICRA 2024. arXiv:2310.02219. https://arxiv.org/abs/2310.02219 — a sim-to-real study of pretrained encoders for navigation.
