---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
tags:
  - diffusion models
  - transformers
aliases:
  - 擴散 Transformer
  - DiT
  - Diffusion Transformer
  - Scalable diffusion models with transformers
---

# DiT: Diffusion Transformers

DiT, or Diffusion Transformer, is a diffusion denoiser that replaces the U-Net with a Transformer operating on patches of a latent image. Peebles and Xie (2022) showed that its quality improves steadily with more compute, in the same way language-model quality does. The family-level picture is on the [Diffusion Models](../../../paradigms/unsupervised/density-and-generative-models/diffusion/index.md) page, and the attention machinery is described in [Transformers & Attention](../index.md).

## Overview

Earlier latent diffusion models used a convolutional U-Net as the denoiser. Its design choices, such as skip connections and multi-resolution blocks, were hand-crafted. Peebles and Xie asked whether a plain Transformer, with the design choices that work for language and vision, could serve as the denoiser and scale predictably. The answer is yes, with the caveat that the benchmark is class-conditional image generation.

## Key concepts

- **Patchify**: the latent of size \(I \times I \times C\) is split into patches of size \(p \times p\), and each patch is linearly embedded as a token. Smaller \(p\) gives more tokens and more compute.
- **Adaptive layer norm (adaLN)**: the time-step and class embeddings produce scale and shift parameters that modulate each Transformer block.
- **Gflops**: the forward-pass compute, used as the x-axis when comparing model sizes.
- **Model variants**: named sizes such as DiT-S, DiT-B, DiT-L and DiT-XL, combined with a patch size, for example DiT-XL/2.

## How it works

For a latent \(z_t\) at time step \(t\) with class label \(c\), the model predicts the noise, and for some configurations also the variance, from the patch tokens:

\[
\epsilon_\theta(z_t, t, c) = \mathrm{DiT}\big(\mathrm{patchify}(z_t);\ \mathrm{emb}(t) + \mathrm{emb}(c)\big)
\]

Training uses the same noise-prediction loss as [DDPM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md), applied to latents. Scaling is studied by varying depth, width and patch size, which changes Gflops, and measuring FID at each point.

## Key methods

### Scalable Diffusion Models with Transformers (Peebles & Xie, 2022/2023)

- **Problem:** the U-Net denoiser is hand-designed, and it was unclear whether diffusion quality scales with compute as Transformer language models do.
- **Core idea:** replace the U-Net in latent diffusion with a Transformer over latent patches, and measure quality against forward-pass compute in Gflops.
- **Equation or algorithm:** the patchify and adaLN conditioning above, trained with the latent noise-prediction loss.
- **Results:** the abstract reports that larger models, with more Gflops from depth, width or more tokens, consistently have lower FID. The largest model, DiT-XL/2, reaches an FID of 2.27 on class-conditional ImageNet at 256×256, outperforming earlier diffusion models. It gives no FID for 512×512 in the abstract.
- **Limitations:** results are on class-conditional ImageNet, a narrower benchmark than text-to-image. The abstract gives no training-compute figures.

## Connections

- DiT uses the latent setting of [Latent Diffusion](../../../paradigms/unsupervised/density-and-generative-models/diffusion/latent-diffusion.md) and replaces its U-Net denoiser.
- The attention blocks are those described in [Transformers & Attention](../index.md).
- DiT models can be sampled with the faster [DDIM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddim.md) updates.

## Open questions

- Does the compute-to-quality scaling hold for text-to-image and video at comparable cost?
- Is the patch size the best way to trade detail against compute for high-resolution images?

## References

### Seminal papers

- Peebles, W. & Xie, S. (2023). Scalable Diffusion Models with Transformers. ICCV 2023. [DOI 10.1109/ICCV51070.2023.00387](https://doi.org/10.1109/ICCV51070.2023.00387). Also [arXiv:2212.09748](https://arxiv.org/abs/2212.09748) — Introduces DiT and reports FID improving with Gflops.
- Rombach, R. et al. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — The latent diffusion setting in which DiT replaces the U-Net.
- Vaswani, A. et al. (2017). Attention Is All You Need. NeurIPS. https://arxiv.org/abs/1706.03762 — The Transformer architecture that DiT reuses as its denoiser.

### Surveys and textbooks

- Song, Y. et al. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Gives the continuous-time background to the noise-prediction objective DiT is trained with.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Discusses preconditioning and design choices that apply to DiT training.

### Articles and documentation

- Peebles, W., *DiT* official code repository. https://github.com/facebookresearch/DiT — The authors' reference implementation of the Diffusion Transformer models and training code.
