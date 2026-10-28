---
status: draft
last_reviewed: 2026-10-28
aliases:
  - OpenAI Five
  - Dota 2 AI
---

# OpenAI Five (OpenAI et al., 2019)

OpenAI Five is a team of five neural-network agents that learned to play Dota 2 by self-play. In April 2019 it beat OG, the reigning world champions, in a best-of-three match. It is the Dota 2 entry in the [Games](../index.md) milestones.

## Problem

Dota 2 is a five-versus-five team game with long time horizons, imperfect information from fog of war, and large continuous action spaces. The question was whether self-play reinforcement learning could reach superhuman play in such a game, at a scale far beyond earlier game-playing systems.

## Key concepts

- **Self-play**: the agents improve by playing copies of themselves, so the opponents get stronger as the agents do.
- **Recurrent policy**: a network with memory across game ticks, so it can use what it saw earlier in a match even though much of the map is hidden.
- **Reward symmetrisation**: each agent's reward is adjusted by the opposing team's reward, so the agents learn to win rather than to maximise their own score.
- **Public arena**: online games against outside players, used as a test the agents had not been tuned for.

## Core idea

Each hero is controlled by a policy network with an LSTM memory. The network reads a processed view of the game and outputs actions. Agents learn by playing against copies of themselves, and about 20% of games are played against older versions of the policy. Rewards are symmetrised by subtracting the opposing team's reward, so the agents learn to win rather than to maximise their own score.

## Equation or algorithm

Training uses Proximal Policy Optimization (PPO), a clipped policy-gradient method (Schulman et al., 2017). The training loop is distributed:

1. Rollout machines run the Dota 2 engine on CPUs and send observations to forward-pass GPUs, which choose actions.
2. Experience is stored in buffers. Optimiser GPUs compute PPO updates on large batches of one to three million timesteps, using up to 1,536 GPUs at peak.
3. Updated parameters are published, and rollouts use the latest version.

## Results

The paper, the source for the figures below, describes one continuous training run from 30 June 2018 to 22 April 2019. The run took about ten months of real time and 180 days of training, using about 770 ± 50 PFlop/s-days of compute. The model is a recurrent network with about 159 million parameters.

- In April 2019, OpenAI Five beat OG, the reigning world champions, in a best-of-three match.
- In an arena open to the public from 18 to 21 April 2019, OpenAI Five won 99.4% of 7,257 games against 3,193 teams. Twenty-nine teams won 42 games against it. Many human players abandoned losing games, which the paper notes makes the measure imperfect.

## Limitations

- The agent played a restricted game. It supported 17 of the 117 heroes and could not use items that let one player control several units at once.
- Winning in an arena does not show broad understanding of the game. The arena was run to test whether creative or out-of-distribution play could exploit the system, and some teams did beat it.
- Training used about 770 PFlop/s-days of compute, which few groups can reproduce.

## Connections

- [Proximal policy optimisation](../../../theory/paradigms/reinforcement-learning/proximal-policy-optimisation/index.md): the training algorithm.
- [Reinforcement learning](../../../theory/paradigms/reinforcement-learning/index.md): the wider family of methods for learning from reward. Its section on the brain covers how reward-prediction signals in animals relate to these methods.
- Brain and mind: the agents learn from delayed reward through trial and error, the same problem that animal learning studies address. The link is one of shared computational problems, not a claim that the agents model human play.

## Applications

- **Research benchmark**: after the paper, Dota 2 became a testbed for long-horizon, partially observed, multi-agent reinforcement learning. The paper is a reference point for how far self-play with a large compute budget can scale.
- **Public evaluation**: the arena and the OG match were a public test of the agents against human teams, and the arena results show where human players found weaknesses.

## Open questions

- **Generalisation**: the agents were trained on a restricted hero pool and a fixed set of rules. How well such agents adapt to new heroes, items or patches is not established by the paper.
- **Robustness**: some teams beat the system in the arena, so how to make self-play agents resistant to unfamiliar strategies is still open.
- **Cost**: the training budget limits who can reproduce the result, and whether comparable play needs less compute is an open question.
- **Coordination with people**: the paper focuses on play with teams of agents. Coordinating with human teammates who do not share the same training is a separate problem.

## References

### Seminal papers

- OpenAI et al. (2019). Dota 2 with Large Scale Deep Reinforcement Learning. arXiv. https://arxiv.org/abs/1912.06680 — Describes OpenAI Five, its training system, its results and its restrictions.
- Schulman et al. (2017). Proximal Policy Optimization Algorithms. arXiv. https://arxiv.org/abs/1707.06347 — The PPO algorithm used to train the agents.
- Silver et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — AlphaGo, the earlier self-play system the paper compares its scale against.
- Vinyals et al. (2019). Grandmaster level in StarCraft II using multi-agent reinforcement learning. *Nature*. https://doi.org/10.1038/s41586-019-1724-z — A contemporary multi-agent game system trained with league self-play.

### Surveys and textbooks

- Yannakakis & Togelius (2018). *Artificial Intelligence and Games*. Springer. https://doi.org/10.1007/978-3-319-63519-4 — Textbook on AI for games, including self-play and multi-agent methods.
