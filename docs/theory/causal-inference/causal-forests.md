---
status: draft
last_reviewed: 2026-11-05
tags:
  - causal inference
  - heterogeneous treatment effects
  - random forests
aliases:
  - Causal forest
  - causal forests
  - 因果森林
  - 異質治療效應
  - CATE estimation
---

# Causal Forests

A causal forest estimates how a treatment effect varies from one individual to another. It adapts random forests so that the trees split where effects differ, and it gives confidence intervals at a point (Wager & Athey 2018). It is one of the landmark methods on the [causal inference overview](index.md).

## Problem

An average effect hides variation across people. The target is the conditional average treatment effect

$$\tau(x) = E\big[Y(1) - Y(0) \mid X = x\big],$$

where $Y(1)$ and $Y(0)$ are the potential outcomes under treatment and control. A standard random forest predicts $Y$, not the difference between two potential outcomes, and it does not give valid intervals for $\tau(x)$. Simpler approaches, such as fitting separate outcome models for treated and control units and subtracting them, can be unstable. Künzel et al. (2019) compare several such meta-learners.

## Core idea

Three ingredients, following Athey and Imbens (2016) and Wager and Athey (2018):

1. **Trees that split on effect differences.** Each split is chosen to maximise the difference in treatment effect between the two child nodes, not the difference in outcomes.
2. **Honest estimation.** Each tree uses one half of its subsample to choose the splits and the other half to estimate the effect in each leaf. Using the same data for both steps would overstate how much the effect varies.
3. **Adaptive averaging.** Averaging over many randomised trees, as in bagging with random feature subsets (Breiman 2001), gives $\hat\tau(x)$ as a weighted average of the observed outcomes. The weights measure how often each training observation falls in the same leaf as $x$.

## Algorithm

1. Draw many subsamples of size $s$ without replacement.
2. For each subsample, split it into two halves. Grow a tree on the first half, choosing each split to maximise the difference in effects between the children, using a random subset of features.
3. Estimate the effect in each leaf on the second half (honest estimation).
4. Average the leaf estimates over all trees to obtain $\hat\tau(x)$.
5. Estimate the sampling variance $\hat\sigma^2(x)$ and form the interval $\hat\tau(x) \pm z_{1-\alpha/2}\,\hat\sigma(x)$.

## Results

Wager and Athey (2018) report that, under their conditions, the causal forest estimate has an asymptotically Gaussian and centred sampling distribution. This is what permits confidence intervals centred on the estimate at a point. Their simulations and empirical checks are in the paper and are not reproduced here.

## Limitations

- **Unconfoundedness and overlap.** Like [DML](double-machine-learning.md), a causal forest needs the covariates to block all confounding. Every type of individual must have a positive chance of receiving each treatment.
- **Efficiency cost.** Honest splitting uses half of each subsample to choose splits, so in finite samples the estimates are less efficient than an unsplit forest would be.
- **Asymptotic guarantees.** The interval validity depends on conditions on subsampling and tree growth. Coverage in small samples is not guaranteed by the theory.
- **Multiple comparisons.** Examining many subgroups invites false discoveries of heterogeneity, so subgroups should be specified in advance or corrected.
- **Description, not mechanism.** The method says where effects differ, not why they differ.

## Connections

Causal forests complement [double/debiased machine learning](double-machine-learning.md). DML targets a single average effect, while a causal forest estimates the whole function $\tau(x)$. The forest itself is a random forest, whose general learning theory is in the [Machine Learning](../machine-learning/index.md) chapter.

## Applications

- **Personalised medicine.** Finding which patients benefit most from a treatment, using data from trials and registries.
- **Online experiments.** Finding which users respond to a product change, as in the online-experiment example of the [overview](index.md).
- **Policy targeting.** Choosing whom to treat when the budget is limited and the effect varies.

## Open questions

- How to estimate effects efficiently when there are many outcomes or dynamic treatments.
- How the interval guarantees behave with weak overlap and high-dimensional covariates.
- How far heterogeneity estimated in one population transfers to another.

## References

### Seminal papers

- Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. doi:[10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324) — Introduces random forests, the averaging over randomised trees on which causal forests are built.
- Athey, S. & Imbens, G. (2016). Recursive partitioning for heterogeneous causal effects. *Proceedings of the National Academy of Sciences*, 113(27), 7353–7360. doi:[10.1073/pnas.1510489113](https://doi.org/10.1073/pnas.1510489113) — Trees that split on differences in treatment effects, with honest estimation of leaf effects.
- Wager, S. & Athey, S. (2018). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. *Journal of the American Statistical Association*, 113(523), 1228–1242. doi:[10.1080/01621459.2017.1319839](https://doi.org/10.1080/01621459.2017.1319839) — The causal forest method, with an asymptotically Gaussian sampling distribution and confidence intervals at a point.
- Wager, S. & Athey, S. (2015). Estimation and Inference of Heterogeneous Treatment Effects using Random Forests. arXiv. https://arxiv.org/abs/1510.04342 — Preprint of the 2018 paper, with the same authors and method.

### Surveys and textbooks

- Athey, S., Tibshirani, J. & Wager, S. (2019). Generalized random forests. *The Annals of Statistics*, 47(2), 1148–1178. doi:[10.1214/18-AOS1709](https://doi.org/10.1214/18-AOS1709) — Extends the forest approach to any estimating equation, with the same honest splitting.
- Künzel, S. R., Sekhon, J. S., Bickel, P. J. & Yu, B. (2019). Metalearners for estimating heterogeneous treatment effects using machine learning. *Proceedings of the National Academy of Sciences*, 116(10), 4156–4165. doi:[10.1073/pnas.1804597116](https://doi.org/10.1073/pnas.1804597116) — Compares meta-learner approaches to estimating CATE with machine learning, the alternative that causal forests are often measured against.
