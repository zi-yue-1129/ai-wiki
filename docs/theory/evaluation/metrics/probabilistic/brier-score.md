---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - calibration
---

# Brier Score

The Brier score is the mean squared difference between each predicted probability and the observed outcome. It is the probabilistic counterpart of mean squared error, and it is bounded, so one bad prediction cannot dominate the way it can with [log-loss](log-loss.md).

## Definition

For a binary outcome $y \in \{0, 1\}$ and predicted probability $p$, averaged over $n$ samples:

$$\text{Brier} = \frac{1}{n} \sum_{i=1}^{n} (p_i - y_i)^2$$

Lower is better. Predicting $p = 0.5$ everywhere gives 0.25, a simple baseline. The score is 0 only when every prediction is correct and fully confident.

## Interpretation

Because the squared error is bounded, a confident mistake costs at most 1 for that sample, while log-loss has no upper limit. The Brier score is a proper scoring rule, so it is minimised by reporting true probabilities.

## When to use it

Use the Brier score when the probabilities are used directly and a single bounded measure is wanted, or when outliers in the predictions should not dominate the result.

## Worked example

Using the same predictions, the squared errors are $0.01$, $0.64$, $0.09$ and $0.16$. The Brier score is their mean, $0.225$. Unlike log loss, the squared error is bounded, so one confident mistake adds at most 1 to a case's contribution.

## Pitfalls

- **Rare events.** For a rare outcome, a model that predicts a small constant probability has a low Brier score without any skill. Compare it with the base rate, $p_{\text{base}}(1 - p_{\text{base}})$, as a baseline.
- **Ranking only.** The score measures probability quality. A model can rank cases well and still score poorly if its probabilities are miscalibrated.

## Related metrics

[Log-loss](log-loss.md) penalises confident errors more strongly. [Calibration error](calibration-error.md) isolates the calibration part. The family overview is [Probabilistic Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *brier_score_loss*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html — API reference describing the score as the mean squared difference between predicted probability and actual outcome.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of scorers that use predicted probabilities.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- Niculescu-Mizil, A. & Caruana, R. (2005). Predicting good probabilities with supervised learning. ICML. https://doi.org/10.1145/1102351.1102430 — Compares probability calibration across common classifiers and the effect of calibration methods.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
