---
status: draft
last_reviewed: 2026-10-28
tags:
  - distribution shift
  - anomaly detection
  - evaluation
aliases:
  - 最大 softmax 機率
  - MSP
  - Maximum Softmax Probability
  - softmax baseline
---

# Maximum Softmax Probability

Maximum softmax probability (MSP) is the simplest post-hoc score for out-of-distribution detection. An input is treated as unfamiliar when the classifier's largest softmax output is low. Hendrycks and Gimpel (2016) proposed it as a baseline, and it is the reference point for later methods. It is one of the scores described on the [out-of-distribution detection](../index.md) page.

## Overview

A classifier trained on known classes always produces a probability for each of them. The MSP baseline assumes that the network is more confident on inputs it knows than on inputs it does not. Hendrycks and Gimpel (2016) found that correctly classified examples tend to have higher maximum softmax probabilities than misclassified or out-of-distribution examples. This gives a usable detector across computer vision, natural language processing and speech recognition tasks. The method needs no change to the network, no extra training and no outlier data. The paper also notes that the baseline can sometimes be surpassed, which left room for later work.

## Key concepts

- **Logit.** The raw score a network assigns to each class before the softmax turns the scores into probabilities.
- **Misclassification detection.** The same score can flag in-distribution inputs that the classifier will get wrong; Hendrycks and Gimpel treat this problem alongside OOD detection.
- **Threshold.** A value chosen on validation data. It sets the trade-off between missed OOD inputs and wrongly flagged ID inputs.

## How it works

Let $f(x)$ be the logit vector for input $x$ and $p_k(x)$ the softmax probability of class $k$. The MSP score and the decision rule are

$$
s_{\text{MSP}}(x) = \max_k p_k(x), \qquad \hat{o}(x) = \mathbb{1}\big[s_{\text{MSP}}(x) < \tau\big].
$$

The procedure is as follows.

1. Train the classifier on in-distribution data, as usual.
2. Compute $s_{\text{MSP}}$ on a held-out in-distribution set and on an out-of-distribution test set.
3. Choose $\tau$ on validation data, for example so that 95% of in-distribution inputs are accepted.
4. Report AUROC, which measures how well the two sets of scores are ordered, and the false positive rate at 95% true positive rate.

## Results

The paper evaluates the baseline on tasks in computer vision, natural language processing and automatic speech recognition. In each case the authors find that correctly classified examples have larger maximum softmax probabilities than misclassified or out-of-distribution examples, so the score separates them to some degree. The abstract describes the baseline as effective across these tasks and notes that it can sometimes be surpassed. Later work reports the baseline's error rates on specific benchmarks; Liang et al. (2017) give one such comparison, in which the false positive rate at 95% true positive rate on a DenseNet trained on CIFAR-10 falls from 34.7% for the baseline to 4.3% with their method.[^1]

## Limitations

- **Inherited overconfidence.** The score is a normalised output of the network. Softmax normalisation forces the probabilities to sum to one, so a large maximum can appear even when the input is far from the training data. Liu et al. (2020) argue that softmax-based scores suffer from overconfident posteriors on OOD data.
- **Dependence on calibration.** If the network is miscalibrated in distribution, the MSP inherits that miscalibration. Guo et al. (2017) showed that modern networks are often poorly calibrated; see [temperature scaling](../../uncertainty-and-calibration/temperature-scaling/index.md).
- **One number.** The score keeps only the largest of the class probabilities. It ignores the overall size of the logits and the shape of the feature space, which the later methods use.

## Open questions

- Why do some OOD datasets fool the maximum softmax probability while others of similar difficulty do not?
- Should misclassification detection and OOD detection share a score, or only look alike?

## Connections

The [energy score](../energy-score/index.md) keeps the logit magnitude that the softmax removes, and was introduced partly as a response to the overconfidence of MSP. The [Mahalanobis distance](../mahalanobis-distance/index.md) instead looks at the feature space and does not rely on the final probabilities. ODIN (Liang et al., 2017) keeps the MSP score but adds temperature scaling and a small input perturbation, which helps separate the two score distributions.

The score is also part of [uncertainty quantification and calibration](../../uncertainty-and-calibration/index.md). Temperature scaling changes the softmax values, and so can change the ordering of MSP scores.

## References

### Seminal papers

- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — Proposes the maximum softmax probability baseline and tests it on vision, language and speech tasks; published at ICLR 2017.
- Liang, S., Li, Y. & Srikant, R. (2017). *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. arXiv. https://arxiv.org/abs/1706.02690 — Introduces ODIN, a modification of the softmax score that uses temperature scaling and input perturbations (ICLR 2018).
- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. arXiv. https://arxiv.org/abs/2010.03759 — Argues that softmax confidence is overconfident on OOD data and proposes the energy score (NeurIPS 2020).
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). *On Calibration of Modern Neural Networks*. arXiv. https://arxiv.org/abs/1706.04599 — Shows that modern networks are poorly calibrated, which affects the reliability of softmax confidence (ICML 2017).

### Surveys and textbooks

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — Surveys classification-based, density-based and distance-based OOD methods.

### Articles and documentation

- Ovadia, Y. et al. (2019). *Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift*. arXiv. https://arxiv.org/abs/1906.02530 — Benchmarks softmax-based uncertainty under dataset shift, where its reliability declines.

[^1]: Figures as reported in the abstract of Liang et al. (2017). The baseline there is the maximum softmax probability method.
