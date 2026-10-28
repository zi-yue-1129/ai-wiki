---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/probabilistic
  - theory/paradigms/probabilistic/variational-inference
  - theory/paradigms/probabilistic/mcmc
  - theory/math/probability-statistics
tags:
  - probabilistic models
  - graphical models
  - inference
aliases:
  - 機率圖模型
  - Probabilistic graphical models
  - PGM
  - Bayesian networks
  - Markov random fields
---

# Probabilistic Graphical Models

Probabilistic graphical models (PGMs) describe a joint distribution over many variables with a graph. Each edge or missing edge records a statement about which variables depend on which. The graph keeps high-dimensional joint distributions compact, and it lets inference be organised as local computation on the graph. Part of [Probabilistic & Bayesian methods](../index.md).

## Overview

A joint distribution over \(n\) binary variables has \(2^n-1\) free parameters, which is impractical for large \(n\). Conditional-independence assumptions shrink this. A PGM states those assumptions graphically and factorises the joint into small local terms. There are two main families:

- **Directed** models (Bayesian networks) factorise the joint as \(p(x)=\prod_i p(x_i\mid \mathrm{pa}(x_i))\), where \(\mathrm{pa}(x_i)\) are the parents of \(x_i\).
- **Undirected** models (Markov random fields) factorise it into clique potentials, \(p(x)=\frac{1}{Z}\prod_c \psi_c(x_c)\).

The directed and undirected forms differ in how they express dependence. Directed graphs are natural for causal or generative stories, and undirected graphs are natural for symmetric interactions such as pixel smoothness in images.

## Key concepts

- **Factorisation**: the joint distribution is a product of local terms, so only local tables or potentials need to be stored.
- **Conditional independence**: a graph separates variables when they are independent given others. Separation rules read these statements off the graph.
- **Partition function**: \(Z=\sum_x\prod_c\psi_c(x_c)\) normalises an undirected model. It is often intractable, which makes learning and inference harder.
- **Factor graph**: a bipartite graph with variable nodes and factor nodes. It gives one common language for the message-passing algorithms that many PGM methods share (Kschischang et al., 2001).
- **Exact and approximate inference**: exact methods compute marginals or the most probable configuration when the graph is small or tree-shaped. Approximate methods cover the rest.

## How it works

Two tasks are central. **Inference** asks for marginals \(p(x_i\mid e)\) or for the most probable assignment given evidence \(e\). **Learning** estimates the factors from data. For a model with parameters \(\theta\), maximum-likelihood learning follows the gradient of the log-likelihood, which equals the difference between data statistics and model expectations. The model expectations need inference, so learning and inference are tied together.

Exact inference by variable elimination has a cost set by the **treewidth** of the graph. On a tree the sum-product algorithm, or [belief propagation](belief-propagation.md), gives exact marginals in two passes. On graphs with loops, exact inference can become intractable, and approximations are needed. The two main approximation families are sampling, covered in [Markov chain Monte Carlo](../mcmc/index.md), and optimisation of a simpler distribution, covered in [variational inference](../variational-inference/index.md).

## Key methods

- [Belief propagation](belief-propagation.md): message passing on a factor graph. It is exact on trees and approximate on graphs with loops.
- [Hidden Markov models](hidden-markov-models.md): a chain-structured directed model for sequences. Forward–backward and the Viterbi algorithm are the standard inference tools (Rabiner, 1989).

Other named models in the family are summarised below. Only the methods above have their own pages in this section.

| Type | Graph | Examples |
|---|---|---|
| Bayesian network | Directed, acyclic | Diagnosis, causal models |
| Markov random field | Undirected | Image smoothing, the Ising model |
| Hidden Markov model | Directed chain with hidden states | Speech recognition, gene finding |
| Conditional random field | Undirected, conditioned on inputs | Sequence labelling |
| Linear-Gaussian state space | Directed chain with continuous states | Tracking, with the Kalman filter (Kalman, 1960) |

## Connections

- [Probability and statistics](../../../math/probability-statistics/index.md) gives the factorisation, conditional independence and maximum-likelihood ideas that PGMs use.
- [Variational inference](../variational-inference/index.md) and [Markov chain Monte Carlo](../mcmc/index.md) are the two approximate inference families for models whose exact inference is too costly.
- The directed-chain models above are the sequence members of this family. Their discriminative counterparts appear among the [supervised learning](../../supervised/index.md) methods.

## Applications

- **Medical and expert systems**: Bayesian networks encode uncertain knowledge and compute diagnoses from observed symptoms. Lauritzen and Spiegelhalter (1988) introduced the local-computation method that made this practical for large networks.
- **Speech recognition**: hidden Markov models were the standard acoustic model for decades (Rabiner, 1989).
- **Tracking and navigation**: linear-Gaussian state-space models underlie the Kalman filter (Kalman, 1960).
- **Error-correcting codes**: iterative decoding is an instance of message passing on a factor graph (Kschischang et al., 2001).

## Open questions

- Approximate inference on loopy graphs has no general guarantee of convergence or accuracy. Theory covers some special cases, and practice relies on experiments.
- Learning the graph structure from data is hard, and the search over structures is expensive.
- Exact inference cost grows with treewidth, so the design of the graph often has to balance expressiveness against tractability.

## References

### Seminal papers

- Lauritzen, S. L. & Spiegelhalter, D. J. (1988). Local computations with probabilities on graphical structures and their application to expert systems. *Journal of the Royal Statistical Society, Series B* 50(2), 157–194. https://doi.org/10.1111/j.2517-6161.1988.tb01721.x — Introduces the local-computation method for exact inference in graphical models, applied to expert systems.
- Kschischang, F. R., Frey, B. J. & Loeliger, H.-A. (2001). Factor graphs and the sum-product algorithm. *IEEE Transactions on Information Theory* 47(2), 498–519. https://doi.org/10.1109/18.910572 — Gives a unified factor-graph view of message passing, including the sum-product rule.
- Rabiner, L. R. (1989). A tutorial on hidden Markov models and selected applications in speech recognition. *Proceedings of the IEEE* 77(2), 257–286. https://doi.org/10.1109/5.18626 — Tutorial on the three basic problems of hidden Markov models: evaluation, decoding and learning.
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering* 82(1), 35–45. https://doi.org/10.1115/1.3662552 — Recursive estimator for linear-Gaussian state-space models.

### Surveys and textbooks

- Yedidia, J. S., Freeman, W. T. & Weiss, Y. (2005). Constructing free-energy approximations and generalized belief propagation algorithms. *IEEE Transactions on Information Theory* 51(7), 2282–2312. https://doi.org/10.1109/tit.2005.850085 — Links belief propagation to the Bethe free energy and generalises it.
- Wainwright, M. J. & Jordan, M. I. (2008). Graphical models, exponential families, and variational inference. *Foundations and Trends in Machine Learning*. https://nowpublishers.com/article/Details/MAL-001 — Monograph connecting graphical models, exponential families and variational methods.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press. https://github.com/probml/pml-book — Free textbook with chapters on graphical models and inference.
