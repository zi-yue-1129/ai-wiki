---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - few-shot
---

# Omniglot

Omniglot is a collection of handwritten characters from many writing systems, each with only a few drawn examples. It was built to test whether a learner can recognise a new character after seeing one or a few examples, which is the setting of few-shot learning (Lake et al., 2015). Matching networks made it a standard few-shot benchmark by reporting one-shot results on it (Vinyals et al., 2016).

## Task and data

The dataset contains 1,623 characters from 50 writing systems, and each character was drawn by 20 different people. An episode samples several characters, shows the learner a few labelled examples of each, and asks it to classify new drawings of the same characters (Lake et al., 2015; Vinyals et al., 2016).

## Protocol and metric

The common protocol is N-way K-shot classification, for example 20-way one-shot, where the learner sees one labelled example per class (Vinyals et al., 2016). The metric is accuracy averaged over many random episodes, usually reported with a confidence interval. The choice of training alphabets and test alphabets must be stated, because it decides how far the test classes are from the training classes.

## What it shows

It shows how well a method generalises to new characters from very few examples, on images that are simple and nearly binary. Methods that score well here do not automatically work on natural images, where the miniImageNet benchmark gives a harder test (Snell et al., 2017).

## Limitations

- **Simple images.** Strokes on a plain background are far from natural photographs, so the benchmark is easier to solve than its name suggests.
- **Saturation.** Recent methods reach near-perfect accuracy, which leaves little room to compare them.
- **Split drift.** Papers differ in how they divide alphabets into training and test sets, so scores are not always comparable.

## Related

- [Few-shot overview](index.md) compares the few-shot benchmarks.
- [miniImageNet](mini-imagenet.md) is the natural-image counterpart.

## References

### Seminal papers

- Lake, B. M. et al. (2015). *Human-level concept learning through probabilistic program induction*. Science. https://doi.org/10.1126/science.aab3050 — Introduces Omniglot as a benchmark for learning from few examples.
- Vinyals, O. et al. (2016). *Matching Networks for One Shot Learning*. arXiv. https://arxiv.org/abs/1606.04080 — Defines one-shot evaluation on Omniglot and ImageNet that later benchmarks follow.

### Articles and documentation

- Snell, J. et al. (2017). *Prototypical Networks for Few-shot Learning*. arXiv. https://arxiv.org/abs/1703.05175 — Uses N-way K-shot episodes with results on Omniglot and miniImageNet.
- Finn, C. et al. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks*. arXiv. https://arxiv.org/abs/1703.03400 — Reports few-shot results on Omniglot for a meta-learning method.

### Additional sources

- Recht, B. et al. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* arXiv. https://arxiv.org/abs/1902.10811 — Shows that a re-collected test set can reveal fit to the original collection.
