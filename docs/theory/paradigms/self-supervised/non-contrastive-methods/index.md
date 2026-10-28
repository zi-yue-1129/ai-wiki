---
tags:
  - self-supervised learning
  - joint embedding
  - representation learning
---

# Non-Contrastive Methods

Non-contrastive joint-embedding methods learn from pairs of views without using negative examples. They avoid collapse, where all embeddings become identical, through architectural tricks, stop-gradients or explicit regularisation of the covariance.

## Overview

Two augmented views of an image are passed through an encoder, and the embeddings are trained to agree. Without negatives, a trivial solution exists: map every input to the same vector. Non-contrastive methods prevent this in different ways, and the choice of mechanism determines what is learned.

## Methods

- **[BYOL](byol.md)** trains an online network to predict the output of a slowly updated target network. The target is a moving average of the online weights, and no negatives are used.
- **SimSiam** shows that a stop-gradient and a predictor head are enough to prevent collapse, even without a momentum encoder or large batches.
- **DINO** applies a self-distillation objective to vision transformers. It uses a teacher with centring and sharpening, and the attention maps of the resulting features segment objects without labels.
- **DINOv2** extends DINO with patch-level objectives and a curated training set. Its frozen features are used in robotic place recognition. See [DINOv2](dinov2.md).
- **VICReg** adds explicit regularisers. Variance keeps each embedding dimension spread out, covariance decorrelates dimensions, and invariance matches the two views.

## Why collapse is avoided

BYOL and SimSiam rely on asymmetry between the online and target branches, and the exact reason they work is still debated. VICReg makes the regularisation explicit, so collapse is prevented by a loss term rather than by architecture. Each approach has different sensitivities to batch size and normalisation.

## Connections

These methods share the aims of [contrastive learning](../contrastive-learning/index.md) but drop the negatives. The regularisers relate to decorrelation ideas in [unsupervised learning](../../unsupervised/index.md). Self-distillation links to [knowledge distillation](../../../../engineering/index.md), where a teacher supervises a student.

## Applications

Pre-training vision backbones for detection and segmentation, self-supervised features for retrieval and clustering of images, and representation learning in settings where negative sampling is expensive or biased.

## Open questions

Which mechanism best prevents collapse at scale, and whether the learned features reflect semantics or augmentation statistics, remain active questions. Methods are also sensitive to design details, which makes reproducing published results difficult.

## References

### Seminal papers

- Grill et al. (2020), "Bootstrap your own latent: a new approach to self-supervised learning", NeurIPS, [arXiv:2006.07733](https://arxiv.org/abs/2006.07733) — BYOL, which learns from a moving-average target network and no negatives.
- Chen & He (2021), "Exploring simple Siamese representation learning", CVPR, [arXiv:2011.10566](https://arxiv.org/abs/2011.10566) — SimSiam, showing that a stop-gradient alone can prevent collapse.
- Bardes, Ponce & LeCun (2022), "VICReg: variance–invariance–covariance regularization for self-supervised learning", ICLR, [arXiv:2105.04906](https://arxiv.org/abs/2105.04906) — Explicit variance and covariance terms that prevent collapse.
- Caron et al. (2021), "Emerging properties in self-supervised vision transformers", ICCV, [arXiv:2104.14294](https://arxiv.org/abs/2104.14294) — DINO, where self-distillation produces attention maps that segment objects.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Bengio, Courville & Vincent (2013), "Representation learning: a review and new perspectives", *IEEE TPAMI* 35(8), [arXiv:1206.5538](https://arxiv.org/abs/1206.5538) — Background on the representation-learning objectives these methods build on.

## Further reading

- Weng, L. (2019), "Self-supervised representation learning", *Lil'Log* blog. https://lilianweng.github.io/posts/2019-11-10-self-supervised/ — A blog survey of self-supervised representation learning methods.
