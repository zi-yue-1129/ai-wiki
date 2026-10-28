---
status: draft
last_reviewed: 2026-10-28
tags:
  - optimization
  - deep learning
aliases:
  - 前向模式自動微分
  - Forward-mode AD
  - Tangent propagation
---

# Forward-Mode Automatic Differentiation

Forward-mode automatic differentiation computes a program's derivative in a chosen input direction by carrying a tangent alongside every intermediate value as the program runs. It is one of the two basic modes of [automatic differentiation](../index.md), and it is efficient when a function has few inputs.

## Overview

Forward mode applies the chain rule in the order in which the program computes its values. Each value $v$ is paired with a tangent $\dot v$, its rate of change along a chosen input direction. Each operation updates tangents with its local rule, so the output tangent is the Jacobian-vector product $J\dot{x}$. Hoffmann (2014) shows that several descriptions of forward mode, including matrix-vector products, dual numbers and Taylor series on dual numbers, carry out the same chain of computations. Baydin and colleagues (2015/2018) treat forward mode and reverse mode as the two basic techniques.

## Key concepts

- **Tangent** $\dot v$: the derivative of an intermediate value along the input direction.
- **Seed**: the initial tangent on the inputs. Choosing $\dot x = e_i$ selects the derivative with respect to input $i$.
- **Dual number**: a pair $a + b\varepsilon$ with $\varepsilon^2 = 0$, where $a$ is a value and $b$ its tangent. Arithmetic on dual numbers computes values and derivatives together.
- **Local rule**: for $z = \varphi(x, y)$, $\dot z = \frac{\partial \varphi}{\partial x}\dot x + \frac{\partial \varphi}{\partial y}\dot y$.

## How it works

The algorithm has three steps:

1. Set each input's tangent from the seed direction $\dot x$.
2. For each operation in program order, compute its value as usual, then its tangent $\dot v_k = \sum_j \frac{\partial v_k}{\partial v_j}\dot v_j$, summed over its parents $j$.
3. Read the output tangent, which equals $J\dot{x}$.

Dual-number arithmetic makes the local rules explicit: $(a + b\varepsilon)(c + d\varepsilon) = ac + (ad + bc)\varepsilon$, because $\varepsilon^2 = 0$, and $\sin(a + b\varepsilon) = \sin a + b\cos a\,\varepsilon$. For $f(x, y) = xy + \sin x$ at $(2, 3)$ with seed $\dot x = 1$, a single pass gives $\partial f/\partial x = 3 + \cos 2 \approx 2.584$, the same value as in the [overview](../index.md).

Each pass yields one column of the Jacobian, so the full gradient of a function with $n$ inputs needs $n$ passes. Forward mode needs no tape, because each tangent is available as soon as its inputs are. Nesting forward mode inside reverse mode gives second derivatives, such as Hessian-vector products (Pearlmutter, 1994).

## Results

No single benchmark defines forward mode, so its evidence is analytic. Its cost grows with the number of inputs, as the survey by Baydin and colleagues (2015/2018) explains. Baydin and colleagues (2022) use forward-mode directional derivatives as the core of "forward gradients". Their abstract reports that the method, which needs one forward run, trains up to twice as fast in some cases on the problems they tested. Pearlmutter (1994) shows exact Hessian-vector products at a cost comparable to a gradient. No figures are copied here beyond those in the abstract.

## Limitations

- **Cost scales with inputs.** For a scalar loss over millions of parameters, one pass per parameter is far too expensive, which is why reverse mode dominates training.
- **Randomised estimates are noisy.** Forward gradients use random tangent directions. Their estimate is unbiased, but its variance can be large.
- **Local rules are still required.** Forward mode is only as good as the derivative rule of each primitive, and non-differentiable operations need separate treatment.

## Open questions

- How forward-mode directional derivatives can be combined efficiently with reverse mode for functions with many inputs and outputs.
- Whether forward gradients scale to the largest models, where reverse mode is the standard.

## References

### Seminal papers

- Baydin, A. G., Pearlmutter, B. A., Syme, D., Wood, F. & Torr, P. (2022). Gradients without Backpropagation. https://arxiv.org/abs/2202.08587 — Estimates gradients from forward-mode directional derivatives in a single forward run, and reports faster training in some cases.
- Pearlmutter, B. A. (1994). Fast Exact Multiplication by the Hessian. *Neural Computation*. https://doi.org/10.1162/neco.1994.6.1.147 — Shows how differentiation gives exact Hessian-vector products, a main use of forward mode inside reverse mode.

### Surveys and textbooks

- Baydin, A. G., Pearlmutter, B. A., Radul, A. A. & Siskind, J. M. (2015/2018). Automatic differentiation in machine learning: a survey. *Journal of Machine Learning Research*. https://arxiv.org/abs/1502.05767 — Survey that defines forward and reverse mode and explains how they relate.
- Griewank, A. & Walther, A. (2008). *Evaluating Derivatives*. SIAM. https://doi.org/10.1137/1.9780898717761 — Standard reference on algorithmic differentiation, with a detailed treatment of forward-mode implementation.
- Hoffmann, P. H. W. (2014). A Hitchhiker's Guide to Automatic Differentiation. arXiv. https://arxiv.org/abs/1411.0583 — Tutorial comparing the matrix, dual-number and Taylor-series descriptions of forward mode.
