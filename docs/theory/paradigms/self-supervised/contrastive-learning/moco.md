---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/non-contrastive-methods
  - theory/models/cnn
tags:
  - self-supervised learning
  - contrastive learning
  - momentum encoder
aliases:
  - MoCo
  - Momentum Contrast
  - 動量對比
---

# MoCo: Momentum Contrast for Unsupervised Visual Representation Learning

MoCo is a contrastive method that keeps a large dictionary of negative keys in a queue, and encodes those keys with a slowly moving copy of the encoder. This decouples the number of negatives from the batch size. The family-level picture is on the [Contrastive Learning](index.md) page.

## Overview

He, Fan, Wu, Xie and Girshick (2020) frame unsupervised visual learning as dictionary look-up: an encoded query should match its positive key among a set of encoded keys. The abstract says the method builds "a dynamic dictionary with a queue and a moving-averaged encoder", so that a large and consistent dictionary can be built on the fly. The paper reports that features learned without labels transfer well to detection and segmentation. The abstract says MoCo can outperform its supervised ImageNet pre-training counterpart on seven detection and segmentation tasks.

## Key concepts

- **Query and key**: two views of the same image are encoded, one by the query encoder and one by the key encoder. The pair of their embeddings is the positive pair.
- **Queue**: a first-in, first-out store of keys from recent mini-batches. The queue supplies the negatives. The paper uses \(K = 65{,}536\) keys.
- **Momentum encoder**: the key encoder is not trained by gradients. Its weights are an exponential moving average of the query encoder's weights, with momentum \(m = 0.999\).
- **Temperature**: \(\tau = 0.07\) in the loss.
- **Shuffling BN**: a multi-GPU detail. Batch-norm statistics are computed per GPU, and the key encoder's mini-batch is shuffled before it is split across GPUs, so a query and its positive key do not share statistics from the same subset.

## How it works

Each mini-batch (256 images in the paper's ImageNet setup, spread over 8 GPUs) is encoded twice. The query encoder is updated by gradient descent. The key encoder is updated by the momentum rule

\[
\theta_k \leftarrow m\,\theta_k + (1-m)\,\theta_q
\]

For each query \(q\), the positive key \(k_+\) is the key of its other view, and the negatives are the \(K\) keys in the queue. The loss is InfoNCE:

\[
\mathcal{L}_q = -\log \frac{\exp(q\cdot k_+/\tau)}{\sum_{i=0}^{K}\exp(q\cdot k_i/\tau)}
\]

After each step, the newest keys are added to the queue and the oldest are removed. Because the keys in the queue were produced by slowly changing encoder states, the dictionary stays consistent while it grows far beyond the batch size.

## Key methods

### Momentum Contrast for Unsupervised Visual Representation Learning (He, Fan, Wu, Xie & Girshick, 2020)

- **Problem:** contrastive learning works better with many negatives, but in end-to-end training the negatives are limited to the current batch. The abstract's stated goal is a dictionary that is both large and consistent.
- **Core idea:** keep keys in a queue, and produce them with a momentum-updated encoder, so the dictionary can be large while the key encoder changes slowly.
- **Equation or algorithm:** the InfoNCE loss with \(\tau = 0.07\), the momentum update with \(m = 0.999\), the queue with \(K = 65{,}536\) keys, and shuffling BN, as described in How it works.
- **Results:** under the linear protocol on ImageNet, MoCo with a ResNet-50 trained for 200 epochs reaches 60.6% top-1 accuracy. On PASCAL VOC detection with Faster R-CNN, AP is 53.5 for supervised ImageNet pre-training and 55.9 for MoCo pre-trained on ImageNet-1M. On COCO with Mask R-CNN (R50-FPN, box AP), it is 40.6 for supervised pre-training and 40.8 for MoCo on ImageNet-1M.
- **Limitations:** the paper's gains over supervised pre-training are small on COCO (40.8 against 40.6 for R50-FPN). The paper reports no supervised baseline under the linear protocol, so the linear result cannot be compared directly with supervised training. Shuffling BN is a workaround for multi-GPU batch statistics rather than a property of the objective. The queue holds keys from earlier encoder states, so the method depends on the momentum value.

## Connections

- [SimCLR](simclr.md) uses a closely related loss, but takes its negatives from the current batch. MoCo's queue removes that dependence on batch size.
- [BYOL](../non-contrastive-methods/byol.md) keeps the momentum-updated encoder idea but drops negatives entirely.
- The linear evaluation protocol and the transfer protocol are discussed in [Theory and evaluation](../theory-and-evaluation/index.md).
- The ResNet backbone is covered under [CNN models](../../../models/cnn/index.md).

## Open questions

- How do queue length and momentum interact? The paper picks \(K = 65{,}536\) and \(m = 0.999\), but the abstract does not show how sensitive the result is to either.
- Does the advantage over supervised pre-training hold for detection and segmentation tasks beyond those reported, and for data that is not ImageNet-like?

## References

### Seminal papers

- He, K., Fan, H., Wu, Y., Xie, S. & Girshick, R. (2020). Momentum Contrast for Unsupervised Visual Representation Learning. CVPR. https://arxiv.org/abs/1911.05722 — The paper described on this page.
- Chen, X., Fan, H., Girshick, R. & He, K. (2020). Improved Baselines with Momentum Contrastive Learning. arXiv:2003.04297. https://arxiv.org/abs/2003.04297 — Follow-up that revisits MoCo as a baseline with an improved training recipe.
- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). A Simple Framework for Contrastive Learning of Visual Representations. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — The contrastive method that uses in-batch negatives, which MoCo's queue replaces.
- Wu, Z., Xiong, Y., Yu, S. X. & Lin, D. (2018). Unsupervised Feature Learning via Non-Parametric Instance Discrimination. CVPR. https://arxiv.org/abs/1805.01978 — Instance discrimination with a memory bank of stored features, an earlier way to get many negatives.
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). Representation Learning with Contrastive Predictive Coding. arXiv:1807.03748. https://arxiv.org/abs/1807.03748 — Introduces the InfoNCE loss used by MoCo.

### Surveys and textbooks

- Balestriero, R. et al. (2023). A Cookbook of Self-Supervised Learning. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — Practical survey of self-supervised design choices, including momentum encoders and queues.
- Liu, X. et al. (2020). Self-supervised Learning: Generative or Contrastive. arXiv:2006.08218. https://arxiv.org/abs/2006.08218 — Survey that compares generative and contrastive approaches to self-supervised learning.
