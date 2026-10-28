---
status: complete
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

DINOv2 is a self-supervised vision transformer whose frozen features work across many image tasks without fine-tuning the backbone. Oquab et al. (2023) combine an image-level self-distillation objective, from DINO, with a patch-level masked objective, from iBOT, and train on a curated collection of about 142 million images.

## Overview

A frozen DINOv2 backbone produces one feature for the whole image and one for each patch. Downstream systems can use these features with a light head, instead of training a separate backbone for each task. The paper's main claim is that features from a self-supervised model trained at scale on curated data are competitive with the best openly available weakly supervised models. It also reports that these features surpass OpenCLIP on most benchmarks. The parent subtopic is [Non-Contrastive Methods](index.md).

## Problem

Supervised pretraining needs labels that are expensive to collect, and it biases the features toward the chosen classes. Earlier self-supervised methods were usually trained on smaller data, and their features were less reliable across tasks. The paper asks whether self-supervised learning can produce general visual features at the scale of weakly supervised models.

## Key concepts

- **Image-level objective**: a cross-entropy between the student's and the teacher's class-token features, computed on different crops of the same image. This is the DINO objective.
- **Patch-level objective**: the student sees some patches masked, and a loss on the masked tokens matches the teacher's patch features. This is the iBOT objective.
- **Centering**: the teacher's outputs are centred, a technique the paper takes from SwAV.
- **KoLeo regulariser**: encourages the features within a batch to spread out evenly.
- **Curated data**: images retrieved from an uncurated pool so that they resemble a set of curated reference datasets.

## How it works

1. **Curate the data.** Start from an uncurated pool of about 1.2 billion images, remove near-duplicates, and retrieve images close to those in curated reference datasets, such as ImageNet-22k, ImageNet-1k and Google Landmarks. Retrieval uses embeddings from a self-supervised ViT-H/16 trained on ImageNet-22k, cosine similarity and k-means clustering. The result is LVD-142M, with 142 million images.
2. **Train the backbone.** Train a vision transformer with the image-level and patch-level objectives, together with the KoLeo regulariser.
3. **Freeze it.** Keep the backbone fixed after pretraining.
4. **Use the features.** Feed the image and patch features to a downstream head, for classification, segmentation, depth estimation or retrieval.

## Key methods

### DINOv2: Learning Robust Visual Features without Supervision (Oquab et al., 2023)

- **Problem:** self-supervised features have been less reliable than weakly supervised ones across tasks, and it was unclear whether scale alone would close the gap.
- **Core idea:** combine DINO's image-level self-distillation with iBOT's masked patch objective, and train on a large curated dataset chosen by retrieval.
- **Equation or algorithm:** the two losses and the KoLeo regulariser are described in the paper's method section. The page describes them in words, not as a single equation.
- **Results:** for the largest model (ViT-g/14, frozen), the paper reports 86.5% linear-probe top-1 on ImageNet-1k, 49.0 mIoU on ADE20k with a linear head (53.0 with multi-scale testing), and an RMSE of 0.279 on NYUd depth with a DPT head (lower is better). The paper also reports mAP 52.3 on Oxford-Hard retrieval.
- **Limitations:** the largest model is a one-billion-parameter ViT, which is costly to run on embedded hardware. The curation step depends on the reference datasets chosen, so the exact data mixture is hard to reproduce without the same retrieval pipeline. Frozen features do not adapt to a new domain, so their robustness to shifts has to be measured for each application.

## Connections

- [Masked prediction](../masked-prediction/index.md): the patch-level objective is a masked prediction idea, applied to image patches.
- [Vision transformer](../../../models/transformer/index.md): the backbone architecture.
- [Robotics](../../../../applications/robotics/index.md): frozen visual features are used as encoders for embodied tasks.

## Applications

- **Image classification, segmentation and depth estimation** with frozen features, as in the paper's evaluations.
- **Image retrieval**, where the paper reports results on instance-level benchmarks.

## Open questions

- Whether a principled selection rule can replace hand-chosen reference datasets when a new domain has little data.
- How frozen features behave under large changes in lighting and viewpoint, which matter in outdoor robotics.

## References

### Seminal papers

- Oquab, M. et al. (2023). DINOv2: Learning Robust Visual Features without Supervision. *Transactions on Machine Learning Research*. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — The paper, with the two objectives, the curated data and the frozen-feature results.
- Caron, M. et al. (2021). Emerging Properties in Self-Supervised Vision Transformers. arXiv:2104.14294. https://arxiv.org/abs/2104.14294 — DINO, the image-level self-distillation objective that DINOv2 keeps.
- Zhou, J. et al. (2022). iBOT: Image BERT Pre-training with Online Tokenizer. arXiv:2111.07832. https://arxiv.org/abs/2111.07832 — The masked patch-level objective that DINOv2 combines with DINO.
- Dosovitskiy, A. et al. (2020). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. arXiv:2010.11929. https://arxiv.org/abs/2010.11929 — The vision transformer architecture used as the backbone.
- Chen, T. et al. (2020). A Simple Framework for Contrastive Learning of Visual Representations. arXiv:2002.05709. https://arxiv.org/abs/2002.05709 — SimCLR, the contrastive alternative to self-distillation.
