---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning/ood-detection
tags:
  - out-of-distribution detection
  - temperature scaling
  - softmax
aliases:
  - ODIN
  - Out-of-distribution detector for neural networks
  - 神經網路分布外偵測器
---

# ODIN

ODIN is an out-of-distribution detector that improves the softmax score in two ways: it divides the logits by a temperature that is greater than one, and it perturbs the input slightly in the direction that increases the maximum softmax score. Part of [Out-of-distribution detection](index.md).

## Overview

A plain softmax confidence is a weak OOD score, because a network can be confident on inputs far from its training data. Liang et al. (2018) found that two small changes sharpen the separation between in-distribution and out-of-distribution inputs without retraining the network. The method needs only a forward pass and one extra gradient step, and it needs a small validation set of OOD inputs to tune its parameters.

## Key concepts

- **Temperature scaling of the softmax**: \(S_i(x;T)=\frac{\exp(f_i(x)/T)}{\sum_j\exp(f_j(x)/T)}\) with \(T>1\). Raising the temperature spreads the scores apart for detection.
- **Input perturbation**: a step \(\tilde{x}=x-\varepsilon\,\mathrm{sign}(-\nabla_x \log S_{\hat y}(x;T))\) that increases the score of the predicted class.
- **Detection rule**: an input is flagged as OOD when its score falls below a threshold.

## How it works

For an input \(x\), ODIN computes the predicted class \(\hat y\), then forms the perturbed input \(\tilde{x}\) that raises the temperature-scaled softmax score of \(\hat y\). It scores \(\tilde{x}\) with \(S_{\hat y}(\tilde{x};T)\). In-distribution inputs respond to the perturbation differently from OOD inputs, and the separation is larger than with the plain softmax. The temperature \(T\) and perturbation size \(\varepsilon\) are chosen on validation data. Liang et al. (2018) report large gains over the baseline on image benchmarks with a standard network.

## Variants

- **Temperature only**: scaling without perturbation, which is cheaper but gives less separation.
- **Perturbation only**: a step on the unscaled softmax, which can help but is less stable.
- **Feature-based scores** replace the output score with a distance in feature space, which is the approach of the [Mahalanobis detector](mahalanobis-distance.md).

## Results and limits

- ODIN improves the detection of OOD inputs over the softmax baseline without changing the network's weights (Liang et al., 2018).
- It uses a small OOD validation set to choose \(T\) and \(\varepsilon\), which may not match the OOD inputs encountered at deployment.
- The gradient step adds cost at inference, and the method is tied to classifiers with a softmax output.
- Gains depend on the pair of in- and out-of-distribution datasets, so results on one benchmark do not guarantee performance on another.

## Applications

- **Image classifiers** in deployment, where a cheap OOD flag is useful.
- **Benchmarking** of OOD detectors against the softmax baseline.
- **Triage**: sending flagged inputs for human review.

## Open questions

- Tuning on one kind of OOD data may not transfer to the shifts that occur later.
- Whether temperature and perturbation help when the network is trained with different objectives or on different modalities is not settled.

## References

### Seminal papers

- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — Introduces ODIN with temperature scaling and input perturbation.
- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — The softmax baseline that ODIN improves on.
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — A feature-based alternative to output scores.

### Surveys and textbooks

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — Benchmark on which OOD detectors and shift robustness are measured.
- Geirhos, R. et al. (2020). Shortcut learning in deep neural networks. *Nature Machine Intelligence* 2(11), 665–673. https://doi.org/10.1038/s42256-020-00257-z — Explains why detectors trained on one shift can miss another.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on softmax calibration and detection.
