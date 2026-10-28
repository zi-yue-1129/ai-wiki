---
status: complete
last_reviewed: 2026-10-28
aliases:
  - FTW
  - For The Win
  - Capture the Flag agents
---

# For The Win (Jaderberg et al., 2019)

A population of independent reinforcement learning agents trained to play team-based Capture the Flag in Quake III Arena. The agents learn from pixels and game points, and the paper reports human-level play as both teammates and opponents.

## Problem

Earlier agents had reached human level in single-agent and turn-based two-player games, but the real world contains many agents that learn and act independently while they both cooperate and compete. Jaderberg et al. study a 3D, first-person, team game in which the agent must learn to cooperate with unseen teammates and to beat unseen opponents. The reward is sparse, since a win comes only at the end of a match.

## Core idea

The method uses a two-tier optimisation process:

- **Inner loop.** Each agent in the population learns a policy with reinforcement learning, from its own internal reward. The internal reward complements the sparse reward from winning, and the agent's policy chooses actions at several timescales.
- **Outer loop.** A population of agents is trained concurrently in thousands of parallel matches, with agents playing in teams together and against each other on randomly generated maps. The outer loop is population-based training, which adapts the internal rewards and hyperparameters of the agents.

The maps are procedurally generated, indoor and outdoor, and the team with the most flag captures after five minutes wins. Because the population contains many different agents, the training matches expose each agent to a varied set of teammates and opponents.

## Equation or algorithm

The paper does not reduce the method to one equation. Each agent is trained with reinforcement learning on its own reward, which combines the game's sparse win signal with a learned internal reward. The outer loop of population-based training adapts those internal rewards and the hyperparameters of every agent during training.

## Results

The paper evaluates the trained agents in a tournament-style setting. The abstract reports that the agents "exceeded the winrate of strong human players both as teammates and opponents" and "proved far stronger than existing state-of-the-art agents". The paper's "strong" humans are the top 20% of its 40 participants, and the abstract gives no numeric win rate against them. Skill is estimated online with Elo scores, borrowed from chess. The agents were trained for two billion steps, about 450,000 games. The learned representations encode a wide variety of game knowledge, which the paper measures with linear probes. The behaviours it describes include navigating, following and defending, and following was discarded midway through training.

## Limitations

- **Compute cost.** Training a large population over thousands of matches requires substantial parallel compute.
- **Specific environment.** The results are for one game and one set of maps, so generality beyond this setting is not shown by the paper.

## Connections

- FTW uses [population-based training](../pbt/index.md) for its outer loop, and it is the main example in the [population-based training](../index.md) overview.
- Its team and opponent setting is the mixed-setting case of the [multi-agent RL overview](../../index.md).
- For other competitive games, see the [games applications](../../../../../../applications/games/index.md) page.

## Applications

- **Video games.** Team-based first-person games and other competitive 3D environments.
- **Training under uncertainty**, where agents must cooperate with partners they have not seen before.

## Open questions

- How to make training cheaper, so that similar results need fewer matches.
- How to test generality across games and maps, not just one game.

## References

### Seminal papers

- Jaderberg et al. (2019), "Human-level performance in 3D multiplayer games with population-based reinforcement learning", *Science* 364, 859–865. https://discovery.ucl.ac.uk/id/eprint/10076318 — The FTW paper, with the two-tier optimisation, the Capture the Flag environment and the human tournament results. The link is the author-institution repository record.
- Jaderberg et al. (2018), "Human-level performance in first-person multiplayer games with population-based deep reinforcement learning", [arXiv:1807.01281](https://arxiv.org/abs/1807.01281) — The preprint version of the FTW paper, with the same method and results.
- Jaderberg et al. (2017), "Population based training of neural networks", [arXiv:1711.09846](https://arxiv.org/abs/1711.09846) — The PBT method that FTW uses for its outer loop.
- Lowe et al. (2017), "Multi-agent actor-critic for mixed cooperative-competitive environments", [arXiv:1706.02275](https://arxiv.org/abs/1706.02275) — Centralised critics for mixed cooperative and competitive settings, the setting FTW studies with a population.

### Surveys and textbooks

- Busoniu, Babuska & De Schutter (2008), "A comprehensive survey of multiagent reinforcement learning", *IEEE Transactions on Systems, Man, and Cybernetics, Part C* 38(2), 156–172. https://doi.org/10.1109/TSMCC.2007.913919 — Survey of multi-agent learning settings, including the competitive and cooperative cases FTW combines.
