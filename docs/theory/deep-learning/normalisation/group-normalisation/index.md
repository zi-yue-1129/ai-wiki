---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/models/computer-vision
tags:
  - normalisation
  - computer vision
  - deep learning
aliases:
  - Group Normalization
  - GroupNorm
  - 群組正規化
---

# Group Normalisation

Group normalisation (GN) divides the channels of a convolutional layer into groups and normalises each group separately, for each example. Its statistics come from one example, so its behaviour does not change with the batch size. Wu and He introduced it in 2018 as a batch-independent alternative to batch normalisation. It is one of the methods described on the parent [normalisation layers](../index.md) page.

## Overview

Batch normalisation works well when batches are large, but computer vision tasks such as object detection, segmentation and video often need small batches, because high-resolution inputs fill GPU memory. Wu and He observed that batch normalisation's error rises quickly as the batch becomes smaller, since the mean and variance estimated from a few examples are inaccurate. Group normalisation avoids this by computing its statistics within one example, over groups of channels and all spatial positions.

The method sits between two existing choices. It reduces to layer normalisation when all channels form one group, and to instance normalisation when each channel is its own group. Layer normalisation is discussed on the [MLP](../../../models/mlp/layer-normalisation/index.md) page.

## Key concepts

- **Channel groups.** The \(C\) channels of a layer are split into \(G\) groups of \(C/G\) channels each. The group count \(G\) is a hyper-parameter; the paper uses \(G = 32\) by default.
- **Per-example statistics.** Each example is normalised on its own, so the output for an input does not depend on the other examples in its batch.
- **Special cases.** With \(G = 1\), the method is layer normalisation over the channels and spatial positions. With \(G = C\), it is instance normalisation, which uses only the spatial positions of each channel.
- **Learned scale and shift.** As in batch normalisation, each channel keeps its own \(\gamma\) and \(\beta\).

## How it works

Take an input of shape \((N, C, H, W)\). For sample \(n\) and group \(g\), the normalisation set \(S\) contains the \(C/G\) channels of group \(g\) at every spatial position \((h, w)\). The mean and variance are computed over that set:

\[
\mu_{n,g} = \frac{1}{|S|}\sum_{(c,h,w)\in S} x_{nchw}, \qquad
\sigma^2_{n,g} = \frac{1}{|S|}\sum_{(c,h,w)\in S} (x_{nchw} - \mu_{n,g})^2,
\]

\[
\hat{x}_{nchw} = \frac{x_{nchw} - \mu_{n,g}}{\sqrt{\sigma^2_{n,g} + \epsilon}}, \qquad
y_{nchw} = \gamma_c\,\hat{x}_{nchw} + \beta_c,
\]

where \(g\) is the group that contains channel \(c\). The algorithm for one layer is:

1. Split the channels into \(G\) groups.
2. For each example and group, compute the mean and variance over the group's channels and all spatial positions.
3. Normalise each value with its group's statistics.
4. Apply the per-channel scale \(\gamma_c\) and shift \(\beta_c\).

There are no running statistics, so training and inference use the same computation.

## Results

According to the abstract of Wu and He (2018), on ResNet-50 trained on ImageNet with a batch size of 2, group normalisation had 10.6% lower error than its batch normalisation counterpart. With typical batch sizes, the paper reports that group normalisation is comparably good with batch normalisation and better than other normalisation variants. The abstract also reports that group normalisation outperformed batch-normalised counterparts for object detection and segmentation on COCO, and for video classification on Kinetics. These results are as reported in the paper and were not re-run for this page.

## Limitations

- **No gain at typical batch sizes.** The paper's main advantage is at small batches. With standard batch sizes, group normalisation is comparable to batch normalisation rather than clearly better.
- **Extra hyper-parameter.** The number of groups must be chosen. The paper uses \(G = 32\) as its default. The method itself gives no rule for choosing \(G\) in a new architecture.
- **Convolutional focus.** The method was developed and tested for convolutional networks. For Transformers, layer normalisation over the features of a token is the usual choice; see the [layer normalisation](../../../models/mlp/layer-normalisation/index.md) page.

## Open questions

- **Choosing the group count.** How \(G\) should be set for a new architecture, and how sensitive results are to it, depends on the task and is not settled by a general rule.
- **Batch-free training.** Whether independence from the batch brings practical advantages in settings with small or uneven batches, such as federated learning, has not been tested in the original paper.
- **Relation to layer normalisation.** The group structure lets each group have its own statistics, which the paper argues gives more representational flexibility than layer normalisation. How much of that gain holds across architectures remains open.

## References

### Seminal papers

- Wu, Y. & He, K. (2018). "Group Normalization". arXiv:1803.08494 — Introduces group normalisation and compares it with batch, layer and instance normalisation across batch sizes.
- Ioffe, S. & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift". arXiv:1502.03167 — Introduces batch normalisation, the method that group normalisation is designed to replace at small batch sizes.
- Ulyanov, D., Vedaldi, A. & Lempitsky, V. (2016). "Instance Normalization: The Missing Ingredient for Fast Stylization". arXiv:1607.08022 — Introduces instance normalisation, the case of group normalisation with one channel per group.
- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". arXiv:1607.06450 — Introduces layer normalisation, the case of group normalisation with a single group.

### Surveys and textbooks

- Huang, L., et al. (2020). "Normalization Techniques in Training DNNs: Methodology, Analysis and Application". arXiv:2009.12836 — A survey that compares batch, layer, instance and group normalisation in one taxonomy.

