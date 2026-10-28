---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/optimization/hyperparameter-optimisation
tags:
  - grid search
  - hyperparameter optimisation
  - exhaustive search
aliases:
  - Grid search
  - 格點搜尋
---

# Grid search

Grid search trains a model at every point of a fixed lattice formed by the candidate values of each hyperparameter, and keeps the best. It is simple and reproducible, but its cost grows exponentially with the number of hyperparameters. Part of [Hyperparameter optimisation](index.md).

## Overview

Grid search is the most common way of tuning models by hand, because the lattice is easy to write down and the results are easy to read. Bergstra and Bengio (2012) showed that it is inefficient when only a few hyperparameters matter: a grid spends most of its runs on combinations that differ only in unimportant dimensions. The method is still a useful baseline, and it is the reference against which random sampling is compared.

## Key concepts

- **Grid**: the set of candidate values for each hyperparameter, whose product gives all the settings to be tried.
- **Lattice point**: one setting in the grid.
- **Resolution**: the number of candidate values per hyperparameter.

## Problem

Given a small number of hyperparameters, which settings should be tried on a regular lattice so that the best one among them is found, within a known budget?

## How it works

For hyperparameters with candidate sets of sizes \(n_1, \dots, n_d\), the grid has \(|\mathcal G| = \prod_{i=1}^{d} n_i\) points. Every point is trained and scored, and the best one is returned. The number of runs therefore grows exponentially with the number of hyperparameters \(d\), and a grid with \(n\) values per hyperparameter has \(n^d\) runs.

## Key methods

This page covers one method: the full-factorial grid, with every point trained at full budget.

1. Choose a set of candidate values for each hyperparameter, often evenly spaced on a log scale for multiplicative hyperparameters.
2. Form the product of the sets, which gives the grid.
3. Train every point and record its validation score.
4. Return the best point.

## Variants

- **Coarse-to-fine grid** runs a coarse grid, then a finer grid around the best region.
- **Random grid subsets** take a random subset of the full grid, which is a middle step between grid and random search.

## Results and limits

- Bergstra and Bengio (2012) show that a grid can give few distinct values of an important hyperparameter, because most of its runs repeat values of the unimportant ones. Random sampling gives many distinct values of each dimension for the same number of runs.
- The number of runs grows as \(n^d\), so a grid is impractical beyond a few hyperparameters.
- Grid search does not use the results of earlier runs to choose later ones, so it cannot concentrate runs where the score is good.
- Its results are reproducible and easy to parallelise, since every point is independent.

## Applications

- **Small searches** over two or three hyperparameters, such as a learning rate and a regularisation strength.
- **Sanity checks** on a model, where a full grid makes the effect of each setting easy to see.
- **Baseline** for comparing new search methods on the same budget.

## Open questions

- How should the grid be spaced when the best value of a hyperparameter depends on the others?
- When is a grid preferable to random search, given that random search is almost always at least as efficient?

## Connections

- Parent topic: [Hyperparameter optimisation](index.md)
- Sampling alternative: [Random search](random-search.md)
- Model-based alternative: [Bayesian optimisation](bayesian-optimisation.md)

## References

### Seminal papers

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — Compares grid search with random sampling and shows the grid's inefficiency when few hyperparameters matter.
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — Model-based alternative that chooses later settings from earlier results, unlike a fixed grid.

### Surveys and textbooks

- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — Chapter that describes grid search as the baseline of the field.
- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — Review that compares grid search with model-based search.
- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — Book chapters that discuss grid search alongside other tuning methods.
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — Compares its budget allocation with grid and random search on the same runs.
