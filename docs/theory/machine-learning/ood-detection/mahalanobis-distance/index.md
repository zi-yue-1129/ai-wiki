---
status: draft
last_reviewed: 2026-10-28
tags:
  - distribution shift
  - anomaly detection
  - evaluation
aliases:
  - 馬氏距離偵測
  - 馬哈拉諾比斯距離
  - Mahalanobis distance
  - Mahalanobis detector
---

# Mahalanobis Distance Detector

The Mahalanobis distance detector scores an input by how far its internal features lie from the features of each class. A network's features are modelled as Gaussian clusters, one per class, and an input far from all of them is flagged as out-of-distribution. Lee et al. (2018) proposed the method for both OOD and adversarial inputs. It is one of the scores described on the [out-of-distribution detection](../index.md) page.

## Overview

Maximum softmax probability uses only the final output of a network. Lee et al. (2018) instead look at the feature space, the intermediate representation from which the classifier makes its decision. In that space, training examples of one class tend to cluster together. The authors fit a Gaussian to each class and treat an input's distance from the nearest class as a measure of how typical it is. The method applies to any pre-trained softmax classifier and needs no outlier data to compute its basic score. The paper also describes refinements, such as using several layers and a small input perturbation, not covered here.

## Key concepts

- **Feature space.** The activations of a chosen layer of the network, used as a representation of the input.
- **Class-conditional Gaussian.** A Gaussian distribution fitted to the features of one class, with its mean at the class centroid.
- **Mahalanobis distance.** A distance that rescales the feature space by its covariance, so that directions of high variance count for less than directions of low variance.
- **Shared covariance.** The method uses one covariance matrix for all classes, as in Gaussian discriminant analysis.

## How it works

Let $f(x)$ be the features of input $x$. Using the training data, the method estimates a mean $\mu_c$ for each class $c$ and one shared covariance $\Sigma$:

$$
\mu_c = \frac{1}{N_c}\sum_{i:\,y_i=c} f(x_i), \qquad \Sigma = \frac{1}{N}\sum_{c}\sum_{i:\,y_i=c}\big(f(x_i)-\mu_c\big)\big(f(x_i)-\mu_c\big)^{\top}.
$$

The score is the negative squared Mahalanobis distance to the nearest class:

$$
M(x) = \max_c \; -\big(f(x)-\mu_c\big)^{\top}\Sigma^{-1}\big(f(x)-\mu_c\big).
$$

An input is flagged when $M(x)$ falls below a threshold $\tau$ chosen on validation data. The procedure is as follows.

1. Train the classifier and freeze it.
2. Extract features for the training data and estimate $\mu_c$ and $\Sigma$.
3. Compute $M(x)$ for held-out in-distribution inputs and for OOD inputs, and choose $\tau$.
4. Report AUROC and the false positive rate at 95% true positive rate.

## Results

The paper reports that the method achieves state-of-the-art performance for detecting both out-of-distribution and adversarial samples in its experiments. Most earlier methods had been evaluated on only one of these two problems. The abstract also reports that the method is more robust in harder settings, such as training data with noisy labels or with few samples. The exact figures are in the paper and were not re-run for this page.

## Limitations

- **Gaussian assumption.** The features of a class may not be well described by a single Gaussian with a shared covariance, which can make the score a poor fit for some classes.
- **Covariance estimation.** The covariance matrix has one row and column per feature. When the feature dimension is large relative to the number of training examples, the estimate is noisy and typically needs regularisation.
- **Labels and layer choice.** The method needs labelled training data to form the class means, and its performance depends on which layer's features are used.
- **Tuning with outliers.** Some settings in the paper are chosen with validation data that include OOD examples. Hsu et al. (2020) point out that tuning on OOD data is hard to justify when such data are not known in advance.

## Open questions

- Which layers carry the most useful information about unfamiliarity, and can they be chosen without outlier data?
- Does a non-parametric alternative do better? Sun et al. (2022) replace the Gaussian with nearest-neighbour distance and report that it avoids the distributional assumption.

## Connections

The method is a Gaussian density model applied to features, which connects it to the [anomaly detection](../../../paradigms/unsupervised/anomaly-detection/index.md) page, where density-based detectors play a similar role. Because it uses intermediate features rather than output probabilities, it does not depend directly on the softmax confidence that the [maximum softmax probability](../max-softmax-probability/index.md) baseline and the [energy score](../energy-score/index.md) work from.

The paper treats adversarial inputs and OOD inputs together, which places it alongside [adversarial examples and robustness](../../adversarial-robustness/index.md). A brain analogy is the idea that perception compares an input with an internal model of typical inputs, as in [predictive coding](../../../../brain-mind/predictive-coding/index.md).

## References

### Seminal papers

- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. arXiv. https://arxiv.org/abs/1807.03888 — Proposes the Mahalanobis distance score for OOD and adversarial inputs, with class-conditional Gaussians in feature space (NeurIPS 2018).
- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — Proposes the maximum softmax probability baseline that the Mahalanobis score is compared against (ICLR 2017).
- Sun, Y., Ming, Y., Zhu, X. & Li, Y. (2022). *Out-of-Distribution Detection with Deep Nearest Neighbors*. arXiv. https://arxiv.org/abs/2204.06507 — Replaces the Gaussian assumption with nearest-neighbour distance in feature space (ICML 2022).

### Surveys and textbooks

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — Surveys classification-based, density-based and distance-based OOD methods.

### Articles and documentation

- Hsu, Y.-C., Shen, Y., Jin, H. & Kira, Z. (2020). *Generalized ODIN: Detecting Out-of-distribution Image without Learning from Out-of-distribution Data*. arXiv. https://arxiv.org/abs/2002.11297 — Discusses why tuning detectors on outlier data biases their evaluation, and proposes an alternative.
