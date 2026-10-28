---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/video
tags:
  - I3D
  - action recognition
  - 3D convolution
aliases:
  - 膨脹三維卷積
  - I3D
  - Inflated 3D ConvNet
---

# I3D: inflated 3D convolutional networks

I3D is a video action recognition model that inflates two-dimensional image filters into three dimensions. Its three-dimensional filters are initialised from the two-dimensional ones, and it is trained on the Kinetics video dataset. The abstract reports 80.9% accuracy on HMDB-51 and 98.0% on UCF-101 after Kinetics pretraining.

## Overview

The [video chapter](index.md) describes the task. This page covers the model: an image network's filters are inflated along time, and the pretrained weights are reused.

## Problem

Three-dimensional convolutional networks can learn motion directly, but training them from scratch on video is hard. The question is how to reuse image pretraining while still modelling motion.

## Core idea

Each two-dimensional filter is inflated along the temporal axis. Its weights are repeated across time and divided by the temporal size, which gives a three-dimensional filter. The paper notes that for a boring video of identical frames, the inflated network gives the same response as the image network applied to a single frame. The paper calls this a fixed point for boring video.

## Equation

For an $N \times N$ filter $W$, the paper repeats it $N$ times along time and divides by $N$, giving an $N \times N \times N$ filter:

$$W_{\text{3D}}(t, i, j) = \frac{1}{N} W(i, j), \qquad t = 1, \ldots, N$$

Summing over the $N$ temporal copies of a constant input recovers $W$, which is the fixed-point property above.

## Results

The abstract reports 80.9% on HMDB-51 and 98.0% on UCF-101 after pretraining on Kinetics. The paper's tables give the full comparisons.

## Limitations

- The reported accuracies follow Kinetics pretraining, and the abstract does not report results without it.
- The inflation rule is stated for filters of this form. Other architectures need their own derivation.

## Connections

The image network that is inflated is a convolutional backbone covered in [Computer vision](../index.md). For an attention-only video model, see [ViViT](vivit.md).

## Applications

Action recognition on video benchmarks such as HMDB-51 and UCF-101, as reported in the paper.

## Open questions

- How does the inflation rule apply to architectures other than the one the paper uses?
- How much of the accuracy comes from Kinetics pretraining, and how much from the inflated architecture?

## References

### Seminal papers

- Carreira and Zisserman, *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset* (2017). https://arxiv.org/abs/1705.07750 — Introduces I3D and the Kinetics dataset.
- Szegedy et al., *Going deeper with convolutions*, IEEE Conference on Computer Vision and Pattern Recognition (2015). https://doi.org/10.1109/CVPR.2015.7298594 — The Inception architecture, the image network whose filters I3D inflates.
- Kay, Carreira, Simonyan, Zhang, Hillier, Vijayanarasimhan, Viola, Green, Back, Natsev, Suleyman and Zisserman, *The Kinetics Human Action Video Dataset* (2017). https://arxiv.org/abs/1705.06950 — Introduces the Kinetics dataset on which I3D is pretrained.
- Simonyan and Zisserman, *Two-Stream Convolutional Networks for Action Recognition in Videos* (2014). https://arxiv.org/abs/1406.2199 — Introduces a two-stream convolutional design for action recognition in video.
- Tran, Bourdev, Fergus, Torresani and Paluri, *Learning Spatiotemporal Features with 3D Convolutional Networks* (2015). https://arxiv.org/abs/1412.0767 — Introduces C3D, an early three-dimensional convolutional model for video.
