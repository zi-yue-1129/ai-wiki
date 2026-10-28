---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/world-models
  - theory/models/transformer
tags:
  - video
  - action recognition
  - video generation
aliases:
  - 影片理解
  - 影片生成
  - 動作辨識
  - Video understanding
---

# Video understanding and generation

Video adds time to images. A model that understands video must recognise motion and events across frames, and a model that generates video must keep objects consistent from one frame to the next. This chapter covers action recognition, video Transformers, and video diffusion, which generates clips from noise in the same way image diffusion models do.

## Overview

A video is a sequence of frames, so most of the difficulty lies in how the model treats the temporal axis. Early methods extended image networks in time. Later methods use attention over space and time, or train on masked video. Generation adds another requirement: the output must be plausible over many frames, not only sharp in each.

## Key concepts

- **Action recognition**: classifying the action in a video clip, such as running or cooking.
- **Two-stream network**: a model with one stream for appearance from single frames and one for motion from optical flow.
- **Spatiotemporal convolution**: a convolution with a temporal kernel as well as spatial ones.
- **Video Transformer**: a Transformer applied to tokens from video patches over space and time.
- **Video diffusion**: a diffusion model that denoises a sequence of frames, often conditioned on text.

## How it works

Simonyan and Zisserman used two streams, one on still frames and one on stacked optical flow, and showed that the combination classifies actions well [(Simonyan and Zisserman, 2014)](https://arxiv.org/abs/1406.2199). Tran and colleagues used three-dimensional convolutions to learn spatiotemporal features directly from clips [(Tran et al., 2015)](https://arxiv.org/abs/1412.0767). Carreira and Zisserman inflated two-dimensional filters into three dimensions to reuse pretrained image weights, which became [I3D](i3d.md).

Transformers changed the design. Arnab and colleagues built [ViViT](vivit.md), a pure Transformer for video classification [(Arnab et al., 2021)](https://arxiv.org/abs/2103.15691). Masked video pretraining, as in VideoMAE, reduces the amount of labelled data needed [(Tong et al., 2022)](https://arxiv.org/abs/2203.12602).

For generation, Ho and colleagues extended diffusion models to video, showing that the same denoising objective can produce coherent short clips [(Ho et al., 2022)](https://arxiv.org/abs/2204.03458). [Video diffusion](video-diffusion.md) is the method page for this family.

## Key methods

- [I3D](i3d.md): inflated convolutional networks for action recognition, trained on a large labelled dataset.
- [ViViT](vivit.md): a Transformer over spatiotemporal tokens, with several factorisations of attention.
- [Video diffusion](video-diffusion.md): a cascade or latent diffusion model that generates frames conditioned on text.

## Connections

Video generation with consistent dynamics is closely tied to [world models](../../world-models/index.md), which predict how an environment changes. The Transformer ideas are in [Transformers](../../transformer/index.md). The overall task map for vision is in [Computer vision](../index.md).

## Applications

Action recognition supports sports analysis, surveillance review and video search. Video understanding supports content moderation and accessibility captions. Video generation supports film pre-visualisation, advertising and synthetic training data, and it raises the questions about synthetic media covered in [Misinformation and deepfakes](../../../../society/misinformation/index.md).

## Open questions

- How long can generated videos stay consistent before objects drift or physics breaks?
- Does video pretraining learn the dynamics of the world, or mainly the statistics of video frames?
- How should action recognition be evaluated, when many benchmark clips can be solved from a single frame?

## References

### Seminal papers

- Simonyan and Zisserman, *Two-Stream Convolutional Networks for Action Recognition in Videos* (2014). https://arxiv.org/abs/1406.2199 — Two streams for appearance and optical flow.
- Tran, Bourdev, Fergus, Torresani and Paluri, *Learning Spatiotemporal Features with 3D Convolutional Networks* (2015). https://arxiv.org/abs/1412.0767 — Three-dimensional convolutions that learn spatiotemporal features directly from video clips.
- Carreira and Zisserman, *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset* (2017). https://arxiv.org/abs/1705.07750 — The I3D model and the Kinetics dataset.
- Arnab, Dehghani, Heigold, Sun, Lučić and Schmid, *ViViT: A Video Vision Transformer* (2021). https://arxiv.org/abs/2103.15691 — A pure Transformer for video classification.
- Ho, Salimans, Gritsenko, Chan, Norouzi and Fleet, *Video Diffusion Models* (2022). https://arxiv.org/abs/2204.03458 — Extends diffusion models to video, denoising a sequence of frames jointly.

### Articles and documentation

- Tong, Song, Wang and Wang, *VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training* (2022). https://arxiv.org/abs/2203.12602 — Masked pretraining that reduces the labelled data video Transformers need.
