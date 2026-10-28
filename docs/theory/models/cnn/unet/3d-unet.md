---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - brain-mind/neuroai
tags:
  - convolutional networks
  - segmentation
  - volumetric imaging
aliases:
  - 3D U-Net
  - 三維 U-Net
---

# 3D U-Net

3D U-Net is a version of [U-Net](index.md) that segments volumetric images directly, using 3D operations in place of 2D ones. It is designed to learn from sparse annotation: a user labels a few slices, and the network produces a dense 3D segmentation. Çiçek et al. (2016) introduced it for biomedical volumes.

## Overview

The parent [U-Net](index.md) segments 2D images with an encoder that downsamples, a decoder that upsamples, and skip connections between them. 3D U-Net keeps that design and changes every 2D operation to its 3D counterpart, so the filters move through depth as well as width and height.

## Problem

Dense 3D labels are costly to make: a clinician would have to annotate every voxel of every volume. Many practical tasks only have a few annotated slices, and a 2D network applied slice by slice ignores the structure between slices. The question is whether a 3D network can learn a full segmentation from sparse labels.

## Core idea

Replace all 2D operations of U-Net with 3D ones, train end to end from scratch, and make the training data rich with on-the-fly elastic deformations. The network then learns from sparsely annotated volumes and generalises to new volumes.

## Algorithm

The network follows the U-Net encoder–decoder with skip connections. Convolutions, pooling and up-sampling operate over three spatial dimensions. Training uses on-the-fly elastic deformation of the input volumes as augmentation, and no pre-trained network is used. The paper evaluates two setups:

1. **Semi-automated**: the user annotates some slices of the volume to be segmented, and the network completes the segmentation.
2. **Fully automated**: a representative, sparsely annotated training set is assumed to exist, and the trained network segments new volumes without user input.

## Key results

The paper evaluates on Xenopus kidney volumes and reports intersection over union (IoU). The numbers below come from its Tables 1 and 3.

- **Semi-automated** (3-fold cross-validation): average IoU is 0.863 with batch normalisation and 0.842 without it. The 2D variant reaches 0.796.
- **Fully automated**: average IoU is 0.704 with batch normalisation and 0.723 without it. The text says batch normalisation helps, but these averages point the other way. It helps on two volumes and hurts on the third (0.554 with it, 0.779 without it, as the paper reports it).

The paper reports IoU only. It gives no Dice score or accuracy figure for these experiments.

## Limitations

- Results are reported on one kind of volume, the Xenopus kidney, so the generality of the method is not shown.
- 3D convolutions cost more memory and compute than their 2D counterparts, which limits the volume size that can be processed.
- The fully-automated batch-normalisation result contradicts the paper's own text, so the averages should be read from the table rather than the summary.

## Connections

- [U-Net](index.md) is the 2D design that 3D U-Net extends.
- [Segmentation metrics](../../../evaluation/metrics/segmentation/index.md) explain IoU and Dice, the overlap measures used to judge volumetric segmentation.
- [Convolution variants](../convolution-variants/index.md) covers the 3D and dilated operations that volumetric networks depend on.
- [Fully convolutional networks (Long et al., 2014)](https://arxiv.org/abs/1411.4038) are the earlier fully convolutional segmentation design that U-Net builds on.

## Applications

- Biomedical volumetric segmentation from sparse annotation, the setting of the paper's Xenopus kidney experiments.
- Semi-automated annotation, where a user labels a few slices and the network completes the rest of the volume.

## Open questions

- How many annotated slices are needed before the semi-automated setting is reliable, and which slices should be chosen?
- Does the method transfer to other organs and imaging modalities without retraining from scratch?

## References

### Seminal papers

- Çiçek, Ö., Abdulkadir, A., Lienkamp, S. S., Brox, T. & Ronneberger, O. (2016). *3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation*. arXiv. https://arxiv.org/abs/1606.06650 — Introduces 3D U-Net and reports IoU on Xenopus kidney volumes in semi-automated and fully-automated settings. Checked: arXiv metadata and the paper's Tables 1 and 3.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — The 2D encoder–decoder with skip connections that 3D U-Net extends. Checked: arXiv metadata.
- Milletari, F., Navab, N. & Ahmadi, S.-A. (2016). *V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation*. arXiv. https://arxiv.org/abs/1606.04797 — A contemporaneous fully convolutional network for 3D medical segmentation. Checked: arXiv metadata.
- Long, J., Shelhamer, E. & Darrell, T. (2014). *Fully Convolutional Networks for Semantic Segmentation*. arXiv. https://arxiv.org/abs/1411.4038 — The fully convolutional design for dense prediction. Checked: arXiv metadata.
- Sudre, C. H., et al. (2017). *Generalised Dice overlap as a deep learning loss function for highly unbalanced segmentations*. arXiv. https://arxiv.org/abs/1707.03237 — Overlap-based loss for highly unbalanced segmentation, relevant to sparse volumetric labels. Checked: arXiv metadata.
