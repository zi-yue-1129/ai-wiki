---
tags:
  - supervised learning
  - kernels
  - optimization
---

# Support Vector Machines and Kernel Methods

Kernel methods get non-linear power from linear algorithms by comparing examples with a similarity function instead of coordinates. The support vector machine (SVM) is the best-known example.

## Maximum-margin classification

For separable data, the SVM picks the hyperplane $w^\top x + b = 0$ that maximises the margin $2/\lVert w\rVert$ to the nearest points of each class. With slack variables $\xi_i$ for violations (soft margin):

$$
\min_{w,b,\xi}\ \tfrac12\lVert w\rVert^2 + C\sum_i \xi_i \quad \text{s.t. } y_i(w^\top x_i + b) \ge 1-\xi_i,\ \xi_i\ge 0.
$$

This is equivalent to minimising the **hinge loss** $\max(0, 1-y f(x))$ with an $\ell_2$ penalty. Only the **support vectors**, points on or inside the margin, determine the solution.

## The kernel trick

The dual problem depends on the data only through inner products $x_i^\top x_j$. Replacing them with a kernel $k(x_i,x_j)=\langle\phi(x_i),\phi(x_j)\rangle$ implicitly works in a high-dimensional feature space.

| Kernel | Formula | Use |
|---|---|---|
| Linear | $x^\top x'$ | High-dimensional sparse text |
| Polynomial | $(x^\top x' + c)^p$ | Feature interactions |
| RBF / Gaussian | $\exp(-\gamma\lVert x-x'\rVert^2)$ | General purpose |
| String, graph, tree kernels | Structure-specific | Biology, chemistry |

A valid kernel is symmetric and positive semi-definite (Mercer's condition). The representer theorem guarantees that the solution is a weighted sum of kernels at training points, $f(x)=\sum_i \alpha_i k(x_i,x)$.

## Related kernel methods

Kernel ridge regression, kernel PCA, [Gaussian processes](../instance-based-and-probabilistic/index.md) (kernel plus Bayesian inference) and the maximum mean discrepancy used in [domain adaptation](../../transfer/index.md).

## Limits and revival

Training scales between $O(n^2)$ and $O(n^3)$ in the number of examples, which is why deep learning displaced SVMs on large data. Random Fourier features and Nyström approximations scale kernels up. The **neural tangent kernel** (Jacot et al., 2018) shows that infinitely wide networks trained by gradient descent behave like a kernel machine, linking the two fields.

## References

### Seminal papers

- Boser, B. E., Guyon, I. M. & Vapnik, V. N. (1992). A training algorithm for optimal margin classifiers. *COLT*. https://doi.org/10.1145/130385.130401 — The first kernel SVM paper, combining maximum margins with the kernel trick.
- Cortes & Vapnik (1995), "Support-vector networks", *Machine Learning* 20. https://link.springer.com/doi/10.1007/BF00994018 — Introduces the soft-margin SVM, which allows some training errors.
- Jacot, Gabriel & Hongler (2018), "Neural tangent kernel", NeurIPS, arXiv:1806.07572 — Shows that infinitely wide networks trained by gradient descent behave like a kernel machine.
- Niculescu-Mizil & Caruana (2005), "Predicting good probabilities with supervised learning", ICML. https://doi.org/10.1145/1102351.1102430 — Compares how well classifiers including SVMs produce calibrated probabilities.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

- Yaser Abu-Mostafa, *Learning From Data*, Caltech online course (2012), lectures on support vector machines and kernels. https://work.caltech.edu/telecourse — Free university course that builds SVMs and kernels from learning theory.

### Articles and documentation

- Belkin, Hsu, Ma & Mandal (2019), "Reconciling modern machine-learning practice and the bias–variance trade-off", *PNAS*, arXiv:1812.11118 — Explains how kernel and neural models can interpolate training data and still generalise.

## Further reading

- Schölkopf & Smola, *Learning with Kernels*, MIT Press (2002). https://is.mpg.de/publications/973 — The reference text on kernel methods and support vector machines, covering theory and algorithms.
- Platt (2000), "Probabilities for SV Machines", in *Advances in Large-Margin Classifiers*, MIT Press. https://doi.org/10.7551/mitpress/1113.003.0008 — Fits a sigmoid to SVM scores to give calibrated probabilities.
