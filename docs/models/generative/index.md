---
related:
- applications/creative
- applications/life-science
- brain-mind/bci
---

# Generative Models

Generative models learn the data distribution \(p(x)\) and can **produce new samples**; discriminative models learn \(p(y\mid x)\).

## Families

| Family | Core idea | Pros | Cons | Examples |
|---|---|---|---|---|
| Autoregressive | \(p(x)=\prod_t p(x_t\mid x_{<t})\) | Exact likelihood, scales well | Sequential sampling | GPT, PixelCNN, WaveNet |
| VAE | Encode to a latent, decode; maximise the ELBO | Structured latent space | Blurrier samples | VAE, VQ-VAE |
| GAN | Generator vs discriminator | Sharp samples, fast sampling | Unstable, mode collapse | StyleGAN, BigGAN |
| Normalising flows | Invertible transforms | Exact likelihood | Architectural constraints | RealNVP, Glow |
| Diffusion | Learn to denoise step by step | High quality, stable, diverse | Many sampling steps (much improved) | DDPM, Stable Diffusion, Imagen |
| Flow matching | Learn a velocity field from noise to data | Simple training, fast sampling | — | Stable Diffusion 3, Flux |
| Energy-based | Learn an energy \(E(x)\) | Flexible | Sampling is hard | Hopfield nets, EBMs |

## Diffusion models

**Forward process**: gradually add Gaussian noise until data become pure noise.
**Reverse process**: train a network to predict the noise at each step; generate by denoising from pure noise.

Simplified objective:

\[
L = \mathbb{E}_{x_0,\epsilon,t}\big[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\big]
\]

Key techniques:

- **Latent diffusion**: diffuse in a VAE latent space, cutting cost dramatically (Stable Diffusion)
- **Classifier-free guidance**: trade off prompt adherence and diversity
- **Diffusion Transformers (DiT)**: Transformers replace U-Nets as the denoiser; widely used for video generation
- **Fast sampling**: DDIM, DPM-Solver, consistency models, distillation — from ~1000 steps to a few or one
- **Control**: ControlNet, LoRA, IP-Adapter

## Where they are used

- Images, video, 3D, music, speech (see [Multimodal Models](../multimodal/index.md), [Art & Creativity](../../applications/creative/index.md))
- Protein design (RFdiffusion), molecule and materials generation (see [Life Sciences](../../applications/life-science/index.md))
- Weather (GenCast produces probabilistic forecasts with diffusion)
- Robot policies (Diffusion Policy)
- Data augmentation and synthetic data

## Links to the brain

- **Perception as inference with a generative model**: Helmholtz's "unconscious inference" and predictive coding hold that the brain uses an internal generative model to predict and explain its sensory input
- **The Helmholtz machine and wake–sleep algorithm** (Hinton et al., 1995): generative-model training inspired by sleep
- **Dreaming and imagination**: one hypothesis treats dreams as offline samples from the brain's generative model that aid generalisation (Hoel, 2021, "overfitted brain hypothesis")
- **Reconstructing images from fMRI** with diffusion models (Takagi & Nishimoto, 2023) — see [Brain-Computer Interfaces](../../brain-mind/bci/index.md)

## Resources

- Lilian Weng, "What are Diffusion Models?"
- Hugging Face Diffusion Models Course
- Stanford CS236, *Deep Generative Models*
- Yang Song, "Generative Modeling by Estimating Gradients of the Data Distribution"
- *Understanding Deep Learning*, chapters 14–18
