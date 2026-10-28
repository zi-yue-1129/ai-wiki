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

Pixel-space diffusion spends most of its compute on fine detail that an autoencoder can represent compactly. Rombach et al. separate the two jobs. An autoencoder handles perceptual compression, and a diffusion model handles the generative modelling in the much smaller latent space. Their experiments show that latent models reach better FID than pixel-based diffusion at a lower training and sampling cost (see Results below).

## Key concepts

- **Perceptual autoencoder**: an encoder \(E\) and decoder \(D\) trained to reconstruct images while keeping the latent space compact.
- **Latent**: \(z = E(x)\), the representation the diffusion model works on. The DDPM objective is applied to \(z\).
- **Cross-attention conditioning**: layers in the denoiser where image features attend to an encoding of the condition, such as text tokens.
- **Downsampling factor** \(f\): how much smaller the latent is than the image. The paper studies \(f\in\{1,2,4,8,16,32\}\), and \(f=1\) is the pixel-based baseline.

## How it works

Training has two steps. First the autoencoder is trained, or reused, to compress images. Then a diffusion model is trained on latents with the usual noise-prediction loss:

\[
L_{\text{LDM}} = \mathbb{E}_{E(x),\epsilon,t,c}\big[\|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|^2\big]
\]

Here \(\tau_\theta(c)\) is the encoding of the condition \(c\). In each cross-attention layer the denoiser's intermediate features supply the queries \(Q\), and the encoded condition supplies the keys and values \(K\) and \(V\), so the attention is \(\mathrm{softmax}(QK^\top/\sqrt d)\,V\). The encoder \(\tau_\theta\) and the denoiser are trained jointly. Sampling runs the reverse process in latent space, and the decoder \(D\) maps the final latent back to an image.

## Key methods

### High-Resolution Image Synthesis with Latent Diffusion Models (Rombach et al., 2022)

- **Problem:** pixel-space diffusion models are expensive to train and sample, and general conditioning inputs are hard to add.
- **Core idea:** train the diffusion model in the latent space of a pretrained autoencoder, and add cross-attention layers so it can be conditioned on text, layouts or other inputs.
- **Equation or algorithm:** the latent loss above, with the denoiser's intermediate features attended to by the condition encoding.
- **Results:** on CelebA-HQ at 256×256, LDM-4 reaches FID 5.11, which the paper reports as a new state of the art over prior likelihood-based models and GANs. In the inpainting study, latent models give at least a 2.7× speed-up in training and sampling throughput over pixel-based diffusion, and improve FID by at least 1.6×. The paper finds that LDM-4 and LDM-8 give the best balance of efficiency and quality. Small factors train slowly, and large factors cap fidelity.
- **Limitations:** the autoencoder limits the fine detail that can be reconstructed, so very small features such as text can be lost. The compute figures above come from the paper's inpainting study, not from a general benchmark of every task.

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
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — The guidance method used for text conditioning in the latent-diffusion family.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Gives the continuous-time view of the noise-prediction objective used on latents.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Discusses design choices that carry over to latent diffusion models.

### Articles and documentation

- Rombach, R. et al., *Stable Diffusion* public release code repository. https://github.com/CompVis/stable-diffusion — The official reference implementation of latent diffusion with text conditioning.
