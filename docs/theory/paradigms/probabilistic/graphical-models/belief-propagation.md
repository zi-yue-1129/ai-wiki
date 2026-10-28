---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic/graphical-models
  - theory/math/probability-statistics
tags:
  - probabilistic models
  - message passing
  - approximate inference
aliases:
  - 信念傳播
  - 和積演算法
  - Sum-product algorithm
  - Loopy belief propagation
---

# Belief Propagation

Belief propagation (BP) computes marginal distributions in a graphical model by passing messages between neighbouring nodes. On a tree the result is exact. On a graph with loops, the same updates are used as an approximation, called loopy belief propagation. Part of [Probabilistic graphical models](index.md).

## Overview

Computing a marginal \(p(x_i)\) by summing over all other variables costs exponentially in the number of variables. BP avoids this by exploiting the structure of the graph. Each factor sends a summary of what it knows about a variable to that variable, and each variable sends the combined information back. The summaries are the messages.

## Key concepts

- **Message**: a function of one variable that summarises the other parts of the graph as seen through an edge.
- **Belief**: the product of all incoming messages at a node, normalised. At convergence on a tree it is the exact marginal.
- **Sum-product rule**: a message from a factor \(f\) to a variable \(x\) sums out all other variables of \(f\), after multiplying in the incoming messages from those variables.
- **Max-product rule**: the same scheme with the sum replaced by a maximum. It computes the most probable configuration rather than the marginals.

## How it works

On a factor graph, let \(\mu_{f\to x}\) denote the message from factor \(f\) to variable \(x\), and \(\mu_{x\to f}\) the message in the other direction. The sum-product updates are

\[
\mu_{f\to x}(x) = \sum_{\mathbf{x}_f\setminus x} f(\mathbf{x}_f)\prod_{y\in \mathrm{ne}(f)\setminus x}\mu_{y\to f}(y),
\qquad
\mu_{x\to f}(x)=\prod_{g\in \mathrm{ne}(x)\setminus f}\mu_{g\to x}(x),
\]

where \(\mathrm{ne}(\cdot)\) denotes neighbours in the factor graph. On a tree, one pass from the leaves to a root and one pass back give every message once, so every belief is exact (Kschischang et al., 2001). The cost is linear in the number of edges, which is far less than the cost of summing the joint directly.

On a graph with cycles, the messages keep changing and BP is no longer guaranteed to stop. Running the same updates until they settle is called loopy BP. Its fixed points correspond to stationary points of the Bethe free energy, an approximation to the true free energy of the model. Yedidia et al. (2005) show this link and give generalised BP methods that use larger clusters of variables.

## Variants

- **Max-product** and its log-space version, **min-sum**, compute the most probable configuration on trees and are used in decoding.
- **Generalised belief propagation** passes messages between clusters of variables rather than single variables, which improves accuracy on graphs with short loops (Yedidia et al., 2005).
- **Damped updates** average the new message with the old one to make loopy BP converge more often.

## Results and limits

- On trees, BP is exact and runs in time linear in the graph size. This is the main result that makes it useful.
- On loopy graphs, BP can converge to an accurate approximation in practice, and it can also oscillate or converge to poor fixed points. There is no general guarantee.
- The Bethe approximation can be inaccurate when the graph is dense or the potentials are strong.
- Message passing on factor graphs is the common foundation of iterative decoding of error-correcting codes (Kschischang et al., 2001).

## Applications

- **Error-correcting codes**: iterative message passing decodes turbo codes and low-density parity-check codes.
- **Sequence models**: the forward–backward algorithm for [hidden Markov models](hidden-markov-models.md) is BP on a chain.

## Open questions

- Convergence conditions for loopy BP are known only for restricted classes of graphs and potentials.
- Choosing clusters for generalised BP, which trades accuracy against cost, has no general recipe.
- BP-based learning and inference in large models with dense, heterogeneous factors remain an active area of work.

## References

### Seminal papers

- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory* 47(2), 498–519. https://doi.org/10.1109/18.910572 — Unifies belief propagation as the sum-product algorithm on factor graphs and shows exactness on trees.
- Yedidia, J. S., Freeman, W. T. & Weiss, Y. (2005). Constructing free-energy approximations and generalized belief propagation algorithms. *IEEE Transactions on Information Theory* 51(7), 2282–2312. https://doi.org/10.1109/tit.2005.850085 — Shows that loopy BP fixed points correspond to Bethe free-energy stationary points and introduces generalised BP.

### Surveys and textbooks

- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — Connects message passing with variational approximations.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook; covers belief propagation on trees and loopy graphs.
- Lauritzen, S. L. & Spiegelhalter, D. J. (1988). Local computations with probabilities on graphical structures and their application to expert systems. *Journal of the Royal Statistical Society, Series B* 50(2), 157–194. https://doi.org/10.1111/j.2517-6161.1988.tb01721.x — Local computation on junction trees, the exact-inference counterpart of message passing.
