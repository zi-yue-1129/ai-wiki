---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# Root Mean Squared Error

Root mean squared error (RMSE) is the square root of the average squared difference between predictions and true values. It is in the same units as the target, like [MAE](mae.md), but it penalises large errors more heavily.

## Definition

$$\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (\hat{y}_i - y_i)^2}$$

A perfect model scores 0. Taking the square root returns the value to the units of the target.

## Interpretation

Squaring makes a single error of size 10 count as much as a hundred errors of size 1. RMSE is therefore sensitive to outliers and rare large errors. It is the quantity that a least-squares fit minimises, which is why it is common in regression training and in forecasting. Willmott and Matsuura (2005) note that RMSE mixes the average error with its variability, so a large RMSE does not by itself indicate large average error.

## When to use it

Use RMSE when large errors are disproportionately costly, or when the target is assumed to have roughly Gaussian errors. Report it with MAE when the two disagree, because the gap between them shows how much a few large errors drive the score.

## Pitfalls

- **Outliers.** A few extreme errors can dominate RMSE. Check the error distribution, not only the summary.
- **Comparison with MAE.** RMSE is always at least as large as MAE on the same data, so the two cannot be compared as if they were the same quantity.

## Related metrics

[MAE](mae.md) is the linear counterpart. [R²](r-squared.md) rescales the error against a baseline. The family overview is [Regression Metrics](index.md).

## References

### Articles and documentation

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — Discusses how RMSE mixes average error with variability in the errors.
- scikit-learn contributors. *root_mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html — API reference for the root mean squared error, with its parameters and worked examples.
