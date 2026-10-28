---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
aliases:
  - Few-shot benchmarks
  - 少樣本基準
---

# Few-Shot Benchmarks

Few-shot benchmarks test whether a learner can recognise new classes from a handful of labelled examples. The score is only meaningful together with the protocol that produced it: how the classes are split, how many examples each class gets, and how many random episodes are averaged.

## Overview

Most few-shot benchmarks are built as a sequence of **episodes**. In each episode the learner sees a small labelled *support set* with N classes and K examples per class, then predicts the label of unlabelled *query* images drawn from the same N classes. This is the N-way K-shot setting. A single episode is noisy, so reported numbers are averages over many episodes, often with a confidence interval.

Matching Networks introduced this style of one-shot evaluation on ImageNet and Omniglot, and it shows why the design matters. The paper reports that its one-shot accuracy on ImageNet rose from 87.6% to 93.2%, and on Omniglot from 88.0% to 93.8%, compared with competing approaches (Vinyals et al., 2016). Comparisons like these are only fair when every method is run on the same episode sampler.

## Benchmarks compared

| Benchmark | Source of images | What it stresses |
|---|---|---|
| [miniImageNet](mini-imagenet.md) | A subset of ImageNet, with classes held out for testing | Natural photographs with fine-grained visual differences |
| [Omniglot](omniglot.md) | Handwritten characters from many writing systems | Learning a new character from one or a few drawings |

The two benchmarks come from different image domains. A method that does well on handwritten characters may not do well on natural photographs, so results on one should not be read as results on the other.

## Key concepts

- **Support set and query set**: the labelled examples an episode provides, and the unlabelled examples the learner must classify.
- **Episode**: one sampled task, with N classes and K examples per class. Accuracy is averaged over many episodes.
- **Base and novel classes**: training uses base classes; testing uses classes the learner has never seen.

## How it works

A few-shot learner usually turns each example into a feature vector and then compares the query with the support set. Prototypical Networks, for example, represent each class by the mean of its support embeddings and assign a query to the nearest prototype. The paper argues that this simpler inductive bias suits the limited-data regime, and that simple design choices can outperform more complicated recent approaches (Snell et al., 2017). Model-agnostic meta-learning takes a different route: it trains an initialisation that adapts to a new task in a few gradient steps, and it reports results on two few-shot image classification benchmarks (Finn et al., 2017).

## Common issues

- **Protocol drift.** Class splits, backbones, image resolutions and episode counts differ between papers, so the same method can report different numbers.
- **Saturation.** Strong methods leave little room on the standard splits, so small differences need confidence intervals to be meaningful.
- **Domain gap.** Omniglot images are simple strokes, while natural images are noisy. Gains on one do not transfer automatically.

## Connections

- [Meta-learning](../../../paradigms/meta-learning/index.md) is the learning paradigm behind most methods evaluated on these benchmarks.
- [Building machines that learn and think like people](../../../../brain-mind/cognitive-science/building-machines-like-people/index.md) discusses how people learn new concepts from few examples, the comparison Omniglot was built to support.

## Open questions

- Whether episodic benchmarks measure the ability to learn new concepts, or mainly the quality of the pre-trained features.
- How few-shot scores relate to few-shot performance in large pre-trained models that learn from a prompt rather than from gradient updates (Brown et al., 2020).

## Related

- [Benchmarks overview](../index.md) lists all families.
- [ImageNet](../vision/imagenet.md) is the source of the images behind miniImageNet.
- [Vision](../vision/index.md) covers the image benchmarks that the few-shot splits are drawn from.

## References

### Seminal papers

- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — Defines one-shot evaluation on ImageNet and Omniglot with a support set and query, and reports the accuracy gains quoted above.
- Lake, B. M., Salakhutdinov, R. & Tenenbaum, J. B. (2015). *Human-level concept learning through probabilistic program induction*. Science, 350(6266), 1332–1338. https://doi.org/10.1126/science.aab3050 — Introduces the handwritten-character setting that Omniglot is built on.
- Snell, J., Swersky, K. & Zemel, R. S. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — Classifies queries by distance to class prototypes, a simple baseline for N-way K-shot tasks.
- Finn, C., Abbeel, P. & Levine, S. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — Trains an initialisation that adapts in a few gradient steps, evaluated on few-shot image classification.

### Articles and documentation

- Russakovsky, O. et al. (2015). *ImageNet Large Scale Visual Recognition Challenge*. International Journal of Computer Vision, 115, 211–252. https://doi.org/10.1007/s11263-015-0816-y — Describes the ImageNet benchmark, the source of the images used by miniImageNet.
- Brown, T. B. et al. (2020). *Language Models are Few-Shot Learners*. arXiv. https://arxiv.org/abs/2005.14165 — Uses the term few-shot for prompting with demonstrations and no gradient updates, a different protocol from episodic learning.
