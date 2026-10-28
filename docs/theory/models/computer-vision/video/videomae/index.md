---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/models/transformer
  - theory/paradigms/self-supervised
tags:
  - computer vision
  - transformers
  - self-supervised learning
aliases:
  - VideoMAE
  - 影片遮罩自編碼器
  - 視訊遮罩自編碼器
  - Video masked autoencoder
---

# VideoMAE

VideoMAE is a masked autoencoder for video. It hides about 90% of the spacetime cubes in a clip and trains a plain Vision Transformer to reconstruct them. Tong et al. (2022) showed that this pre-training works on video datasets alone, without image weights or extra data. It is one of the methods on the [Video Understanding and Generation](../index.md) page.

## Overview

Video Transformers have usually been built on image models. A plain Vision Transformer trained from scratch on a video dataset performs poorly, so the usual remedy is image pre-training.[^1] VideoMAE asks whether the video data itself is enough. It adapts the [masked autoencoder](../../../../paradigms/self-supervised/masked-prediction/index.md) idea from images to video, with much more aggressive masking, because neighbouring frames are highly redundant.

## Key concepts

- **Cube (tubelet).** A block of $2\times16\times16$ pixels, two frames by a $16\times16$ patch. Each cube becomes one token.
- **Tube masking.** The same spatial mask is applied to every frame, so a hidden region stays hidden through time. A hidden cube cannot then be recovered from its visible temporal neighbour, a leak that random masking allows for static regions.[^2]
- **Asymmetric encoder–decoder.** The encoder sees only the visible tokens, and a lighter decoder reconstructs the hidden ones.

## How it works

1. Sample a clip, subsample it in time, and split it into cubes.
2. Mask about 90% of the tokens with tube masking.
3. Pass the visible tokens through a [Vision Transformer](../../../transformer/vision-transformer/vit/index.md) with joint space-time attention.
4. Feed the encoder output and learnable mask tokens to a shallow decoder that predicts the hidden pixels.

The loss is a mean squared error over the masked cubes, computed on normalised pixels. For a set $\Omega$ of masked tokens, with $I(p)$ the target and $\hat I(p)$ the prediction,

$$
\mathcal{L} = \frac{1}{|\Omega|}\sum_{p\in\Omega}\left\lVert I(p)-\hat I(p)\right\rVert_2^2 .
$$

This is the image MAE objective with cubes in place of patches.[^3] Only about 10% of the tokens reach the encoder, so pre-training is cheaper than the contrastive baseline MoCo v3 even with more epochs. The paper reports 19.5 hours against 61.7 hours.[^2]

## Results

With a 16-frame ViT-B, each method is pre-trained only on the training split of the target dataset. VideoMAE beats both training from scratch and MoCo v3 on every dataset:[^2]

| Dataset | Training clips | From scratch | MoCo v3 | VideoMAE |
|---|---|---|---|---|
| [Kinetics-400](https://arxiv.org/abs/1705.06950) | 240k | 68.8 | 74.2 | 80.0 |
| Something-Something V2 | 169k | 32.6 | 54.2 | 69.6 |
| UCF101 | 9.5k | 51.4 | 81.7 | 91.3 |
| HMDB51 | 3.5k | 18.0 | 39.2 | 62.6 |

Without extra data, Kinetics-400 accuracy reaches 81.5% for ViT-B, 85.2% for ViT-L and 86.6% for ViT-H, and 87.4% for ViT-H at higher resolution.[^2]

## Limitations

- **Domain matters.** Pre-training on Kinetics and transferring to Something-Something V2 is slightly worse than pre-training on the target data, which the authors attribute to domain shift.[^2]
- **Long training.** The ablations use 800 epochs and the Kinetics-400 comparison 1600, and the largest model has 633 million parameters.[^2]
- **Quadratic attention.** Joint space-time attention still scales quadratically with token count, which the high masking ratio only partly relieves.[^2]

## Open questions

- Does reconstructing pixels teach motion as well as appearance? [V-JEPA](https://arxiv.org/abs/2404.08471) predicts features instead of pixels and reports strong video representations, which suggests the choice of target matters.[^4]
- Is a 90% masking ratio best for tasks beyond recognition, such as generation or video-language modelling?

## References

### Seminal papers

- Tong, Z., Song, Y., Wang, J. & Wang, L. (2022). *VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training*. NeurIPS. https://arxiv.org/abs/2203.12602 — The paper: masked cube reconstruction with tube masking at a 90% ratio.
- He, K., et al. (2021). *Masked Autoencoders Are Scalable Vision Learners*. arXiv. https://arxiv.org/abs/2111.06377 — The image MAE that VideoMAE adapts, with an asymmetric encoder.
- Dosovitskiy, A., et al. (2020). *An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale*. arXiv. https://arxiv.org/abs/2010.11929 — The Vision Transformer that VideoMAE uses as its backbone.
- Chen, X., Xie, S. & He, K. (2021). *An Empirical Study of Training Self-Supervised Vision Transformers*. arXiv. https://arxiv.org/abs/2104.02057 — MoCo v3, the contrastive baseline in the comparison.
- Kay, W., et al. (2017). *The Kinetics Human Action Video Dataset*. arXiv. https://arxiv.org/abs/1705.06950 — The Kinetics-400 dataset used for pre-training and evaluation.
- Goyal, R., et al. (2017). *The "something something" video database for learning and evaluating visual common sense*. arXiv. https://arxiv.org/abs/1706.04261 — The Something-Something dataset, which tests motion-sensitive recognition.
- Soomro, K., Zamir, A. R. & Shah, M. (2012). *UCF101: A Dataset of 101 Human Actions Classes From Videos in The Wild*. arXiv. https://arxiv.org/abs/1212.0402 — The 101-class action dataset used in the transfer experiments.
- Kuehne, H., Jhuang, H., Garrote, E., Poggio, T. & Serre, T. (2011). *HMDB: A large video database for human motion recognition*. ICCV. https://doi.org/10.1109/ICCV.2011.6126543 — The 51-class action dataset, the smallest used here.
- Bardes, A., et al. (2024). *Revisiting Feature Prediction for Learning Visual Representations from Video*. arXiv. https://arxiv.org/abs/2404.08471 — V-JEPA, which learns video features by predicting features rather than pixels.

[^1]: Tong et al. (2022), Introduction: video Transformers are usually derived from image models, and training from scratch gives unsatisfactory results.
[^2]: Tong et al. (2022): Section 3 (tube masking, encoder, timing), Table 2 (16-frame ViT-B comparison), Table 3 (pre-training time), Table 7 (Kinetics-400 scaling) and the domain-shift discussion in the pre-training dataset section.
[^3]: He et al. (2021): the MSE loss is computed on normalised pixels of the masked patches.
[^4]: Bardes et al. (2024), abstract: feature prediction without pixel reconstruction, on two million videos.
