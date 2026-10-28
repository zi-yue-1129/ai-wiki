---
status: complete
last_reviewed: 2026-10-28
aliases:
  - 差分隱私
  - DP-SGD
  - Differential privacy
---

# Differential Privacy

!!! info "Part of Privacy and Data Protection"
    This method page belongs to [Privacy and Data Protection](index.md). It explains the method in detail; the parent page compares it with other protections.

Differential privacy is a formal definition of privacy for data analysis. It guarantees that the output of an analysis changes only slightly when any one person's record is added or removed. Dwork et al. (2006) introduced the definition and the noise-based mechanisms that achieve it. In machine learning, the same idea is applied during training, where it limits how much any single example can shape the model.

## Problem

An analysis or a trained model can reveal information about individuals even when it is meant to describe a population. Anonymising the records is not enough, because the output of a statistic can still expose a person. The problem is to release useful results with a guarantee that does not depend on what an attacker already knows.

## Core idea

Add random noise to the output, scaled to how much one record could change the answer. If the answer barely changes whether or not a given person is included, an observer learns little about that person. The amount of noise is set by two numbers: the privacy parameter ε (smaller means stronger privacy) and, for the relaxed version, δ.

## How it works

**The definition.** A randomised mechanism \(M\) is \(\varepsilon\)-differentially private if, for every pair of datasets \(D\) and \(D'\) that differ in one record, and every set of outputs \(S\),

\[
\Pr[M(D)\in S] \le e^{\varepsilon}\,\Pr[M(D')\in S].
\]

**The Laplace mechanism.** For a numeric query with sensitivity \(\Delta f\), the mechanism returns \(f(D)\) plus Laplace noise with scale \(\Delta f / \varepsilon\).

**In training (DP-SGD).** Abadi et al. (2016) adapted this idea to stochastic gradient descent: each example's gradient is limited in size, and noise is added to the combined gradient before each update. A privacy accountant then tracks the total privacy cost across all training steps.

## Results

Dwork et al. (2006) give a formal guarantee and a method for calibrating noise, rather than an empirical benchmark. Abadi et al. (2016) report that deep neural networks with non-convex objectives can be trained under a modest privacy budget. The exact accuracy trade-off depends on the task, the dataset and the privacy budget, so comparisons should be made against the specific paper.

## Limitations

- **Accuracy cost.** Noise lowers accuracy. The loss is usually largest for small groups, which can raise fairness concerns (see [Ethics & Fairness](../ethics/index.md)).
- **Budget use.** Each release spends part of a privacy budget, so repeated queries weaken the guarantee unless the budget is tracked.
- **Scope.** The guarantee covers the records in the dataset. It does not stop a model from learning general facts, and it does not by itself stop memorisation of public data that appears outside the protected dataset.
- **Choosing ε.** The definition does not say what value of ε is acceptable. That is a policy choice.

## Connections

- Membership inference is the attack that differential privacy is designed to limit. See [Membership Inference](membership-inference.md).
- Memorisation of training text is the risk that DP-SGD reduces. See [Training Data Extraction](training-data-extraction.md).
- Federated learning often combines secure aggregation with differential privacy; see [Federated & Privacy-Preserving Learning](../../theory/paradigms/federated/index.md).

## Open questions

- How should the privacy budget be chosen and communicated to people whose data is used?
- Can DP training reach accuracy close to non-private training for large language models at practical cost?
- How should the guarantee be explained when the protected unit is a person but the model also learns from public text?

## References

### Seminal papers

- Dwork, C., McSherry, F., Nissim, K. & Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference (TCC)*. https://doi.org/10.1007/11681878_14 — Introduces differential privacy and the noise-calibration framework used across the field.
- Abadi, M. et al. (2016). Deep learning with differential privacy. *ACM CCS*. https://arxiv.org/abs/1607.00133 — DP-SGD, the method for training deep models with a differential privacy guarantee.
- Shokri, R., Stronati, M., Song, C. & Shmatikov, V. (2017). Membership inference attacks against machine learning models. *IEEE Symposium on Security and Privacy*. https://arxiv.org/abs/1610.05820 — The attack that differential privacy is meant to limit.
- Yeom, S., Giacomelli, I., Fredrikson, M. & Jha, S. (2018). Privacy risk in machine learning: Analyzing the connection to overfitting. arXiv:1709.01604. https://arxiv.org/abs/1709.01604 — Shows that overfitting alone is enough for membership inference, which explains why limiting memorisation matters.

### Surveys and textbooks

- Dwork, C. & Roth, A. (2014). *The Algorithmic Foundations of Differential Privacy*. Foundations and Trends in Theoretical Computer Science, 9(3–4). https://doi.org/10.1561/0400000042 — The standard textbook, with the mechanisms and proofs in full.
