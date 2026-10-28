---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/computer-vision/video
  - theory/models/transformer
tags:
  - ViViT
  - video Transformer
  - attention
aliases:
  - 影片視覺 Transformer
  - ViViT
  - Video Vision Transformer
---

# ViViT: video vision Transformer

ViViT is a video classification model built only from Transformer layers. It turns a clip into spatiotemporal tokens and applies self-attention over them, with several ways to factorise the attention across space and time. It is the video counterpart of the Vision Transformer and shows that convolution is not required for video classification.

## Overview

The [video chapter](index.md) gives the wider context. This page covers the model. A Transformer for images splits a picture into patches and treats each patch as a token. ViViT does the same for video, using tubelets that span a few frames as tokens, and then attends over all of them.

## Problem

Full attention over every spatiotemporal token is expensive, because the number of tokens grows with the product of the spatial and temporal size. The question is how to keep the expressiveness of attention while reducing the cost, and how to train such a model when labelled video is scarce.

## Core idea

A clip is cut into non-overlapping spatiotemporal tubelets, each embedded as a token. The authors propose several factorised encoders that split the attention. One variant applies spatial attention within each frame and then temporal attention across frames at each position. Another applies spatial and temporal transformers in sequence. The factorised versions cut the cost, and the paper's experiments compare the variants.

## Equation

For a video with $T$ frames and $N$ spatial tokens per frame, full self-attention costs on the order of $(TN)^2$ operations. A factorised encoder with spatial attention followed by temporal attention costs on the order of $T N^2 + N T^2$, which is much smaller when $T$ and $N$ are both large. The attention itself is the standard scaled dot-product form from the Transformer paper. The cost expressions above are this page's own estimate, not figures quoted from the paper.

## Results

The abstract reports state-of-the-art results on several video classification benchmarks, including Kinetics 400 and 600, Epic Kitchens, Something-Something v2 and Moments in Time. The figures are in the paper's results tables and are not restated here.

## Limitations

- The attention cost still grows quickly with clip length and resolution.
- Performance depends on pretraining, and models trained only on small video datasets can underperform convolutional baselines.
- Like other video classifiers, ViViT can learn appearance shortcuts in benchmark clips.

Masked pretraining methods such as [VideoMAE](index.md) address the data problem.

## Connections

ViViT is a direct use of the Transformer architecture described in [Transformers](../../transformer/index.md), and it extends the Vision Transformer approach to time. Its attention is one of the factorised forms discussed in the same chapter as [I3D](i3d.md).

## Applications

Action recognition, video retrieval and video representation learning for downstream tasks such as captioning.

## Open questions

- Which factorisation of space and time is best as clips get longer?
- How much of the advantage of video Transformers comes from pretraining, not from the architecture itself?

## References

### Seminal papers

- Arnab, Dehghani, Heigold, Sun, Lučić and Schmid, *ViViT: A Video Vision Transformer* (2021). https://arxiv.org/abs/2103.15691 — The ViViT model and its factorised encoders.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — The Transformer architecture that ViViT applies to video.
- Dosovitskiy et al., *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale* (2020). https://arxiv.org/abs/2010.11929 — The Vision Transformer that ViViT extends to video.
- Bertasius, Wang and Torresani, *Is Space-Time Attention All You Need for Video Understanding?* (2021). https://arxiv.org/abs/2102.05095 — A convolution-free space-time attention model for video, which compares factorised attention designs.
- Tong, Song, Wang and Wang, *VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training* (2022). https://arxiv.org/abs/2203.12602 — Masked pretraining that reduces the labelled data needed by video Transformers.
