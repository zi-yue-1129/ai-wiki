---
status: draft
last_reviewed: 2026-10-28
related:
  - brain-mind/predictive-coding
  - theory/information-theory
  - theory/models/gnn
tags:
  - message passing
  - uncertainty
aliases:
  - 信念傳播
  - 置信傳播
  - 和積演算法
  - Belief propagation
  - Sum-product algorithm
  - Loopy belief propagation
---

# Belief Propagation

Belief propagation (BP), also called the sum-product algorithm, computes marginal probabilities in a graphical model by passing messages between neighbouring nodes. On a tree it gives exact marginals. On a graph with loops it gives approximations that often work well. It is one of the core methods of [Probabilistic Graphical Models](../index.md).

## Overview

Computing one marginal naively means summing over every configuration of the other variables, a cost that grows exponentially with their number. Belief propagation exploits the graph instead: each node sends each neighbour a summary of what it has learned from its other neighbours. On a tree, two passes (leaves to root and back) make every marginal exact.

Applying the same updates to a graph with cycles gives loopy belief propagation, which has no general guarantee of convergence or correctness. Kschischang et al. (2001) gave the unifying description on factor graphs, and Kschischang and Frey (1998) connected iterative decoding of compound codes with probability propagation on graphs. Wainwright and Jordan (2008) place the algorithm within the variational framework, which links it to [Variational Inference](../../variational-inference/index.md).

## Key concepts

- **Message** \(m_{i \to j}\): what node \(i\) tells neighbour \(j\) about its variable, summarising what it has learned from its other neighbours.
- **Belief**: the (approximate) marginal of a variable, proportional to the product of all incoming messages from its factors.
- **Sum-product and max-product**: sum-product computes marginals. Replacing sums with maxima gives max-product, which computes the most probable joint configuration (MAP).

## How it works

On a factor graph, with variables \(x\) and factors \(f\), the messages are

\[
m_{x \to f}(x) = \prod_{g \in N(x)\setminus f} m_{g \to x}(x), \qquad
m_{f \to x}(x) = \sum_{x_f \setminus x} f(x_f)\prod_{y \in N(f)\setminus x} m_{y \to f}(y),
\]

where \(N(\cdot)\) gives the neighbours and \(x_f\) are the variables of factor \(f\). The belief at a variable is

\[
b_x(x) \propto \prod_{f \in N(x)} m_{f \to x}(x).
\]

The algorithm is:

1. Initialise all messages to uniform values.
2. Update the messages in a chosen schedule, using the two formulas above.
3. Stop when the messages change by less than a tolerance, or after a fixed number of iterations.
4. Read the beliefs as the marginals. On a tree, the beliefs are exact after the two passes.

Replacing each sum with a maximum gives max-product, which is exact for MAP on trees.

## Results

Murphy, Weiss and Jordan (2013) compared loopy beliefs with exact marginals on four Bayesian networks, including two real-world ones, ALARM and QMR. The loopy beliefs often converged, and when they did they approximated the correct marginals well. On QMR they oscillated with no obvious relation to the correct posteriors, and simple ways of preventing the oscillation gave wrong results.

Weiss (2000) analysed graphs with a single loop. He related the beliefs computed by local propagation to the correct marginals, and showed that for one category of such graphs the MAP assignments are provably optimal, although the marginals are not.

## Limitations

- **No general convergence guarantee.** On graphs with loops, messages can oscillate instead of settling (Murphy et al., 2013).
- **Double counting.** Evidence can circulate around a loop and be counted more than once, so the computed marginals can be wrong (Weiss, 2000).
- **Factor size.** Each message sums over the variables of its factor, so large factors are expensive.

## Open questions

- Under what conditions does loopy BP converge and give accurate marginals? The single-loop analysis and the oscillation results suggest that the answer depends on the graph structure and the strength of interactions, but a general theory is missing.
- Does the brain perform something like message passing? Lee and Mumford (2003) and Ma et al. (2006) propose such computations for cortex, in line with [predictive coding](../../../../brain-mind/predictive-coding/index.md). The evidence does not yet decide between this and other mechanisms.
- Can learned message passing, as in [graph neural networks](../../../models/gnn/index.md), correct the errors of loopy BP while keeping its speed?

## References

### Seminal papers

- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/18.910572 — Gives the factor-graph description of sum-product message passing that is used throughout this page.
- Kschischang, F. R. & Frey, B. J. (1998). Iterative decoding of compound codes by probability propagation in graphical models. *IEEE Journal on Selected Areas in Communications*. https://doi.org/10.1109/49.661110 — Applies probability propagation on graphs to the iterative decoding of compound codes.
- Weiss, Y. (2000). Correctness of Local Probability Propagation in Graphical Models with Loops. *Neural Computation*. https://doi.org/10.1162/089976600300015880 — Analyses what local propagation computes on graphs with a single loop, and when its MAP assignments are optimal.
- Murphy, K. P., Weiss, Y. & Jordan, M. I. (2013). *Loopy Belief Propagation for Approximate Inference: An Empirical Study*. arXiv. https://arxiv.org/abs/1301.6725 — Compares loopy belief propagation with exact marginals on four Bayesian networks, finding convergence and good approximations in some cases and oscillation in another.

### Surveys and textbooks

- Wainwright, M. J. & Jordan, M. I. (2008). *Graphical Models, Exponential Families, and Variational Inference*. Foundations and Trends in Machine Learning. https://doi.org/10.1561/2200000001 — Survey that places message-passing algorithms within variational inference.

### Articles and documentation

- Lee, T. S. & Mumford, D. (2003). Hierarchical Bayesian inference in the visual cortex. *Journal of the Optical Society of America A*. https://doi.org/10.1364/JOSAA.20.001434 — Proposes that visual cortex performs hierarchical Bayesian inference, with signals between levels acting as messages.
- Ma, W. J., Beck, J. M., Latham, P. E. & Pouget, A. (2006). Bayesian inference with probabilistic population codes. *Nature Neuroscience*. https://doi.org/10.1038/nn1790 — Argues that populations of neurons can represent probability distributions, so that Bayesian computations could be carried out by neural populations.
