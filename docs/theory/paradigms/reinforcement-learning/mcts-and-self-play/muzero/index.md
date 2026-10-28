---
status: draft
last_reviewed: 2026-10-28
aliases:
  - MuZero
---

# MuZero (Schrittwieser et al., 2020)

MuZero plans with [Monte Carlo tree search](../monte-carlo-tree-search/index.md) inside a model it learns, rather than inside a simulator given by the rules. It keeps the search and self-play loop of [AlphaZero](../alphazero/index.md) and removes the need to know how the environment works, which lets the same method play Atari games as well as board games.

## Overview

AlphaZero's search needs an exact simulator: it must be able to ask what happens after a move. For board games the rules provide one, but for most other problems, including video games with pixels as input, no simulator is available. Model-based planning had struggled in such visually complex domains. MuZero asks whether an agent can learn a model that is accurate enough for planning without modelling the whole observation. The answer proposed in the paper is a model that predicts only what planning uses: the reward, the policy and the value.

The arXiv abstract reports that MuZero achieved a new state of the art across 57 Atari games, the standard benchmark of visually rich game environments. It also reports that on Go, chess and shogi, without knowing the rules, MuZero matched the superhuman performance of AlphaZero, which was given the rules.

## Key concepts

- **Representation function**: maps the recent observations to an internal state $s^0$. This state is learned and need not reconstruct the observation.
- **Dynamics function**: takes an internal state and an action and predicts the reward and the next internal state.
- **Prediction function**: maps an internal state to a policy and a value, the same two outputs as AlphaZero's network.
- **Latent planning**: MCTS runs on the internal states, where each step is a call to the dynamics function.

## How it works

For an observation sequence $o_1,\dots,o_t$ and a planned sequence of actions $a^1,\dots,a^K$, the three learned functions are

$$
s^0 = h_\theta(o_1,\dots,o_t), \qquad r^k, s^k = g_\theta(s^{k-1}, a^k), \qquad \mathbf{p}^k, v^k = f_\theta(s^k).
$$

MCTS uses these functions as its simulator. Each simulated step calls $g_\theta$ to predict the reward, then $f_\theta$ for the policy and value at the new internal state, and the usual selection and backup rules apply. The internal state is never checked against a real observation during search, which is why the model must be trained to be useful for planning.

Training unrolls the model for several steps from observed starting points and matches its predictions to targets from real experience: the observed rewards, a bootstrapped value from the stored search results, and the search policy from the visit counts. The algorithm proceeds as follows:

1. Play episodes with MCTS in the learned model, storing observations, actions, rewards, search policies and search values.
2. Sample a segment of a stored episode at random.
3. Unroll the model for $K$ steps from the segment's first observation, using the actions actually taken.
4. Build targets: the observed rewards, $n$-step value targets, and the search policies.
5. Update the three networks together by gradient descent on the sum of the reward, value and policy errors over the unrolled steps.

## Results

The arXiv abstract (Schrittwieser et al., 2020) states two results. On 57 Atari games, the paper's test environment for visually complex domains, MuZero achieved a new state of the art. On Go, chess and shogi, MuZero matched the superhuman performance of AlphaZero, even though it did not know the game rules.

## Limitations

- **The model is only as good as its planning use.** The learned state is trained to predict rewards, values and policies, not to represent the environment faithfully. A model that is useful for planning may be unhelpful for other purposes such as prediction or explanation.
- **Errors compound.** Mistakes in the learned dynamics accumulate over the steps of a long search, as with any learned-model planner.
- **Test domains.** The main evidence comes from games with clear rewards and deterministic dynamics. Performance in noisy real-world settings is not shown in the paper.

## Open questions

How should the learned model be made more accurate where it matters for planning without being trained on full observations? Can a model that predicts only rewards and values be checked or corrected in practice? And does the approach scale to stochastic or partially observed environments, where a single search path may not capture the uncertainty?

## Connections

MuZero is the clearest example of [model-based reinforcement learning](../../model-based-rl/index.md), and it sits next to other learned-world-model agents such as Dreamer, covered on the [model-based RL](../../model-based-rl/index.md) page, and the [world models](../../../../models/world-models/index.md) of Ha and Schmidhuber (2018). Its planning step is the same search as [AlphaZero](../alphazero/index.md), and the earlier board-game results are described on the [parent topic](../index.md).

## References

### Seminal papers

- Schrittwieser, J. et al. (2020). *Mastering Atari, Go, chess and shogi by planning with a learned model*. Nature. https://doi.org/10.1038/s41586-020-03051-4 — The MuZero paper, planning with search in a learned model that predicts reward, policy and value.
- Silver, D. et al. (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero, the rules-based search that MuZero generalises.
- Silver, D. et al. (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo, the first system to combine learned networks with tree search at this scale.
- Ha, D. & Schmidhuber, J. (2018). *World Models*. arXiv:1803.10122. https://arxiv.org/abs/1803.10122 — Learns a compressed model of an environment and trains a controller entirely inside its imagined rollouts.

### Articles and documentation

- Hafner, D. et al. (2023). *Mastering Diverse Domains through World Models*. arXiv:2301.04104. https://arxiv.org/abs/2301.04104 — DreamerV3, a single world-model agent that learns a latent model and plans through it across many domains.
