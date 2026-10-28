---
related:
- theory/paradigms/reinforcement-learning/index.md
tags:
  - bandits
  - UCB
  - Thompson sampling
---

# Stochastic Bandits

The stochastic bandit problem assumes each arm has a fixed unknown reward distribution. The learner must balance exploring arms to learn their means and exploiting the best arm found so far. Upper confidence bound and Thompson sampling methods are the two standard answers, and both achieve logarithmic regret under mild conditions.

## Overview

Regret compares the total reward with that of always playing the best arm. Lai and Robbins showed that logarithmic regret is the best possible, and UCB methods achieve it by playing the arm with the highest optimistic estimate of its mean. Thompson sampling keeps a posterior over the means, samples from it, and plays the arm that is best under the sample.

## Key algorithms

- **Upper confidence bound (UCB1)**: add a confidence width to each arm's empirical mean and play the largest total.
- **Thompson sampling**: sample each arm's mean from its posterior and play the best sample, which is simple and often works well in practice.
- **Explore-then-commit and epsilon-greedy**: simpler schemes with weaker guarantees, still common as baselines.

## Connections

Bandits are the one-step case of [reinforcement learning](../../reinforcement-learning/index.md), with no state transitions. The posterior sampling of Thompson sampling is the same Bayesian reasoning used in [probabilistic models](../../supervised/instance-based-and-probabilistic/index.md). The contextual extension is covered in [contextual bandits](../contextual-bandits/index.md).

## Applications

A/B testing that shifts traffic toward better variants, dose-finding in clinical trials, and choosing among a fixed set of prompts or models.

## Open questions

Heavy-tailed rewards, delayed feedback and non-stationary arms break the standard guarantees. In practice, the choice between UCB and Thompson sampling often depends on how reward models are updated.

## References

### Seminal papers

- Lai & Robbins (1985), "Asymptotically efficient adaptive allocation rules", Advances in Applied Mathematics. https://doi.org/10.1016/0196-8858(85)90002-8 — Proves the logarithmic lower bound on regret that good bandit algorithms must match.
- Auer, Cesa-Bianchi & Fischer (2002), "Finite-time analysis of the multiarmed bandit problem", Machine Learning. https://homes.di.unimi.it/~cesabian/Pubblicazioni/ml-02.pdf — UCB1, with finite-time regret bounds that are simple to apply.
- Agrawal & Goyal (2012), "Analysis of Thompson sampling for the multi-armed bandit problem", COLT, arXiv:1111.1797 — The first regret analysis of Thompson sampling, showing that it matches the logarithmic lower bound.

### Surveys and textbooks

- Bubeck & Cesa-Bianchi (2012), "Regret analysis of stochastic and nonstochastic multi-armed bandit problems", Foundations and Trends in Machine Learning, arXiv:1204.5721 — Survey that treats stochastic and adversarial bandits side by side.
- Lattimore & Szepesvári (2020), *Bandit Algorithms*, Cambridge University Press. https://cambridge.org/core/books/bandit-algorithms/introduction/022B0BDCFDC5B66E5EF2C2690467D928 — Comprehensive textbook covering UCB, Thompson sampling and lower bounds.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Slivkins (2019), "Introduction to multi-armed bandits", arXiv:1904.07272 — Accessible introduction to the bandit literature, including Bayesian and contextual settings.
