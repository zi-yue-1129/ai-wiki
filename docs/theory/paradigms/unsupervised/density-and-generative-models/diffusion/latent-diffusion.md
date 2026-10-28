---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/models/transformer
tags:
  - diffusion models
  - latent diffusion
aliases:
  - 潛在擴散模型
  - Latent diffusion
  - LDM
  - Stable Diffusion
---

# Latent Diffusion Models

Latent diffusion runs the diffusion process in the compressed latent space of a pretrained autoencoder instead of on raw pixels. Rombach et al. (2022) also added cross-attention so the same model can be conditioned on text and other inputs. This design is the basis of the Stable Diffusion family. The family-level picture is on the [Diffusion Models](index.md) page.

## Overview

Pixel-space diffusion spends most of its compute on fine detail that an autoencoder can represent compactly. Rombach et al. separate the two jobs. An autoencoder handles perceptual compression, and a diffusion model handles the generative modelling in the much smaller latent space. The authors describe pixel-space diffusion as often needing hundreds of GPU days.

## Key concepts

- **Perceptual autoencoder**: an encoder \(E\) and decoder \(D\) trained to reconstruct images while keeping the latent space compact.
- **Latent**: \(z = E(x)\), the representation the diffusion model works on. The DDPM objective is applied to \(z\).
- **Cross-attention conditioning**: layers in the denoiser where image features attend to an encoding of the condition, such as text tokens.
- **Downsampling factor**: how much smaller the latent is than the image. The choice trades reconstruction quality against compute.

## How it works

Training has two steps. First the autoencoder is trained, or reused, to compress images. Then a diffusion model is trained on latents with the usual noise-prediction loss:

\[
L_{\text{LDM}} = \mathbb{E}_{E(x),\epsilon,t,c}\big[\|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|^2\big]
\]

Here \(\tau_\theta(c)\) is the encoding of the condition \(c\), and the denoiser attends to it through cross-attention. Sampling runs the reverse process in latent space, and the decoder \(D\) maps the final latent back to an image.

## Key methods

### High-Resolution Image Synthesis with Latent Diffusion Models (Rombach et al., 2021/2022)

- **Problem:** pixel-space diffusion models are expensive to train and sample, and general conditioning inputs are hard to add.
- **Core idea:** train the diffusion model in the latent space of a pretrained autoencoder, and add cross-attention layers so it can be conditioned on text, layouts or other inputs.
- **Equation or algorithm:** the latent loss above, with the denoiser's intermediate features attended to by the condition encoding.
- **Results:** the abstract reports state-of-the-art synthesis on image data, a new state of the art for image inpainting, and competitive results on unconditional generation, semantic scene synthesis and super-resolution, at lower computational cost than pixel-space models. It gives no benchmark numbers in the abstract.
- **Limitations:** the autoencoder limits the fine detail that can be reconstructed. The abstract does not quantify the compute saving; the paper's body does.

## Connections

- The latent objective is the [DDPM](ddpm.md) objective applied to latents.
- Latent sampling typically uses the faster sampler in [DDIM](ddim.md).
- The later Transformer denoiser is [DiT](../../../../models/transformer/dit/index.md).
- Text conditioning relies on the guidance method in [classifier-free guidance](classifier-free-guidance.md).
- The denoiser's convolutional and attention layers are described in [Convolutional Networks](../../../../models/cnn/index.md) and [Transformers & Attention](../../../../models/transformer/index.md).

## Open questions

- How much reconstruction quality is lost by the autoencoder, and does this limit fine text rendering or faces?
- How should the latent space be designed for video, where temporal consistency matters?

## References

### Seminal papers

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — Introduces diffusion in an autoencoder latent space with cross-attention conditioning.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The pixel-space objective that latent diffusion applies to latents.
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598 — The guidance method used for text conditioning in the latent-diffusion family.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Gives the continuous-time view of the noise-prediction objective used on latents.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Discusses design choices that carry over to latent diffusion models.

### Articles and documentation

- Rombach, R. et al., *Stable Diffusion* public release code repository. https://github.com/CompVis/stable-diffusion — The official reference implementation of latent diffusion with text conditioning.
