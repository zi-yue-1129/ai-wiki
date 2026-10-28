---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/supervised/kernel-methods-svm
  - theory/paradigms/supervised/linear-models
  - theory/paradigms/supervised/loss-functions-and-optimization
  - theory/paradigms/supervised/generalization-theory
  - theory/paradigms/supervised/trees-and-ensembles
tags:
  - supervised learning
  - kernels
  - classification
aliases:
  - SVM
  - Support vector machine
  - Support-vector networks
  - 支援向量機
  - 支持向量機
---

# Support Vector Machines

A support vector machine (SVM) is a classifier that chooses, among all boundaries that separate the classes, the one with the widest margin. It can draw non-linear boundaries by working with a kernel instead of explicit features. The family-level picture of kernel methods is on the [Support Vector Machines and Kernel Methods](index.md) page.

## Overview

The SVM combines two ideas. The first is the maximum-margin principle: among the boundaries that separate the training data, pick the one farthest from the nearest points. Cortes and Vapnik (1995) state that the special properties of the resulting decision surface give high generalization ability. The second is the kernel trick. The training problem depends on the data only through inner products, so replacing those products with a kernel gives a linear rule in a high-dimensional feature space without building that space.

Boser, Guyon and Vapnik (1992) gave a training algorithm that maximises the margin, whose solution is a linear combination of supporting patterns, and whose form can use kernels. Cortes and Vapnik (1995) extended the method to non-separable training data. That is the version most people mean today by "SVM".

## Key concepts

- **Margin**: the distance between the decision boundary and the nearest training points. For a hyperplane \(w^\top x + b = 0\), the gap between the two supporting hyperplanes is \(2/\lVert w\rVert\).
- **Support vectors**: training points on or inside the margin. Only they have non-zero weights in the solution.
- **Slack and soft margin**: slack variables \(\xi_i \ge 0\) let some points violate the margin, and a constant \(C\) sets the cost of those violations.
- **Hinge loss**: the penalty \(\max(0, 1 - y f(x))\) that the soft-margin objective applies to each point.
- **Kernel**: a function \(k(x, x') = \langle \phi(x), \phi(x') \rangle\) that equals an inner product in a feature space \(\phi\), which is never computed directly. A valid kernel is symmetric and positive semi-definite (Mercer's condition).

## How it works

The soft-margin problem in primal form is

\[
\min_{w, b, \xi}\ \tfrac12\lVert w\rVert^2 + C\sum_{i=1}^{n}\xi_i \quad \text{subject to}\quad y_i\big(w^\top\phi(x_i) + b\big) \ge 1 - \xi_i,\ \ \xi_i \ge 0
\]

Its dual depends on the data only through kernel values:

\[
\max_{\alpha}\ \sum_{i}\alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j\,y_i y_j\,k(x_i,x_j) \quad \text{subject to}\quad 0 \le \alpha_i \le C,\ \ \sum_i \alpha_i y_i = 0
\]

Prediction uses only the support vectors, the points with \(\alpha_i > 0\):

\[
f(x) = \operatorname{sign}\Big(\sum_{i} \alpha_i\, y_i\, k(x_i, x) + b\Big)
\]

The usual kernels are linear, polynomial and Gaussian (RBF):

- Linear: \(k(x, x') = x^\top x'\).
- Polynomial: \(k(x, x') = (x^\top x' + c)^p\).
- Gaussian (RBF): \(k(x, x') = \exp(-\gamma\lVert x - x'\rVert^2)\).

## Key methods

### A training algorithm for optimal margin classifiers (Boser, Guyon & Vapnik, 1992)

- **Problem:** A maximum-margin classifier generalises well, but it needs a non-linear boundary. Computing a high-dimensional feature map explicitly is expensive, so the method must work without it.
- **Core idea:** Train the maximum-margin classifier through its dual form, where the data appear only as inner products. Replacing each inner product with a kernel evaluates the classifier in a feature space without constructing it. The solution is a linear combination of the supporting patterns.
- **Equation or algorithm:** the hard-margin dual. It is the soft-margin dual above with the upper bound \(C\) removed and \(\alpha_i \ge 0\):

\[
\max_{\alpha}\ \sum_{i}\alpha_i - \tfrac12\sum_{i,j}\alpha_i\alpha_j\,y_i y_j\,k(x_i,x_j) \quad \text{subject to}\quad \alpha_i \ge 0,\ \ \sum_i \alpha_i y_i = 0
\]

- **Results:** The paper reports experiments on handwritten digit databases. The abstract gives no error figures, and the paper's tables were not checked in this pass, so no values are stated here.
- **Limitations:** The hard-margin form requires separable data. Training solves a quadratic programme over all training points, so the cost grows quickly with the number of examples.

### Support-vector networks (Cortes & Vapnik, 1995)

- **Problem:** Real training data are rarely separable, so the hard-margin problem may have no solution. The method needs to allow some errors while keeping the margin idea.
- **Core idea:** Extend the margin method to non-separable data. Inputs are mapped into a very high-dimensional feature space, where a linear decision surface is built. Each violation is charged through slack variables and the constant \(C\).
- **Equation or algorithm:** the soft-margin primal and dual, and the kernel decision function, as given in How it works.
- **Results:** The abstract mentions a benchmark on optical character recognition but gives no error rates, so none are stated here.
- **Limitations:** The constant \(C\) and the kernel parameters, such as \(\gamma\) for the RBF kernel, must be tuned, usually by cross-validation. On noisy data the number of support vectors, and with it the prediction cost, can grow. Training cost still rises quickly with the number of examples.

## Connections

- The family view and the comparison of kernels is on [Support Vector Machines and Kernel Methods](index.md).
- The decision function is linear in feature space, so the method sits beside [Linear Models](../linear-models/index.md).
- The hinge loss links SVM training to the [loss functions](../loss-functions-and-optimization/index.md) view of classification.
- The margin is the central quantity in margin-based bounds in [Generalization Theory](../generalization-theory/index.md).
- On tabular data, the usual alternatives are [Random Forests](../trees-and-ensembles/random-forests.md) and [Gradient Boosting](../trees-and-ensembles/gradient-boosting.md).
- Kernel-based Bayesian models such as Gaussian processes are covered in [Instance-Based and Probabilistic Methods](../instance-based-and-probabilistic/index.md).

## Open questions

- Learned deep features can replace hand-chosen kernels. When is a fixed kernel still the better choice, especially with little data?
- How should \(C\) and the kernel width be set when the data are too large for repeated cross-validation?

## References

### Seminal papers

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers. COLT 1992, pp. 144–152. https://doi.org/10.1145/130385.130401 — Introduces the maximum-margin training algorithm in its dual form, which lets kernels replace inner products.
- Cortes, C. & Vapnik, V. (1995). Support-vector networks. *Machine Learning*, 20(3), 273–297. https://doi.org/10.1007/BF00994018 — Extends the margin classifier to non-separable training data by allowing violations at a cost.

### Surveys and textbooks

- Vapnik, V. N. (1995). *The Nature of Statistical Learning Theory*. Springer. https://doi.org/10.1007/978-1-4757-2440-0 — The statistical learning theory behind margin-based generalisation.
- Schölkopf, B. & Smola, A. J. (2002). *Learning with Kernels*. MIT Press. https://dblp.uni-trier.de/rec/books/lib/ScholkopfS02.html — Standard text on kernels, support vector machines and their theory and algorithms.

### Articles and documentation

- Chang, C.-C. & Lin, C.-J. (2011). LIBSVM: A library for support vector machines. *ACM Transactions on Intelligent Systems and Technology*, 2(3), Article 27. https://www.csie.ntu.edu.tw/~cjlin/papers/libsvm.pdf — The widely used SVM library and its solver.
