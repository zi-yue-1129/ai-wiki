---
status: complete
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

Diffusion models are a family of generative networks that create data by reversing a gradual noising process. They power most modern image, video and audio generators. Diffusion is one generative algorithm, so its general place is in [Generative Models](../generative-models/index.md). This page covers the algorithm itself: the forward and reverse processes, how the denoising network is conditioned on text or other inputs, and how samples are drawn. The networks that do the denoising are ordinary architecture families, described in [Convolutional Networks](../../../../models/cnn/index.md) and [Transformers & Attention](../../../../models/transformer/index.md).

## Overview

A diffusion model has two processes. The **forward process** adds Gaussian noise to a data sample \(x_0\) over \(T\) steps until it is close to pure noise \(x_T\). It needs no learning. The **reverse process** is a neural network \(\epsilon_\theta(x_t, t)\) trained to predict the noise that was added at each step. Generation starts from random noise and applies the learned reverse steps until a sample \(x_0\) appears.

Compared with other generative families, diffusion models trade speed for stability and quality. Training is a simple regression problem, which avoids the instability of adversarial training, but sampling needs many network evaluations. Much of the recent work reduces that cost.

## Key concepts

- **Noise schedule**: how much noise is added at each step, often written as \(\bar\alpha_t\).
- **Denoiser**: the network that predicts the noise (or the clean image, or a velocity) from a noisy input and a time step.
- **Backbone**: the architecture of the denoiser. Early image models used a U-Net, a convolutional network with skip connections; newer models use Transformers on patches of a latent image.
- **Latent diffusion**: running the diffusion process in the compressed latent space of an autoencoder rather than on raw pixels.
- **Conditioning**: supplying extra inputs such as a class label or a text prompt, which the denoiser uses through cross-attention or by adding them to its layers.
- **Classifier-free guidance**: a way to strengthen conditioning by combining a conditional and an unconditional prediction.
- **Sampler**: the rule that turns the reverse steps into a sampling procedure, for example DDPM's ancestral sampler or [DDIM](ddim.md).

## How it works

The simplest training objective is the noise-prediction loss:

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big], \qquad x_t = \sqrt{\bar\alpha_t}\,x_0 + \sqrt{1-\bar\alpha_t}\,\epsilon
\]

Each training example is a clean sample with a random time step and random noise. The network sees the noisy input and the step, and learns to predict the noise. Sampling is an iterative update that removes a little of the predicted noise at each step. [DDPM](ddpm.md) introduced this objective with a simplified loss that was enough to produce high-quality images.

### Backbone

- **U-Net**: a convolutional encoder–decoder with skip connections and attention at lower resolutions. It was the default for pixel-space image models.
- **Transformer (DiT)**: the latent is cut into patches, each becomes a token, and a Transformer processes the tokens. The time step and class label are injected through adaptive layer normalisation. Peebles and Xie (2023) report that FID improves as the model's Gflops increase.

### Latent diffusion and conditioning

Latent diffusion first compresses images with a pretrained autoencoder and runs diffusion on the much smaller latent, which lowers the memory and compute of each denoising step. [Latent Diffusion](latent-diffusion.md) (Rombach et al., 2022) adds cross-attention from the denoiser to the embeddings of a text encoder or other conditioning inputs, and applies the same framework to tasks such as inpainting and super-resolution.

### Faster sampling

A naive sampler needs as many steps as training. Three families of methods reduce this:

- **Non-Markovian samplers** such as [DDIM](ddim.md) reuse the same trained model with far fewer steps. On unconditional CIFAR-10, DDIM reaches FID 4.67 with 50 steps, where DDPM reaches 8.01 at the same step count.
- **Distillation** trains a student model to match two of the teacher's sampling steps with one. Salimans and Ho (2022) apply this progressively, halving the number of steps each round.
- **Guidance** trades diversity for prompt fidelity at sampling time. [Classifier-free guidance](classifier-free-guidance.md) needs no separate classifier, only the model's own conditional and unconditional predictions.

## Key methods

Each named method has its own page with the problem, core idea, equations, results and limitations.

- [DDPM](ddpm.md) (Ho, Jain & Abbeel, 2020): the noise-prediction objective and the sampler that made diffusion practical for images.
- [DDIM](ddim.md) (Song, Meng & Ermon, 2021): a non-Markovian sampler that reuses the DDPM model in far fewer steps.
- [Consistency models and fast samplers](consistency-models.md) (Song et al., 2023): models that map any point of a trajectory to its output, supporting one-step generation.
- [Latent Diffusion](latent-diffusion.md) (Rombach et al., 2022): diffusion in the latent space of an autoencoder, with cross-attention conditioning.
- [DiT](../../../../models/transformer/dit/index.md) (Peebles & Xie, 2023): a Transformer denoiser that replaces the U-Net and scales with compute.
- [Classifier-free guidance](classifier-free-guidance.md) (Ho & Salimans, 2022): conditioning control without a separate classifier.

### Comparison

| Method | What it changes | Denoiser | Conditioning |
|---|---|---|---|
| [DDPM](ddpm.md) | Training objective and Markov sampler | U-Net | Time step |
| [DDIM](ddim.md) | Non-Markovian sampler on the same trained model | Same as DDPM | Same as DDPM |
| [Latent Diffusion](latent-diffusion.md) | Diffusion in an autoencoder latent | U-Net | Cross-attention |
| [DiT](../../../../models/transformer/dit/index.md) | Transformer denoiser on latent patches | Transformer | Time step and class label, through adaptive layer norm |
| [Classifier-free guidance](classifier-free-guidance.md) | Sampling-time combination of two predictions | Any | Guidance weight \(w\); \(w = 0\) gives the plain conditional model |

## Connections

- **Generative modelling:** diffusion is one of several generative algorithms, alongside autoregressive models, VAEs and GANs, described in [Generative Models](../generative-models/index.md).
- **Transformers:** the DiT backbone reuses the attention machinery in [Transformers & Attention](../../../../models/transformer/index.md).
- **Convolutional networks:** the U-Net backbone is built from the layers in [Convolutional Networks](../../../../models/cnn/index.md).
- **Brain and mind:** conditional diffusion models have been used to reconstruct images from fMRI recordings, as in MinD-Vis (Chen et al., 2023), described in [Brain-Computer Interfaces](../../../../../brain-mind/bci/index.md). For how the brain's own learning compares with these training objectives, see [NeuroAI](../../../../../brain-mind/neuroai/index.md).

## Applications

- **Text-to-image and editing:** latent diffusion models generate images from text, and the same framework supports inpainting and super-resolution (Rombach et al., 2022).
- **Video:** Ho et al. (2022) extend the image architecture to video and train jointly on image and video data.
- **Robot control:** Chi et al. (2023) represent a visuomotor policy as a conditional denoising diffusion process, and report gains over earlier robot learning methods on 15 tasks.
- **Brain decoding:** MinD-Vis (Chen et al., 2023) conditions a diffusion model on fMRI signals to reconstruct viewed images.

## Open questions

- How far can sampling be reduced to a single step without losing quality or diversity?
- Does the Transformer backbone scale better than the U-Net for video, and at what cost?
- How much of the benefit of guidance is a real improvement in the model, and how much is a trade-off that reduces diversity?

## References

### Seminal papers

- Sohl-Dickstein, J., Weiss, E. A., Maheswaranathan, N. & Ganguli, S. (2015). Deep Unsupervised Learning using Nonequilibrium Thermodynamics. ICML. https://arxiv.org/abs/1503.03585 — Defines a diffusion model as a gradual noising process with a learned reverse process.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — Simplifies training to noise prediction and shows high-quality image generation.
- Song, J., Meng, C. & Ermon, S. (2021). Denoising Diffusion Implicit Models. ICLR. https://arxiv.org/abs/2010.02502 — A non-Markovian sampler that reaches 1000-step quality in far fewer steps.
- Rombach, R. et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — Diffusion in autoencoder latent space with cross-attention conditioning.
- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV. https://arxiv.org/abs/2212.09748 — Replaces the U-Net with a Transformer and shows that FID improves with compute.
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — Guidance that combines conditional and unconditional predictions without an external classifier.
- Salimans, T. & Ho, J. (2022). Progressive Distillation for Fast Sampling of Diffusion Models. ICLR. https://arxiv.org/abs/2202.00512 — Distils a sampler into a model that takes half as many steps, applied repeatedly.
- Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M. & Fleet, D. J. (2022). Video Diffusion Models. NeurIPS. https://arxiv.org/abs/2204.03458 — Extends image diffusion to video and trains jointly on image and video data.
- Chi, C. et al. (2023). Diffusion Policy: Visuomotor Policy Learning via Action Diffusion. RSS. https://arxiv.org/abs/2303.04137 — Represents a robot policy as a conditional denoising diffusion process.
- Chen, Z. et al. (2023). Seeing Beyond the Brain: Conditional Diffusion Model with Sparse Masked Modeling for Vision Decoding. CVPR. https://arxiv.org/abs/2211.06956 — Conditions a diffusion model on fMRI signals to reconstruct viewed images.

### Surveys and textbooks

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Unifies diffusion and score-based models as stochastic differential equations.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Separates the design choices of diffusion models so each can be tuned on its own.

### Articles and documentation

- Rombach, R. et al. *latent-diffusion*, official code repository. https://github.com/CompVis/latent-diffusion — The authors' implementation of latent diffusion models and their experiments.

## Further learning

- Rogge, N. & Rasul, K., *The Annotated Diffusion Model*. Hugging Face blog. https://huggingface.co/blog/annotated-diffusion — Step-by-step code walk-through of DDPM, useful for checking the equations on this page.
