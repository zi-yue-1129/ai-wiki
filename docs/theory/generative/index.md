---
related:
- applications/creative
- applications/life-science
- brain-mind/bci
---

# Generative Models

Generative models learn the data distribution \(p(x)\) and can **produce new samples**; discriminative models learn \(p(y\mid x)\).

Generative modelling is an **approach**, not an architecture. Any family in [Models](../models/index.md), such as convolutional, recurrent, Transformer or state-space networks, can be trained as a generative model. The families below are generative algorithms that differ in how they represent the distribution and how they sample from it.

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

![Animated illustration of diffusion sampling: an initially noisy grid gradually becomes a structured sample as denoising progresses.](../../assets/concept-animations/diffusion-denoising.gif)

*Animated concept diagram · Original illustration, CC BY-SA 4.0.*

**Reading the animation:** Sampling begins from noise and repeatedly applies a learned reverse-process update until a structured sample emerges. The pixel grid is a **conceptual illustration**, not a real model sample. During training, the forward process deliberately corrupts clean data with noise.

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

- Images, video, 3D, music, speech (see [Multimodal Models](../models/multimodal/index.md), [Art & Creativity](../../applications/creative/index.md))
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

## References

### Seminal papers

- Goodfellow, I. J., et al. (2014). *Generative Adversarial Networks*. arXiv. https://arxiv.org/abs/1406.2661 — Introduces GANs, where a generator and a discriminator are trained against each other.
- Kingma, D. P. & Welling, M. (2013). *Auto-Encoding Variational Bayes*. arXiv. https://arxiv.org/abs/1312.6114 — The variational autoencoder, a latent-variable model trained with a reparameterised variational bound.
- Ho, J., et al. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — Shows that learning to reverse a gradual noising process yields high-quality image generation.
- Rombach, R., et al. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. CVPR. https://arxiv.org/abs/2112.10752 — Runs diffusion in a compressed latent space, the approach behind Stable Diffusion.

### Surveys and textbooks

- Yang, L., et al. (2022). *Diffusion Models: A Comprehensive Survey of Methods and Applications*. arXiv. https://arxiv.org/abs/2209.00796 — A survey of diffusion methods and their uses across vision, audio and other domains.

### Articles and documentation

- Weng, L. (2021). *What are Diffusion Models?* Lil'Log. https://lilianweng.github.io/posts/2021-07-11-diffusion-models/ — A clear derivation of the diffusion training objective and its variants, with diagrams.
