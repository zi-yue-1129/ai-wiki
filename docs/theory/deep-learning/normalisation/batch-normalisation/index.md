---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/models/computer-vision
tags:
  - normalisation
  - optimization
  - convolutional networks
aliases:
  - Batch Normalization
  - BatchNorm
  - BN
  - 批次正規化
---

# Batch Normalisation

Batch normalisation (BN) normalises each channel of a layer's activations using the mean and variance of the current mini-batch, then applies a learned scale and shift. Ioffe and Szegedy introduced it in 2015 to speed up training of deep convolutional networks. It is one of the methods described on the parent [normalisation layers](../index.md) page.

## Overview

Ioffe and Szegedy proposed batch normalisation as a way to train deep image classifiers faster and with less care over initialisation and learning rate. Among the normalisation methods, it is the one most tied to the batch, and the one the others were designed to replace in some settings. They argued that it allows much higher learning rates, and that it can reduce the need for dropout. The method became a standard part of convolutional backbones, and it is still common in image models, although newer architectures often use other normalisers.

Its popularity was not matched by an agreed explanation. The original account, that it reduces internal covariate shift, was later challenged, and the reasons it works are still debated (see the parent [normalisation layers](../index.md) page and the open questions below).

## Key concepts

- **Mini-batch statistics.** The mean and variance computed over the examples in one training step. For a convolutional layer, each channel's statistics are taken over the batch and over all spatial positions.
- **Running statistics.** Exponential moving averages of the mini-batch statistics. At inference, the layer uses these fixed values, so a single input does not depend on other inputs.
- **Scale and shift.** Learned parameters \(\gamma\) and \(\beta\) for each channel. They let the layer undo the normalisation if the network needs to.
- **Internal covariate shift.** The change in the distribution of each layer's inputs as earlier layers are updated. It was the motivation given in the original paper.

## How it works

For one channel of a layer, with a mini-batch of \(m\) values \(x_1, \dots, x_m\):

\[
\mu_B = \frac{1}{m}\sum_{i=1}^{m} x_i, \qquad
\sigma_B^2 = \frac{1}{m}\sum_{i=1}^{m} (x_i - \mu_B)^2,
\]

\[
\hat{x}_i = \frac{x_i - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}, \qquad
y_i = \gamma\,\hat{x}_i + \beta.
\]

The procedure for a training step is:

1. For each channel, compute the mean and variance over the mini-batch and the spatial positions.
2. Normalise each value with those statistics.
3. Scale and shift with the learned \(\gamma\) and \(\beta\).
4. Update the running mean and variance used at inference.

Because \(\mu_B\) and \(\sigma_B^2\) depend on the whole batch, the gradient of the loss flows through them as well as through each value. In the original paper, the layer was placed immediately before the nonlinearity.

## Results

According to the abstract of Ioffe and Szegedy (2015), applying batch normalisation to a state-of-the-art image classification model reached the same accuracy with 14 times fewer training steps, and it beat the original model by a significant margin. An ensemble of batch-normalised networks reached 4.9% top-5 validation error on ImageNet classification, which the authors reported as exceeding human raters. These figures are from the paper and were not re-run for this page.

## Limitations

- **Batch dependence.** The statistics are only as good as the batch. Wu and He (2018) show that BN's error rises quickly as the batch size shrinks, because batch statistics become inaccurate. On ResNet-50 with a batch size of 2, their group normalisation had 10.6% lower error than BN.
- **Train–test mismatch.** Training uses mini-batch statistics and inference uses running averages, so the two can differ if the data distribution changes.
- **Awkward for sequences.** Sequences in a batch can have different lengths, and recurrent networks apply the same layer at every time step, which makes per-step batch statistics hard to define.
- **Distributed training.** Unless statistics are synchronised across devices, each device normalises over its own small batch.

## Open questions

- **Why it works.** Ioffe and Szegedy credited the reduction of internal covariate shift. Santurkar et al. (2018) tested this and reported that stability of layer inputs has little to do with the method's success; they argued that it smooths the optimisation landscape. Bjorck et al. (2018) found that its main effect is to allow training with larger learning rates, since it keeps activations zero-mean and unit-scale. These accounts are not fully exclusive, and the causal ordering is not settled.
- **Batch-free alternatives.** How much of BN's benefit can be kept without depending on batch statistics is a major open question, and it is the motivation for the group and RMS variants.
- **Scope.** Whether the same explanation covers normalisation in other architectures and training regimes is not yet established.

## References

### Seminal papers

- Ioffe, S. & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift". arXiv:1502.03167 — Introduces batch normalisation, normalising each mini-batch and reporting faster training of image classifiers.
- Santurkar, S., Tsipras, D., Ilyas, A. & Madry, A. (2018). "How Does Batch Normalization Help Optimization?". arXiv:1805.11604 — Tests the internal covariate shift explanation and proposes that batch normalisation smooths the optimisation landscape.
- Bjorck, J., Gomes, C., Selman, B. & Weinberger, K. Q. (2018). "Understanding Batch Normalization". arXiv:1806.02375 — Empirical study concluding that batch normalisation mainly enables training with larger learning rates.
- Wu, Y. & He, K. (2018). "Group Normalization". arXiv:1803.08494 — Shows how batch normalisation's error grows at small batch sizes and proposes a batch-independent alternative.

### Surveys and textbooks

- Huang, L., et al. (2020). "Normalization Techniques in Training DNNs: Methodology, Analysis and Application". arXiv:2009.12836 — A survey that places batch normalisation in a taxonomy with the other normalisation methods.


### Articles and documentation

- He, K., Zhang, X., Ren, S. & Sun, J. (2016). "Identity Mappings in Deep Residual Networks". arXiv:1603.05027 — Analyses identity skip connections in residual networks and proposes a new residual unit that makes training easier.
