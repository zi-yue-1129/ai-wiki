---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# Mean Absolute Error

Mean absolute error (MAE) is the average of the absolute differences between predictions and true values. It is in the same units as the target and treats every unit of error the same, whatever its size.

## Definition

$$\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |\hat{y}_i - y_i|$$

A perfect model scores 0. The value is a typical size of error, so an MAE of 2 means predictions are off by 2 units on average.

## Interpretation

Because MAE grows linearly with each error, a few very large errors have a proportionate effect rather than a dominant one. Its minimiser is the median of the errors, so a model trained to minimise MAE predicts something close to the conditional median rather than the mean. Willmott and Matsuura (2005) argue that this makes MAE the more natural measure of average model performance.

## When to use it

Use MAE when the error costs grow in proportion to the size of the error, and when results should be reported in the units of the target. It is also a sensible default when outliers in the target are real but should not dominate the score.

## Pitfalls

- **Scale.** MAE cannot be compared across targets with different units. Normalise the target, or report a relative metric such as [R²](r-squared.md) for cross-task comparison.
- **Zero targets.** Relative errors built on MAE need care when true values are near zero; the absolute form avoids this but does not show proportional error.

## Related metrics

[RMSE](rmse.md) is the squared-error counterpart and penalises large errors more. The family overview is [Regression Metrics](index.md).

## References

### Articles and documentation

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — Argues for MAE as a measure of average model error.
- scikit-learn contributors. *mean_absolute_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html — API reference for the regression loss, with a worked example.

### Additional sources

- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the scorers for classification, regression and ranking, and when each is appropriate.
- scikit-learn contributors. *mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html — API reference for mean squared error, the squared form of RMSE, with a worked example.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
