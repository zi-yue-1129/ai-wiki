---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# Log-Loss

Log-loss, also called cross-entropy loss, is the negative average log-likelihood that the model assigns to the true labels. It rewards predicted probabilities that put high weight on the correct outcome, and it penalises confident mistakes heavily.

## Definition

For a binary label $y \in \{0, 1\}$ and predicted probability $p = \Pr(y = 1)$, the loss for one sample is

$$L_{\log}(y, p) = -\big(y \log p + (1 - y) \log(1 - p)\big)$$

The reported value is the mean over all samples. It is the same quantity that logistic regression and neural classifiers minimise during training.

## Interpretation

Predicting $p = 0.5$ for every sample gives a log-loss of $\log 2 \approx 0.693$, a useful baseline. A confident wrong prediction, such as $p = 0.01$ for a true positive, costs $-\log 0.01 \approx 4.6$ on its own, so a few such cases can dominate the average. Lower is better, and the value depends on the class balance as well as on the model.

## When to use it

Use log-loss to compare probabilistic models on the same data, or to monitor a model whose probabilities feed a later decision. Because it is a proper scoring rule, a model minimises its expected value by reporting its true probabilities.

## Worked example

Take four predicted probabilities $p = (0.9, 0.8, 0.3, 0.6)$ for true labels $y = (1, 0, 0, 1)$. The per-case losses are $0.105$, $1.609$, $0.357$ and $0.511$. Their mean, $0.646$, is the log loss. The second case is confidently wrong and dominates the total.

## Properties and variants

- **Proper scoring rule.** Log loss is the negative log-likelihood of a Bernoulli model. Its expected value $-\mathbb{E}[\,y \log q + (1 - y) \log(1 - q)\,]$ is minimised when $q$ equals the true probability, which is why it rewards honest probabilities.
- **Unbounded.** A predicted probability of exactly 0 for a true positive gives infinite loss, so implementations clip probabilities to $[\epsilon, 1 - \epsilon]$. The clipping constant is a convention and should be reported.
- **Multi-class.** With softmax outputs, the same quantity is the cross-entropy over classes.
- **Limit.** A few confident mistakes can dominate the mean, so a model can rank well and still have a poor log loss.

## Pitfalls

- **Outliers.** A single extreme wrong prediction can raise the average sharply. Clip probabilities away from 0 and 1 only with a stated bound.
- **Mixed goals.** Log-loss combines ranking and calibration. To see which one is failing, read it together with [calibration error](calibration-error.md).

## Related metrics

The [Brier score](brier-score.md) is the squared-error counterpart. The family overview is [Probabilistic Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *log_loss*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html — API reference giving the binary and multiclass definition, with a worked example.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Places log-loss among the scorers that use predicted probabilities.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- Guo, C. et al. (2017). On calibration of modern neural networks. ICML. https://arxiv.org/abs/1706.04599 — Shows that modern networks are overconfident and that temperature scaling corrects it.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
