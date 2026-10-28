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

I3D is a video action recognition model that inflates two-dimensional image filters into three dimensions. Its weights can start from networks pretrained on images, and it is trained on the Kinetics video dataset. It set a strong baseline for action recognition and remains a common reference point.

## Overview

The [video chapter](index.md) describes the task. This page covers the model. The main idea is to take a successful image architecture, add a temporal dimension to each filter, and reuse the pretrained two-dimensional weights by repeating them along time.

## Problem

Three-dimensional convolutional networks learn motion directly but are hard to train from scratch, because video datasets are small compared with image datasets. The question is how to benefit from image pretraining while still modelling motion.

## Core idea

Each two-dimensional $k \times k$ filter is inflated to a three-dimensional $k \times k \times k$ filter by repeating its weights along the temporal axis and rescaling them. The inflated network starts from the behaviour of the image network applied to every frame, and it learns temporal structure during training on video. The authors use a two-stream design in which one stream takes RGB frames and another takes optical flow, and they combine the two.

## Equation

If a two-dimensional filter $W \in \mathbb{R}^{k \times k}$ is inflated to $T$ frames, the three-dimensional filter is

$$W_{\text{3D}}(t, i, j) = \frac{1}{T} W(i, j), \qquad t = 1, \ldots, T,$$

so that a video of identical frames produces the same output as the image network applied to one frame. The division by $T$ keeps the response scale stable.

## Results

The paper reports that pretraining on Kinetics and then fine-tuning on smaller datasets gives strong results on HMDB-51 and UCF-101, with the figures given in the abstract and results tables. Refer to the paper for exact numbers.

## Limitations

- Three-dimensional convolutions are expensive in memory and compute, which limits clip length and resolution.
- Local kernels capture motion over short windows, so long-range dependencies are harder to model than with attention.
- Performance depends heavily on large labelled datasets, and dataset biases can be learned as shortcuts.

[ViViT](vivit.md) replaces the convolutional design with attention over tokens.

## Connections

The inflation idea links to the image-model backbones in [Computer vision](../index.md), and the Inception-style architecture it builds on is described in the cited GoogLeNet paper. Its training uses the batch normalisation discussed in [Normalisation](../../../deep-learning/normalisation/index.md).

## Applications

Action recognition for sports and video analytics, human activity monitoring, and as a feature extractor for video retrieval.

## Open questions

- Do convolutional video models learn motion or appearance shortcuts on current benchmarks?
- How should inflation be done for architectures other than Inception?

## References

### Seminal papers

- Carreira and Zisserman, *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset* (2017). https://arxiv.org/abs/1705.07750 — Introduces I3D and the Kinetics dataset.
- Szegedy et al., *Going deeper with convolutions*, IEEE Conference on Computer Vision and Pattern Recognition (2015). https://doi.org/10.1109/CVPR.2015.7298594 — The Inception architecture whose filters I3D inflates.
- Kay, Carreira, Simonyan, Zhang, Hillier, Vijayanarasimhan, Viola, Green, Back, Natsev, Suleyman and Zisserman, *The Kinetics Human Action Video Dataset* (2017). https://arxiv.org/abs/1705.06950 — The dataset on which I3D is pretrained.
- Simonyan and Zisserman, *Two-Stream Convolutional Networks for Action Recognition in Videos* (2014). https://arxiv.org/abs/1406.2199 — The two-stream design that I3D extends.
- Tran, Bourdev, Fergus, Torresani and Paluri, *Learning Spatiotemporal Features with 3D Convolutional Networks* (2015). https://arxiv.org/abs/1412.0767 — The C3D model, an early three-dimensional convolutional baseline.
