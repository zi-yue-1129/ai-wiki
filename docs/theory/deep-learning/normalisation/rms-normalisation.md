---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/normalisation
  - theory/models/transformer
tags:
  - RMSNorm
  - normalisation
  - language models
aliases:
  - 均方根正規化
  - RMSNorm
  - Root mean square layer normalization
---

# RMSNorm

RMSNorm normalises a feature vector by its root mean square, without subtracting the mean. It is a simpler and cheaper form of layer normalisation, and it is now common in large language models.

## Overview

The [chapter](index.md) covers the normalisation family. This page covers RMSNorm, which keeps the rescaling step of layer normalisation and drops the re-centring step. The idea is to test whether the mean subtraction is needed for the benefit that layer normalisation provides.

## Problem

Layer normalisation computes a mean and a variance for every token. In large models this costs time, and the mean subtraction adds an operation that must be carried through training and inference. The question is whether a cheaper normalisation keeps the same performance.

## Core idea

For a vector $\mathbf{x} \in \mathbb{R}^d$, compute the root mean square of its entries and divide by it. Then apply a learned per-feature gain. There is no mean subtraction and no learned bias. Zhang and Sennrich report that the method gives performance comparable to layer normalisation while reducing running time [(Zhang and Sennrich, 2019)](https://arxiv.org/abs/1910.07467).

## Equation

$$\mathrm{RMS}(\mathbf{x}) = \sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2 + \epsilon}, \qquad \mathrm{RMSNorm}(\mathbf{x}) = \frac{\mathbf{x}}{\mathrm{RMS}(\mathbf{x})} \odot \mathbf{g}$$

Here $\mathbf{g}$ is a learned gain vector and $\epsilon$ is a small constant for stability. Layer normalisation would instead subtract the mean of $\mathbf{x}$ before dividing by its standard deviation.

## Results

The abstract reports that RMSNorm achieves comparable performance to layer normalisation, and that it reduces running time by between 7% and 64% depending on the model. The detailed comparisons are in the paper.

## Limitations

- The benefit is mainly speed. Where layer normalisation is already cheap relative to the rest of the model, the gain is small.
- The claim of comparable performance rests on the tasks the paper tests. Other tasks may behave differently.
- Like layer normalisation, it sits inside a residual block, so its placement still matters. The pre-norm and post-norm discussion is in the [chapter](index.md).

## Connections

RMSNorm is a direct simplification of [layer normalisation](../../models/mlp/layer-normalisation/index.md). Its use in the Transformer block is covered on the [Transformer](../../models/transformer/index.md) page, and the placement question is analysed by Xiong and colleagues [(Xiong et al., 2020)](https://arxiv.org/abs/2002.04745).

## Applications

Normalisation inside large language models, where its lower cost matters at scale.

## Open questions

- Is the mean subtraction ever important for particular architectures or data?
- Does RMSNorm change the training dynamics at very large scale in ways the original experiments did not test?

## References

### Seminal papers

- Zhang and Sennrich, *Root Mean Square Layer Normalization* (2019). https://arxiv.org/abs/1910.07467 — Introduces RMSNorm and reports its speed and performance.
- Ba, Kiros and Hinton, *Layer Normalization* (2016). https://arxiv.org/abs/1607.06450 — Layer normalisation, the normalisation that RMSNorm simplifies by dropping the mean subtraction.
- Ioffe and Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift* (2015). https://arxiv.org/abs/1502.03167 — The batch-based method that motivated the family.
- Xiong, Yang, He, Zheng, Zheng, Xing, Zhang, Lan, Wang and Liu, *On Layer Normalization in the Transformer Architecture* (2020). https://arxiv.org/abs/2002.04745 — Analyses where normalisation is placed in Transformer blocks.
- Vaswani et al., *Attention Is All You Need* (2017). https://arxiv.org/abs/1706.03762 — The Transformer architecture in which these normalisations are used.
