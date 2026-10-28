---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# R² (Coefficient of Determination)

$R^2$ compares a model's squared error with the error of a baseline that always predicts the mean of the true values. It reads as the share of variance the model explains, and it is unitless, so it can be compared across targets with different scales.

## Definition

$$R^2 = 1 - \frac{\sum_{i}(y_i - \hat{y}_i)^2}{\sum_{i}(y_i - \bar{y})^2}$$

where $\bar{y}$ is the mean of the true values. A perfect model scores 1.0. A model that always predicts $\bar{y}$ scores 0.0, and a model worse than that scores below zero. scikit-learn's documentation gives the example of predictions that are the reverse of the truth, which score −3.0 (see References).

## Interpretation

$R^2$ answers a different question from MAE or RMSE. Those tell how large the errors are; $R^2$ tells whether the model does better than the mean. A low $R^2$ with a small RMSE can happen when the target has little variance, so both should be read together.

## When to use it

Use $R^2$ to summarise how much of the target's variation a model explains, and to compare models on the same data. It is less useful for judging forecast accuracy in the units that matter to a user.

## Pitfalls

- **Test-set variance.** $R^2$ depends on the variance of the test targets. A model can score well on one dataset and poorly on another with the same errors.
- **Non-linear and out-of-sample use.** On held-out data, $R^2$ can be negative. It is not bounded below by zero.
- **Not a fit guarantee.** A high $R^2$ does not show that the model is correct, only that its errors are small relative to the spread of the target.

## Related metrics

[MAE](mae.md) and [RMSE](rmse.md) give the error in the units of the target. The family overview is [Regression Metrics](index.md).

## References

### Articles and documentation

- scikit-learn contributors. *r2_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html — API reference that gives the definition, the best value of 1.0, the meaning of negative values, and a worked example.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of regression scorers and how they are used.

### Additional sources

- Murphy, K. P. *Probabilistic Machine Learning: An Introduction*. MIT Press, 2022. https://probml.github.io/pml-book/book1.html — Textbook with a free online draft on probabilistic machine learning.
- scikit-learn contributors. *mean_squared_error*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html — API reference for mean squared error, the squared form of RMSE, with a worked example.
- *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd edition. https://hastie.su.domains/ElemStatLearn/ — Standard textbook on statistical learning and its evaluation.
