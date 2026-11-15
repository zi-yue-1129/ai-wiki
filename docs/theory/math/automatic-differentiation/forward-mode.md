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

### Rotating the seed: a JVP measures a direction

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable forward-mode teaching motion">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-directional-jvp-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-directional-jvp-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-directional-jvp-still.svg" alt="A unit seed rotates around a fixed gradient (5,2) while a marker tracks the exact directional derivative 5 cos theta plus 2 sin theta." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 teaching motion. [GitHub static preview](../../../assets/concept-animations/forward-ad-directional-jvp-still.svg) · [12-second animated SVG](../../../assets/concept-animations/forward-ad-directional-jvp-motion.svg).* At the same synthetic point \((x,y)=(2,3)\), the gradient of \(f(x,y)=xy+2x\) is \((5,2)\). A unit seed \(v(\theta)=(\cos\theta,\sin\theta)\) produces

\[
J_fv(\theta)=5\cos\theta+2\sin\theta.
\]

The orange arrow rotates counter-clockwise while the graph cursor follows the **corresponding analytic derivative**, not the function's output value. The examples \(\theta=0\) and \(\theta=\pi/2\) return **5** and **2**, respectively. The SVG approximates the smooth cursor trajectory with sampled points; the formula is exact. These are constructed derivatives, **not model measurements**. On MkDocs, use Play/Pause (including keyboard activation); reduced-motion users initially see the static preview.

### Basis seeds: assemble a complete two-column Jacobian

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable forward-mode teaching motion">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-jacobian-columns-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-jacobian-columns-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-jacobian-columns-still.svg" alt="Two sequential basis-seed passes yield the first Jacobian column (5,1) and second column (2,-1), assembling a two-by-two matrix." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 teaching motion. [GitHub static preview](../../../assets/concept-animations/forward-ad-jacobian-columns-still.svg) · [12-second animated SVG](../../../assets/concept-animations/forward-ad-jacobian-columns-motion.svg).* Extend the synthetic example to the **two-output** map \(F(x,y)=(xy+2x,\ x-y)\). At \((2,3)\), its Jacobian is

\[
J_F=\begin{bmatrix}5&2\\1&-1\end{bmatrix},
\qquad J_Fe_1=(5,1)^\top,\quad J_Fe_2=(2,-1)^\top.
\]

Follow the teal first sweep and amber second sweep: each basis seed supplies **one column**, and the two results form \(J_F\). The animation shows causal data flow, not a runtime benchmark; a single arbitrary seed gives a JVP, **not both columns**. The MkDocs player supports Play/Pause and a reduced-motion still, but not single-stepping or seeking.


### Dual-number arithmetic: a nonlinear chain with a shortcut

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable nonlinear dual-number propagation">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-dual-chain-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-dual-chain-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-dual-chain-still.svg" alt="Two input value-and-tangent pairs propagate through a product, a square, and a skip-path sum; the final primal is 6 and the directional tangent is 9." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 animated calculation. [GitHub-readable static fallback](../../../assets/concept-animations/forward-ad-dual-chain-still.svg) · [animated SVG](../../../assets/concept-animations/forward-ad-dual-chain-motion.svg).* Consider \(f(x,y)=(xy)^2+x\) at the **synthetic** point \((2,1)\), with seed \((\dot x,\dot y)=(1,0.5)\). Each box shows a primal (teal) and its tangent (amber). The moving paths show how the direct skip connection from \(x\) and the nonlinear chain contribute to the same final JVP:

\[
\begin{aligned}
a&=xy=2,& \dot a&=y\dot x+x\dot y=1+1=2,\\
b&=a^2=4,& \dot b&=2a\dot a=8,\\
z&=b+x=6,& \dot z&=\dot b+\dot x=9.
\end{aligned}
\]

As a check, \(\nabla f(2,1)=(5,8)\), so \(\nabla f\cdot(1,0.5)=9\). The diagram represents **exact, hand-computed calculus**, not a measured model trace. On MkDocs, Play/Pause is available through the shared player; readers using reduced motion initially get the still image.

### Branch-sensitive differentiation: ReLU at a kink

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable ReLU branchwise derivative">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-branch-kink-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-branch-kink-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-branch-kink-still.svg" alt="A moving point traverses ReLU's flat negative-input branch and sloped positive-input branch, while the tangent switches between zero and one; hollow circles mark the undefined classical derivative at zero." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 branchwise teaching motion. [GitHub-readable static fallback](../../../assets/concept-animations/forward-ad-branch-kink-still.svg) · [animated SVG](../../../assets/concept-animations/forward-ad-branch-kink-motion.svg).* For \(y=\mathrm{ReLU}(x)=\max(0,x)\) and a unit tangent seed \(\dot x=1\), forward-mode AD follows the **executed branch**. Away from the kink,

\[
\dot y=
\begin{cases}
0,&x<0,\\
1,&x>0.
\end{cases}
\]

The linked primal and tangent panels animate the two regions. At **\(x=0\)** the classical derivative does **not** exist, so neither panel assigns a unique derivative there. One-sided directional derivatives may exist, but they do not define one linear Jacobian map at the kink; an AD implementation's returned tangent there depends on its derivative convention. This is a constructed mathematical example, not an empirical model result. The MkDocs player can pause the movement, and its reduced-motion fallback shows both branches simultaneously.


### Tangents through an iterative program

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable iteration and tangent sensitivity animation">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-loop-tangent-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-loop-tangent-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-loop-tangent-still.svg" alt="Paired teal primal values approach their fixed point while orange tangent values halve at each iteration, with synchronized animated markers across six steps." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 teaching motion. [GitHub static fallback](../../../assets/concept-animations/forward-ad-loop-tangent-still.svg) · [12-second animated SVG](../../../assets/concept-animations/forward-ad-loop-tangent-motion.svg).* Consider the synthetic recurrence \(x_{t+1}=\tfrac12x_t+1\), initialized at \(x_0=4\). Seed the derivative of the **initial condition** with \(\dot x_0=\partial x_0/\partial x_0=1\), and keep the coefficient and constant fixed. One dual-number evaluation per iteration gives

\[
x_{t+1}=\tfrac12 x_t+1,\qquad \dot x_{t+1}=\tfrac12\dot x_t.
\]

The two synchronized curves show \(x_t=2+2^{1-t}\) approaching the fixed point \(2\) and \(\dot x_t=2^{-t}\) shrinking to zero. At \(t=5\), \(x_5=2.0625\) while \(\dot x_5=0.03125\). **Do not conflate state convergence with sensitivity:** the orange curve is the derivative with respect to the initial state, not the state itself. These are exact hand-calculated toy values, not measurements from a learned model. On MkDocs the shared player supports Play/Pause and keyboard activation; reduced-motion visitors initially see the still.

### Forward-over-reverse: differentiate the gradient along a direction

<div style="max-width:100%;overflow-x:auto" role="group" tabindex="0" aria-label="Horizontally scrollable Hessian-vector product teaching animation">
<img data-source-asset-urls src="../../../assets/concept-animations/forward-ad-hessian-vector-still.svg" data-motion-src="../../../assets/concept-animations/forward-ad-hessian-vector-motion.svg" data-still-src="../../../assets/concept-animations/forward-ad-hessian-vector-still.svg" alt="Synchronized dots move along a seed direction in input space and its image in gradient space; the gradient directional derivative is Hessian-vector product (1,-3)." style="width:800px;min-width:800px;max-width:none;height:auto">
</div>

*Original CC BY-SA 4.0 teaching motion. [GitHub static fallback](../../../assets/concept-animations/forward-ad-hessian-vector-still.svg) · [12-second animated SVG](../../../assets/concept-animations/forward-ad-hessian-vector-motion.svg).* For the synthetic quadratic \(f(x,y)=x^2+xy+2y^2\), first obtain its gradient \(g(x,y)=\nabla f(x,y)=(2x+y,\ x+4y)\). At \(p=(1,1)\), follow the seed \(v=(1,-1)\). The left marker moves along \(p(t)=(1+t,1-t)\) while the right marker follows

\[
g(p(t))=(3+t,\ 5-3t),\qquad
\left.\frac{d}{dt}g(p(t))\right|_{t=0}
=H_f(p)v=(1,-3).
\]

This is the **JVP of the gradient**: a forward-mode directional derivative applied to a gradient function that can be obtained by reverse mode. No full Hessian matrix needs to be materialized. Both curves and the value \(H_f(p)v\) are exact analytic examples, not timing or model-training results. The plotted axes use separate schematic scales; the paired points depict corresponding parameter values, not comparable Euclidean distances. The MkDocs player supports Play/Pause and a reduced-motion still, not seek or single-step. For the general forward/reverse tradeoff, see [Griewank and Walther (2008)](https://doi.org/10.1137/1.9780898717761).

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
