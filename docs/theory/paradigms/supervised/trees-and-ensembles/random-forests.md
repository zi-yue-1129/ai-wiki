---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/trees-and-ensembles
  - theory/paradigms/supervised/kernel-methods-svm
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/evaluation-and-validation
tags:
  - supervised learning
  - ensembles
  - tabular data
aliases:
  - Random forest
  - RF
  - 隨機森林
---

# Random Forests

A random forest averages many decision trees. Each tree is grown on a bootstrap sample of the training data, and at every split it may consider only a random subset of the features. Breiman (2001) showed that this extra randomness makes the trees less correlated, and that the error of the forest depends on the strength of the individual trees and on how correlated they are. The family-level picture is on the [Decision Trees and Ensembles](index.md) page.

## Overview

Bagging already reduces the variance of an unstable learner by averaging trees trained on resamples. In bagged trees, however, the strongest feature tends to be chosen near the root of nearly every tree, so the trees make similar errors and averaging removes less error than it could. Breiman's random forest breaks this similarity by restricting each split to a random subset of features.

The method needs little tuning, handles mixed feature types without scaling, and gives an error estimate from the training data alone through out-of-bag samples. For these reasons it is a common first model for tabular problems.

## Key concepts

- **Bootstrap sample**: a sample of the training set of the same size, drawn with replacement. Each tree sees its own sample.
- **Feature subset size F**: the number of features considered at each split. Breiman tried F = 1 and a second default, the first integer less than \(\log_2 M + 1\), where \(M\) is the number of inputs.
- **Out-of-bag (OOB) estimate**: each training point is left out of about a third of the bootstrap samples, so the trees that did not see it can predict it. Their errors give an estimate of generalisation error without a separate test set.
- **Strength and correlation**: strength measures how accurate each tree is, and correlation measures how similar the errors of two trees are. Breiman's analysis expresses the forest's generalization error in terms of these two quantities.

## How it works

For \(t = 1, \dots, T\):

1. Draw a bootstrap sample of size \(n\) from the training set.
2. Grow a tree on that sample. At each node, choose the best split among a random subset of \(F\) features.

Then combine the trees. For classification, take a majority vote. For regression, average the predictions:

\[
\hat f(x) = \frac{1}{T}\sum_{t=1}^{T} h_t(x)
\]

Breiman's paper argues that adding trees does not make the forest overfit. Because more trees do not hurt, the number of trees can be set large instead of being tuned for early stopping as in boosting.

## Key methods

### Random Forests (Breiman, 2001)

- **Problem:** Single trees have high variance, and bagged trees often remain correlated because the same strong feature drives many of their splits. The ensemble needs trees that are both accurate and different from one another.
- **Core idea:** At each node, split using only a random subset of features. The smaller the subset, the less correlated the trees become, at some cost in each tree's strength. The paper states the goal directly: the randomness should aim for low correlation while keeping reasonable strength.
- **Equation or algorithm:** the bootstrap-and-vote procedure and the averaging rule above. The out-of-bag error for a training point \(i\) is the error of the average over only those trees whose bootstrap sample excludes \(i\).
- **Results:** On the synthetic data of Section 9, with 1,000 binary inputs and a Bayes error of 1.0%, the forest with F = 25 reached 2.8% test error. With F = 1 it reached 10.7%. On the breast cancer data in Table 2, the forest that splits on a single random feature (F = 1) reached 2.7% test error against 3.2% for AdaBoost. The paper reports these as published values from its experiments.
- **Limitations:** A forest is harder to interpret than one tree. Averaging piecewise-constant trees cannot extrapolate beyond the range of the training targets. Memory and prediction time grow with the number of trees. Correlated input features spread importance across many variables, which weakens variable-importance measures.

## Connections

- The method is the variance-reducing counterpart of [Gradient Boosting](gradient-boosting.md), which reduces bias by fitting trees in sequence.
- Its alternatives on tabular data, and the wider comparison with margin methods, are on the [Support Vector Machines](../kernel-methods-svm/svm.md) page.
- Error estimates from out-of-bag samples connect to the methods in [Evaluation and Validation](../evaluation-and-validation/index.md).
- The theory of why forests generalise is covered in [Generalization Theory](../generalization-theory/index.md).

## Open questions

- Why do forests generalise so well even though individual deep trees fit the training data almost exactly?
- Which default for the feature subset size works across tasks, and when does tuning it matter?

## References

### Seminal papers

- Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324 — Introduces random feature selection at each split, the out-of-bag error estimate and the strength and correlation analysis.
- Breiman, L. (1996). Bagging predictors. *Machine Learning*, 24, 123–140. https://doi.org/10.1007/BF00058655 — Introduces bootstrap aggregation, the averaging idea that random forests build on. The paper argues that the instability of the prediction method is the vital element.
- Ho, T. K. (1995). Random decision forests. *Proceedings of the Third International Conference on Document Analysis and Recognition (ICDAR 1995)*. https://doi.org/10.1109/ICDAR.1995.598994 — An early proposal for tree ensembles grown on random feature subsets.
- Amit, Y. & Geman, D. (1997). Shape quantization and recognition with randomized trees. *Neural Computation*, 9(7), 1545–1588. https://doi.org/10.1162/neco.1997.9.7.1545 — Uses randomised trees for shape recognition, an early source of the random-feature idea.

### Surveys and textbooks

- Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer. https://doi.org/10.1007/978-0-387-84858-7 — Chapters on trees, boosting and random forests, with a free PDF from the authors.
- Scornet, E., Biau, G. & Vert, J.-P. (2015). Consistency of random forests. *Annals of Statistics*. https://doi.org/10.1214/15-AOS1321 — Proves consistency of Breiman's original forest algorithm in additive regression models.
