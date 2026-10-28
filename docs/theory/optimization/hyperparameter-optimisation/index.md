---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/optimization
  - theory/deep-learning/nas-automl
tags:
  - hyperparameter optimisation
  - Bayesian optimisation
  - multi-fidelity
  - AutoML
aliases:
  - Hyperparameter optimisation
  - Hyperparameter tuning
  - Hyperparameter optimization
  - 超參數最佳化
---

# Hyperparameter optimisation

Hyperparameters are the settings of a learning algorithm that are not fitted by gradient descent, such as the learning rate, the batch size, the regularisation strength and the width of a network. Hyperparameter optimisation searches for the settings that give the best validation performance, within a budget of training runs. Part of [Optimisation](../index.md).

## Overview

Tuning hyperparameters is often the largest cost of building a model. Bergstra and Bengio (2012) showed that random sampling of settings beats a regular grid when only a few hyperparameters matter, because a grid spends most of its runs on dimensions that do not matter. Snoek, Larochelle and Adams (2012) then showed that a model of the validation score, fitted to earlier runs, can choose the next setting more efficiently than random search. Later methods reduce cost in a different way: they stop poor runs early, copy the state of good runs, or fit the settings on a small model and transfer them to a large one.

## Key concepts

- **Search space**: the range and type of each hyperparameter, such as a log-uniform learning rate or a choice of optimiser.
- **Objective**: the validation score the search tries to optimise, usually a loss or an error rate.
- **Budget**: the total compute the search may spend, measured in training runs, epochs or GPU-hours.
- **Surrogate model**: a cheap model of the objective, fitted to earlier runs, which proposes the next setting.
- **Multi-fidelity**: runs that use a cheap approximation of the full training, such as fewer epochs or less data, to rank settings early.

## Problem

Given a search space and a fixed budget, which settings should be trained, and how should runs be stopped or continued, so that the best setting is found with the fewest runs?

## How it works

Most methods repeat one loop. They propose a setting, train it with some budget, record the validation score, and use the new score to decide the next proposal. The methods differ in how they make the proposal and how much of each run they keep.

- **Model-free sampling** draws settings at random or on a grid. Random search is the standard baseline.
- **Model-based search** fits a surrogate to the observed scores and proposes the setting with the best expected gain. The [Bayesian optimisation](bayesian-optimisation.md) page covers this family.
- **Bandit and early-stopping methods** treat the budget as a resource. Many settings are started and the poor ones are dropped early. The [Hyperband](hyperband.md) page covers this family.
- **Population-based training** runs many settings in parallel and copies the weights and settings of the best runs into the weaker ones during training. See [Population-based training](../../paradigms/reinforcement-learning/multi-agent-rl/population-based-training/index.md).
- **Transfer of settings** fits the best settings on a small model and reuses them on a large model. Yang et al. (2022) show that, under the maximal update parametrisation (μP), many optimal settings stay stable as the width of a network grows, which makes this transfer possible. See [μP](../../deep-learning/initialisation/mup.md).

## Key methods

This section gives the comparison and links down. Each method has its own page.

- [Bayesian optimisation](bayesian-optimisation.md): a Gaussian-process surrogate and an acquisition function choose each next setting. Best when runs are expensive and the space is small.
- [Hyperband](hyperband.md): successive halving across several budgets, which starts many settings and gives more budget only to the best. Best when early scores predict final scores.
- [Population-based training](../../paradigms/reinforcement-learning/multi-agent-rl/population-based-training/index.md): a population adapts settings during a single training run.
- [μP](../../deep-learning/initialisation/mup.md): tune on a small model, then transfer the settings to a large one.

## Variants

- **Hybrid methods** combine a bandit schedule with a model that proposes the settings, which keeps the early stopping and improves the choice of settings (Falkner et al., 2018).
- **Multi-objective tuning** optimises accuracy together with cost, such as latency or memory.
- **Conditional spaces**, where some hyperparameters only exist when others take a value, need a search method that handles structure.

## Results and limits

- Random search beats grid search when few hyperparameters matter (Bergstra & Bengio, 2012).
- Bayesian optimisation reached or surpassed expert-level tuning of several learning algorithms in the experiments of Snoek et al. (2012). Its choices depend on the prior on the surrogate, which can change the outcome a great deal.
- Hyperband gave over an order-of-magnitude speedup over the Bayesian optimisation methods it was compared with, in the experiments of Li et al. (2017).
- μP makes it possible to tune a model with 13 million parameters and transfer the settings to BERT-large, with a total tuning cost equal to one pre-training run of BERT-large (Yang et al., 2022).
- Surrogate models scale poorly with many runs and high-dimensional spaces, and early-stopping methods assume that early scores rank settings correctly.

## Applications

- **Training deep networks**, where the learning rate and schedule dominate the result.
- **Pre-training large models**, where transferring settings from a small model saves most of the tuning cost.
- **AutoML pipelines**, which combine hyperparameter search with [architecture search](../../deep-learning/nas-automl/index.md).

## Open questions

- When do early scores predict final scores well enough for early stopping, and when do they mislead?
- How should a search be run when the budget is so small that only one or two full runs are possible?
- Do transferred settings remain correct when the data or the architecture changes, not only the width?

## Connections

- Parent topic: [Optimisation](../index.md)
- Architecture choice: [Neural architecture search and AutoML](../../deep-learning/nas-automl/index.md)
- Learning-rate schedules, which are often among the hyperparameters tuned: [Learning-rate schedules](../learning-rate-schedules.md)

## References

### Seminal papers

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — Shows that random sampling of settings finds good configurations faster than a grid when few hyperparameters matter.
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — Uses a Gaussian-process surrogate and expected improvement to tune learning algorithms.
- Jamieson, K. & Talwalkar, A. (2016). Non-stochastic Best Arm Identification and Hyperparameter Optimization. In *AISTATS 2016*, PMLR 51. https://proceedings.mlr.press/v51/jamieson16.html — Formulates successive halving for hyperparameter search, with theoretical guarantees.
- Li, L. et al. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — Runs successive halving over several budgets and compares it with Bayesian optimisation.
- Jaderberg, M. et al. (2017). Population Based Training of Neural Networks. arXiv:1711.09846. https://arxiv.org/abs/1711.09846 — Adapts settings and weights during one training run by copying the best members of a population.

### Surveys and textbooks

- Shahriari, B. et al. (2016). Taking the Human Out of the Loop: A Review of Bayesian Optimization. *Proceedings of the IEEE* 104(1), 148–175. https://doi.org/10.1109/JPROC.2015.2494218 — Review of Bayesian optimisation, its surrogates and acquisition functions.
- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — Chapter that surveys the methods above with their trade-offs.
- Yang, G. et al. (2022). Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer. arXiv:2203.03466. https://arxiv.org/abs/2203.03466 — Shows that optimal settings under μP transfer from a small network to a large one.
- Falkner, S., Klein, A. & Hutter, F. (2018). BOHB: Robust and Efficient Hyperparameter Optimization at Scale. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/falkner18a.html — Combines a bandit schedule with a model-based choice of settings.

## Further learning

- Hutter, F., Kotthoff, L. & Vanschoren, J. (eds.) (2019). *Automated Machine Learning: Methods, Systems, Challenges*. Springer. https://doi.org/10.1007/978-3-030-05318-5 — Book with chapters on hyperparameter optimisation and architecture search.
