---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning
  - theory/paradigms/transfer/domain-adaptation
  - theory/machine-learning/adversarial-robustness
tags:
  - out-of-distribution detection
  - distribution shift
  - robustness
aliases:
  - 分布外偵測
  - 分布偏移
  - Out-of-distribution detection
  - Distribution shift
  - Open-set recognition
---

# Out-of-Distribution Detection and Distribution Shift

Out-of-distribution (OOD) detection asks whether an input comes from a different distribution than the training data, so that the model can flag it instead of predicting confidently. Distribution shift is the broader problem that the test data differ from the training data. Part of [Machine learning](../index.md).

## Overview

A model trained on one distribution often receives inputs from another: a photograph taken at night, a sensor that has aged, a new hospital with a different scanner. The model may still give a confident prediction. Hendrycks and Gimpel (2017) showed that a simple confidence score already separates many misclassified and out-of-distribution inputs from correct ones, which made the problem a measurable benchmark.

## Key concepts

- **Covariate shift**: the input distribution changes while the conditional label distribution stays the same.
- **Label shift**: the label distribution changes while the conditional input distribution stays the same.
- **OOD score**: a number computed from the model that is high for in-distribution inputs and low for out-of-distribution ones, used to threshold a decision.
- **Open-set recognition**: classifying known classes and rejecting unknown ones, a close relative of OOD detection.
- **Shortcut learning**: a model relies on features that correlate with the label in training but not in general, which makes it fail under shift (Geirhos et al., 2020).

## How it works

Most OOD detectors compute a score from the network's outputs or internal features and threshold it. Output-based scores, such as confidence, are cheap but can be overconfident on OOD inputs. Feature-based scores fit a density or distance to in-distribution features. Some methods add a small perturbation or a temperature to sharpen the separation (Liang et al., 2018). Benchmarks such as WILDS measure how models behave under natural shifts across hospitals, cameras and regions (Koh et al., 2021).

## Key methods

- [ODIN](odin.md): a softmax score improved by temperature scaling and small input perturbations.
- [Mahalanobis distance detector](mahalanobis-distance.md): a feature-space distance to class-conditional Gaussians, which also covers adversarial inputs (Lee et al., 2018).

## Connections

- [Domain adaptation](../../paradigms/transfer/domain-adaptation/index.md) tries to make models work under shift by using unlabelled target data, which complements detection.
- [Adversarial examples and robustness](../adversarial-robustness/index.md) addresses inputs that are deliberately changed, while OOD inputs are usually natural.

## Applications

- **Medical imaging**: flagging scans from a scanner or population the model was not trained on.
- **Autonomous systems**: deferring to a human or to a safe fallback when the scene is unfamiliar.
- **Quality control**: detecting new product types on a production line before errors accumulate.

## Open questions

- Methods that detect one kind of OOD input often fail on another, and no single score is reliable across all shifts.
- Deep models can be confidently wrong on far-away inputs, which weakens confidence-based detection.
- Shortcut features are hard to find and remove without labelled examples of the shortcut.

## References

### Seminal papers

- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — Shows that the maximum softmax probability already separates misclassified and out-of-distribution inputs, and sets a benchmark.
- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — Introduces ODIN, which improves the detector with temperature scaling and input perturbation.
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — Introduces a Mahalanobis-distance detector on feature space.
- Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F. & Vaughan, J. W. (2010). A theory of learning from different domains. *Machine Learning* 79(1–2), 151–175. https://doi.org/10.1007/s10994-009-5152-4 — Gives a theoretical bound on the error of a model under a change of domain.

### Surveys and textbooks

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — Benchmark of natural distribution shifts across many real-world datasets.
- Geirhos, R. et al. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence* 2(11), 665–673. https://doi.org/10.1038/s42256-020-00257-z — Describes how models rely on shortcuts that fail under shift.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers distribution shift and uncertainty for out-of-distribution inputs.
