---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# Few-Shot Benchmarks

Few-shot benchmarks test whether a learner can recognise new classes from a handful of labelled examples. They are usually run as N-way K-shot episodes, and the score is an average over many random episodes, so the protocol matters as much as the number.

| Benchmark | Source of images | Main metric |
|---|---|---|
| [miniImageNet](mini-imagenet.md) | Subset of ImageNet | Episode accuracy with confidence intervals |
| [Omniglot](omniglot.md) | Handwritten characters from many writing systems | Episode accuracy with confidence intervals |

## Common issues

- **Protocol drift.** Class splits, backbones and episode counts differ between papers.
- **Saturation.** Top methods leave little room, so differences need intervals.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [ImageNet](../vision/imagenet.md) is the source of the images.

## References

### Seminal papers

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — Defines one-shot evaluation on ImageNet and Omniglot that later benchmarks follow.
- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — Introduces Omniglot for learning from few examples.

### Articles and documentation

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — Uses N-way K-shot episodes with results on miniImageNet.
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — Reports few-shot results on miniImageNet for a meta-learning method.
- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision. https://doi.org/10.1007/s11263-015-0816-y — The source dataset from which miniImageNet images are taken.
