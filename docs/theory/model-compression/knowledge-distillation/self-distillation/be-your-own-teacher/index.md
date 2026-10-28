---
status: draft
last_reviewed: 2026-10-28
tags:
- model compression
- knowledge distillation
- self-distillation
aliases:
  - Be your own teacher
  - Deep-layer self-distillation
  - 自己當老師
---

# Be Your Own Teacher

Be Your Own Teacher is a self-distillation method that improves a single network within one training run. The network is split into sections, a classifier is attached to each section, and the knowledge of the deepest classifier is passed down to the shallower ones. Zhang et al. reported an average accuracy gain of 2.65% over the baselines. It is a [self-distillation](../index.md) method that needs no separate teacher run.

## Problem

Knowledge distillation with separate teacher and student networks is expensive, because a large teacher has to be trained first. A single network should be able to improve itself within one training run, and it should keep the same inference cost.

## Core idea

Divide a convolutional network into sections. Each section gets a bottleneck and a classifier. Every shallow classifier is trained on the true labels, on the output of the deepest classifier, and on the feature maps of the deepest section. The deepest classifier acts as the teacher for everything below it, and it is trained on the labels alone. Knowledge therefore flows downwards inside the network during training.

## Equation or algorithm

The total loss sums a per-classifier loss over all \(C\) classifiers:

\[
\mathcal{L} = \sum_{i=1}^{C} \Big( (1-\alpha)\,\mathrm{CE}(q^i, y) + \alpha\,\mathrm{KL}(q^i \,\Vert\, q^C) + \lambda\,\Vert F_i - F_C \Vert_2^2 \Big)
\]

where \(q^i\) is the softmax output of classifier \(i\), \(q^C\) is the deepest classifier's output, \(y\) is the label and \(F_i\) and \(F_C\) are the feature maps of section \(i\) and the deepest section. The first term is the label loss, the second is the distillation term and the third is a feature-hint term that aligns the shallow feature maps with the deepest ones. The paper sets the \(\alpha\) and \(\lambda\) of the deepest classifier to zero. The softmax temperature is normally set to 1. The shallow classifiers are used for depth-wise scalable inference, which the authors propose for resource-limited devices.

## Results

On CIFAR-100 the paper's main table compares a baseline with self-distillation, using the deepest classifier's accuracy:

| Network | Baseline (%) | Self-distillation (%) |
|---|---|---|
| VGG19 (BN) | 64.47 | 67.73 |
| ResNet18 | 77.09 | 78.64 |
| ResNet50 | 77.68 | 80.56 |
| ResNet101 | 77.98 | 81.23 |
| ResNet152 | 79.21 | 81.61 |
| ResNeXt29-8 | 81.29 | 81.51 |

The abstract reports an average accuracy improvement of 2.65%, ranging from 0.61% for ResNeXt to 4.07% for VGG19. The table also reports the shallower classifiers and an ensemble of the classifiers, which the page does not repeat.

## Limitations

The method adds classifiers and training terms, so training is more expensive than the baseline even though inference is not. The paper evaluates convolutional networks on image classification. Whether the same downward flow helps transformers, where layers differ more in function, is not tested in the paper. The loss weights \(\alpha\) and \(\lambda\) are not fixed by the paper and must be tuned.

## Open issues and related variants

- **Architectures.** Whether the same downward flow helps transformers is open.
- **Full-run alternative.** [Born-again networks](../born-again-networks/index.md) get a similar effect by training a full extra generation of the same network, at a much higher training cost.
- **Feature targets.** The feature-hint term follows the idea of [FitNets](../../feature-based/fitnets/index.md).

## Connections

The method is a form of deep supervision, in which intermediate layers receive their own training signal. The downward flow from a deep classifier to shallow ones is also a question of [deep learning theory](../../../../../theory/deep-learning/index.md).

## References

### Seminal papers

- Zhang, L., Song, J., Gao, A., Chen, J., Bao, C., Ma, K. (2019). *Be Your Own Teacher: Improve the Performance of Convolutional Neural Networks via Self Distillation*. arXiv:1905.08094. https://arxiv.org/abs/1905.08094 — Deep-layer self-distillation with auxiliary classifiers; an average 2.65% accuracy gain, from 0.61% (ResNeXt) to 4.07% (VGG19).
- Furlanello, T., Lipton, Z. C., Tschannen, M., Itti, L., Anandkumar, A. (2018). *Born Again Neural Networks*. arXiv:1805.04770. https://arxiv.org/abs/1805.04770 — Students with the same architecture as their teachers, trained by distillation, can outperform those teachers.
- Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network*. arXiv:1503.02531. https://arxiv.org/abs/1503.02531 — The distillation objective that the shallow classifiers use.

### Surveys and textbooks

- Gou, J., Yu, B., Maybank, S. J., Tao, D. (2021). *Knowledge Distillation: A Survey*. arXiv:2006.05525. https://arxiv.org/abs/2006.05525 — Survey of distillation methods, including self-distillation; the arXiv page lists the published version at https://doi.org/10.1007/s11263-021-01453-z.

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Romero, A., et al. (2014). *FitNets: Hints for Thin Deep Nets*. arXiv:1412.6550. https://arxiv.org/abs/1412.6550 — Intermediate hints, the feature-level counterpart of deep-layer self-teaching.
