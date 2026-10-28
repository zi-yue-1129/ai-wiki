---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/healthcare
  - theory/paradigms/unsupervised/density-and-generative-models/diffusion
tags:
  - computer vision
  - convolutional networks
  - diffusion models
aliases:
  - U-Net
  - U 型網路
  - U-Net architecture
---

# U-Net

U-Net is an encoder–decoder convolutional network for segmenting biomedical images. A contracting path captures context, a symmetric expanding path recovers precise localisation, and skip connections carry high-resolution features across. It was designed to work from very few annotated images, and it became a widely used baseline in medical imaging and, later, the denoiser of many diffusion models. It is one of the four landmark methods on the [Image Segmentation](../index.md) page.

## Overview

Biomedical segmentation has two constraints that natural-image benchmarks lack. Annotated training data are scarce, because an expert must trace every cell or organ, and the outputs must localise boundaries precisely. Ronneberger, Fischer and Brox designed a network that uses the available images more efficiently, through strong data augmentation and a training loss that gives extra weight to pixels between touching cells.[^1] The paper's first experiments used electron microscopy images of neuronal structures from the ISBI 2012 challenge, where the training set consisted of 30 images of 512×512 pixels.

## Key concepts

- **Contracting path**: repeated pairs of unpadded 3×3 convolutions, each followed by a ReLU, then a 2×2 max pooling with stride 2. The number of feature channels doubles at each step.
- **Expanding path**: each step upsamples the feature map with a 2×2 up-convolution, which halves the channels, concatenates the cropped feature map from the contracting path, and applies two 3×3 convolutions.
- **Skip connections by concatenation**: the encoder features are joined to the decoder features along the channel axis, so the decoder receives fine detail directly.
- **Overlap-tile strategy**: the image is predicted tile by tile, with missing context at the border filled in by mirroring the input. This keeps arbitrarily large images in use.
- **Weight map**: a per-pixel loss weight that balances class frequencies and emphasises the thin borders between touching cells.

## How it works

The network has 23 convolutional layers in total and ends with a 1×1 convolution that maps each feature vector to the number of classes. Because the convolutions are unpadded, the output is smaller than the input, and the input tile size must be chosen so that every pooling step acts on an even size.

Training minimises a weighted cross-entropy over the pixels:

$$
E = -\sum_{x \in \Omega} w(x) \log p_{\ell(x)}(x)
$$

Here \(\ell(x)\) is the true label and \(p_k(x)\) the softmax output. The weight map is

$$
w(x) = w_c(x) + w_0 \exp\left(-\frac{(d_1(x) + d_2(x))^2}{2\sigma^2}\right)
$$

where \(w_c\) balances class frequencies, \(d_1\) and \(d_2\) are the distances to the nearest and second-nearest cell borders, and the paper sets \(w_0 = 10\) and \(\sigma \approx 5\) pixels. The paper also uses random elastic deformations of the training images as augmentation, and initialises the weights from a Gaussian scaled so that each feature map has roughly unit variance.

## Results

On the ISBI 2012 electron microscopy challenge, the network, averaged over seven rotated versions of the input, reached a warping error of 0.0003529 and a Rand error of 0.0382, with no pre- or post-processing. The previous best submission, a sliding-window convolutional network, had 0.000420 and 0.0504.[^2] On the ISBI cell tracking challenge, the paper reports an average intersection over union of 92% on phase-contrast images of U373 cells, against 83% for the second-best entry, and 77.5% on DIC images of HeLa cells, against 46%. The abstract also reports winning the 2015 cell tracking challenge categories by a large margin, and segmentation of a 512×512 image in under a second on a recent GPU.

## Limitations

- **Heavy reliance on augmentation.** The result depends on elastic deformations and on the weight map, and the paper reports the combined recipe rather than a study of each choice alone.
- **Two-dimensional design.** The network operates on 2D slices. Volumetric data such as CT or MRI need a different design, which the paper does not address.
- **Small benchmarks.** The experiments use a few dozen images per dataset. The results show that the design works in that regime, not how it scales with data.
- **Border effects.** The unpadded convolutions and the tiling strategy add bookkeeping, and predictions near image edges rely on mirrored context.

## Open questions

- How much of U-Net's success comes from the skip-connected architecture, and how much from its training recipe? Later work on medical segmentation often reports both together.
- Whether attention or Transformer blocks can replace the convolutional path without losing data efficiency. The question is open.

[^1]: Ronneberger et al. (2015), introduction and experiments: the design targets biomedical images with few annotated samples, using augmentation and a weighted loss.
[^2]: Ronneberger et al. (2015), Experiments section and Table 1 of the paper, ranking on the EM segmentation challenge as of March 2015.

## References

### Seminal papers

- Ronneberger, O., Fischer, P. & Brox, T. (2015). *U-Net: Convolutional Networks for Biomedical Image Segmentation*. MICCAI. https://doi.org/10.1007/978-3-319-24574-4_28 — The paper itself: a contracting and expanding path with skip connections, trained from few images.
- Long, J., Shelhamer, E. & Darrell, T. (2015). *Fully Convolutional Networks for Semantic Segmentation*. CVPR. https://arxiv.org/abs/1411.4038 — The fully convolutional segmenter whose skip fusion U-Net replaces with concatenation.
- Ho, J., Jain, A. & Abbeel, P. (2020). *Denoising Diffusion Probabilistic Models*. NeurIPS. https://arxiv.org/abs/2006.11239 — Uses a U-Net backbone, with time-step conditioning, as the denoiser of a diffusion model.
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). *High-Resolution Image Synthesis with Latent Diffusion Models*. CVPR. https://arxiv.org/abs/2112.10752 — Runs the denoiser in an autoencoder's latent space, with cross-attention for conditioning.
- Minaee, S., Boykov, Y., Porikli, F., Plaza, A., Kehtarnavaz, N. & Terzopoulos, D. (2021). *Image Segmentation Using Deep Learning: A Survey*. IEEE TPAMI. https://doi.org/10.1109/TPAMI.2021.3059968 — Places encoder–decoder networks such as U-Net among the main families of deep segmentation models.
