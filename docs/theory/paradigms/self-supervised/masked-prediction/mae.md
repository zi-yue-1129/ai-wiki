---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/contrastive-learning
  - theory/models/transformer/vision-transformer
  - theory/models/cnn
tags:
  - self-supervised learning
  - masked modelling
  - vision transformer
aliases:
  - MAE
  - Masked Autoencoders
  - 遮罩自編碼器
---

# MAE: Masked Autoencoders Are Scalable Vision Learners

Masked autoencoders (MAE) pre-train a vision transformer by hiding most of an image and reconstructing the hidden patches. The encoder processes only the visible patches, which makes training fast, and a small decoder fills in the rest. The family-level picture is on the [Masked Prediction](index.md) page.

## Overview

He et al. (2022) show that BERT-style masked prediction works for images when the masked fraction is large. The abstract says the approach trains "3× or more" faster and improves accuracy. The abstract's 87.8% fine-tuning accuracy is for a vanilla ViT-Huge pre-trained only on ImageNet-1K and fine-tuned at 448 input size. The same model reaches 86.9% at 224 input. The abstract describes the 87.8% result as the best accuracy among methods that use only ImageNet-1K data.

## Key concepts

- **Patches and masking**: the image is split into square patches, and a random 75% of them are removed. Figure 5 of the paper, a masking-ratio study, supports 75% as a good default for image data.
- **Asymmetric encoder–decoder**: the encoder sees only the visible patches, with no mask tokens. The decoder receives the encoded visible patches together with mask tokens, and reconstructs the whole image.
- **Lightweight decoder**: the default decoder has 8 Transformer blocks with width 512, which is smaller than the encoder. It is used only during pre-training.
- **Reconstruction target**: pixel values. The paper reports that normalised pixel targets improve representation quality over raw pixels.
- **Loss on masked patches**: mean squared error, computed only on the masked patches, as in BERT.

## How it works

1. Split the image into patches and embed them, as in a vision transformer.
2. Keep a random subset of the patches (25%) and drop the rest.
3. Encode only the kept patches with a vision transformer encoder.
4. Add mask tokens at the dropped positions, and let the lightweight decoder reconstruct the pixels of all patches.
5. Compute the mean squared error on the masked patches only.
6. After pre-training, discard the decoder and feed the complete, unmasked image to the encoder for recognition tasks.

Because the encoder runs on the 25% of patches that are visible, pre-training is much cheaper than encoding every patch. The paper's timing experiment measures a 2.8× wall-clock speedup for ViT-L, which is below the "3× or more" that the abstract reports.

### Visual walkthrough: visible-only encoding and masked reconstruction

![MAE animation: retain four of sixteen patches, encode only the visible tokens, restore mask tokens in the decoder, and score the masked reconstruction.](../../../../assets/concept-animations/mae-visible-patch-reconstruction-motion.svg)

[Static four-stage overview for GitHub](../../../../assets/concept-animations/mae-visible-patch-reconstruction-still.svg)

The **mask → encode → decode → masked loss** sequence uses a schematic 4 × 4 image with **12 of 16 patches masked (75%)**. The encoder receives only four visible tokens; the decoder then combines their encoded representations with twelve mask tokens to predict all patch pixels. **Only the twelve originally masked positions contribute to reconstruction MSE**, although the decoder outputs all sixteen. Patch colours and reconstructions are illustrative, **not model outputs or benchmark measurements**.

On the MkDocs site, use **Play/Pause** to stop the eight-second loop. GitHub Markdown and reduced-motion settings have a static four-stage fallback. This original visual is licensed **CC BY-SA 4.0** and illustrates He et al. (2022), cited in References.

## Key methods

### Masked Autoencoders Are Scalable Vision Learners (He, Chen, Xie, Li, Dollár & Girshick, 2022)

- **Problem:** BERT's masked-language approach had worked for text. The question was whether a similar masked objective could train large vision transformers efficiently. Images contain much spatial redundancy, so a small masked fraction can often be filled in from neighbouring patches.
- **Core idea:** mask a high fraction of random patches, encode only the visible ones, and decode pixels from the encoded visible patches plus mask tokens.
- **Equation or algorithm:** mean squared error on the masked patches only, a 75% masking ratio, an asymmetric encoder and an 8-block, width-512 decoder, and normalised pixel targets, as in the six steps above.
- **Results:** fine-tuning a ViT-L pre-trained with MAE on ImageNet-1K gives 85.9% top-1 accuracy at 224 input. A ViT-H at 448 input gives 87.8%, and the same ViT-H at 224 input gives 86.9%. In the paper's ablation for ViT-L on ImageNet-1K, normalised pixel targets raise fine-tuning accuracy from 84.9% to 85.4%, and linear probing from 73.5% to 73.9%. In the paper's timing experiment, leaving mask tokens out of the encoder gives a 2.8× wall-clock speedup for ViT-L.
- **Limitations:** linear probing lags far behind fine-tuning (73.9% against 85.4% in the ViT-L ablation with normalised pixel targets), so the features depend heavily on fine-tuning. The decoder is an extra design choice that needs tuning, and the 75% masking ratio was tuned on image data.

## Connections

- The masked-language origin of the approach is described on the [Masked Prediction](index.md) page, which also covers BERT and other masked models.
- The encoder is a [vision transformer](../../../models/transformer/vision-transformer/index.md), so MAE pre-trains the same architecture used for supervised image classification.
- [Contrastive learning](../contrastive-learning/index.md) is the alternative route: it matches views rather than reconstructing content. [SimCLR](../contrastive-learning/simclr.md) is the reference example, and [MoCo](../contrastive-learning/moco.md) uses a queue of negatives.
- [DINOv2](../non-contrastive-methods/dinov2.md) also uses a masked patch objective, combined with self-distillation, and scales it to a curated dataset.
- MAE's reconstruction objective is a masked form of the denoising idea in [autoencoders and representations](../../unsupervised/autoencoders-and-representations/index.md).
- Image models more broadly are covered under [computer vision](../../../models/computer-vision/index.md).
- The gap between linear probing and fine-tuning is part of the wider discussion of [theory and evaluation](../theory-and-evaluation/index.md).

## Open questions

- Is pixel regression the best reconstruction target? Predicting features or tokens instead of pixels is a natural alternative, and parallel methods such as [BEiT](https://arxiv.org/abs/2106.08254) and [SimMIM](https://arxiv.org/abs/2111.09886) explore it.
- How does the best masking ratio change with image resolution, model size and data type? The paper's 75% setting comes from its own image experiments.
- Can the representation be made more linearly separable without the cost of fine-tuning?

## References

### Seminal papers

- He, K., Chen, X., Xie, S., Li, Y., Dollár, P. & Girshick, R. (2022). Masked Autoencoders Are Scalable Vision Learners. CVPR. https://arxiv.org/abs/2111.06377 — The paper described on this page.
- Devlin, J., Chang, M.-W., Lee, K. & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. NAACL-HLT. https://arxiv.org/abs/1810.04805 — Masked-language pre-training, whose loss-on-masked-positions design MAE follows.
- Dosovitskiy, A. et al. (2021). An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale. ICLR. https://arxiv.org/abs/2010.11929 — The vision transformer architecture that MAE pre-trains.
- Bao, H. et al. (2022). BEiT: BERT Pre-Training of Image Transformers. ICLR. https://arxiv.org/abs/2106.08254 — A parallel masked image modelling method for vision transformers.
- Xie, Z. et al. (2022). SimMIM: A Simple Framework for Masked Image Modeling. CVPR. https://arxiv.org/abs/2111.09886 — A masked image modelling framework with a simpler design, developed in parallel with MAE.
- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). Momentum Contrast for Unsupervised Visual Representation Learning. CVPR. https://arxiv.org/abs/1911.05722 — The contrastive alternative that MAE is compared against in the self-supervised literature.
- Oquab, M. et al. (2023). DINOv2: Learning Robust Visual Features without Supervision. arXiv:2304.07193. https://arxiv.org/abs/2304.07193 — Combines a masked patch objective with self-distillation at larger scale.

### Surveys and textbooks

- Balestriero, R. et al. (2023). A Cookbook of Self-Supervised Learning. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — Practical survey of self-supervised design choices, including masked modelling.
