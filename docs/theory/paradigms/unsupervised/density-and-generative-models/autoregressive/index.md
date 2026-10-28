---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/llm/index.md
  - theory/models/speech/index.md
tags:
  - generative models
  - autoregressive models
  - density estimation
aliases:
  - Autoregressive generative models
  - 自迴歸生成模型
  - 自回歸生成模型
  - PixelRNN
  - PixelCNN
  - WaveNet
---

# Autoregressive Generative Models

An autoregressive generative model writes the joint probability of a data object as a product of conditional probabilities, one element at a time. For an image, a sound or a sentence, this turns the hard problem of modelling everything at once into a sequence of easier problems: predict the next pixel, the next sample of audio or the next token, given everything before it. Language models are the best-known example, and the same idea generates images and audio.

## Overview

The chain rule of probability states that for a sequence $x_1, \dots, x_n$,

$$
p(x_1, \dots, x_n) = \prod_{i=1}^{n} p(x_i \mid x_1, \dots, x_{i-1}),
$$

so a model that can predict each element from its predecessors defines a full distribution over the sequence. Training maximises the sum of the log conditional probabilities over the data, which is exact maximum likelihood with no latent variables and no approximation of the likelihood. Sampling runs the chain forward: draw $x_1$, then $x_2$ given $x_1$, and so on.

The price is in sampling. Generation takes one step per element, and the steps cannot be parallelised across the sequence in the usual way. The ordering of the elements is also a design choice, because the factorisation depends on it, even though the joint distribution does not.

## Key concepts

- **Factorisation**: the choice of order in which elements are modelled. For images, the order is usually raster order, row by row.
- **Likelihood**: the model's log probability of the data, which can be computed exactly and compared across models.
- **Teacher forcing**: during training each conditional is fitted with the true previous elements, so all positions are trained in parallel.
- **Tokens**: discrete units, such as words or codebook entries, over which the conditionals are defined. Images or audio are often mapped to tokens first.
- **Sampling cost**: the number of sequential steps needed to generate one object.

## How it works

**Pixels.** PixelRNN (van den Oord, Kalchbrenner & Kavukcuoglu, 2016) models an image by predicting its pixels sequentially along the two spatial dimensions, so that each pixel depends on the pixels before it in the ordering. The paper's abstract describes a deep network that sequentially predicts the pixels in an image in this way. Convolutional variants, known as PixelCNN, follow the same factorisation and can be computed more efficiently during training.

**Raw audio.** WaveNet (van den Oord et al., 2016) is a deep network for generating raw audio waveforms. It predicts each audio sample from the samples before it, which gives a model that can produce speech and music one sample at a time.

**Transformers over pixels.** Image GPT (Chen et al., 2020) trains a sequence Transformer to predict pixels auto-regressively, without built-in knowledge of the two-dimensional structure of the input. The approach is the same next-element objective as language modelling, applied to image pixels. The Transformer architecture itself is described in [Attention Is All You Need](../../../../models/transformer/attention-is-all-you-need/index.md), which the paper introduces as "based solely on attention mechanisms, dispensing with recurrence and convolutions entirely" (Vaswani et al., 2017).

**Tokens and latent codes.** Modelling every pixel is expensive, so many systems first compress the data. VQ-VAE (van den Oord, Vinyals & Kavukcuoglu, 2017) learns discrete latent representations by incorporating vector quantisation into an autoencoder. An autoregressive prior can then be fitted over the discrete codes, which is much shorter than the raw data.

## Key methods

Brief comparison. Each named method is a candidate for its own method page; those pages are not yet written, so the detail is given in this section for now.

- **PixelRNN and PixelCNN (pixel-level)**: the ordering is spatial, and the model predicts each pixel's value. Exact likelihood on images, slow sampling at full resolution.
- **WaveNet (sample-level)**: the same factorisation applied to audio samples, which are very long sequences.
- **Image GPT (Transformer over pixels)**: a Transformer in place of a recurrent or convolutional model, with the same next-element objective used for language.
- **Token-based autoregressive priors (VQ-VAE)**: the autoregressive model runs over a short sequence of discrete codes, not over pixels.

## Connections

The same objective underlies [Large Language Models](../../../../models/llm/index.md), which generate text one token at a time, and the speech models on the [Speech & Audio](../../../../models/speech/index.md) page. Among the other generative families, [diffusion models](../diffusion/index.md) generate by iterative denoising rather than by a fixed order, and comparisons of the two are part of the [Generative Models](../generative-models/index.md) overview.

The brain connection is at the level of prediction. Predictive frameworks in neuroscience propose that the brain anticipates its next input, which is the same objective as next-element prediction. Whether neural circuits implement this as an autoregressive model is an open question, discussed in [NeuroAI](../../../../../brain-mind/neuroai/index.md).

## Applications

- **Text.** Language models that generate text token by token.
- **Speech and audio.** Waveform and codec models that generate speech or music.
- **Images.** Pixel-level and token-level models for image generation and completion.

## Open questions

- Sampling is sequential, so generating long objects is slow. Parallel decoding schemes narrow the gap but add complexity.
- Errors made early in the sequence can compound, because later conditionals depend on them.
- The best ordering for images and other non-sequential data is not obvious, and different orderings give different models.
- Autoregressive and diffusion models trade off exact likelihood, sampling speed and sample quality differently, and the best choice depends on the data and the task.

## References

### Seminal papers

- van den Oord, A., Kalchbrenner, N. & Kavukcuoglu, K. (2016). *Pixel Recurrent Neural Networks*. arXiv. https://arxiv.org/abs/1601.06759 — Models images by predicting their pixels sequentially along the spatial dimensions, the basis of the PixelRNN family.
- van den Oord, A., Dieleman, S., Zen, H., Simonyan, K., Vinyals, O., Graves, A., Kalchbrenner, N., Senior, A. & Kavukcuoglu, K. (2016). *WaveNet: A Generative Model for Raw Audio*. arXiv. https://arxiv.org/abs/1609.03499 — A deep network that generates raw audio waveforms sample by sample.
- Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D. & Sutskever, I. (2020). Generative Pretraining from Pixels. In *Proceedings of the 37th International Conference on Machine Learning (ICML 2020)*, PMLR 108. https://cdn.openai.com/papers/Generative_Pretraining_from_Pixels_V1_ICML.pdf — A sequence Transformer trained to predict pixels auto-regressively, with no built-in two-dimensional structure.
- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — VQ-VAE, which learns discrete latent codes with vector quantisation, so that priors can be fitted over short token sequences.
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. & Polosukhin, I. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — The Transformer, used as the sequence model in autoregressive generation.
