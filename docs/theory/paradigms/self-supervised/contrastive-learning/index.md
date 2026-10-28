---
tags:
  - self-supervised learning
  - contrastive learning
  - representation learning
---

# Contrastive Learning

Contrastive learning trains representations by pulling together embeddings of related inputs (two augmentations of one image, a sentence and its translation, an image and its caption) and pushing apart embeddings of unrelated inputs. It is the main self-supervised method for images and multimodal models.

## Overview

Take a batch of $N$ inputs, make two views of each, and embed them. For each view, the positive is its partner and the negatives are all other views in the batch. The **InfoNCE** loss is a softmax cross-entropy over the similarities:

$$
\mathcal{L}_i = -\log \frac{\exp(\operatorname{sim}(z_i, z_i^+)/\tau)}{\sum_{j} \exp(\operatorname{sim}(z_i, z_j)/\tau)}
$$

where $\tau$ is a temperature. Minimising this loss maximises a lower bound on the mutual information between the views, which is the theoretical motivation (Oord et al., 2018).

## Key methods

- **SimCLR** uses strong augmentations (random crops, colour jitter, blur) and a large batch, plus a small projection head that is discarded after training.
- **MoCo** keeps a queue of past embeddings and a slowly updated key encoder, so the number of negatives does not depend on the batch size.
- **CPC** applies the same loss to predict future latent states of a sequence, and works for speech, images and text.
- **CLIP** contrasts image and text embeddings across a large dataset of web image–caption pairs, giving zero-shot classification by comparing an image with text prompts.

## Design choices that matter

Strong augmentations define what invariances are learned, so the augmentation pipeline is the real supervision. The temperature controls how hard negatives are weighted. Batch size or queue length determines how many negatives are compared. Bad negatives (false negatives from the same class) hurt performance.

## Why it works, and what it learns

Contrastive objectives encourage **alignment** of positive pairs and **uniformity** of embeddings on the hypersphere (Wang & Isola, 2020). The learned features transfer well when the augmentations match the downstream invariances, and poorly otherwise.

## Connections

Contrastive methods without negatives are covered under [non-contrastive methods](../non-contrastive-methods/index.md). The loss is closely related to the softmax of a classifier, linking to [supervised learning](../../supervised/index.md). CLIP-style training connects vision and language, see [multimodal models](../../../models/multimodal/index.md). The idea of comparing similar and dissimilar items also appears in human perceptual learning.

## Applications

Pre-training image encoders for medical imaging with few labels, learning speaker and audio embeddings, retrieval and search across images and text, and zero-shot recognition in large vision-language models.

## Open questions

Why contrastive pre-training transfers so well is only partly understood. Choosing augmentations for non-visual data, such as time series or molecules, remains difficult, and removing false negatives without labels is an open problem.

## References

### Seminal papers

- Chen, Kornblith, Norouzi & Hinton (2020), "A simple framework for contrastive learning of visual representations", ICML, arXiv:2002.05709 — SimCLR, showing that augmentation, large batches and a projection head are the key ingredients.
- He, Fan, Wu, Xie & Girshick (2020), "Momentum contrast for unsupervised visual representation learning", CVPR, arXiv:1911.05722 — MoCo, which uses a momentum encoder and a queue for many negatives.
- Oord, Li & Vinyals (2018), "Representation learning with contrastive predictive coding", arXiv:1807.03748 — Introduces the InfoNCE loss and CPC for sequential data.
- Radford et al. (2021), "Learning transferable visual models from natural language supervision", ICML, arXiv:2103.00020 — CLIP, contrastive image–text pre-training that enables zero-shot recognition.
- Wang & Isola (2020), "Understanding contrastive representation learning through alignment and uniformity on the hypersphere", ICML, arXiv:2005.10242 — Explains contrastive loss through alignment and uniformity.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none beyond the entries above)

## Further reading

- Weng, L. (2021), "Contrastive representation learning", *Lil'Log* blog. https://lilianweng.github.io/posts/2021-05-31-contrastive/ — A blog survey of contrastive learning methods and their losses.
