---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/self-supervised
  - theory/paradigms/self-supervised/non-contrastive-methods
  - theory/paradigms/self-supervised/masked-prediction
  - theory/models/cnn
tags:
  - self-supervised learning
  - contrastive learning
aliases:
  - SimCLR
  - 簡單對比學習框架
---

# SimCLR: A Simple Framework for Contrastive Learning of Visual Representations

SimCLR is a contrastive method for images that needs no memory bank and no special architecture. It takes two random augmentations of each image, encodes them, and trains the two resulting embeddings to agree while separating them from the other images in the batch. It is the reference framework for most image-based contrastive learning. The family-level picture is on the [Contrastive Learning](index.md) page.

## Overview

Chen, Kornblith, Norouzi and Hinton (2020) study which parts of the contrastive recipe matter. The abstract names three findings: the composition of data augmentations is critical to defining a useful prediction task; a learnable nonlinear transformation between the representation and the contrastive loss improves representation quality; and contrastive learning benefits from larger batch sizes and more training steps than supervised learning. The abstract reports that a linear classifier on SimCLR features reaches 76.5% top-1 accuracy on ImageNet, a 7% relative improvement over earlier self-supervised methods, matching a supervised ResNet-50.

## Key concepts

- **Positive pair**: two augmented views of the same image.
- **Negatives**: the other augmented views in the batch. With \(N\) images there are \(2N\) views, so each anchor has \(2N-2\) negatives.
- **Augmentation policy**: random crop with resize and flip, colour distortion, and Gaussian blur. The paper treats the composition of these as the main source of supervision.
- **Projection head** \(g\): a two-layer MLP that maps the representation to a 128-dimensional space, where the loss is computed. It is discarded after training.
- **Temperature** \(\tau\): scales the similarities before the softmax. The paper's sweep finds \(\tau = 0.1\) best among the values it tests, with \(\ell_2\)-normalised embeddings.

## How it works

For each image in a batch, two views are sampled from the augmentation distribution. An encoder \(f\) (a ResNet) produces a representation \(h\), and the projection head produces \(z = g(h)\). Similarity is cosine, \(\operatorname{sim}(u,v) = u^\top v / (\|u\|\,\|v\|)\), and the per-pair loss is the normalised temperature-scaled cross-entropy (NT-Xent):

\[
\ell_{i,j} = -\log \frac{\exp(\operatorname{sim}(z_i, z_j)/\tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k\neq i]}\exp(\operatorname{sim}(z_i, z_k)/\tau)}
\]

Here \(i\) and \(j\) are the two views of the same image, and the denominator covers all other views in the batch. The batch loss is built from these per-pair terms. Downstream tasks use \(h\), and the projection head is thrown away.

Training uses the LARS optimizer. The paper trains with batch sizes from 256 to 8192. Its default is batch size 4096 for 100 epochs, and its main ImageNet comparison uses 1000 epochs. The crop area is sampled uniformly from 0.08 to 1.0 of the image, followed by a random horizontal flip half the time. Colour distortion has strength \(s\) (default 1.0), with jitter \(0.8s\) for brightness, contrast and saturation and \(0.2s\) for hue. It is applied with probability 0.8, with grayscale with probability 0.2. Gaussian blur is applied to half of the images.

## Key methods

### A Simple Framework for Contrastive Learning of Visual Representations (Chen, Kornblith, Norouzi & Hinton, 2020)

- **Problem:** earlier contrastive methods for images relied on specialised architectures or memory banks, and it was unclear which design choices mattered most.
- **Core idea:** use a standard ResNet, strong augmentations, a nonlinear projection head, and the NT-Xent loss over in-batch negatives, then scale batch size and training length.
- **Equation or algorithm:** the NT-Xent loss above with cosine similarity, together with the augmentation policy and LARS training described in How it works.
- **Results:** Table 6 of the paper reports ImageNet linear-evaluation top-1 accuracy of 69.3% for ResNet-50 (1×), 74.2% for ResNet-50 (2×) and 76.5% for ResNet-50 (4×). Table 7 reports semi-supervised top-5 accuracy with 1% of labels of 85.8% for ResNet-50 (4×), and 92.6% with 10% of labels.
- **Limitations:** the paper finds that contrastive learning benefits from large batches (up to 8192) and long training. Negatives come only from the current batch, so their number is tied to the batch size and therefore to hardware. The best results use the largest encoder; the 1× model is well below the 4× model in Table 6. [MoCo](moco.md) addresses the batch-size limit with a queue.

## Connections

- [MoCo](moco.md) uses a closely related loss, but takes its negatives from a queue, so their number is not limited by the batch size.
- [BYOL](../non-contrastive-methods/byol.md) removes negatives entirely.
- [Masked autoencoders](../masked-prediction/mae.md) take the other route: they predict missing content rather than contrasting views.
- The linear evaluation protocol used for the results above is discussed in [Theory and evaluation](../theory-and-evaluation/index.md).
- The ResNet backbone is covered under [CNN models](../../../models/cnn/index.md).

## Open questions

- How much of SimCLR's gain comes from the augmentation policy, and how much from batch size and training length? The paper studies both, but the two interact.
- Why does a nonlinear head before the loss improve the representation used downstream? The paper shows the effect empirically, and the abstract does not give a mechanism.

## References

### Seminal papers

- Chen, T., Kornblith, S., Norouzi, M. & Hinton, G. (2020). A Simple Framework for Contrastive Learning of Visual Representations. ICML (PMLR 119). https://arxiv.org/abs/2002.05709 — The paper described on this page.
- Chen, T. et al. (2020). Big Self-Supervised Models are Strong Semi-Supervised Learners. NeurIPS. https://arxiv.org/abs/2006.10029 — Follow-up that scales up the SimCLR approach for semi-supervised learning.
- Wu, Z., Xiong, Y., Yu, S. X. & Lin, D. (2018). Unsupervised Feature Learning via Non-Parametric Instance Discrimination. CVPR. https://arxiv.org/abs/1805.01978 — Instance discrimination with a memory bank of negatives, which SimCLR avoids.
- Oord, A. van den, Li, Y. & Vinyals, O. (2018). Representation Learning with Contrastive Predictive Coding. arXiv:1807.03748. https://arxiv.org/abs/1807.03748 — Introduces the InfoNCE loss on which the NT-Xent loss is based.
- Wang, T. & Isola, P. (2020). Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere. ICML (PMLR 119). https://arxiv.org/abs/2005.10242 — Explains the contrastive objective in terms of alignment and uniformity.
- He, K., Zhang, X., Ren, S. & Sun, J. (2016). Deep Residual Learning for Image Recognition. CVPR. https://arxiv.org/abs/1512.03385 — The ResNet architecture used as the encoder.

### Surveys and textbooks

- Balestriero, R. et al. (2023). A Cookbook of Self-Supervised Learning. arXiv:2304.12210. https://arxiv.org/abs/2304.12210 — Practical survey of self-supervised design choices, including those SimCLR studies.
