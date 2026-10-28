---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - generative models
  - transformers
  - self-supervised learning
aliases:
  - iGPT
  - Image GPT
  - Generative pretraining from pixels
  - 影像 GPT
---

# Image GPT

Image GPT (iGPT) trains a GPT-2-style Transformer to predict the next pixel of a low-resolution image, with no convolutions or other image-specific structure. Chen and colleagues (2020) showed that the features it learns are strong enough to compete with supervised and self-supervised representations on standard benchmarks. It is one of the landmark methods of the [Autoregressive generative models](../index.md) overview, and the image counterpart of next-token prediction in language.

## Overview

Next-token prediction pretrained large Transformers for language, as in GPT-style [large language models](../../../../../models/llm/index.md). Chen et al. asked whether the same generative pretraining works for images. A 32 × 32 RGB image already has 3,072 values, and dense self-attention grows quadratically with sequence length.

The authors shorten the sequence by lowering the resolution and quantising colours, pretrain on unlabelled ImageNet, and measure the result with linear probes and fine-tuning. The best features are not in the final layer, and quality improves with model size.

## Key concepts

- **Raster sequence**: the image is flattened into a one-dimensional sequence of pixels, row by row. Each position is predicted from the earlier positions only.
- **Colour palette**: the (R, G, B) values are clustered with k-means into 512 colours, so each pixel becomes one token.
- **Linear probe**: a linear classifier trained on frozen features from one layer. It measures how linearly separable the learned representation is.

## How it works

The model is trained to minimise the negative log-likelihood of the sequence, with the next-token cross-entropy as the loss:

\[
\mathcal{L}_{\text{AR}} = \mathbb{E}_{x}\Big[-\sum_{i} \log p\big(x_i \mid x_1, \dots, x_{i-1}\big)\Big]
\]

The steps are:

1. Resize the image, for example to 32 × 32, and map each pixel to its nearest palette colour. Larger inputs use a VQ-VAE with a 4,096-entry vocabulary.
2. Embed the tokens and add learned position embeddings. A stack of Transformer blocks with a causal mask on the attention logits then produces one vector per position.
3. A projection gives 512 logits per position, and training minimises the loss above.
4. For classification, a linear probe reads features from a chosen layer, and fine-tuning adds a classification head.

Generation samples tokens one at a time, as in other autoregressive models. [KV caching](../../../../../models/transformer/kv-cache/index.md) makes each step cheaper but keeps the process sequential.

## Results

- **CIFAR-10.** A linear probe reaches 96.3%, which the authors report as higher than a supervised Wide ResNet. Full fine-tuning reaches 99.0%.
- **ImageNet.** The best single-layer linear probe reaches 60.3% at a 32 × 32 model resolution and 65.2% at 48 × 48. Concatenating features from 11 layers and using the VQ-VAE preprocessing gives 69.0%, which the authors describe as competitive with contrastive learning methods of the time.
- **Model size.** At a 32 × 32 model resolution, the best-layer ImageNet probe reaches 41.9% for the smallest model (iGPT-S, 76 million parameters), 54.5% for iGPT-M (455 million) and 60.3% for iGPT-L (1.4 billion).
- **Layer depth.** Representation quality rises with depth and then falls. On CIFAR-10, the final layer is 2.4% worse than the best layer.
- **BERT comparison.** A BERT-style masked objective gave weaker linear probes, but fine-tuned to 98.6% on CIFAR-10.

The authors state that their goal is representation learning rather than high-quality samples, and they show only qualitative class-unconditional samples.

## Limitations

- **Quadratic attention.** Dense self-attention costs grow with the square of the sequence length, which forces low resolutions. The authors call this a significant limitation and point to sparse attention as a remedy.
- **Scale.** The results depend on large models and large compute. The authors note that iGPT-L has two to three times as many parameters as similarly performing ImageNet models and uses more compute.
- **No spatial prior.** The model must learn spatial structure from data, and the authors note that bridging the gap to convolutional encoders is not obvious.

## Open questions

- **Generative and discriminative training.** Whether pixel prediction can match contrastive methods at high resolution, without much larger models, is not yet settled.
- **Tokeniser choice.** The colour palette is a crude tokeniser. Learned codes from a [VQ-VAE](../../vae/vq-vae/index.md) keep more detail at the same length.

## Connections

- **Parent.** iGPT is the image case of the family in [Autoregressive generative models](../index.md), alongside [PixelCNN](../pixelcnn/index.md).
- **Language models.** The objective matches the [large language models](../../../../../models/llm/index.md) that predict the next token. See also [Tokenisation](../../../../../models/llm/tokenisation/index.md) and [Multimodal models](../../../../../models/multimodal/index.md).
- **Masked prediction.** The BERT-style alternative is in [Masked prediction](../../../../self-supervised/masked-prediction/index.md).

## Applications

- **Image generation.** Transformers over text and image tokens generate images from text prompts (Ramesh et al., 2021). VQGAN-based Transformers were state of the art among autoregressive models for class-conditional ImageNet (Esser et al., 2021).

## References

### Seminal papers

- Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D. & Sutskever, I. (2020). *Generative Pretraining From Pixels*. ICML (PMLR 119). https://proceedings.mlr.press/v119/chen20s.html — The paper itself: a GPT-2-style Transformer trained to predict pixels.
- Vaswani, A. et al. (2017). *Attention Is All You Need*. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the Transformer on which iGPT is built.
- Child, R. et al. (2019). *Generating Long Sequences with Sparse Transformers*. arXiv. https://arxiv.org/abs/1904.10509 — Introduces sparse attention factorisations that reduce the quadratic cost.
- van den Oord, A., Vinyals, O. & Kavukcuoglu, K. (2017). *Neural Discrete Representation Learning*. arXiv. https://arxiv.org/abs/1711.00937 — Introduces the VQ-VAE codes used for higher-resolution inputs.
- Ramesh, A. et al. (2021). *Zero-Shot Text-to-Image Generation*. arXiv. https://arxiv.org/abs/2102.12092 — Models text and image tokens as one autoregressive stream.
- Esser, P., Rombach, R. & Ommer, B. (2021). *Taming Transformers for High-Resolution Image Synthesis*. arXiv. https://arxiv.org/abs/2012.09841 — Transformers over VQ codebook sequences for high-resolution synthesis.

### Surveys and textbooks

- Bond-Taylor, S., Leach, A., Long, Y. & Willcocks, C. G. (2021). *Deep Generative Modelling: A Comparative Review of VAEs, GANs, Normalizing Flows, Energy-Based and Autoregressive Models*. arXiv. https://arxiv.org/abs/2103.04922 — Compares autoregressive models with other generative families.
