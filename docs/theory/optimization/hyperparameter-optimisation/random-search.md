---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/optimization/hyperparameter-optimisation
tags:
  - random search
  - hyperparameter optimisation
  - baseline
aliases:
  - Random search
  - Random hyperparameter search
  - 隨機搜尋
---

# Random search (Bergstra and Bengio, 2012)

Random search samples each hyperparameter setting independently from a distribution over the search space, trains it, and keeps the best. It is the standard baseline for hyperparameter optimisation. Part of [Hyperparameter optimisation](index.md).

## Overview

Before this paper, grid search was the usual way to tune a model. Bergstra and Bengio (2012) showed that when only a few hyperparameters matter, sampling settings at random covers the important dimensions far better than a grid with the same number of runs. Random search needs no model of the objective, parallelises trivially, and does not waste runs on combinations that differ only in unimportant dimensions.

## Key concepts

- **Sampling distribution**: the distribution each hyperparameter is drawn from, such as a uniform distribution on a log scale for a learning rate.
- **Effective dimension**: the number of hyperparameters that actually change the objective, which is often much smaller than the number tuned.
- **Trial**: one sampled setting, trained and scored on the validation set.

## Problem

Given a fixed budget of \(n\) training runs and a search space, which settings should be trained so that the best one is found with high probability?

## How it works

Each trial draws a setting \(x\) from the sampling distribution and records the validation score \(f(x)\). The best trial is returned. Trials are independent, so the procedure can run on as many workers as are available.

For a region of the search space that holds a fraction \(p\) of the sampling mass, the probability that none of \(n\) independent trials falls inside it is \((1-p)^n\). So the chance of landing in that region is \(1-(1-p)^n\). For example, with \(n = 60\) trials and \(p = 0.05\), the chance is about \(1 - 0.95^{60} \approx 0.95\).

## Key methods

This page covers one method: independent sampling from a distribution over the space, keeping the best trial.

1. Choose a sampling distribution for each hyperparameter, on a log scale where the effect is multiplicative.
2. Draw \(n\) settings independently.
3. Train each setting with the full budget and record its validation score.
4. Return the best setting.

## Variants

- **Quasi-random sampling** replaces independent draws with a low-discrepancy sequence, which spreads the trials more evenly.
- **Random search with early stopping** stops weak trials early, which is the idea behind [Hyperband](hyperband.md).
- **Random search with a prior** draws from distributions that depend on earlier results, which moves towards model-based methods.

## Results and limits

- In the experiments of Bergstra and Bengio (2012), random search found configurations at least as good as grid search, with fewer trials, on the problems studied, where some hyperparameters have little effect.
- Random search does not learn from earlier trials, so it spends runs on regions that earlier results already showed to be poor. Model-based methods such as [Bayesian optimisation](bayesian-optimisation.md) use that information.
- Its quality depends on the sampling distributions, so a poor choice of scale (for example a linear scale for a learning rate) can waste most of the budget.

## Applications

- **Baseline tuning** for deep networks, where a few dozen to a few hundred runs are affordable.
- **Large parallel sweeps**, where the independence of trials removes the need for coordination.
- **Reference point** when a new search method claims to be more efficient.

## Open questions

- How many trials are enough when the effective dimension is unknown in advance?
- Can the sampling distribution be chosen automatically without a model of the objective?

## Connections

- Parent topic: [Hyperparameter optimisation](index.md)
- Exhaustive alternative: [Grid search](grid-search.md)
- Model-based alternative: [Bayesian optimisation](bayesian-optimisation.md)

## References

### Seminal papers

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — Shows that random sampling of settings beats grid search when few hyperparameters matter.
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — Model-based tuning that uses the history of trials, which random search does not.
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — Uses random sampling as the source of candidates and allocates budget across them.

### Surveys and textbooks

- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — Chapter that compares random search with other tuning methods.
- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — Review that positions random search as the baseline for model-based methods.
- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — Book chapters on hyperparameter search, including random search.
