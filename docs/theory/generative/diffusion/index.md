---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/models/cnn
  - brain-mind/neuroai
  - brain-mind/bci
tags:
  - diffusion models
  - generative models
aliases:
  - 擴散模型
  - 擴散式模型
  - Diffusion models
  - DDPM
  - 去噪擴散
  - Latent diffusion
---

# Diffusion Models

Diffusion models are a family of generative networks that create data by reversing a gradual noising process. They power most modern image, video and audio generators. Diffusion is one generative algorithm, so its general place is in [Generative Models](../index.md). This page covers the algorithm itself: the forward and reverse processes, how the denoising network is conditioned on text or other inputs, and how samples are drawn. The networks that do the denoising are ordinary architecture families, described in [Convolutional Networks](../../models/cnn/index.md) and [Transformers & Attention](../../models/transformer/index.md).

## Overview

A diffusion model has two processes. The **forward process** adds Gaussian noise to a data sample \(x_0\) over \(T\) steps until it is close to pure noise \(x_T\). It needs no learning. The **reverse process** is a neural network \(\epsilon_\theta(x_t, t)\) trained to predict the noise that was added at each step. Generation starts from random noise and applies the learned reverse steps until a sample \(x_0\) appears.

Compared with other generative families, diffusion models trade speed for stability and quality. Training is a simple regression problem, which avoids the instability of adversarial training, but sampling needs many network evaluations. Much of the recent work reduces that cost.

## Key concepts

- **Noise schedule**: how much noise is added at each step, often written as \(\bar\alpha_t\).
- **Denoiser**: the network that predicts noise (or the clean image, or a velocity) from a noisy input and a time step.
- **Backbone**: the architecture of the denoiser. Early models used a U-Net, a convolutional network with skip connections; newer models use Transformers on patches of a latent image.
- **Latent diffusion**: running the diffusion process in the compressed latent space of an autoencoder rather than on raw pixels.
- **Conditioning**: supplying extra inputs such as a text prompt, which the denoiser attends to, usually with cross-attention.
- **Classifier-free guidance**: a way to strengthen conditioning by combining a conditional and an unconditional prediction.
- **Sampler**: the rule that turns the reverse steps into a fast sampling procedure, for example DDIM.

## How it works

The simplest training objective is the noise-prediction loss:

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big], \qquad x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon
\]

Each training example is a clean sample with a random time step and random noise. The network sees the noisy input and the step, and learns to predict the noise. Sampling is an iterative update that removes a little of the predicted noise at each step.

### Backbone

- **U-Net**: a convolutional encoder–decoder with skip connections and attention at lower resolutions. It was the default for pixel-space image models.
- **Transformer (DiT)**: the latent is cut into patches, each becomes a token, and a Transformer processes the tokens with the time step and condition injected as extra inputs. Its quality improves predictably with more compute, similar to language models.

### Latent diffusion and conditioning

Latent diffusion first compresses images with a pretrained autoencoder and runs diffusion on the small latent. This reduces the cost of each step by roughly the compression factor. Text conditioning is usually done by cross-attention from the denoiser to the embeddings of a text encoder.

### Faster sampling

A naive sampler needs as many steps as training. Two ideas reduce this. Non-Markovian samplers such as DDIM reuse the same trained model with far fewer steps. Distillation trains a student model to match several teacher steps in one. Classifier-free guidance trades diversity for prompt fidelity, and is applied at sampling time without a separate classifier.

## Key methods

Each named method has its own page with the problem, core idea, equations, results and limitations.

- [DDPM](ddpm.md) (Ho, Jain & Abbeel, 2020): the noise-prediction objective and the sampler that made diffusion practical for images.
- [DDIM](ddim.md) (Song, Meng & Ermon, 2020/2021): a non-Markovian sampler that reuses the DDPM model in far fewer steps.
- [Latent Diffusion](latent-diffusion.md) (Rombach et al., 2021/2022): diffusion in the latent space of an autoencoder, with cross-attention conditioning.
- [DiT](dit.md) (Peebles & Xie, 2022/2023): a Transformer denoiser that replaces the U-Net and scales with compute.
- [Classifier-free guidance](classifier-free-guidance.md) (Ho & Salimans, 2022): conditioning control without a separate classifier.
- [Consistency models and fast samplers](consistency-models.md) (Song et al., 2023; Lu et al., 2022): distillation and high-order ODE solvers that reduce sampling to one to about twenty steps.

### Comparison

| Method | What it changes | Sampling steps | Denoiser | Conditioning |
|---|---|---|---|---|
| [DDPM](ddpm.md) | Training objective and Markov sampler | About 1,000 | U-Net | Time step; class or text added by other methods |
| [DDIM](ddim.md) | Non-Markovian sampler on the same model | Any subsequence, far fewer | Same as DDPM | Same as DDPM |
| [Latent Diffusion](latent-diffusion.md) | Diffusion in an autoencoder latent | Few to many | U-Net | Cross-attention |
| [DiT](dit.md) | Transformer denoiser | Few to many | Transformer on patches | Adaptive layer norm with time step and class |
| [Consistency models and fast samplers](consistency-models.md) | Distilled one-step maps, and high-order ODE solvers | One to about 20 | Same as the trained model | Same as the trained model |

## Connections

- **Generative modelling:** diffusion is one of several generative algorithms, alongside autoregressive models, VAEs and GANs, described in [Generative Models](../index.md).
- **Transformers:** the DiT backbone reuses the attention machinery in [Transformers & Attention](../../models/transformer/index.md).
- **Convolutional networks:** the U-Net backbone is built from the layers in [Convolutional Networks](../../models/cnn/index.md).
- **Brain and mind:** diffusion models have been used to decode images from brain activity; see [Brain-Computer Interfaces](../../../brain-mind/bci/index.md). For how the brain's own learning compares with these training objectives, see [NeuroAI](../../../brain-mind/neuroai/index.md).

## Applications

- Text-to-image and image editing, such as inpainting and super-resolution.
- Video generation with diffusion Transformers.
- Audio and speech synthesis.
- Robot control policies that model action sequences with a denoising process.

## Open questions

- How far can sampling be reduced to a single step without losing quality or diversity?
- Does the Transformer backbone scale better than the U-Net for video, and at what cost?
- How much of the benefit of guidance is a real improvement in the model, and how much is a trade-off that reduces diversity?

## References

### Seminal papers

- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — The first diffusion-based generative model, which learns to reverse a gradual noising process.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — Simplifies training to noise prediction and shows high-quality image generation.
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — Non-Markovian sampler that produces samples 10× to 50× faster than DDPM.
- Rombach, R. et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — Diffusion in autoencoder latent space with cross-attention conditioning.
- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV. https://arxiv.org/abs/2212.09748 — Replaces the U-Net with a Transformer and shows FID improves with compute.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Separates the design choices of diffusion models so each can be tuned on its own.
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — Guidance that combines conditional and unconditional predictions without an external classifier.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Unifies diffusion and score-based models as stochastic differential equations.

### Articles and documentation

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Step-by-step code walk-through of DDPM, useful for checking the equations in this page.
