---
status: complete
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# Regression Metrics

Regression metrics compare a predicted number with the true number. They differ mainly in how they treat large errors and in whether they are read on the scale of the target or relative to a baseline. Choosing one is a decision about which kind of error matters.

## Problem

Given true values \(y_i\) and predictions \(\hat y_i\) for \(n\) examples, a metric has to turn these pairs into one number. The choice fixes three things: the units of the result, how strongly large errors count, and whether the score is judged against a trivial predictor.

## Key concepts

- **Residual:** the error \(y_i - \hat y_i\) for one example.
- **Scale:** a metric in the units of the target is easy to read, while a unitless one can be compared across targets.
- **Baseline:** a reference predictor, usually the mean of the targets, that a unitless score compares against.

## Key methods

### Mean absolute error (MAE)

\[
\mathrm{MAE} = \frac{1}{n} \sum_{i=1}^{n} \lvert y_i - \hat y_i \rvert
\]

MAE averages the size of the errors, in the units of the target, and penalises large errors linearly. The details are on the [MAE](mae.md) page.

- **Results:** Willmott and Matsuura (2005) argue that MAE is a more natural measure of average model error than RMSE, because RMSE mixes the average error with the variance of the errors.
- **Limitations:** MAE does not distinguish a few large errors from many moderate ones, and it says nothing about the sign of the error.

### Root mean squared error (RMSE)

\[
\mathrm{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat y_i)^2}
\]

RMSE is also in the units of the target, but squaring before averaging penalises large errors more than MAE does. The details are on the [RMSE](rmse.md) page.

- **Limitations:** RMSE is dominated by the largest errors, so one outlier can change it substantially. By the inequality between the quadratic and the arithmetic mean, RMSE is never smaller than MAE, with equality only when all absolute errors are equal.

### Coefficient of determination (R²)

\[
R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat y_i)^2}{\sum_{i=1}^{n} (y_i - \bar y)^2}, \qquad \bar y = \frac{1}{n} \sum_{i=1}^{n} y_i
\]

R² compares the squared error of the model with that of predicting the mean, so 1 is a perfect fit and 0 matches the mean predictor. The details are on the [R²](r-squared.md) page.

- **Limitations:** R² can be negative for predictions worse than the mean. It can mislead when the test targets have a different spread from the training targets, because the denominator changes.

## Connections

Choosing between MAE and RMSE is also a choice about the loss used in training: squared-error training pulls predictions towards the mean, while absolute-error training pulls them towards the median. The metrics for predicted probabilities are covered in [probabilistic metrics](../probabilistic/index.md).

## Open questions

- How to report regression error when the target spans orders of magnitude, where relative errors may be the right scale.
- How the choice of metric should follow the cost of errors in a specific application.

## References

### Articles and documentation

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://doi.org/10.3354/cr030079 — Argues that MAE is a more natural measure of average model error than RMSE.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the regression scorers and their definitions.

### Additional sources

- scikit-learn contributors. *mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html — API reference for mean squared error, the squared form of RMSE, with a worked example.
- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
