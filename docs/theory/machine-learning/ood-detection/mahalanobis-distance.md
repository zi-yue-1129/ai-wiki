---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/machine-learning/ood-detection
tags:
  - out-of-distribution detection
  - feature space
  - Gaussian model
aliases:
  - Mahalanobis distance detector
  - 馬氏距離偵測器
  - Mahalanobis distance
---

# Mahalanobis Distance Detector

The Mahalanobis distance detector models the features of in-distribution training data as class-conditional Gaussians with a shared covariance, and it scores a test input by its distance to the nearest class mean. Inputs far from every class are flagged as out-of-distribution. Part of [Out-of-distribution detection](index.md).

## Overview

Output scores such as softmax confidence depend on the final layer and can be overconfident. The features in the penultimate or intermediate layers carry more information about how typical an input is. Lee et al. (2018) fit a simple Gaussian model to these features and use the Mahalanobis distance, which accounts for correlations between feature dimensions, as the OOD score.

## Key concepts

- **Class-conditional Gaussian**: each class \(c\) has a mean \(\mu_c\) of its features in training data.
- **Shared covariance**: one covariance \(\Sigma\) is estimated from the centred features of all classes, which keeps the model stable with few samples.
- **Mahalanobis distance**: \(M(x)=\min_c (f(x)-\mu_c)^\top\Sigma^{-1}(f(x)-\mu_c)\), where \(f(x)\) is the feature vector.
- **Feature layers**: the features may come from several layers of the network, and their scores can be combined.

## How it works

Compute features for each training example and estimate the class means and the shared covariance. For a test input, compute the minimum Mahalanobis distance over the classes. A large distance means the input is unlike any training class, and it is flagged as OOD when the distance exceeds a threshold. Lee et al. (2018) also add a small input perturbation that increases the score, similar to the idea in [ODIN](odin.md), and they combine scores from several layers with a logistic regressor trained on a small set of OOD inputs.

## Variants

- **Single-layer score** uses only the final feature layer, which is simpler and cheaper.
- **Multi-layer score** combines distances from several layers, which captures low-level as well as high-level differences.
- **Class-agnostic density** fits one Gaussian to all features, which removes the need for class labels.

## Results and limits

- The detector works with a pretrained network and needs only feature statistics from the training data (Lee et al., 2018).
- The Gaussian assumption is approximate. Features of real networks are not Gaussian, and the scores depend on how well the Gaussian fits.
- The detector can be used for adversarial inputs as well as OOD inputs, but it can be fooled by an attacker who knows the detector.
- Combining layers may need a small set of OOD examples, which can be missing in practice.

## Applications

- **Image classifiers** with a pretrained backbone, where feature statistics are easy to compute.
- **Adversarial and OOD screening**, since the same score can flag both kinds of input.
- **Monitoring**: tracking the distance over time to detect drift in the input distribution.

## Open questions

- The shared-covariance assumption fails for some architectures, and better density models for features are an open area.
- A score that resists adaptive attacks, which target the detector itself, is hard to guarantee.

## References

### Seminal papers

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). A simple unified framework for detecting out-of-distribution samples and adversarial attacks. In *Advances in Neural Information Processing Systems* 31. arXiv:1807.03888. https://arxiv.org/abs/1807.03888 — Introduces the Mahalanobis-distance detector and its multi-layer combination.
- Liang, S., Li, Y. & Srikant, R. (2018). Enhancing the reliability of out-of-distribution image detection in neural networks. In *International Conference on Learning Representations*. arXiv:1706.02690. https://arxiv.org/abs/1706.02690 — Shows that input perturbation and temperature help output-based detection, related to the input-perturbation step used here.
- Hendrycks, D. & Gimpel, K. (2017). A baseline for detecting misclassified and out-of-distribution examples in neural networks. In *International Conference on Learning Representations*. arXiv:1610.02136. https://arxiv.org/abs/1610.02136 — The output-score baseline that feature-based detectors aim to improve on.

### Surveys and textbooks

- Koh, P. W. et al. (2021). WILDS: a benchmark of in-the-wild distribution shifts. In *Proceedings of the 38th International Conference on Machine Learning*, PMLR 139. https://proceedings.mlr.press/v139/koh21a.html — Benchmark that tests detectors under natural shifts.
- Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F. & Vaughan, J. W. (2010). A theory of learning from different domains. *Machine Learning* 79(1–2), 151–175. https://doi.org/10.1007/s10994-009-5152-4 — Theory of how a change of domain affects error, relevant to when a distance-based detector should trigger.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; background on Gaussian models and density-based detection.
