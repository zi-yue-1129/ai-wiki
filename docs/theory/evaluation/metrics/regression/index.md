---
related:
  - engineering/evaluation
tags:
  - evaluation
  - metrics
  - regression
---

# Regression Metrics

Regression metrics compare a predicted number with the true number. They differ mainly in how they treat large errors and in whether they are read on the scale of the target or relative to a baseline. Choosing one is a decision about what kind of error matters.

## Key metrics

| Metric | What it measures | Units | Large errors |
|---|---|---|---|
| [MAE](mae.md) | Average absolute error | Same as target | Penalised linearly |
| [RMSE](rmse.md) | Square root of average squared error | Same as target | Penalised more than MAE |
| [R²](r-squared.md) | Share of variance explained, relative to predicting the mean | Unitless | Penalised through squared error |

MAE and RMSE are easy to interpret in the units of the target. R² compares the model with a constant baseline and so is useful for asking whether the model explains anything at all, but it can be misleading on data with a different spread from the training data.

## Connections

Willmott and Matsuura (2005) argue that MAE is a more natural measure of average error than RMSE in many settings, because RMSE mixes the average error with the variance of the errors. The metrics for predicted probabilities are covered in [Probabilistic Metrics](../probabilistic/index.md).

## References

### Articles and documentation

- Willmott, C. J. & Matsuura, K. (2005). Advantages of the mean absolute error (MAE) over the root mean square error (RMSE) in assessing average model performance. *Climate Research* 30, 79–82. https://www.int-res.com/abstracts/cr/v30/n1/p79-82/ — Argues that MAE is a more natural measure of average model error than RMSE.
- scikit-learn contributors. *Metrics and scoring: quantifying the quality of predictions*. https://scikit-learn.org/stable/modules/model_evaluation.html — Overview of the regression scorers and their definitions.
