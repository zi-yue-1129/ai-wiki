---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/mlp/layer-normalisation
  - theory/models/transformer
tags:
  - normalisation
  - optimisation
  - training stability
aliases:
  - 正規化層
  - 歸一化
  - 批次正規化
  - Normalisation layers
---

# Normalisation layers

Normalisation layers rescale the activations inside a network, usually by subtracting a mean and dividing by a standard deviation, and then apply a learned scale and shift. They make deep networks easier to train, allow larger learning rates, and are now present in almost every modern architecture. The choice of which dimensions to normalise over is the main design decision.

## Overview

When a network is trained, the distribution of each layer's inputs changes as the earlier layers change. Normalisation keeps those distributions in a stable range. Batch normalisation was introduced to address a particular account of this, and later work has questioned whether that account is the real reason it helps. Other variants normalise over different axes, which matters when batches are small or when sequences have variable length.

## Key concepts

- **Normalisation axis**: the set of dimensions over which the mean and variance are computed. Batch, channel and token axes give different methods.
- **Learned affine parameters**: a scale and shift applied after normalisation, so the layer can recover the original scale if needed.
- **Internal covariate shift**: the proposed reason for the benefit of batch normalisation, namely the changing distribution of layer inputs during training.
- **Pre-norm and post-norm**: whether normalisation is applied before or after the residual branch in a Transformer block.

## How it works

Given activations $x$ over a set $S$ of axes, the layer computes $\hat{x} = (x - \mu_S)/\sqrt{\sigma^2_S + \epsilon}$, then returns $\gamma \hat{x} + \beta$. The methods differ in $S$. Batch normalisation uses the batch and spatial axes, group normalisation uses groups of channels within a sample, and layer normalisation uses all features of one token. Ioffe and Szegedy introduced batch normalisation and reported that it reached the same accuracy in 14 times fewer training steps on an image classification model [(Ioffe and Szegedy, 2015)](https://arxiv.org/abs/1502.03167).

## Key methods

The landmark methods differ in what they normalise over.

- [Batch normalisation](batch-normalisation.md): normalises over the batch, the standard choice for convolutional networks with large batches.
- [Group normalisation](group-normalisation.md): normalises over groups of channels within each sample, independent of batch size.
- [RMSNorm](rms-normalisation.md): drops the mean subtraction and normalises by the root mean square, which is cheaper.
- [Layer normalisation](../../models/mlp/layer-normalisation/index.md) normalises over features of one token and is covered on the MLP page.

## Why it works, and the debate

The internal covariate shift account is contested. Santurkar and colleagues argue that batch normalisation mainly makes the optimisation landscape significantly smoother, rather than reducing the shift of input distributions [(Santurkar et al., 2018)](https://arxiv.org/abs/1805.11604). Treat any single explanation as partial. The effect is well established in practice, and the mechanism is still an open question.

## Pre-norm and post-norm in Transformers

The original Transformer placed layer normalisation after the residual addition, which is called post-norm. Xiong and colleagues analysed the gradients at initialisation and showed that placing normalisation inside the residual branch, called pre-norm, gives well-behaved gradients near the output layer, which makes learning-rate warm-up less critical [(Xiong et al., 2020)](https://arxiv.org/abs/2002.04745). Most current large models use pre-norm or a variant.

## Connections

The mechanics of gradient flow through these layers rely on [Automatic differentiation](../../math/automatic-differentiation/index.md). Initialisation and normalisation work together, covered in [Weight initialisation](../initialisation/index.md). The Transformer context is in [Transformers](../../models/transformer/index.md).

## Applications

Batch normalisation in image classifiers and detectors, group normalisation in small-batch and video models, RMSNorm and layer normalisation in language models, and normalisation in diffusion models.

## Open questions

- Why does normalisation help, and which of the proposed explanations carries most of the effect?
- What is the best normalisation for models trained at very large scale, where batch statistics are unavailable across devices?

## References

### Seminal papers

- Ioffe and Szegedy, *Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift* (2015). https://arxiv.org/abs/1502.03167 — Introduces batch normalisation and reports the 14-times reduction in training steps.
- Ba, Kiros and Hinton, *Layer Normalization* (2016). https://arxiv.org/abs/1607.06450 — Normalises over features within each sample, avoiding the dependence on batch size.
- Wu and He, *Group Normalization*, European Conference on Computer Vision (2018). https://arxiv.org/abs/1803.08494 — Normalises over channel groups, with stable performance at small batch sizes.
- Zhang and Sennrich, *Root Mean Square Layer Normalization* (2019). https://arxiv.org/abs/1910.07467 — A cheaper alternative to layer normalisation that drops the mean subtraction.
- Xiong, Yang, He, Zheng, Zheng, Xing, Zhang, Lan, Wang and Liu, *On Layer Normalization in the Transformer Architecture* (2020). https://arxiv.org/abs/2002.04745 — Analyses pre-norm and post-norm Transformers at initialisation.
- Santurkar, Tsipras, Ilyas and Madry, *How Does Batch Normalization Help Optimization?* (2018). https://arxiv.org/abs/1805.11604 — Argues that the main effect of batch normalisation is a smoother optimisation landscape.
