---
status: draft
last_reviewed: 2026-10-28
aliases:
  - ArcFace
  - 加性角度間隔損失
  - Additive angular margin loss
---

# ArcFace (Deng et al., 2019)

ArcFace is a training loss for deep face recognition. It adds an additive angular margin to the softmax loss, so that each face's embedding is pulled toward its own identity and away from others on the unit hypersphere. It is one of the training losses behind the embedding models of modern face matching, the subject of [Surveillance, Facial Recognition and Human Rights](../index.md).

## Overview

A face recognition system turns each face into an embedding vector and compares vectors to decide identity. Good recognition needs faces of the same person close together and faces of different people far apart. Softmax-trained models separate identities weakly, so earlier work added margins.

Deng et al. (2019) propose the additive angular margin loss. The margin has a geometric meaning: on the normalised hypersphere it equals the geodesic distance between a face and its class centre.

## Key concepts

- **Embedding**: the vector a network produces for a face. The paper's experiments use 512 numbers.
- **Hypersphere**: the surface of the unit sphere in high dimensions, where classification becomes a comparison of angles.
- **Feature scale** $s$: a fixed multiplier on all cosine logits. The paper uses $s = 64$.
- **Angular margin** $m$: an angle added to the true-class angle during training, so the correct class must win by a clear gap. The paper's best value is $m = 0.5$.

## How it works

Softmax computes a logit for each class $j$ as the dot product between the embedding and the class weight. With normalised vectors, the logit reduces to $s\cos\theta_j$, where $\theta_j$ is the angle between the embedding and the weight for class $j$. ArcFace adds the margin to the angle of the true class $y_i$:

$$
L = -\frac{1}{N}\sum_{i=1}^{N}\log\frac{e^{s\cos(\theta_{y_i}+m)}}{e^{s\cos(\theta_{y_i}+m)}+\sum_{j\neq y_i}e^{s\cos\theta_j}}
$$

For each batch:

1. Normalise each face embedding $x_i$ and each class weight $W_j$ to unit length.
2. Compute $\cos\theta_j$ for every class $j$ as the inner product of the normalised vectors.
3. For the true class $y_i$, replace $\theta_{y_i}$ with $\theta_{y_i}+m$.
4. Multiply all cosines by $s$, apply cross-entropy and back-propagate.

The paper also introduces a sub-centre variant, in which each class has several centres and a face need only be close to one of them. It is meant to tolerate the label noise common in web-collected face datasets.

## Results

The ablation in Table 2 of the paper trains on the CASIA dataset with a ResNet-50 network. The figures below are verification accuracy in percent, read from the arXiv version of the paper.

| Loss | LFW | CFP-FP | AgeDB |
|---|---|---|---|
| Softmax | 99.08 | 94.39 | 92.33 |
| Normalised softmax with s = 64 | 98.56 | 89.79 | 88.72 |
| CosFace (margin 0.35) | 99.51 | 95.44 | 94.56 |
| ArcFace (margin 0.5) | 99.53 | 95.56 | 95.15 |

ArcFace with margin 0.5 is at or near the top, and its advantage over softmax is largest on the harder CFP-FP and AgeDB sets. The arXiv version may differ from the conference version, so check before quoting.

## Limitations

- **Benchmark scores are not deployment scores.** LFW, CFP-FP and AgeDB are curated test sets. Matching against a large gallery of strangers, as an identification system does, is harder and is tested separately.
- **The loss does not fix biased data.** A margin changes how classes are separated but adds no missing faces. The gaps described in [Gender Shades](../gender-shades/index.md) can persist after a loss is improved. Buolamwini and Gebru (2018) report an estimate that LFW is 77.5% male and 83.5% White.
- **Label noise.** Web-collected datasets contain mislabelled faces. The sub-centre variant helps, but how well it cleans a dataset depends on that dataset.
- **Privacy of embeddings.** The paper also shows that the pre-trained model can be inverted to generate face images that keep the subject's identity. This is a risk for any system that stores embeddings.

## Connections

- Training data matters as much as the loss (Cao et al., 2017, cited below).
- Margin-based metric learning belongs to the wider family of embedding methods in [Other learning paradigms](../../../theory/paradigms/other/index.md). The networks are covered in [Computer Vision](../../../theory/models/computer-vision/index.md).
- Whether machine face recognition shares human biases, such as the other-race effect, is discussed on the [topic page](../index.md).

## Open questions

- Do gains on verification benchmarks carry over to identification against millions of faces?
- Can a loss be designed to reduce demographic differentials directly, or must the fix come from data and evaluation?
- How should embeddings be protected, given that a model can be inverted to recover face images?

## References

### Seminal papers

- Deng, J. et al. (2019). ArcFace: Additive Angular Margin Loss for Deep Face Recognition. *CVPR*. https://doi.org/10.1109/CVPR.2019.00482 — Introduces the additive angular margin loss and its sub-centre variant for noisy web faces.

### Articles and documentation

- Buolamwini, J. & Gebru, T. (2018). Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification. *FAT\**. https://proceedings.mlr.press/v81/buolamwini18a.html — Audit showing that commercial gender classifiers' error rates vary sharply with skin type and gender.
- Cao, Q. et al. (2017). VGGFace2: A dataset for recognising faces across pose and age. arXiv. https://arxiv.org/abs/1710.08092 — Large web-collected face dataset that shapes what recognition models learn.
- Phillips, P. J. et al. (2011). An other-race effect for face recognition algorithms. *ACM Transactions on Applied Perception*. https://doi.org/10.1145/1870076.1870082 — Shows that algorithms, like human observers, perform better on the majority race.
- Raji, I. D. & Buolamwini, J. (2019). Actionable Auditing. *AAAI/ACM Conference on AI, Ethics, and Society*. https://doi.org/10.1145/3306618.3314244 — Follow-up on audits of commercial face analysis products.
