---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# miniImageNet

miniImageNet is a few-shot image classification benchmark built from ImageNet images. It is used to test whether a model can recognise new classes from a handful of labelled examples. Most few-shot papers report results on it, and it is usually evaluated with N-way K-shot episodes (Snell et al., 2017; Finn et al., 2017).

## Task and data

Each evaluation episode samples N classes the model has not seen in training and gives K labelled examples per class as the support set. The model then classifies new query images from those classes. Episodes are sampled at random from a held-out set of classes, so training and test classes do not overlap.

The most common split uses 64 classes for training, 16 for validation and 20 for testing, as defined by Ravi and Larochelle (2017). Other papers use different splits, so the split must be checked before results are compared.

## Protocol and metric

The metric is **accuracy** on query images, averaged over many random episodes, often with a confidence interval. Results depend on the backbone, the number of training episodes and the input resolution, so a comparison is valid only when those match.

Vinyals et al. (2016) set the template for one-shot evaluation on ImageNet and Omniglot. Their reported one-shot accuracy on ImageNet rose from 87.6% to 93.2% against the competing approaches in their comparison. That setting used its own class split and is not the same as miniImageNet.

## What it shows

Few-shot benchmarks test whether a learner can adapt from little data, which ordinary supervised training does not do. miniImageNet became the standard test for meta-learning methods such as Prototypical Networks (Snell et al., 2017) and MAML (Finn et al., 2017).

## Limitations

- **Low resolution and small classes.** Images are small, and the classes are fine-grained, so scores depend on the resolution used.
- **Protocol drift.** Splits, backbones and training tricks differ between papers, which makes many reported gains hard to compare.
- **Saturation.** Recent methods score high, so small differences are hard to interpret without intervals.

## Related

- [Omniglot](https://doi.org/10.1126/science.aab3050), the handwritten-character benchmark of Lake et al. (2015), is the other standard few-shot test.
- [ImageNet](../vision/imagenet.md) is the source of the images.
- [Few-shot family overview](index.md) describes this area.

## References

### Seminal papers

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — Defines one-shot evaluation on ImageNet and Omniglot that later benchmarks follow.
- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — Introduces the Omniglot handwritten-character benchmark for learning from few examples.
- Ravi, S. & Larochelle, H. (2017). *Optimization as a Model for Few-Shot Learning*. ICLR. https://openreview.net/forum?id=rJY0-Kcll — Defines the 64/16/20 class split that most miniImageNet papers use.

### Articles and documentation

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — Uses N-way K-shot episodes, with results on miniImageNet.
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — Reports few-shot results on miniImageNet for a meta-learning method.

### Additional sources

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — The source of the images from which miniImageNet is built.
