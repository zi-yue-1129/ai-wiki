---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
tags:
  - generative models
  - convolutional networks
  - density estimation
aliases:
  - PixelCNN
  - PixelRNN
  - Gated PixelCNN
  - 像素卷積網路
---

# PixelCNN

PixelCNN is an autoregressive model of natural images that predicts each pixel from the pixels before it, using a stack of masked convolutions. It was introduced with its recurrent sibling, PixelRNN, by van den Oord, Kalchbrenner and Kavukcuoglu (2016), and it is one of the landmark methods of the [Autoregressive generative models](../index.md) overview.

## Overview

Autoregressive image models factorise an image into one conditional distribution per pixel, taken in a fixed order. PixelRNN computes each conditional with two-dimensional LSTM layers, which give a large context but must be evaluated one step after another.

PixelCNN keeps the factorisation and replaces the recurrent layers with masked convolutions, which stop each prediction from using later pixels. All conditionals of a training image can then be computed in parallel. The cost is a bounded context: in the original experiments the convolutional model, with the smallest context, was the least accurate of the three compared. Sampling stays sequential for both.

## Key concepts

- **Raster order**: pixels are visited row by row, from top left to bottom right. The conditional for a pixel depends only on the pixels earlier in this order.
- **Masked convolution**: a convolution whose weights are zeroed wherever they would reach a pixel not yet generated. Mask A is used in the first layer, and mask B in later layers, where a colour channel may also connect to itself.
- **Discrete softmax output**: each colour channel takes one of 256 values, and the network outputs a categorical distribution over them.
- **Blind spot**: a single masked stack ignores part of the pixels that precede the current one. The Gated PixelCNN removes it with two stacks.

## How it works

For an image \(x\) of \(n \times n\) pixels, the model defines

\[
p(x) = \prod_{i=1}^{n^2} \prod_{c \in \{R, G, B\}} p\big(x_{i,c} \mid x_{<i},\, x_{i,<c}\big)
\]

where \(x_{i,<c}\) are the earlier colour values of the same pixel. Each factor is a softmax over 256 values. Training maximises the log-likelihood, and results are reported in bits per dimension, the negative log-likelihood in base 2 divided by the number of values in the image.[^1]

1. **Training.** One masked pass over the image computes every conditional at once, because the true pixels are known.
2. **Sampling.** Start from an empty image. For each pixel and colour channel in raster order, run the network, draw a value from the softmax and write it back. A 32 × 32 RGB image needs 3,072 network evaluations.

## Results

- **CIFAR-10, test set.** The PixelRNN paper reports 3.14 bits per dimension for PixelCNN, 3.07 for a Row LSTM and 3.00 for a Diagonal BiLSTM, whose context is the largest of the three.
- **Gated PixelCNN.** The follow-up paper adds gated units and a two-stack design. It reports 3.03 bits per dimension on the CIFAR-10 test set, 0.11 better than PixelCNN, and 3.83 and 3.57 on ImageNet at 32 × 32 and 64 × 64, slightly better than PixelRNN. It matches PixelRNN in less than half the training time.[^2]

## Limitations

- **Bounded context and slow sampling.** The receptive field grows only with depth, and generation needs one network evaluation per colour value.
- **Discrete outputs.** The 256-way softmax treats neighbouring intensities as unrelated categories. The PixelRNN authors note that the model does not know pixel values 51 and 52 are neighbours. PixelCNN++ replaces the softmax with a discretised logistic mixture, which its authors report speeds up training.[^3]

## Open questions

- **Context against parallelism.** It is unclear how far depth alone can close the gap to recurrent models while training stays parallel.
- **Ordering.** Raster order is a choice, and these papers do not test other orders.
- **Pixels against codes.** A PixelCNN prior over a small grid of learned codes is cheaper than one over every pixel, as in the [VQ-VAE](../../vae/vq-vae/index.md), but whether that holds at equal quality is still being studied.

## Connections

- **Parent.** The factorisation, masking and sampling procedure are shared across the family in [Autoregressive generative models](../index.md).
- **Audio.** [WaveNet](../wavenet/index.md) adapts the same design to causal convolutions over audio samples.
- **Transformers.** [Image GPT](../image-gpt/index.md) pursues the next-pixel objective with self-attention instead.

## Applications

- **Class-conditional generation.** Conditioning on a label or a learned embedding gives diverse images of a chosen class (van den Oord et al., 2016b).
- **Priors over codes.** PixelCNN models the discrete codes of [VQ-VAE](../../vae/vq-vae/index.md) image generators.

[^1]: Bits per dimension is the average negative log-likelihood in base 2, divided by the number of values in the image (3,072 for 32 × 32 RGB). Lower is better.

[^2]: The PixelRNN ImageNet figures come from the table in the Gated PixelCNN paper. The original PixelRNN paper reports its ImageNet results on the validation set, so the two sets of figures are not strictly comparable.

## References

### Seminal papers

- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. ICML (PMLR 48). https://arxiv.org/abs/1601.06759 — Introduces PixelRNN and PixelCNN, with results on MNIST, CIFAR-10 and ImageNet.
- van den Oord, A., Kalchbrenner, N., Vinyals, O., Espeholt, L., Graves, A. & Kavukcuoglu, K. (2016). *Conditional Image Generation with PixelCNN Decoders*. arXiv. https://arxiv.org/abs/1606.05328 — Adds gated units and a two-stack design that removes the blind spot.
- Salimans, T., Karpathy, A., Chen, X. & Kingma, D. P. (2017). *PixelCNN++: Improving the PixelCNN with Discretized Logistic Mixture Likelihood and Other Modifications*. arXiv. https://arxiv.org/abs/1701.05517 — Replaces the 256-way softmax with a logistic mixture and adds shortcut connections.
- Germain, M., Gregor, K., Murray, I. & Larochelle, H. (2015). *MADE: Masked Autoencoder for Distribution Estimation*. arXiv. https://arxiv.org/abs/1502.03509 — Masks an autoencoder so that each output depends only on earlier inputs.

### Surveys and textbooks

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — Compares autoregressive models with other deep generative families.
