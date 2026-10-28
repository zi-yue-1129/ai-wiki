---
status: draft
last_reviewed: 2026-10-28
tags:
  - reinforcement learning
  - self-play
aliases:
  - PBT
  - Population-based training
  - 基於族群的訓練
  - AlphaStar league
---

# Population-Based Training (Jaderberg et al., 2017)

Population-based training (PBT) trains many agents in parallel. Weaker members periodically copy the weights and hyperparameters of stronger ones and perturb the copied hyperparameters. First designed for tuning neural networks, it became the basis of multi-agent training in systems such as the Quake III team agents and AlphaStar, which trains against a league of agents. See the [multi-agent reinforcement learning](../index.md) overview.

## Overview

Usual hyperparameter tuning runs many separate jobs and keeps the best, spending most compute on runs that are discarded. Jaderberg et al. (2017) optimise a population of models and their hyperparameters jointly, within one fixed budget, and obtain a schedule of settings rather than one fixed setting.

In multi-agent settings the population also supplies opponents. A learner that trains against one fixed rival can settle on strategies that beat that rival and lose to others. A diverse population, in which members play one another, is a form of [self-play](../../mcts-and-self-play/index.md) with a memory of past strategies.

## Key concepts

- **Population**: $N$ agents, each with its own weights, hyperparameters and performance history.
- **Exploit**: a weak member replaces its weights and hyperparameters with those of a strong member.
- **Explore**: after copying, the hyperparameters are perturbed at random, so the population keeps searching.
- **League**: in AlphaStar, a population with several roles. Main agents play against the whole league, while exploiters look for the weaknesses of the others.
- **Fictitious self-play**: learning against a mixture of past opponents rather than the latest one (Heinrich & Silver, 2016), an idea the league's opponent sampling builds on.

## How it works

PBT is an algorithm rather than a single equation. Its loop is:

1. Initialise $N$ workers with random weights and random hyperparameters.
2. Train all workers in parallel for a fixed number of steps, and record each one's fitness, such as its average return or win rate.
3. For each worker in the bottom quantile, copy the weights and hyperparameters of a worker drawn from the top quantile.
4. Perturb the copied hyperparameters, for example by multiplying each one by a random factor.
5. Repeat steps 2 to 4 until the budget is spent, and keep the best member.

In AlphaStar's league, the roles are separated. Main agents train against a mixture of league members, weighted towards opponents they currently lose to. Main exploiters target the main agents, and league exploiters target weaknesses across the league. Past snapshots stay in the league so that old strategies are not forgotten.

OpenAI Five is closely related, but its published account centres on large-scale self-play with continual training over months (Berner et al., 2019).

## Results

The PBT paper reports hyperparameter schedules found within a fixed budget on deep learning tasks, including reinforcement learning; the comparisons are in the paper. Jaderberg et al. (2019) report that population-trained teams competed successfully against human players in Quake III Capture the Flag. Vinyals et al. (2019) report grandmaster-level play in StarCraft II, and Berner et al. (2019) report that OpenAI Five defeated the Dota 2 world champions in 2019.

## Limitations

- **Compute.** Populations and leagues need many parallel games. Few groups can reproduce the largest results.
- **Heuristic search.** The exploit and explore rules are sensible but carry no general guarantee of finding good schedules.
- **Non-transitive strength.** Rock-paper-scissors-like cycles mean that a single fitness number can rank agents misleadingly. The league addresses this, but it adds complexity.
- **Limited transfer.** The reported successes are in games with clear win conditions and simulators. Their transfer to physical or open-ended multi-agent problems is not shown.

## Open questions

What population structure best prevents cycling, and how should progress be measured when strength is not transitive? Lanctot et al. (2017) relate population training to game-theoretic best responses. Exploit-and-explore also resembles [evolutionary search](../../../evolutionary/index.md), and it is unclear how far that analogy carries to learned policies.

## References

### Seminal papers

- Jaderberg, M. et al. (2017). *Population Based Training of Neural Networks*. arXiv:1711.09846. https://arxiv.org/abs/1711.09846 — Introduces PBT, which jointly optimises a population of networks and their hyperparameters within a fixed compute budget.
- Jaderberg, M. et al. (2019). *Human-level performance in 3D multiplayer games with population-based reinforcement learning*. Science. https://doi.org/10.1126/science.aau6249 — Trains teams of agents for Quake III Capture the Flag through a population, which competed with human players.
- Vinyals, O. et al. (2019). *Grandmaster level in StarCraft II using multi-agent reinforcement learning*. Nature. https://doi.org/10.1038/s41586-019-1724-z — AlphaStar, trained with a league of main agents and exploiters.
- Heinrich, J. & Silver, D. (2016). *Deep Reinforcement Learning from Self-Play in Imperfect-Information Games*. arXiv:1603.01121. https://arxiv.org/abs/1603.01121 — Neural fictitious self-play, which learns against a mixture of past opponents and approaches equilibria in imperfect-information games.

### Surveys and textbooks

- Hernandez-Leal, P., Kartal, B. & Taylor, M. E. (2018). *A Survey and Critique of Multiagent Deep Reinforcement Learning*. arXiv:1810.05587. https://arxiv.org/abs/1810.05587 — Reviews deep multi-agent methods, including the population and self-play approaches used in games.

### Articles and documentation

- Berner, C. et al. (2019). *Dota 2 with Large Scale Deep Reinforcement Learning*. arXiv:1912.06680. https://arxiv.org/abs/1912.06680 — The OpenAI Five system, trained by large-scale self-play and continual training over months.
- Baker, B. et al. (2019). *Emergent Tool Use From Multi-Agent Autocurricula*. arXiv:1909.07528. https://arxiv.org/abs/1909.07528 — Shows that competition inside a population produces a sequence of new strategies, a self-generated curriculum.
- Lanctot, M. et al. (2017). *A Unified Game-Theoretic Approach to Multiagent Reinforcement Learning*. arXiv:1711.00832. https://arxiv.org/abs/1711.00832 — Proposes approximate best responses to mixtures of policies, a population-level view of multi-agent training.
