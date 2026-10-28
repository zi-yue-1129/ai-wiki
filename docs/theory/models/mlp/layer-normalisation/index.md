---
related:
- theory/models/mlp
- theory/models/transformer
aliases:
  - Layer Normalisation
  - LayerNorm
  - 層正規化
tags:
  - normalisation
  - feedforward networks
  - sequence models
last_reviewed: 2026-10-28
---

# Layer Normalisation

Layer normalisation is a method that normalises the summed inputs of a hidden layer over all of its units, for one training case at a time. Ba, Kiros and Hinton introduced it in 2016 in the paper "Layer Normalization". Because it does not depend on batch statistics, it suits sequence models.

## Problem

Batch normalisation's benefit depends on the mini-batch size. It is unclear how to apply it to recurrent networks, and it cannot be used for online learning.

## Core idea

Normalise over all hidden units of one layer for a single training case, then give each unit its own learned gain and bias. Training and test time use the same computation, so the result for an input does not depend on other examples in a batch.

## Equation or algorithm

With \(H\) hidden units and summed inputs \(a_i\), the layer computes the mean and standard deviation over the units:

\[
\mu = \frac{1}{H}\sum_{i=1}^{H} a_i, \qquad
\sigma = \sqrt{\frac{1}{H}\sum_{i=1}^{H}(a_i - \mu)^2}.
\]

Each unit's normalised activation is then scaled by its gain and shifted by its bias.

## Results

On order embeddings for MSCOCO, caption retrieval R@1 rose from 46.6 to 48.5 and image retrieval R@1 rose from 37.8 to 38.9. The model reached its best validation result in 60% of the baseline's training time. On binarised MNIST with DRAW, the layer-normalised model reached 82.09 nats after 200 epochs, against 82.36 for the baseline.

## Limitations

Unlike batch normalisation, layer normalisation is not invariant to rescaling individual weight vectors. In ConvNets, batch normalisation performed better, and the authors state that "further research is needed to make layer normalization work well in ConvNets".

## Connections

The [MLP](../index.md) family page contrasts it with batch normalisation, which suits [CNNs](../../cnn/index.md). It is also the normalisation layer discussed alongside the [Transformer](../../transformer/index.md) family, and the activation covered in [Gaussian error linear units](../gelu/index.md) sits in the same feedforward blocks. For recurrent networks, where applying batch normalisation was unclear, see the [RNN](../../rnn/index.md) family page.

## Open issues and further variants

- **Convolutional networks.** Making layer normalisation work well in ConvNets, where batch normalisation performed better in the paper's comparison, still needs further research.
- **Sequence and online settings.** Its independence from batch size suits sequence models and online learning. How far that advantage holds across tasks is a question for further study.
- **Rescaling invariance.** The lack of invariance to rescaling individual weight vectors may matter for some architectures and not others, so it has to be checked for each model.

## References

### Seminal papers

- Ba, J. L., Kiros, J. R. & Hinton, G. E. (2016). "Layer Normalization". arXiv:1607.06450 — Normalises over features rather than over the batch.
- Ioffe, S. & Szegedy, C. (2015). "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift". arXiv:1502.03167 — Normalises activations over each mini-batch, the method that layer normalisation was proposed as an alternative to.
- He, K., et al. (2015). "Deep Residual Learning for Image Recognition". arXiv:1512.03385 — Residual connections that make deep networks trainable.

### Surveys and textbooks

- Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press. https://www.deeplearningbook.org/ — Chapter 6 covers feedforward networks, activations and the universal approximation results.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Hendrycks, D. & Gimpel, K. (2016). "Gaussian Error Linear Units (GELUs)". arXiv:1606.08415 — The GELU activation, used in many Transformer models.
