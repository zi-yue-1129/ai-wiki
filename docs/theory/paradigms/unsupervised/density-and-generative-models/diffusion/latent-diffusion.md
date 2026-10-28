---
status: complete
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

Latent diffusion runs the diffusion process in the compressed latent space of a pretrained autoencoder instead of on raw pixels. Rombach et al. (2022) also added cross-attention layers, so the same model can be conditioned on text, layouts and other inputs. The family-level picture is on the [Diffusion Models](index.md) page.

## Overview

Pixel-space diffusion spends most of its compute on fine detail that an autoencoder can represent compactly. Rombach et al. separate the two jobs. An autoencoder handles perceptual compression, and a diffusion model handles the generative modelling in the much smaller latent space. This makes training and sampling cheaper, and the paper's experiments show that the latent models also reach better sample quality on several tasks.

## Problem

Diffusion models in pixel space were state of the art on image synthesis, but they are expensive to train and sample, because every denoising step operates on the full-resolution image. Adding general conditioning inputs, such as text or layouts, was also not built into the approach. Rombach et al. ask how to keep the quality of pixel-space diffusion while cutting its cost and making conditioning flexible.

## Core idea

Train a perceptual autoencoder once to compress images into a latent \(z = E(x)\), then train a diffusion model on the latents. The denoiser contains cross-attention layers, so that the image features attend to an encoding of any condition. The paper studies several downsampling factors \(f\) and finds that moderate compression gives the best trade-off between efficiency and quality.

## Algorithm

Training has two stages. First the autoencoder \(E, D\) is trained, or reused, to compress images. Then a diffusion model is trained on latents with the noise-prediction loss:

\[
L_{\text{LDM}} = \mathbb{E}_{E(x),\epsilon,t,c}\big[\|\epsilon - \epsilon_\theta(z_t, t, \tau_\theta(c))\|^2\big]
\]

Here \(\tau_\theta(c)\) is the encoding of the condition \(c\). In each cross-attention layer the denoiser's intermediate features supply the queries \(Q\), and the encoded condition supplies the keys and values \(K\) and \(V\), so that the attention is \(\mathrm{softmax}(QK^\top/\sqrt d)\,V\). The encoder \(\tau_\theta\) and the denoiser are trained jointly. Sampling runs the reverse process in latent space, and the decoder \(D\) maps the final latent back to an image.

The autoencoder is regularised, either with a KL penalty or with vector quantisation. The paper's Table 8 reports that the regularised first stages (KL and VQ) give slightly worse results than their continuous counterparts, so the choice of regularisation affects sample quality as well as reconstruction.

## Results

- **Compression factor.** The paper trains models with \(f \in \{1, 2, 4, 8, 16, 32\}\), where \(f = 1\) is the pixel-space baseline. It concludes that LDM-4 and LDM-8 offer the best conditions for high-quality synthesis. Small factors train slowly, and large factors cap fidelity.
- **CelebA-HQ 256×256.** LDM-4, sampled with 500 DDIM steps, reaches FID 5.11, which the paper describes as a new state of the art, outperforming previous likelihood-based models and GANs.
- **Inpainting.** Compared with pixel-based diffusion, the latent models give a speed-up of at least 2.7× in training and sampling throughput, and improve FID by at least 1.6×.

## Limitations

- **Autoencoder limits.** The autoencoder's reconstruction error limits the detail the diffusion model can produce. The paper also notes that complex datasets such as ImageNet need less compression to avoid reducing quality.
- **Choice of factor.** The best \(f\) depends on the dataset, so the factor has to be tuned for each task.
- **Scope of comparisons.** The compute and throughput numbers come from the paper's own experiments on a single NVIDIA A100 with matched budgets, not from a general benchmark of every task.

## Connections

- The latent objective is the [DDPM](ddpm.md) objective applied to latents.
- Latent sampling in the paper uses the faster sampler in [DDIM](ddim.md).
- The later Transformer denoiser is [DiT](../../../../models/transformer/dit/index.md).
- Text conditioning relies on the guidance method in [classifier-free guidance](classifier-free-guidance.md).
- The denoiser's convolutional and attention layers are described in [Convolutional Networks](../../../../models/cnn/index.md) and [Transformers & Attention](../../../../models/transformer/index.md).

## Open questions

- How much reconstruction quality does the autoencoder lose, and does this limit fine text rendering or faces?
- How should the latent space be designed for video, where temporal consistency matters?

## References

### Seminal papers

- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. CVPR. https://arxiv.org/abs/2112.10752 — Introduces diffusion in an autoencoder latent space with cross-attention conditioning, and reports CelebA-HQ and inpainting results.
- Ho, J., Jain, A. & Abbeel, P. (2020). Denoising Diffusion Probabilistic Models. NeurIPS. https://arxiv.org/abs/2006.11239 — The pixel-space objective that latent diffusion applies to latents.
- Ho, J. & Salimans, T. (2022). Classifier-Free Diffusion Guidance. arXiv. https://arxiv.org/abs/2207.12598 — The guidance method the latent-diffusion text-to-image models use.

### Surveys and textbooks

- Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S. & Poole, B. (2021). Score-Based Generative Modeling through Stochastic Differential Equations. ICLR. https://arxiv.org/abs/2011.13456 — Gives the continuous-time view of diffusion models; latent models use the discrete noise-prediction form.
- Karras, T., Aittala, M., Aila, T. & Laine, S. (2022). Elucidating the Design Space of Diffusion-Based Generative Models. NeurIPS. https://arxiv.org/abs/2206.00364 — Separates the design choices of diffusion models, which apply to latent models as well.

### Articles and documentation

- Rombach, R. et al. *latent-diffusion*, official code repository. https://github.com/CompVis/latent-diffusion — The authors' implementation of the latent diffusion models and their experiments.
