---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/math
  - theory/deep-learning
tags:
  - optimization
  - natural gradient
  - curvature
aliases:
  - EKFAC
  - Eigenvalue-corrected Kronecker factorisation
  - 特徵值修正的 Kronecker 分解
---

# EKFAC

EKFAC (Eigenvalue-corrected Kronecker factorisation) keeps the Kronecker-factored eigenbasis of [K-FAC](index.md), but tracks a diagonal variance in that basis instead of using the product of the factor eigenvalues as the scaling. George et al. (2018) introduced it. They argue that it is a provably better approximation of the Fisher matrix than K-FAC, and that its per-iteration cost stays low once the eigenbasis is available.

## Problem

K-FAC approximates the Fisher with a Kronecker product $A \otimes G$. Its preconditioner rescales the gradient in the eigenbasis of that product, but the scaling it uses, the product of the factor eigenvalues, need not match the true second moment of the gradient along each eigenvector. Computing the eigenbasis is also expensive, so K-FAC must refresh it infrequently, and the basis can lag behind the local curvature.

## Core idea

Take the eigenvectors of the two K-FAC factors, $U_A$ and $U_B$, and use their Kronecker product $U = U_A \otimes U_B$ as the basis. In that basis, track a running estimate of the second moment of each rotated gradient coordinate. Preconditioning rotates the gradient into the basis, divides each coordinate by its tracked value, and rotates back. The diagonal can be updated at every iteration, while the eigenbasis is recomputed only occasionally.

## Equation or algorithm

With $\nabla\theta$ the gradient and $\epsilon$ a damping constant, each step is

1. Rotate: $\tilde{g} = U^\top \nabla\theta$.
2. Rescale: $\tilde{g}_i \leftarrow \tilde{g}_i / (s_i + \epsilon)$, where $s_i$ is a running average of $\tilde{g}_i^{\,2}$.
3. Rotate back: $\Delta\theta = U\,\tilde{g}$.

The paper's key point is in step 2. The scale is the second moment measured along the eigenvectors themselves, not the scale predicted from the factor eigenvalues.

## Results

On a deep autoencoder task and on convolutional networks trained on CIFAR-10, the paper reports that EKFAC reduces training loss faster than K-FAC over epochs. A variant that the paper calls EKFAC-ra also reduces training loss faster than K-FAC per unit of wall-clock time. The two methods reach similar validation performance.

## Limitations

- The eigenbasis is expensive to compute, so between refreshes it can lag behind the true curvature. The refresh frequency is an extra hyperparameter.
- The claim of a better Fisher approximation is made under the paper's own criterion. The empirical gains come from a small number of architectures.
- EKFAC inherits the independence assumptions of the underlying Kronecker approximation.

## Key methods

- [K-FAC](index.md) is the factored preconditioner whose eigenbasis EKFAC reuses.
- [KFC](kfc.md) extends the Kronecker factorisation to convolution layers, and the paper's experiments include convolutional networks.
- [Adam](../adaptive/adam.md) tracks a diagonal second moment in the parameter basis. EKFAC keeps that diagonal idea but applies it in a rotated basis.

## Open issues and related variants

- **Refresh schedule.** How often the eigenbasis should be recomputed, given its cost, is a practical question that the paper studies only in part.
- **Other bases.** Whether other rotated bases give a better diagonal approximation than the Kronecker-factored eigenbasis is open.

## Connections

- [Second-order and quasi-Newton methods](../second-order.md) is the overview where the K-FAC family sits.
- [Adaptive methods](../adaptive/index.md) share the idea of per-coordinate scaling.

## References

### Seminal papers

- George, T., Laurent, C., Bouthillier, X., Ballas, N. & Vincent, P. (2018). *Fast Approximate Natural Gradient Descent in a Kronecker-factored Eigenbasis*. arXiv:1806.03884. https://arxiv.org/abs/1806.03884 — Tracks a diagonal variance in the Kronecker-factored eigenbasis, which the paper argues is a provably better Fisher approximation than K-FAC.
- Martens, J. & Grosse, R. (2015). *Optimizing Neural Networks with Kronecker-factored Approximate Curvature*. arXiv:1503.05671. https://arxiv.org/abs/1503.05671 — Introduces the K-FAC factors whose eigenbasis EKFAC uses.
- Grosse, R. & Martens, J. (2016). *A Kronecker-factored approximate Fisher matrix for convolution layers*. ICML, PMLR 48:573–582. https://proceedings.mlr.press/v48/grosse16.html — The convolution extension of K-FAC, for comparison on convolutional networks.
- Amari, S. (1998). *Natural Gradient Works Efficiently in Learning*. Neural Computation, 10(2), 251–276. https://doi.org/10.1162/089976698300017746 — The natural-gradient method that EKFAC approximates.

### Surveys and textbooks

- Bottou, L., Curtis, F. E. & Nocedal, J. (2018). *Optimization Methods for Large-Scale Machine Learning*. arXiv:1606.04838. https://arxiv.org/abs/1606.04838 — Survey of large-scale optimisers that places natural-gradient methods in context.
