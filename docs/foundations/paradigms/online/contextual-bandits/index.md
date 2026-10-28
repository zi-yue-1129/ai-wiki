---
related:
- foundations/paradigms/reinforcement-learning/index.md
tags:
  - bandits
  - contextual bandits
  - recommendation
---

# Contextual Bandits

Contextual bandits extend the bandit problem with features. Before each choice the learner observes a context, such as a user profile or a news article, and chooses an action whose expected reward depends on that context. Linear models are the usual starting point, with confidence bounds or posterior sampling used for exploration.

## Overview

The learner maintains a model of expected reward as a function of context and action. Exploration comes from uncertainty in that model: LinUCB adds a confidence width to a linear prediction, while Thompson sampling draws a parameter from the posterior. The regret bounds depend on the dimension of the context and on how well the model class fits the rewards.

## Key methods

- **LinUCB**: a linear reward model with an optimistic confidence bound on each action's predicted reward.
- **Thompson sampling for contextual bandits**: sample a parameter from the posterior and act greedily under the sample, which works with richer models.
- **Neural and non-linear bandits**: use a neural network to predict rewards and exploit its uncertainty estimates for exploration.

## Connections

Contextual bandits combine [stochastic bandits](../stochastic-bandits/index.md) with supervised regression of the reward, see [supervised learning](../../supervised/linear-models/index.md). The reward model is the same kind of function that [reinforcement learning](../../reinforcement-learning/index.md) approximates, without the state transitions.

## Applications

Personalised news and product recommendation, ad selection, and choosing treatments or interventions based on patient features.

## Open questions

Contextual models can be biased when the logged data comes from an old policy, and exploration in high-dimensional contexts is costly. Fairness and safety constraints add further requirements that are hard to satisfy in the basic model.

## References

### Seminal papers

- Li, Chu, Langford & Schapire (2010), "A contextual-bandit approach to personalized news article recommendation", WWW, arXiv:1003.0146 — LinUCB, applied to news recommendation with real user logs.
- Chu, Li, Reyzin & Schapire (2011), "Contextual bandits with linear payoff functions", AISTATS. https://proceedings.mlr.press/v15/chu11a — Gives regret bounds for linear contextual bandits, a theoretical companion to LinUCB.
- Chapelle & Li (2011), "An empirical evaluation of Thompson sampling", NeurIPS. https://papers.nips.cc/paper/4321-an-empirical-evaluation-of-thompson-sampling — Shows that Thompson sampling performs strongly in practice, in a contextual news recommendation setting.

### Surveys and textbooks

- Russo, Van Roy, Kazerouni, Osband & Wen (2018), "A tutorial on Thompson sampling", Foundations and Trends in Machine Learning, arXiv:1707.02038 — Tutorial on posterior sampling for bandits, including contextual models.
- Slivkins (2019), "Introduction to multi-armed bandits", arXiv:1904.07272 — Survey that covers contextual bandits and their regret analysis.

### Lectures and videos

No further entries for this page.

### Articles and documentation

No further entries for this page.

## Further reading

- Lattimore & Szepesvári (2020), *Bandit Algorithms*, Cambridge University Press. https://cambridge.org/core/books/bandit-algorithms/introduction/022B0BDCFDC5B66E5EF2C2690467D928 — Textbook with chapters on linear and contextual bandits.
