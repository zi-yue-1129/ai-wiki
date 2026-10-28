---
status: complete
last_reviewed: 2026-10-28
related:
- theory/paradigms/unsupervised/density-and-generative-models
- brain-mind/neuroimaging-methods
tags:
- neuroscience
- brain-computer interface
- generative models
aliases:
  - fMRI 影像重建
  - Image reconstruction from fMRI
  - Takagi and Nishimoto
---

# Reconstructing viewed images from fMRI (Takagi & Nishimoto, 2023)

This method reconstructs an image that a person is looking at from their functional MRI (fMRI) activity. It maps the fMRI pattern into the latent space of a pretrained image generator, a latent diffusion model, and then generates an image from that latent representation. The output resembles the viewed image in content and layout, which shows that the generator's representation can be linked to brain activity.

This page is part of [Brain-Computer Interfaces & Neural Decoding](../index.md). It covers one decoding method in detail.

## Overview

fMRI measures blood-oxygen changes that follow neural activity, and it is the usual tool for non-invasive brain imaging. Earlier work could identify which of a set of known images a person was viewing, but not produce a new image from brain activity. Takagi and Nishimoto asked whether a generative image model could act as a bridge: the brain pattern would be read into the generator's latent space, and the generator would draw the image.

## Key concepts

- **fMRI pattern**: the spatial pattern of blood-oxygen signals across visual cortex during viewing, used as the input to the decoder.
- **Latent diffusion model**: a generator that produces images by denoising in a compressed latent space, which keeps generation tractable.
- **Linear mapping**: a regression from fMRI features to the generator's latent representation, fitted separately for each person.
- **Text conditioning**: a textual or semantic description, derived from the brain pattern, that guides the generator toward the right content.

## Problem

Can the content of a viewed image be recovered from fMRI well enough to produce a new image that matches it? The difficulty is that fMRI has low spatial and temporal resolution, and the number of images in a dataset is small compared with the number of possible images. A generator that already knows the space of natural images supplies the prior that makes the problem tractable.

## Core idea

Train a mapping from the fMRI activity recorded while a person viewed images to two representations of those images: a semantic embedding, which captures what is in the picture, and a low-level latent, which captures layout and texture. At test time, the mapped representations condition a pretrained latent diffusion model, which generates the reconstruction. The generator contributes the image statistics, and the fMRI contributes the content.

## Method

1. Record fMRI responses in visual cortex while a participant views many natural images.
2. Encode each viewed image with the generator's own encoders, to obtain target latent and semantic representations.
3. Fit a regression from the fMRI features to these representations, separately for each participant.
4. For a new fMRI pattern, predict the representations and condition the latent diffusion model on them to generate an image.

## Results

The paper reports reconstructions that resemble the viewed images in content and general layout, and it compares them with earlier reconstruction methods, which produced blurrier or less specific images. The evaluation uses held-out images, so the reconstructions are not recalled from the training set. The paper's quantitative scores should be read from the paper.

## Limitations

- **Reconstructions can be plausible without being accurate.** A generator produces realistic images, and some details may come from its prior rather than from the brain signal.
- **Per-person training.** The mapping is fitted separately for each participant, and needs a large amount of scanning time.
- **Viewed images, not imagined ones.** The method reconstructs what a person is seeing, not thoughts or dreams, and it does not read private mental content.

## Connections

- **Neuroimaging methods**: the fMRI signal and its limits are covered on [Neuroimaging Methods](../../neuroimaging-methods/index.md), including [BOLD fMRI](../../neuroimaging-methods/bold-fmri/index.md).
- **Generative models**: the generator is a latent diffusion model, covered in the density and generative-model section of [Theory](../../../theory/paradigms/unsupervised/density-and-generative-models/index.md).
- **Parent topic**: [Brain-Computer Interfaces & Neural Decoding](../index.md), which covers the invasive decoders and the ethics of decoding.

## Applications

- **Basic research**: reconstructions show what information about a viewed image is present in visual cortex.
- **Clinical communication**: decoding of perception is studied as a possible aid for people who cannot speak or move, though this is still at the research stage.

## Open questions

- **How much of the output comes from the generator's prior?** Separating what the brain signal contributes from what the generator adds is the central validity question.
- **Does the method work for imagery and for people with different brain structure?** Generalisation beyond viewing and beyond the scanned participants is not established.
- **What are the privacy limits?** Decoding perception raises questions about consent and about what decoding systems can reveal, which are discussed in the parent topic.

## References

### Seminal papers

- Takagi, Y. & Nishimoto, S. (2023). High-resolution image reconstruction with latent diffusion models from human brain activity. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*. https://doi.org/10.1109/CVPR52729.2023.01389 — Maps fMRI activity into the latent space of a diffusion model, which generates reconstructions of viewed images.
- Rombach, R., Blattmann, A., Lorenz, D., Esser, P. & Ommer, B. (2022). High-Resolution Image Synthesis with Latent Diffusion Models. *CVPR*. https://arxiv.org/abs/2112.10752 — The latent diffusion model used as the generator.
- Kay, K. N., Naselaris, T., Prenger, R. J. & Gallant, J. L. (2008). Identifying natural images from human brain activity. *Nature*. https://doi.org/10.1038/nature06713 — Identifies which natural image a person is viewing from fMRI, an earlier step toward reconstruction.
- Nishimoto, S., Vu, A. T., Naselaris, T., Benjamini, Y., Yu, B. & Gallant, J. L. (2011). Reconstructing visual experiences from brain activity evoked by natural movies. *Current Biology*. https://doi.org/10.1016/j.cub.2011.08.031 — Reconstructs natural movies from fMRI using a learned encoding model.

### Surveys and reviews

- Naselaris, T., Kay, K. N., Nishimoto, S. & Gallant, J. L. (2011). Encoding and decoding in fMRI. *NeuroImage*. https://doi.org/10.1016/j.neuroimage.2010.05.051 — A review of the encoding and decoding framework that these reconstruction methods use.
