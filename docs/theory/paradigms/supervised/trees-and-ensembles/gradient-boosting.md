---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/trees-and-ensembles
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/paradigms/supervised/evaluation-and-validation
  - theory/paradigms/supervised/kernel-methods-svm
tags:
  - supervised learning
  - ensembles
  - boosting
aliases:
  - Gradient boosting
  - GBDT
  - GBM
  - XGBoost
  - LightGBM
  - CatBoost
  - 梯度提升
  - 梯度提升機
---

# Gradient Boosting

Gradient boosting builds an additive model in stages. At each stage a small tree is fitted to the negative gradient of the loss at the current predictions, and that tree is added with a step size. Friedman (2001) presented this as steepest descent in function space. XGBoost (Chen & Guestrin, 2016) is a scalable system for the same idea, and LightGBM and CatBoost are later systems built on it. The family-level picture is on the [Decision Trees and Ensembles](index.md) page.

## Overview

Boosting fits models in sequence, each one correcting the errors of the ensemble so far. Gradient boosting makes this general. Instead of re-weighting examples for a particular loss, it treats the current predictions as a point in function space and moves them downhill. The direction at each step is given by the gradient of the loss at every training point, and a regression tree approximates that direction.

This framing makes it possible to use many losses, from squared error for regression to multiclass logistic loss for classification. Each tree is kept shallow so that each step stays simple, and the step size and the number of trees control how far the ensemble moves toward the training data.

## Key concepts

- **Additive model**: the prediction is a sum of trees, \(F_M(x) = \sum_m \nu\, h_m(x)\), with each tree built on the residual signal left by the earlier ones.
- **Pseudo-residual**: the negative gradient of the loss with respect to the current prediction, \(r_{im} = -\partial L(y_i, F(x_i))/\partial F(x_i)\) at \(F = F_{m-1}\). For squared loss it is the ordinary residual \(y_i - F_{m-1}(x_i)\).
- **Weak learner**: a shallow regression tree fitted to the pseudo-residuals.
- **Learning rate or shrinkage** \(\nu\): a factor between 0 and 1 that scales each tree's contribution. Smaller values need more trees.
- **Subsampling**: fitting each tree to a random subset of rows, a common variant for speed and regularisation.

## How it works

1. Start from a constant prediction \(F_0\) that best fits the loss.
2. For \(m = 1, \dots, M\):
   - compute the pseudo-residuals \(r_{im}\) at the current predictions \(F_{m-1}\);
   - fit a regression tree \(h_m\) to the pairs \((x_i, r_{im})\);
   - update \(F_m = F_{m-1} + \nu\, h_m\).

For squared loss, the pseudo-residuals are the plain residuals, so each tree fits what the ensemble still gets wrong. For other losses, the same recipe applies once the gradient is known. The number of trees \(M\) and the learning rate are normally chosen with a validation set, because too many trees fit noise.

## Key methods

### Greedy function approximation: a gradient boosting machine (Friedman, 2001)

- **Problem:** Boosting was tied to particular losses and to a particular reweighting rule. A general method was needed that works for any differentiable loss and can handle regression and classification with one framework.
- **Core idea:** View a stagewise additive expansion as numerical optimisation in function space rather than parameter space. Each stage is a steepest-descent step. The step is approximated by fitting a weak learner to the negative gradient, which makes the method general.
- **Equation or algorithm:** the stagewise procedure above, with the pseudo-residual definition and the update \(F_m = F_{m-1} + \nu h_m\).
- **Results:** The abstract presents specific algorithms for least squares, least absolute deviation and Huber-M regression, and for multiclass logistic likelihood in classification. It reports no benchmark figures, so none are stated here.
- **Limitations:** The procedure is greedy. Without a shrinkage factor or a stopping rule chosen on held-out data, the ensemble can overfit. Trees are built one after another, so boosting does not parallelise across trees the way a forest does.

### XGBoost: A Scalable Tree Boosting System (Chen & Guestrin, 2016)

- **Problem:** Gradient-boosted trees were slow to train on very large data sets, and handling sparse inputs needed care. The method needed to scale without losing accuracy.
- **Core idea:** A complete tree boosting system with a sparsity-aware algorithm for split finding and a weighted quantile sketch for approximate split finding. The abstract also points to attention to cache access patterns, data compression and sharding, which are engineering choices for speed.
- **Equation or algorithm:** the same stagewise update \(F_m = F_{m-1} + \nu\, h_m\) as Friedman's method. The regularised objective and the split-gain formula used by the system are not reproduced here, because they were not checked against the paper in this pass.
- **Results:** The abstract states that XGBoost "scales beyond billions of examples using far fewer resources than existing systems." Its benchmark tables were not checked in this pass, so no speed-up or accuracy figures are given here.
- **Limitations:** The system has many hyperparameters, including depth, learning rate, regularisation and subsampling settings, that interact. It inherits the sequential nature of boosting. The abstract makes a scaling claim, not a claim about accuracy against every alternative.

### LightGBM (Ke et al., 2017)

- **Problem:** On large data, finding the best split for every feature over every example is the main cost of gradient boosting.
- **Core idea:** Gradient-based one-side sampling (GOSS) excludes a significant proportion of the instances with small gradients, so that split search runs on fewer examples. Exclusive feature bundling (EFB) bundles features that rarely take non-zero values at the same time, which reduces the number of features to scan.
- **Equation or algorithm:** no closed form is given here. The method is the gradient boosting procedure above with GOSS sampling and EFB bundling applied at each split search.
- **Results:** The abstract states that LightGBM "speeds up the training process of conventional GBDT by up to over 20 times." The phrase "up to" marks this as a best-case figure, and the experiments behind it were not checked in this pass.
- **Limitations:** The speed-up depends on the data set, and the abstract gives it as an upper bound ("up to"). The paper's experiments were not checked in this pass.

### CatBoost (Prokhorenkova et al., 2017)

- **Problem:** The abstract describes the problem as a prediction shift caused by a special kind of target leakage, which affects boosting when categorical features are present.
- **Core idea:** Ordered boosting is a permutation-driven alternative to the classic boosting algorithm. The paper also introduces an innovative algorithm for processing categorical features. Both address the same prediction shift.
- **Equation or algorithm:** the algorithm is described in the paper and is not reproduced here.
- **Results:** The abstract does not report numerical results, so none are stated here.
- **Limitations:** The benefit is argued mainly for categorical features and for the prediction shift. The size of the gain on purely numeric tables is not stated in the abstract.

## Connections

- Random forests reduce variance by averaging independent trees. Gradient boosting reduces bias by fitting trees in sequence. See [Random Forests](random-forests.md).
- The pseudo-residual is the negative gradient of a loss, so the choice of loss is part of the method. See [Loss Functions and Optimization](../loss-functions-and-optimization/index.md).
- The number of trees and the learning rate are usually chosen by validation and early stopping. See [Evaluation and Validation](../evaluation-and-validation/index.md).
- On tabular data, boosted trees are compared with margin methods such as the [Support Vector Machine](../kernel-methods-svm/svm.md).

## Open questions

- How much of the gap between the newer systems comes from the algorithm, and how much comes from engineering for speed?
- Which combination of learning rate, tree depth and number of trees gives the best accuracy with the least tuning?

## References

### Seminal papers

- Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics*, 29(5), 1189–1232. https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boosting-machine/10.1214/aos/1013203451.full — Frames boosting as steepest descent in function space, which allows many losses.
- Chen, T. & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD 2016*. https://arxiv.org/abs/1603.02754 — The XGBoost system, with a sparsity-aware split algorithm and a weighted quantile sketch for scalable training.
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q. & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems 30 (NIPS 2017)*. https://papers.nips.cc/paper/6907-lightgbm-a-highly-efficient-gradient-boosting-decision-tree — Introduces GOSS and EFB to speed up gradient boosting on large data.
- Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V. & Gulin, A. (2017). CatBoost: Unbiased boosting with categorical features. arXiv:1706.09516. https://arxiv.org/abs/1706.09516 — Introduces ordered boosting and an ordered target-statistics scheme against prediction shift.

### Surveys and textbooks

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-84858-7 — Chapters on boosting and tree ensembles, with a free PDF from the authors.
