---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/models/cnn
  - theory/paradigms/unsupervised/density-and-generative-models
  - brain-mind/neuroai
tags:
  - convolutional networks
  - segmentation
  - architecture
aliases:
  - U-Net
  - U 型網路
  - 編碼器–解碼器卷積網路
---

# U-Net

U-Net is a convolutional encoder–decoder with skip connections. It was designed for biomedical image segmentation, where labelled images are scarce and each output pixel needs both context and fine localisation. Its symmetric shape, with a contracting path that captures context and an expanding path that restores resolution, became the default backbone for dense prediction. It is also the usual denoiser in image diffusion models. The family overview is on the [Convolutional Networks](../index.md) page.

## Overview

Ronneberger, Fischer and Brox (2015) combined two ideas. Convolutional networks already captured context well at low resolution, and the expanding path recovers precise localisation by concatenating high-resolution features from the encoder. Together with heavy data augmentation, the architecture worked from very few annotated images. It won the 2015 ISBI cell-tracking challenge in two categories, and the paper reports that it outperformed the previous sliding-window approach on electron-microscopy segmentation.

## Key concepts

- **Contracting path**: repeated pairs of convolutions followed by pooling, which halve the resolution and double the number of channels.
- **Expanding path**: up-convolutions that double the resolution and halve the channels.
- **Skip connection**: concatenation of an encoder feature map with the decoder feature map at the same resolution, which passes fine detail across the bottleneck.
- **Overlap-tile strategy**: predicting a large image in overlapping tiles, so that every output pixel sees a full context window.
- **Weight map**: a per-pixel loss weight that emphasises thin separating borders between touching objects.

## How it works

The network is a symmetric U. Each level of the contracting path applies two unpadded 3×3 convolutions with ReLU, then a 2×2 max-pooling with stride two. At the bottom, the representation has the largest receptive field and the most channels. Each level of the expanding path applies a 2×2 up-convolution, concatenates the cropped encoder features from the same level, and applies two 3×3 convolutions with ReLU. A final 1×1 convolution produces the per-pixel class scores. The paper's version has 23 convolutional layers.

Training uses per-pixel cross-entropy with the weight map

\[
w(\mathbf{x}) = w_c(\mathbf{x}) + w_0 \exp\!\left(-\frac{(d_1(\mathbf{x}) + d_2(\mathbf{x}))^2}{2\sigma^2}\right)
\]

The paper sets \(w_0 = 10\) and \(\sigma \approx 5\) pixels. It uses stochastic gradient descent with a high momentum of 0.99, and a batch of one image. It augments the few training images with elastic deformations, which simulate natural tissue variation.

## Key methods

U-Net is the landmark architecture here. The main variant changes the design from two-dimensional to volumetric images, and it gets its own page as a follow-up.

- **U-Net (Ronneberger et al., 2015)**: the architecture described above, with skip connections for dense prediction.
- **3D U-Net (Çiçek et al., 2016)**: the same encoder–decoder design for volumetric images, trained from sparse annotations. Its own page is [3D U-Net](3d-unet.md).

### U-Net: Convolutional Networks for Biomedical Image Segmentation (Ronneberger et al., 2015)

- **Problem:** dense segmentation of biomedical images with only a few annotated examples, where neighbouring objects must be separated precisely.
- **Core idea:** a symmetric encoder–decoder in which skip connections carry high-resolution features to the decoder, combined with overlap-tile inference and elastic-deformation augmentation.
- **Equation or algorithm:** the architecture above. The loss is per-pixel cross-entropy with a weight map that boosts thin separating borders.
- **Results:** the abstract reports that the network trains end to end from very few images. On the ISBI electron-microscopy challenge, the paper's table reports a warping error of 0.000353 and a Rand error of 0.0382, against 0.000420 and 0.0504 for the sliding-window network of Ciresan et al. The network also won the ISBI 2015 cell-tracking challenge in the phase-contrast and DIC categories, and the abstract states that it segments a 512×512 image in less than a second on a recent GPU.
- **Limitations:** the paper's design is for two-dimensional images, and the overlap-tile scheme adds inference overhead. Padding choices matter, and the architecture is fixed in its depth, so very large or very small inputs need changes.

## Connections

- U-Net is the denoiser in most pixel-space image diffusion models. Dhariwal and Nichol (2021) used an improved U-Net, see [DDPM](../../../paradigms/unsupervised/density-and-generative-models/diffusion/ddpm.md), and the Transformer replacement is [DiT](../../transformer/dit/index.md) in the [Transformers](../../transformer/index.md) family.
- The U-shaped skip idea is a close relative of fully convolutional networks for dense prediction (Long et al., 2015), which the U-Net extends with a symmetric decoder.
- The encoder–decoder pattern appears in the [VAE](../../../paradigms/unsupervised/density-and-generative-models/vae/index.md), where the encoder and decoder play the same roles in a probabilistic model.
- Hierarchical processing with skip-like connections is a loose analogy to cortical pathways, see [NeuroAI](../../../../brain-mind/neuroai/index.md).

## Applications

Biomedical segmentation of cells, organelles and tissue; satellite and remote-sensing segmentation; the denoising backbone of image diffusion models; and dense prediction tasks such as depth and optical-flow estimation.

## Open questions

- Whether skip connections are the best way to combine scales, or whether attention and transformers replace them at scale.
- How much the U-shape matters once the network is trained on very large data.
- Generalising the design to three-dimensional and video data with limited memory.

## References

### Seminal papers

- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. MICCAI (arXiv). https://arxiv.org/abs/1505.04597 — Introduces the encoder–decoder architecture with skip connections, overlap-tile inference and weighted loss.
- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR (arXiv). https://arxiv.org/abs/1411.4038 — Shows that convolutional networks can be trained end to end for dense prediction, with skip connections between scales.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. arXiv. https://arxiv.org/abs/2006.11239 — Uses a U-Net with time-step conditioning as the denoiser for image diffusion.
- Dhariwal, P. & Nichol, A. (2021). *Diffusion Models Beat GANs on Image Synthesis*. arXiv. https://arxiv.org/abs/2105.05233 — Improves the U-Net denoiser used in diffusion models and reports that it surpasses GANs on image synthesis.
- Çiçek, Ö., Abdulkadir, A., Lienkamp, S. S., Brox, T. & Ronneberger, O. (2016). *3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation*. arXiv. https://arxiv.org/abs/1606.06650 — Extends the U-Net to volumetric data and trains it from sparsely annotated slices.
