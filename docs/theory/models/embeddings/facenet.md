---
status: draft
tags:
  - metric learning
  - face recognition
  - embeddings
  - triplet loss
aliases:
  - FaceNet
  - 人臉嵌入
  - triplet loss
  - 三元組損失
---

# FaceNet

FaceNet trains a deep convolutional network to map a face image to a 128-dimensional vector, so that the Euclidean distance between two vectors measures whether the faces show the same person. Unlike a classifier trained on a fixed set of identities, the learned space can be used for new identities without retraining. The parent page, [Embeddings and Representation Learning](index.md), describes metric learning as one of the four training signals; this page gives the method in detail.

## Problem

Face recognition systems of the time often trained a classifier over a fixed set of identities and used a layer of its network as the face representation. That approach has two limits. The representation is tied to the identities seen in training, and the classifier must be retrained when identities are added. Schroff, Kalenichenko and Philbin (2015) asked for a representation that is learned directly from the distances the task cares about, so that it can be used for verification, recognition and clustering with one embedding.

## Core idea

The network `f` maps each image to a vector normalised to unit length, `‖f(x)‖₂ = 1`, so that all embeddings lie on a hypersphere. Training uses triplets: an anchor image `x^a`, a positive image `x^p` of the same person, and a negative image `x^n` of a different person. The objective requires the anchor to be closer to the positive than to the negative by a margin `α`.

Because the target is a distance comparison, the embedding is trained for the task itself. The same vectors can then be compared directly, with no separate classifier.

## Equation and algorithm

The loss over `N` triplets is

`L = Σ_i [ ‖f(x_i^a) − f(x_i^p)‖₂² − ‖f(x_i^a) − f(x_i^n)‖₂² + α ]₊`

where `[·]₊` is the hinge, which is zero when the constraint is satisfied. The paper sets the margin to `α = 0.2`.

Choosing which triplets to train on matters. The paper mines triplets online, inside each mini-batch of a few thousand face images, so that the network sees about 40 images per identity. Every anchor–positive pair in the batch is used, and the negatives are chosen among the hard ones. The authors use *semi-hard* negatives: those farther from the anchor than the positive, but still inside the margin. They report that always choosing the hardest negatives can lead to poor local minima early in training, including a collapsed model in which every embedding is zero.

## Results

Verification accuracy is reported on two standard benchmarks:

| Benchmark | Protocol | Accuracy |
|---|---|---|
| Labeled Faces in the Wild (LFW) | Standard unrestricted protocol, with extra face alignment | 99.63% ± 0.09 |
| YouTube Faces DB | Average over pairs from the first 100 frames of each video | 95.12% ± 0.39 |

The paper uses 128-dimensional vectors, which the authors note can be quantised to 128 bytes without loss of accuracy. The LFW figure is the one most often quoted, and it is the paper's own measurement. The paper reports clustering only as a qualitative example, a cluster from one user's photo collection, and it does not report a quantitative clustering score.

## Limitations

- **Training cost.** Training took 1,000 to 2,000 CPU-cluster hours, and the authors say that the loss decrease slows sharply after about 500 hours.
- **Label noise.** The sharp drop in the ROC curve at very low false-acceptance rates is attributed to noisy ground-truth labels in the test data.
- **Image quality.** Accuracy falls for small thumbnails, and the main model was trained at 220 by 220 pixels.
- **Mining evidence.** The offline triplet-generation experiments were inconclusive, and the paper does not directly compare hard with all anchor–positive selection.
- **Unfinished evaluation.** The authors list better understanding of the error cases and smaller models as future work.

## References

### Seminal papers

- Schroff, F., Kalenichenko, D. & Philbin, J. (2015). *FaceNet: A Unified Embedding for Face Recognition and Clustering*. arXiv. https://arxiv.org/abs/1503.03832 — Defines the triplet loss, semi-hard mining and the LFW and YouTube Faces results reported on this page.
- Hermans, A., Beyer, L. & Leibe, B. (2017). *In Defense of the Triplet Loss for Person Re-Identification*. arXiv. https://arxiv.org/abs/1703.07737 — Argues that the triplet loss remains a strong end-to-end metric-learning objective, with results on person re-identification.

### Surveys and textbooks

- Bengio, Y., Courville, A. & Vincent, P. (2012). *Representation Learning: A Review and New Perspectives*. arXiv. https://arxiv.org/abs/1206.5538 — Background on learned representations and their use across tasks.

### Articles and documentation

- Khosla, P. et al. (2020). *Supervised Contrastive Learning*. arXiv. https://arxiv.org/abs/2004.11362 — Extends the pull-and-push idea of contrastive embeddings to batches that use class labels.
- Wang, T. & Isola, P. (2020). *Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere*. arXiv. https://arxiv.org/abs/2005.10242 — Describes the alignment and uniformity properties of normalised embeddings, the geometry FaceNet relies on.
