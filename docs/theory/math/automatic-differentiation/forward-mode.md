---
status: draft
last_reviewed: 2026-11-15
related:
  - theory/math/automatic-differentiation
  - theory/math
tags:
  - forward-mode differentiation
  - dual numbers
  - Jacobian-vector product
aliases:
  - 前向模式自動微分
  - Forward-mode automatic differentiation
  - Forward mode
---

# Forward-mode differentiation

Forward-mode differentiation propagates derivatives from the inputs to the outputs of a program, alongside the values themselves. For one chosen input direction it returns the directional derivative of every output in a single pass. It is cheap when a function has few inputs, and it is the dual of [reverse mode](reverse-mode.md), which is cheap when a function has few outputs.

## Overview

The [automatic differentiation chapter](index.md) introduces both modes. This page covers forward mode: what it computes, how the computation is organised, and when it is the better choice.

## Problem

Many scientific and machine learning tasks need how the outputs of a function respond to a few inputs, or the action of a Jacobian on a single vector, rather than the full gradient of a scalar. Reverse mode is wasteful for these tasks. It produces one row of the Jacobian per output, whereas these tasks need one column per input, or only one product. The question is how to obtain directional derivatives directly, without building the full Jacobian.

## Key concepts

- **Tangent**: the derivative of an intermediate value with respect to the chosen input direction. Every intermediate value carries one.
- **Seed**: the chosen input direction $\dot{x}$. It sets the starting tangents.
- **Jacobian-vector product (JVP)**: $J\dot{x}$, the derivative of the outputs along the seed direction.
- **Dual number**: a pair $(v, \dot{v})$ of a value and its tangent. Arithmetic on pairs applies the chain rule automatically.
- **Tangent-linear model**: the program obtained by running the original operations together with their tangent rules.

## Key methods

Forward mode and reverse mode are the two ways to apply the chain rule to a program. Each has its own page.

- [Forward-mode differentiation](forward-mode.md) (this page): one pass per input direction, so the cost grows with the number of inputs.
- [Reverse-mode differentiation](reverse-mode.md): one pass per output, so the cost grows with the number of outputs. It is the mode that implements backpropagation.

## How it works

Attach a tangent to every intermediate value. If the input is perturbed along a direction $\dot{x}$, each elementary operation transforms the tangents of its inputs by its own differentiation rule, in the same order in which the program runs. One forward pass returns $J\dot{x}$.

Dual numbers express this compactly. Each value is carried as a pair, and the rules for addition and multiplication are

$$(a,\dot{a}) + (b,\dot{b}) = (a+b,\ \dot{a}+\dot{b}), \qquad (a,\dot{a})\,(b,\dot{b}) = (ab,\ a\dot{b}+\dot{a}\,b).$$

Running any program on dual numbers, with the tangent part of each input set to the seed, returns the output values and the JVP in one run. No symbolic expression for the derivative is needed.

![Forward-mode AD animation: seed the input direction, propagate tangents through the shared computation graph, and obtain the Jacobian-vector product.](../../../assets/concept-animations/forward-ad-jvp-motion.svg)

*Original four-stage teaching animation, CC BY-SA 4.0.* For the illustrative program $a=xy$, $b=x+x$, $z=a+b$ at $(x,y)=(2,3)$, seed the input direction $(\dot{x},\dot{y})=(1,0)$. The local rules give $\dot{a}=3$, $\dot{b}=2$ and $\dot{z}=5=J(1,0)^\top$. Follow the highlighted edges from **Seed** to **Tangents** to **JVP**; one pass gives a directional derivative, **not** the full Jacobian. Values are hand-computed teaching examples, not model measurements. The MkDocs player offers Play/Pause and a reduced-motion fallback; [view the GitHub-compatible static final state](../../../assets/concept-animations/forward-ad-jvp-still.svg).

The same example can be checked by hand. Since $z = xy + 2x$, the derivative with respect to $x$ is $\partial z/\partial x = y + 2 = 5$, which matches the tangent $\dot{z}=5$ computed above.

## Equation

For an elementary operation $v = \phi(u)$, the tangent rule is

$$\dot{v} = \phi'(u)\,\dot{u}.$$

For a program that computes $y = f(x)$, the tangent-linear model maps a seed $\dot{x}$ to $\dot{y} = J_f(x)\,\dot{x}$. Taking $\dot{x}$ to be each standard basis vector $e_1, \dots, e_n$ in turn recovers the columns of the Jacobian. A full $m \times n$ Jacobian therefore needs $n$ forward passes, one per input.

## Results

Forward mode gives exact derivatives, up to the rounding of the floating-point operations themselves. It does not need the graph of operations to be stored for a later replay, so intermediate values can be discarded once their tangents have been computed. Griewank and Walther analyse the tangent-linear model in detail, including its cost relative to the original program and the trade-off against reverse mode [(Griewank & Walther, 2008)](https://doi.org/10.1137/1.9780898717761).

The survey by Baydin and colleagues presents forward mode in its Section 3.1 and reverse mode in its Section 3.2. It states that computing the gradient of a scalar function with $n$ inputs by forward mode takes $n$ evaluations of the forward pass [(Baydin et al., 2015)](https://arxiv.org/abs/1502.05767). This page does not report benchmark timings, which depend on the implementation.

Early work described the same idea of evaluating a program's derivatives alongside its values [(Wengert, 1964)](https://doi.org/10.1145/355586.364791). Pearlmutter and Siskind present reverse-mode differentiation in a functional framework, which is the natural counterpart to this page [(Pearlmutter & Siskind, 2008)](https://doi.org/10.1145/1330017.1330018).

## Limitations

- A full Jacobian grows linearly with the number of inputs. For a neural network loss with millions of parameters and a single output, forward mode would need one pass per parameter, which is why training uses reverse mode.
- Forward mode computes one direction at a time. Higher-order derivatives can be built from it, typically by combining it with reverse mode, but the combinations need care to stay efficient.
- Like reverse mode, it differentiates the path that the program actually executes. At non-smooth points, such as the kink of $|x|$ at zero, the derivative may not exist, and the result depends on the convention the implementation uses.

## Connections

Forward mode is the efficient choice for sensitivity analysis and for Jacobian-vector products. Combined with reverse mode, it gives Hessian-vector products, a standard device in second-order optimisation [(Griewank & Walther, 2008)](https://doi.org/10.1137/1.9780898717761). The parent [chapter](index.md) explains how the two modes relate. Training with [backpropagation](../../deep-learning/index.md) uses reverse mode, because a neural network loss has one output and very many inputs. The underlying calculus is in [Calculus](../index.md).

## Applications

- **Sensitivity analysis** of simulations with few input parameters, where one JVP per parameter gives the local response of the outputs [(Griewank & Walther, 2008)](https://doi.org/10.1137/1.9780898717761).
- **Uncertainty propagation** through a small number of inputs, where the tangent of each output gives its first-order sensitivity to the input uncertainty.
- **Hessian-vector products** for second-order optimisation, obtained by applying forward mode to a reverse-mode gradient [(Griewank & Walther, 2008)](https://doi.org/10.1137/1.9780898717761).

## Open questions

- How should forward and reverse mode be combined in large programs, so that each part of the program uses the cheaper mode?
- How can tangents be propagated efficiently through control flow and iterative numerical solvers, where the executed path can change with the input?

## References

### Seminal papers

- Wengert, *A simple automatic derivative evaluation program*, Communications of the ACM (1964). https://doi.org/10.1145/355586.364791 — Early description of evaluating a program's derivatives alongside its values.
- Pearlmutter and Siskind, *Reverse-Mode AD in a Functional Framework: Lambda the Ultimate Backpropagator*, ACM Transactions on Programming Languages and Systems (2008). https://doi.org/10.1145/1330017.1330018 — Reverse-mode differentiation in a functional framework, the counterpart to forward mode.
- Rumelhart, Hinton and Williams, *Learning representations by back-propagating errors*, Nature (1986). https://doi.org/10.1038/323533a0 — Popularised back-propagation, the reverse-mode computation used to train neural networks.

### Surveys and textbooks

- Griewank and Walther, *Evaluating Derivatives: Principles and Techniques of Algorithmic Differentiation*, SIAM (2008). https://doi.org/10.1137/1.9780898717761 — Standard textbook covering tangent-linear models, the cost of each mode, and second derivatives.
- Baydin, Pearlmutter, Radul and Siskind, *Automatic differentiation in machine learning: a survey*, arXiv (2015). https://arxiv.org/abs/1502.05767 — Survey of automatic differentiation for machine learning; Section 3.1 covers forward mode and Section 3.2 reverse mode.

### Articles and documentation

- Hascoët and Pascual, *The Tapenade automatic differentiation tool*, ACM Transactions on Mathematical Software (2013). https://doi.org/10.1145/2450153.2450158 — Describes Tapenade, an automatic differentiation tool, for readers who want a concrete implementation.
