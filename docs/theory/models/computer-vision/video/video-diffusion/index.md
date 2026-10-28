---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
tags:
  - diffusion models
  - generative models
  - computer vision
aliases:
  - Video Diffusion Models
  - 影片擴散模型
  - 視訊擴散模型
  - 影片生成
---

# Video Diffusion Models

A video diffusion model generates a clip by reversing a noising process over all of its frames at once. Ho et al. (2022) showed that the standard image diffusion formulation, with a three-dimensional U-Net as the denoiser, produces temporally coherent video, and that training on images and videos together helps. It is one of the methods on the [Video Understanding and Generation](../index.md) page.

## Overview

The [diffusion model](../../../../paradigms/unsupervised/density-and-generative-models/diffusion/index.md) recipe needs little change for video. A clip is one tensor, and the network learns to remove noise from it. The main difficulties are memory, since every frame passes through the network together, and coherence across frames. The paper argues that a natural extension of image architectures handles both.[^1]

## Key concepts

- **Space-time U-Net.** A [U-Net](../../segmentation/unet/index.md) whose blocks contain spatial layers and temporal attention, factorised so that space and time are handled separately.[^1]
- **Joint image–video training.** Independent images are appended to each video, with temporal attention masked so that they do not mix with the frames. The authors report that this reduces the variance of minibatch gradients.[^1]
- **Reconstruction guidance.** Conditioning sampling on known frames, to extend a clip in time or raise its resolution.

## How it works

The forward process adds Gaussian noise, $q(z_t \mid x) = \mathcal{N}(z_t;\,\alpha_t x,\ \sigma_t^2 I)$. The network $\hat x_\theta(z_t)$ recovers the clean clip, trained with a weighted mean squared error over uniformly sampled times:[^1]

$$
\mathcal{L}(\theta) = \mathbb{E}_{x,\,t}\left[\, w(\lambda_t)\,\lVert \hat x_\theta(z_t) - x\rVert_2^2 \,\right].
$$

Sampling starts from Gaussian noise and applies the learned denoiser step by step, with an ancestral sampler or a predictor–corrector sampler that adds Langevin steps.

Clips longer than the fixed frame count are made autoregressively: a second clip is sampled conditioned on the end of the first. The usual replacement method gave clips that did not match their context, so reconstruction guidance adjusts the denoising prediction instead.[^1]

## Results

The paper covers unconditional generation, video prediction and text conditioning.

- **UCF-101, unconditional, 16 frames at 64×64.** The model reaches a Fréchet Inception Distance (FID) of 295, computed with C3D features.[^2] The best 64×64 entry in the paper's table reaches 3431.[^1]
- **Robot-pushing video prediction.** The model reaches a Fréchet Video Distance (FVD) of 68.2 with 512 ancestral steps and 66.9 with 256 Langevin steps, against 86.9 and 103.3 for two earlier video models. FVD uses [I3D](../i3d/index.md) features.[^1]
- **Text-conditioned generation.** The paper trains on 10 million captioned videos and presents the first results on this task. Its evidence is largely qualitative.[^1]

## Limitations

- **Resolution.** The unconditional model works at 64×64, which the authors acknowledge may disadvantage it.[^1]
- **Fixed length and cost.** The base model makes a fixed number of frames, with hundreds of sampling steps.
- **Sensitive scores.** On a 600-class action benchmark, sampling test videos with replacement, as some earlier papers did, raised the paper's FVD from 16.2 to 16.9.[^1]

## Open questions

- Does the image recipe scale to long, high-resolution video? [Align your Latents](https://arxiv.org/abs/2304.08818) and [Stable Video Diffusion](https://arxiv.org/abs/2311.15127) denoise a compressed latent space to cut cost, and the latter stresses data curation.[^3]
- Is a U-Net or a Transformer the better denoiser for video? [Diffusion Transformers](https://arxiv.org/abs/2212.09748) replace the U-Net with a Transformer over latent patches for images, and video is less settled.[^4]

[^1]: Ho et al. (2022): the abstract, Sections 2 to 4, and Tables 1 to 3, including the sampling note in the video prediction section.
[^2]: Ho et al. (2022), Section 4.1: FID for UCF-101 is computed with C3D features, and FVD for video prediction with I3D features.
[^3]: Blattmann et al. (2023), both abstracts: temporal layers on latent image models, and the study of training stages and data curation.
[^4]: Peebles and Xie (2022): the Transformer denoiser operates on latent patches.

## References

### Seminal papers

- Ho, J., Salimans, T., Gritsenko, A., Chan, W., Norouzi, M. & Fleet, D. J. (2022). *Video Diffusion Models*. arXiv. https://arxiv.org/abs/2204.03458 — The first diffusion model for video, with a space-time U-Net.
- Carreira, J. & Zisserman, A. (2017). *Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset*. arXiv. https://arxiv.org/abs/1705.07750 — Introduces I3D, whose features underlie FVD.
- Tran, D., et al. (2014). *Learning Spatiotemporal Features with 3D Convolutional Networks*. arXiv. https://arxiv.org/abs/1412.0767 — The C3D network, whose features underlie FID here.
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — The action dataset used for unconditional training.
- Heusel, M., et al. (2017). *GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium*. arXiv. https://arxiv.org/abs/1706.08500 — Defines the Fréchet Inception Distance, the image-quality metric that later video metrics extend.
- Unterthiner, T., et al. (2018). *Towards Accurate Generative Models of Video: A New Metric & Challenges*. arXiv. https://arxiv.org/abs/1812.01717 — Introduces the Fréchet Video Distance, a metric for comparing generated and real video distributions.
- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. arXiv. https://arxiv.org/abs/1505.04597 — Encoder–decoder with skip connections, extended here to space-time.
- Blattmann, A., et al. (2023). *Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models*. arXiv. https://arxiv.org/abs/2304.08818 — Adds temporal layers to a latent image diffusion model.
- Blattmann, A., et al. (2023). *Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets*. arXiv. https://arxiv.org/abs/2311.15127 — Studies training stages and data curation.
- Peebles, W. & Xie, S. (2022). *Scalable Diffusion Models with Transformers*. arXiv. https://arxiv.org/abs/2212.09748 — Replaces the U-Net denoiser with a Transformer over latent patches.
