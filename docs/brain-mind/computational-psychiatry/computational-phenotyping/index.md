---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- reinforcement learning
- Bayesian inference
aliases:
  - 計算表型分析
  - 階層式貝氏強化學習模型
  - hBayesDM
  - Computational phenotyping
  - Hierarchical Bayesian reinforcement learning
---

# Computational phenotyping with hierarchical Bayesian RL models (Ahn, Haines & Zhang, 2017)

Computational phenotyping fits a computational model to each person's choices in a task, then uses the fitted parameters as numerical summaries of how that person learns or decides. Hierarchical Bayesian fitting estimates those parameters for all people at once. This page covers the method as packaged in hBayesDM (Ahn et al., 2017).

This page is part of [Computational Psychiatry](../index.md). It is a research method. The parameters it produces are not diagnoses.

## Overview

A behavioural task gives each person a sequence of choices and outcomes. Standard summaries, such as overall accuracy or average choice rate, mix together several processes. Two people with the same accuracy may differ in how fast they learn from outcomes, how much they explore, or how strongly losses change their choices. A model with a few parameters tries to separate these processes, and the fitted values become candidate measures of individual differences.

## Problem

Fitting a model to one person at a time is simple, but it works poorly when each person contributes few trials. The estimates are noisy and can take implausible values. Psychiatric samples are often small. Ahn et al. (2017) note that these methods are also often too technical for clinical researchers to use.

## Core idea

Each person's choices are described by a model with a few free parameters, such as a learning rate and a choice-sensitivity parameter. Hierarchical Bayesian fitting assumes that individual parameters come from a shared group distribution. It estimates the individual parameters and the group distribution together, so each person's estimate is informed by everyone else's data. People with little data are pulled toward the group, and the group distribution itself is learned from the sample. Ahn et al. (2017) built hBayesDM to make this approach available with minimal code, covering model fitting, visualisation and model comparison for a set of decision-making tasks. The package can also export trial-by-trial latent variables, such as prediction errors, for model-based neuroimaging.

## Equation or algorithm

A common example is a delta-rule reinforcement learning model for a two-choice task. The value of the chosen option is updated by the prediction error:

\(\delta_t = r_t - Q_t(a)\), and \(Q_{t+1}(a) = Q_t(a) + \alpha\,\delta_t\)

Choices are made with a softmax rule, where \(\beta\) controls how strongly the higher-value option is preferred:

\(P(a_t = a) = \dfrac{\exp(\beta\,Q_t(a))}{\sum_b \exp(\beta\,Q_t(b))}\)

The procedure for fitting such a model hierarchically is:

1. Choose a task and one or more candidate models from theory.
2. Write the likelihood, the probability of each observed choice given the model and its parameters.
3. Place each person's parameters on a transformed scale, for example \(\alpha_i = \Phi(\mu_\alpha + \sigma_\alpha z_i)\) with \(z_i \sim \mathcal{N}(0,1)\), where \(\Phi\) is the standard normal distribution function, and give the group-level parameters \(\mu\) and \(\sigma\) their own priors.
4. Estimate the individual and group parameters together with Bayesian sampling. hBayesDM uses Stan for this.
5. Compare candidate models, and report the parameter estimates with their uncertainty.

Step 3 is a general form, not a formula from one paper. Gershman (2016) argues for setting the group-level priors from the data rather than fixing them in advance.

## Results

Ahn et al. (2017) present hBayesDM as a usable tool for fitting these models across decision-making tasks, with model comparison and latent-variable export. Their claims concern usability; the paper does not show that the parameters predict clinical outcomes.

## Limitations

- **Model dependence.** A parameter means what the model says it means. A different model of the same behaviour can give different parameter values. Wilson and Collins (2019) emphasise that models must be used with care if they are to yield meaningful insights.
- **Shrinkage.** Pulling individual estimates toward the group mean stabilises them when data are sparse, but it can also blur real differences between people. The degree of shrinkage depends on the prior, which is why the choice of prior matters (Gershman, 2016).
- **Task specificity.** Parameters are measured within a task. A parameter may capture a strategy that is specific to that task rather than a stable trait.
- **Validity.** Showing that a model fits behaviour does not show that its parameters are the mechanisms behind symptoms.

## Connections

- **Reinforcement learning**: the delta rule and softmax choice rule are the standard models in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md). The prediction error in the update is the same quantity as in the dopamine account of [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).
- **Controllers**: when a task separates habitual and planned choice, phenotyping can estimate how much each controller is used. See [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md) and [Decision Making, Dopamine & Reward](../../decision-reward/index.md).
- **Bayesian inference**: hierarchical fitting applies the probabilistic methods covered in [Probabilistic Methods](../../../theory/paradigms/probabilistic/index.md) to the model's parameters.
- **Neuroimaging**: trial-by-trial latent variables are used as regressors in model-based fMRI. See [Neuroimaging & Recording Methods](../../neuroimaging-methods/index.md).

## Applications

- **Group comparison**: researchers compare learning and decision parameters between clinical and comparison samples to test whether they differ.
- **Model-based imaging**: prediction errors estimated from the fitted model are correlated with brain activity on each trial.

## Open questions

- **Stability.** Do fitted parameters stay consistent across sessions, and do they predict symptoms or treatment response?
- **Model choice.** Which candidate model is right for a given condition, and how far do conclusions depend on that choice?
- **Small samples.** How much do conclusions change with the choice of group-level priors when data are limited?

## References

### Seminal papers

- Ahn, W.-Y., Haines, N. & Zhang, L. (2017). Revealing Neurocomputational Mechanisms of Reinforcement Learning and Decision-Making With the hBayesDM Package. *Computational Psychiatry*. https://doi.org/10.1162/cpsy_a_00002 — Introduces hBayesDM, an open-source package for hierarchical Bayesian fitting of reinforcement learning and decision models, with model comparison and latent-variable export.
- Gershman, S. J. (2016). Empirical priors for reinforcement learning models. *Journal of Mathematical Psychology*. https://doi.org/10.1016/j.jmp.2016.01.006 — Argues for setting priors on reinforcement learning parameters from data, rather than fixing them in advance.

### Surveys and textbooks

- Wilson, R. C. & Collins, A. G. (2019). Ten simple rules for the computational modeling of behavioral data. *eLife*. https://doi.org/10.7554/eLife.49547 — A beginner-friendly guide to relating computational models to behavioural data, with ten rules for meaningful conclusions and code examples.
- Sutton, R. S. & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — The standard textbook on the value-learning and choice models used in this method.

### Articles and documentation

- CCS-Lab. *hBayesDM: hierarchical Bayesian modeling of decision-making tasks*. GitHub repository. https://github.com/CCS-Lab/hBayesDM — Source code and tutorials for the package, which is the practical form of this method.
