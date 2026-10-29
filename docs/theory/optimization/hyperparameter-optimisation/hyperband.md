---
status: complete
last_reviewed: 2026-10-28
related:
  - theory/optimization/hyperparameter-optimisation
tags:
  - Hyperband
  - successive halving
  - multi-fidelity
  - bandits
aliases:
  - Hyperband
  - Successive halving
  - 超頻帶
---

# Hyperband (Li et al., 2017)

Hyperband runs successive halving over several starting budgets. It samples many settings, trains them briefly, keeps only the best fraction, and gives the survivors a larger budget, repeating this across brackets that trade the number of settings against the budget each one receives. Part of [Hyperparameter optimisation](index.md).

## Overview

Random search spends the full training budget on every sampled setting, so most of its compute goes to poor settings. Li, Jamieson, DeSalvo, Rostamizadeh and Talwalkar (2017) treated hyperparameter search as a pure-exploration bandit problem, where the budget is a resource that can be allocated across settings. Successive halving, from Jamieson and Talwalkar (2016), gives the basic schedule. Hyperband removes the need to choose how many settings to try, by running several schedules and choosing among them.

## Key concepts

- **Resource** \(r\): the budget of one run, such as epochs, data samples or iterations.
- **Maximum resource** \(R\): the budget of a full run.
- **Reduction factor** \(\eta\): the fraction kept between rounds is \(1/\eta\), and the budget per survivor grows by \(\eta\).
- **Bracket**: one schedule of successive halving, with a fixed trade-off between the number of settings and the starting budget.

## Problem

Given a fixed total budget, how many settings should be tried, and how many resources should each receive, when the early performance of a setting is only a noisy guide to its final performance?

## How it works

Successive halving starts with \(n\) settings, each given a budget \(r\). After each round, the best \(1/\eta\) of the settings continue with \(\eta\) times more budget. In round \(i\), the schedule runs

\[
n_i = \left\lfloor n\,\eta^{-i} \right\rfloor \text{ settings, each with budget } r_i = r\,\eta^{i}.
\]

Hyperband runs this procedure for several brackets. Let \(s_{\max} = \lfloor \log_\eta (R/r) \rfloor\). Bracket \(s\) starts with a number of settings and a minimum budget chosen so that every bracket uses about the same total budget. Brackets with a large \(s\) try many settings with little budget each, and brackets with \(s = 0\) run a few settings to full budget. The best final score over all brackets is returned.

![Animated Hyperband budget allocation: nine configurations are successively halved to three and one, alongside a separate higher-budget bracket.](../../../assets/concept-animations/hyperband-budget-motion.svg)

*Original four-stage teaching animation, CC BY-SA 4.0.* In the illustrative bracket A, a reduction factor of **three** promotes 9 configurations at resource 1 to 3 at resource 3 and then 1 at resource 9. Bracket B independently starts 3 configurations at resource 3 and promotes 1 to resource 9. Letters, rankings, and resource units are schematic, **not measured results or a benchmark**; the brackets use different sampled configurations. The animation shows budget allocation rather than claiming that early rankings are reliable. MkDocs provides Play/Pause and a reduced-motion fallback; [view the GitHub-readable static overview](../../../assets/concept-animations/hyperband-budget-still.svg).

## Key methods

This page covers one method: successive halving, run across several brackets with different trade-offs between the number of settings and their budgets.

1. Choose \(R\), \(\eta\) and \(r\), where \(R/r\) sets how many rounds of halving are possible.
2. For each bracket \(s\), sample the settings for that bracket and run successive halving on them.
3. Keep the best of the final scores from all brackets.

## Variants

- **Successive halving** on its own, with one bracket, which needs the number of settings to be chosen in advance.
- **Model-guided hybrids** replace the random sampling of settings with a model fitted to the scores, which keeps the early stopping and improves the choice of settings (Falkner et al., 2018).
- **Asynchronous variants** start new settings as soon as workers are free, instead of waiting for each round to finish.

## Results and limits

- In the experiments of Li et al. (2017), Hyperband gave over an order-of-magnitude speedup over the competitor set, which included Bayesian optimisation methods, on deep-learning and kernel-based learning problems.
- Jamieson and Talwalkar (2016) analyse successive halving in a bandit setting, and Li et al. (2017) add guarantees for the bracket schedule.
- The method assumes that the ranking of settings at a small budget predicts the ranking at full budget. When this fails, good settings can be dropped too early.
- It does not model which settings are promising. Random sampling wastes some of the budget on settings that a model would have rejected, which is the motivation for the hybrid methods.

## Applications

- **Tuning deep networks** when a training run can be stopped early, for example by a number of epochs.
- **Tuning on data subsets**, where the resource is the amount of training data.
- **Large sweeps on a cluster**, where many cheap runs can run in parallel.

## Open questions

- How should the resource be chosen when different settings change the cost of an epoch?
- When does early performance fail to predict final performance, and can the method detect this?

## Connections

- Parent topic: [Hyperparameter optimisation](index.md)
- Model-based alternative: [Bayesian optimisation](bayesian-optimisation.md)
- Population-based alternative that adapts settings during training: [Population-based training](../../paradigms/reinforcement-learning/multi-agent-rl/population-based-training/index.md)

## References

### Seminal papers

- Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A. & Talwalkar, A. (2017). Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization. *Journal of Machine Learning Research* 18(185). arXiv:1603.06560. https://arxiv.org/abs/1603.06560 — Introduces Hyperband, which runs successive halving over several brackets.
- Jamieson, K. & Talwalkar, A. (2016). Non-stochastic Best Arm Identification and Hyperparameter Optimization. In *AISTATS 2016*, PMLR 51. https://proceedings.mlr.press/v51/jamieson16.html — Gives the successive-halving schedule and its theoretical analysis.
- Falkner, S., Klein, A. & Hutter, F. (2018). BOHB: Robust and Efficient Hyperparameter Optimization at Scale. In *Proceedings of the 35th ICML*, PMLR 80. https://proceedings.mlr.press/v80/falkner18a.html — Replaces random sampling in Hyperband with a model of good settings.

### Surveys and textbooks

- Bergstra, J. & Bengio, Y. (2012). Random Search for Hyper-Parameter Optimization. *Journal of Machine Learning Research* 13, 281–305. https://jmlr.org/papers/v13/bergstra12a.html — The random-search baseline on which Hyperband improves by allocating budget across settings.
- Snoek, J., Larochelle, H. & Adams, R. P. (2012). Practical Bayesian Optimization of Machine Learning Algorithms. In *NeurIPS 2012*. arXiv:1206.2944. https://arxiv.org/abs/1206.2944 — The model-based competitor in the Hyperband experiments.
- Feurer, M. & Hutter, F. (2019). Hyperparameter Optimization. In *Automated Machine Learning*, Springer, 3–33. https://doi.org/10.1007/978-3-030-05318-5_1 — Chapter that compares early-stopping and model-based tuning.
