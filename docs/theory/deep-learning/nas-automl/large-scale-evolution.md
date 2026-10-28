---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/deep-learning/nas-automl
tags:
  - neural architecture search
  - evolutionary algorithms
  - mutation operators
aliases:
  - Large-scale evolution
  - 大規模演化
---

# Large-scale evolution of image classifiers (Real et al., 2017)

Large-scale evolution applies simple evolutionary algorithms to architecture search at very large scale, starting from trivial networks and using mutation operators designed to navigate a large search space. Part of [Neural architecture search](index.md).

## Overview

Real, Moore, Selle, Saxena, Suematsu, Tan, Le and Kurakin (2017) asked how far a search without any learned controller could go when given large compute. Their aim was to minimise human participation, so the method starts from trivial initial networks and evolves them into fully trained classifiers with no further human input. The paper also emphasises the repeatability of the results and the variability of the outcomes, which were reported across runs. The later method [Regularized evolution](regularized-evolution.md) builds on this work.

## Key concepts

- **Trivial initial model**: a minimal network from which evolution starts.
- **Mutation operator**: a rule that changes a network, such as adding a layer, changing a filter size, or changing a connection.
- **Population**: the set of networks kept during evolution, with each network trained to completion.

## Problem

Can simple evolutionary search, without a learned controller and starting from trivial models, reach accuracy comparable to architectures designed by human experts?

## How it works

The algorithm keeps a population of trained networks. Each step chooses a parent, applies a mutation operator to produce a child, trains the child, and adds it to the population. Over many steps the population improves, and the final models are fully trained without human intervention.

The mutation operators are the main design choice. They are intended to make it possible to move through a large search space, so that the population can reach good architectures from trivial starting points.

## Key methods

This page covers one method: simple evolution with novel mutation operators, starting from trivial networks, run at very large scale.

- **Initialisation**: trivial networks, with no complex structure.
- **Mutation**: operators that add, remove or change layers and connections, with a focus on large moves.
- **Selection and replacement**: the population is updated as children are trained.

## Variants

- **Ensemble output**: the paper reports the accuracy of an ensemble of evolved models in addition to single models.
- **Other search spaces** change the mutations and the networks they act on, without changing the evolutionary loop.

## Results and limits

- Real et al. (2017) report accuracies of 94.6% on CIFAR-10 for a single model (95.6% for an ensemble) and 77.0% on CIFAR-100, starting from trivial initial conditions.
- The paper stresses the computational requirements of the search, which were very large for the time, and reports the variability of outcomes across runs.
- The results depend on the mutation operators, which were designed for the search space in the paper.
- Because each candidate is trained to completion, the approach needs a great deal of compute, and it is hard to reproduce on a small budget.

## Applications

- **Image classifier search** when a large compute budget is available and human design effort is to be minimised.
- **Studies of search repeatability**, since the paper reports variability across runs.
- **Baseline** for later evolutionary methods such as [regularised evolution](regularized-evolution.md).

## Open questions

- How much of the result depends on the scale of compute, and how much on the mutation operators?
- How stable are evolutionary search outcomes across seeds, when the budget is small?

## Connections

- Parent topic: [Neural architecture search](index.md)
- Later evolutionary method: [Regularized evolution](regularized-evolution.md)
- Reinforcement-learning search it is compared with: Zoph and Le (2017), cited on the [parent page](index.md)

## References

### Seminal papers

- Real, E., Moore, S., Selle, A., Saxena, S., Suematsu, Y. L., Tan, J., Le, Q. & Kurakin, A. (2017). Large-Scale Evolution of Image Classifiers. In *Proceedings of the 34th ICML*, PMLR 70. https://proceedings.mlr.press/v70/real17a.html — Shows that simple evolution at large scale, from trivial starting networks, reaches accuracy comparable to published models on CIFAR-10 and CIFAR-100.
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence* 33, 4780–4789. https://doi.org/10.1609/aaai.v33i01.33014780 — Later evolutionary method that changes the replacement rule.
- Zoph, B. & Le, Q. V. (2017). Neural Architecture Search with Reinforcement Learning. In *ICLR 2017*. arXiv:1611.01578. https://arxiv.org/abs/1611.01578 — The reinforcement-learning search that this work compares against.

### Surveys and textbooks

- Elsken, T., Metzen, J. H. & Hutter, F. (2019). Neural Architecture Search: A Survey. *Journal of Machine Learning Research* 20(55). https://jmlr.org/papers/v20/18-598.html — Survey that organises evolutionary search among the search strategies.
- Liu, H., Simonyan, K. & Yang, Y. (2019). DARTS: Differentiable Architecture Search. In *ICLR 2019*. arXiv:1806.09055. https://arxiv.org/abs/1806.09055 — Gradient-based search that avoids the cost of training every candidate.
- Pham, H. et al. (2018). Efficient Neural Architecture Search via Parameter Sharing. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/pham18a.html — Weight-sharing alternative that reduces the cost of each candidate.
