---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/generative
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

Diffusion models are a family of generative networks that create data by reversing a gradual noising process. They power most modern image, video and audio generators. The general idea of learning to denoise is explained in [Generative Models](../../generative/index.md); this page covers the architecture family: the networks that do the denoising, how they are conditioned on text or other inputs, and how they are sampled.

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

### Denoising Diffusion Probabilistic Models (Ho, Jain & Abbeel, 2020)

- **Problem:** GANs produce sharp images but train unstably, and likelihood-based models of the time produced weaker samples.
- **Core idea:** train a network to predict the noise added at random time steps, with a weighted variational bound that simplifies to the noise-prediction loss above.
- **Equation or algorithm:** the loss in the section above, with a fixed linear noise schedule and ancestral sampling over \(T\) steps.
- **Results:** the abstract reports an Inception score of 9.46 and an FID of 3.17 on unconditional CIFAR-10, described as state of the art at the time. It describes sample quality on 256×256 LSUN as similar to ProgressiveGAN, without a number in the abstract.
- **Limitations:** sampling needs hundreds of network evaluations, which makes generation slow. The abstract does not report training or sampling cost.

### High-Resolution Image Synthesis with Latent Diffusion Models (Rombach et al., 2021/2022)

- **Problem:** pixel-space diffusion consumes very large amounts of compute, which the authors describe as often hundreds of GPU days.
- **Core idea:** train the diffusion model in the latent space of a pretrained autoencoder, and add cross-attention layers so the model can be conditioned on text, layouts or other inputs.
- **Equation or algorithm:** the same objective as DDPM applied to latents \(z = E(x)\), with cross-attention on the denoiser's intermediate features.
- **Results:** the abstract reports state-of-the-art results on image data and a new state of the art for image inpainting, with competitive results on unconditional generation, semantic scene synthesis and super-resolution at lower compute than pixel-space models. It gives no benchmark numbers in the abstract.
- **Limitations:** the autoencoder limits the detail that can be reconstructed. The abstract does not quantify the compute saving; the main text does.

### Scalable Diffusion Models with Transformers (Peebles & Xie, 2022/2023)

- **Problem:** the U-Net backbone is hand-designed, and it was unclear whether diffusion quality scales with compute in the same way as Transformer language models.
- **Core idea:** replace the U-Net in latent diffusion with a Transformer over latent patches, and measure quality against forward-pass compute in Gflops.
- **Equation or algorithm:** the latent is split into patches of size \(p\), embedded as tokens, and processed with adaptive layer normalisation that takes the time step and class label as conditioning.
- **Results:** the abstract reports that larger models, with more Gflops from depth, width or more tokens, consistently have lower FID. The largest model, DiT-XL/2, reaches an FID of 2.27 on class-conditional ImageNet at 256×256, outperforming earlier diffusion models. It gives no FID for 512×512 in the abstract.
- **Limitations:** the results are on class-conditional ImageNet, which is a narrower benchmark than text-to-image. The abstract gives no training-compute figures.

## Connections

- **Generative modelling:** diffusion is one of several generative families, and its general theory is in [Generative Models](../../generative/index.md).
- **Transformers:** the DiT backbone reuses the attention machinery in [Transformers & Attention](../transformer/index.md).
- **Convolutional networks:** the U-Net backbone is built from the layers in [Convolutional Networks](../cnn/index.md).
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
