---
status: draft
last_reviewed: 2026-10-28
related:
- brain-mind/decision-reward
- brain-mind/predictive-coding
- theory/paradigms/reinforcement-learning
tags:
- computational psychiatry
- psychiatry
- reinforcement learning
- machine learning
aliases:
  - 計算精神醫學
  - 計算精神病學
  - Computational psychiatry
  - Computational models of psychiatric symptoms
---

# Computational Psychiatry

Computational psychiatry uses mathematical models of learning, decision making and perception to describe psychiatric symptoms in terms of the underlying computations. The models are research tools for measuring those computations. They are not diagnostic tests.

This page is part of [Brain & Mind](../index.md). It introduces the field and compares its two landmark methods, which have their own pages.

## Overview

Psychiatric symptoms are usually described through self-report and clinical observation. These descriptions vary widely between people and over time, and two people with the same symptom may differ in many ways. Computational psychiatry asks whether some of that variation can be captured by a few model parameters. Examples include how quickly a person updates expectations after a surprise, or how strongly prior beliefs outweigh noisy sensory evidence. If a parameter can be estimated from behaviour, it can be compared across people, groups and treatments.

The field draws on three families of tools. Reinforcement learning (RL) models describe how choices are shaped by rewards and by prediction errors, the same update that [Decision Making, Dopamine & Reward](../decision-reward/index.md) discusses. Bayesian models describe how beliefs change with evidence and how prior expectations shape perception. Machine learning methods find patterns in large data sets and are used to predict diagnosis or treatment response.

Huys, Maia and Frank (2016) separate the field into two complementary branches. Data-driven methods apply machine learning to high-dimensional data, generally without modelling the mechanism. Theory-driven methods build models that encode a hypothesis about mechanism. The review highlights the value of combining the two, with an emphasis on clinical applications.

## Key concepts

- **Computational phenotype**: a set of model parameters, estimated from behaviour, that summarises how a person learns or decides.
- **Endophenotype**: a measurable trait that is linked to an illness and may be shared across people or conditions.
- **Prediction error**: the difference between what happened and what was expected. Its role in learning is explained in [Dopamine Reward Prediction Error](../neuroscience/dopamine-reward-prediction-error/index.md), which is not repeated here.
- **Hierarchical model**: a model in which individual parameters are drawn from a shared group distribution, so that each person's estimate is informed by the others.

## Core ideas

Three ideas recur across the field.

First, symptoms can be studied as variation along continuous dimensions, not only as fixed categories. Wang and Krystal (2014) argue that computational modelling can identify core deficits that cut across disorders, and that models can link cells and circuits to behaviour.

Second, a model is only useful if it is tied to a mechanism that can be tested. A learning model makes specific predictions about choices and about the brain signals that track learning, and both can be checked. This is why the field pairs with [Neuroimaging & Recording Methods](../neuroimaging-methods/index.md).

Third, measurement is the hard part. Model parameters are inferred, not observed, and their meaning depends on the model. Wilson and Collins (2019) give practical rules for relating models to behavioural data so that the conclusions are meaningful.

## Key methods

Each method has its own page. This list is only a comparison.

- [Computational phenotyping with hierarchical Bayesian RL models (Ahn et al., 2017)](computational-phenotyping/index.md): fits a learning model to each person's choices while estimating group-level parameter distributions. It separates itself from single-person fitting by sharing information across people.
- [Aberrant prediction error in psychosis (Corlett et al., 2007)](aberrant-prediction-error-psychosis/index.md): starts from a brain signal and asks whether it is disrupted in people with delusional beliefs. It separates itself from phenotyping by testing a neural mechanism rather than a set of behavioural parameters.

Machine learning for diagnosis and treatment prediction does not have its own method page here. It is discussed under Applications.

## Connections

- **Reinforcement learning**: the model class behind most phenotyping work is covered in [Reinforcement Learning](../../theory/paradigms/reinforcement-learning/index.md), and the controllers that these models separate are on [Model-Based vs Model-Free Control](../decision-reward/model-based-vs-model-free/index.md).
- **Predictive coding**: several accounts of psychosis treat it as a disorder of prediction. See [Predictive Coding & Free Energy](../predictive-coding/index.md).
- **Attention**: aberrant salience, the idea that events feel more significant than they are, links to [Attention in Brains & Machines](../attention-brain-machine/index.md).
- **Psychology**: the human side of choice, including biases, is in [Psychology & AI](../psychology/index.md).
- **Probabilistic methods**: Bayesian fitting uses the same inference tools as [Probabilistic Methods](../../theory/paradigms/probabilistic/index.md).

## Applications

- **Research phenotyping**: researchers fit learning and decision models to behaviour and compare the parameters across groups. The hBayesDM package makes this possible with few lines of code (Ahn et al., 2017).
- **Prediction from data**: machine learning has been used to predict whether people with depression will respond to a treatment. Chekroud et al. (2016) tested whether such predictions carried across clinical trials.
- **Biomarkers**: models trained on brain data are being evaluated as potential biomarkers in translational neuroimaging (Woo et al., 2017). These remain research tools.

## Open questions

- **Are the parameters stable?** It is unclear whether fitted parameters stay consistent over time and across tasks, and whether they predict symptoms or treatment response.
- **Shared or specific?** Wang and Krystal's idea of shared deficits across disorders is attractive, but it is not settled whether one model family fits several conditions.
- **Does prediction generalise?** Classifiers that work in one sample may not transfer to other clinics, populations or trials.
- **How should the two branches combine?** Huys et al. (2016) highlight the value of combining data-driven and theory-driven work, but how best to combine them is still open.

## References

### Seminal papers

- Montague, P. R., Dolan, R. J., Friston, K. J. & Dayan, P. (2012). Computational psychiatry. *Trends in Cognitive Sciences*. https://doi.org/10.1016/j.tics.2011.11.018 — Introduces computational psychiatry, which characterises mental dysfunction as aberrant computations, and highlights reinforcement learning and game-theoretic work.
- Chekroud, A. M. et al. (2016). Cross-trial prediction of treatment outcome in depression: a machine learning approach. *The Lancet Psychiatry*. https://doi.org/10.1016/S2215-0366(15)00471-X — Trains a machine learning model to predict depression treatment outcome in one trial and tests it in an independent trial.
- Ahn, W.-Y., Haines, N. & Zhang, L. (2017). Revealing Neurocomputational Mechanisms of Reinforcement Learning and Decision-Making With the hBayesDM Package. *Computational Psychiatry*. https://doi.org/10.1162/cpsy_a_00002 — Introduces hBayesDM, an R package for hierarchical Bayesian fitting of reinforcement learning and decision models, with model comparison and latent-variable export.
- Corlett, P. R. et al. (2007). Disrupted prediction-error signal in psychosis: evidence for an associative account of delusions. *Brain*. https://doi.org/10.1093/brain/awm173 — An fMRI study of 12 healthy participants and 12 with delusional beliefs, reporting disrupted frontal prediction-error responses related to delusion-forming tendency.

### Surveys and textbooks

- Huys, Q. J. M., Maia, T. V. & Frank, M. J. (2016). Computational psychiatry as a bridge from neuroscience to clinical applications. *Nature Neuroscience*. https://doi.org/10.1038/nn.4238 — Separates data-driven from theory-driven approaches, reviews clinical applications of both, and highlights the value of combining them.
- Wang, X.-J. & Krystal, J. H. (2014). Computational Psychiatry. *Neuron*. https://doi.org/10.1016/j.neuron.2014.10.018 — Argues that computational models can identify core deficits across disorders and inform diagnosis and treatment, and calls for cross-disciplinary training.
- Maia, T. V. & Frank, M. J. (2011). From reinforcement learning models to psychiatric and neurological disorders. *Nature Neuroscience*. https://doi.org/10.1038/nn.2723 — Reviews how reinforcement learning models describe behaviour in psychiatric and neurological disorders.
- Woo, C.-W. et al. (2017). Building better biomarkers: brain models in translational neuroimaging. *Nature Neuroscience*. https://doi.org/10.1038/nn.4478 — Reviews how predictive brain models can be developed and validated as biomarkers.
- Wilson, R. C. & Collins, A. G. (2019). Ten simple rules for the computational modeling of behavioral data. *eLife*. https://doi.org/10.7554/eLife.49547 — A beginner-friendly guide to relating computational models to behavioural data, set out as ten rules for meaningful conclusions.
