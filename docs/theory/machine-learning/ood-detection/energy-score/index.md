---
status: draft
last_reviewed: 2026-10-28
tags:
  - distribution shift
  - anomaly detection
  - evaluation
aliases:
  - 能量分數
  - 能量函數
  - Energy score
  - Energy-based OOD detection
---

# Energy Score

The energy score is an out-of-distribution score computed from a classifier's logits. It replaces the softmax confidence with a log-sum-exp of the logits, which keeps information about their overall size that the softmax throws away. Liu et al. (2020) proposed it as a more reliable score than the softmax, and as a training objective. It is one of the scores described on the [out-of-distribution detection](../index.md) page.

## Overview

The [maximum softmax probability](../max-softmax-probability/index.md) baseline reads the largest class probability. Softmax normalisation makes that probability unchanged when the same constant is added to every logit, so the baseline cannot see how large the logits are. Liu et al. (2020) argue that this makes softmax scores overconfident on out-of-distribution data. Their energy score keeps the logit magnitude. The authors state that energy is theoretically aligned with the probability density of the inputs. The method can be applied to any pre-trained classifier, and the paper also proposes training with energy-based objectives.

## Key concepts

- **Logit.** The raw score a network gives each class. The softmax turns logits into probabilities.
- **Log-sum-exp.** The function $\log \sum_i \exp(a_i)$. It behaves like the maximum of the $a_i$ but stays smooth and keeps the scale of the inputs.
- **Energy.** A scalar computed from the logits. In this method, lower energy means the input is more typical of the training data.
- **Energy-based training.** A variant that changes the training objective so that training inputs have low energy and outlier inputs have high energy.

## How it works

For a classifier with logits $f_i(x)$, the energy of an input $x$ is defined with a temperature $T$ as

$$
E(x; f) = -T \log \sum_i \exp\!\big(f_i(x)/T\big).
$$

With $T = 1$ this is the negative log-sum-exp of the logits. An input is flagged as out-of-distribution when its energy is above a threshold $\tau$ chosen on validation data.

Compared with the softmax, the energy keeps the size of the logits. If every logit is shifted by a constant $c$, the softmax probabilities are unchanged, but the energy changes by $-c$. An input with large logits therefore has lower energy than one with small logits, even when both have the same softmax distribution. This is the property the authors exploit.

The procedure is as follows.

1. Train the classifier as usual, or use a pre-trained one.
2. Compute $E(x; f)$ for held-out in-distribution inputs and for OOD test inputs.
3. Choose $\tau$ on validation data and report AUROC and the false positive rate at 95% true positive rate.

## Results

On a CIFAR-10 pre-trained WideResNet, the paper reports that the energy score reduces the average false positive rate at 95% true positive rate by 18.03% compared with the softmax score.[^1] The authors also report that their energy-based training outperforms the state of the art on common benchmarks. The paper compares it with several post-hoc and training-based methods. The exact tables are in the paper and were not re-run for this page.

## Limitations

- **Still a single number.** The energy compresses the logits into one value. Like the softmax score, it ignores the structure of the feature space, which methods such as the [Mahalanobis distance](../mahalanobis-distance/index.md) use.
- **Sensitivity to the logit scale.** The score depends on the overall size of the logits, so it is only as reliable as the training that produced them. A network whose logits are inflated for every input would make the score less informative.
- **Training variant needs outliers.** The energy-based training in the paper uses outlier data, which is hard to define in advance. Post-hoc use of the energy does not need it.

## Open questions

- Do the gains on standard benchmarks carry over to natural distribution shifts?
- When does the logit magnitude carry real evidence of unfamiliarity, and when does it reflect training artefacts?

## Connections

The energy score links the classifier to a density model: the negative energy is the log of an unnormalised density of the input. The [density and generative models](../../../paradigms/unsupervised/density-and-generative-models/index.md) page covers the general idea. The energy-based variant uses outliers in a way similar to Outlier Exposure (Hendrycks et al., 2018).

Liu et al. (2020) frame the score as an answer to the overconfidence that the softmax inherits from training, a concern shared with [uncertainty quantification and calibration](../../uncertainty-and-calibration/index.md).

## References

### Seminal papers

- Liu, W., Wang, X., Owens, J. D. & Li, Y. (2020). *Energy-based Out-of-distribution Detection*. arXiv. https://arxiv.org/abs/2010.03759 — Proposes the energy score for OOD detection, and an energy-based training objective (NeurIPS 2020).
- Hendrycks, D. & Gimpel, K. (2016). *A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks*. arXiv. https://arxiv.org/abs/1610.02136 — Proposes the maximum softmax probability baseline that the energy score is compared against (ICLR 2017).
- Liang, S., Li, Y. & Srikant, R. (2017). *Enhancing The Reliability of Out-of-distribution Image Detection in Neural Networks*. arXiv. https://arxiv.org/abs/1706.02690 — Introduces ODIN, a post-hoc score that uses temperature scaling and input perturbations (ICLR 2018).
- Lee, K., Lee, K., Lee, H. & Shin, J. (2018). *A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks*. arXiv. https://arxiv.org/abs/1807.03888 — Proposes the Mahalanobis distance score in feature space, which the energy score is compared with (NeurIPS 2018).

### Surveys and textbooks

- Yang, J., Zhou, K., Li, Y. & Liu, Z. (2021). *Generalized Out-of-Distribution Detection: A Survey*. arXiv. https://arxiv.org/abs/2110.11334 — Surveys classification-based, density-based and distance-based OOD methods.

### Articles and documentation

- Hendrycks, D., Mazeika, M. & Dietterich, T. (2018). *Deep Anomaly Detection with Outlier Exposure*. arXiv. https://arxiv.org/abs/1812.04606 — Trains detectors against auxiliary outliers, a training approach related to the energy-based variant (ICLR 2019).

[^1]: Figure as reported in the abstract of Liu et al. (2020).
