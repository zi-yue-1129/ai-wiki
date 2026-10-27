---
tags:
  - supervised learning
  - ensembles
  - tabular data
---

# Decision Trees and Ensembles

Tree-based methods split the input space into regions with simple rules, and ensembles combine many trees. On tabular data, gradient-boosted trees are still usually the strongest practical choice.

## Decision trees

A tree recursively picks the feature and threshold that best separates the labels, using an impurity measure: Gini impurity $1-\sum_k p_k^2$ or entropy $-\sum_k p_k\log p_k$ for classification, variance for regression (CART, Breiman et al. 1984; ID3/C4.5, Quinlan). A single deep tree has low bias and high variance; pruning or depth limits control it. Trees need no feature scaling, handle mixed data types and missing values, and give readable rules.

## Bagging and random forests

**Bagging** trains many trees on bootstrap resamples and averages them, which reduces variance. **Random forests** (Breiman, 2001) also pick a random subset of features at every split, which decorrelates the trees. Out-of-bag samples give a free validation estimate. Forests are robust, need little tuning and rarely overfit badly.

## Boosting

Boosting builds trees sequentially, each one correcting the errors of the ensemble so far.

- **AdaBoost** re-weights misclassified examples.
- **Gradient boosting** (Friedman, 2001) fits each new tree to the negative gradient of the loss, so $F_m = F_{m-1} + \eta\, h_m$.
- **XGBoost, LightGBM, CatBoost** add second-order information, regularisation, histogram-based splits and better handling of categorical features.

| Method | Reduces | Trees are | Tuning effort |
|---|---|---|---|
| Bagging / forest | Variance | Deep, independent | Low |
| Boosting | Bias (and some variance) | Shallow, sequential | Medium |

## Stacking and other ensembles

Stacking trains a meta-model on the predictions of diverse base models. Averaging several neural networks (deep ensembles) is also a strong baseline for uncertainty estimates.

## Connections

Why do trees beat deep networks on many tabular tasks? Grinsztajn et al. (2022) point to irregular target functions and uninformative features, where trees are more robust. Tree ensembles are widely used in finance, healthcare risk scoring and recommender ranking; see [Applications](../../../../applications/index.md).

## Further reading

- Quinlan (1986), "Induction of decision trees", *Machine Learning* 1(1). The ID3 algorithm.
- Breiman (2001), "Random forests", *Machine Learning* 45(1). Introduces bagged trees with random feature selection.
- Friedman (2001), "Greedy function approximation: a gradient boosting machine", *Annals of Statistics* 29(5). Derives gradient boosting as functional gradient descent.
- Chen & Guestrin (2016), "XGBoost: a scalable tree boosting system", KDD, arXiv:1603.02754.
- Ke et al. (2017), "LightGBM: a highly efficient gradient boosting decision tree", NeurIPS. Histogram-based splits and leaf-wise growth.
- Prokhorenkova et al. (2018), "CatBoost: unbiased boosting with categorical features", NeurIPS. Ordered boosting for categorical data.
- Grinsztajn, Oyallon & Varoquaux (2022), "Why do tree-based models still outperform deep learning on tabular data?", arXiv:2207.08815. Benchmark and analysis.
- Video: StatQuest with Josh Starmer (YouTube channel), episodes on random forests and gradient boosting.
