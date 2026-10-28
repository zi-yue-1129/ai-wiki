---
status: draft
last_reviewed: 2026-10-28
aliases:
  - Decision Transformer
  - DT
---

# Decision Transformer (Chen et al., 2021)

An offline reinforcement learning method that treats decision making as sequence modelling. A causally masked Transformer is trained on trajectories, and at test time it is conditioned on a desired return, so that it generates actions that aim for that return. No value function is learned.

## Problem

Value-based offline methods must estimate the value of actions the data does not cover, and policy-gradient methods need many on-policy samples. Chen et al. ask whether the sequence-modelling tools behind large language models can replace both. The idea is to abstract reinforcement learning as a sequence problem: given the past states, actions and desired return, predict the next action.

## Core idea

Each trajectory is written as a sequence of tokens, in which each step contributes three entries: the return-to-go (the sum of future rewards that the agent wants to obtain), the state, and the action. A causally masked Transformer is trained to predict each action from the preceding tokens, which is supervised learning on logged trajectories. At test time, the agent starts with a high desired return, appends each observed state, and samples the next action. The return-to-go is then decreased by the reward received, so that it always states the return still wanted.

Because the desired return acts as a prompt for generation, the same trained model can be asked for different levels of performance. The method needs no Bellman backups and no value estimates.

## Equation or algorithm

The model is trained to maximise the likelihood of the logged actions given the previous tokens,

\[
\mathcal{L} = -\mathbb{E}_{\tau \sim \mathcal{D}}\left[\sum_t \log \pi_\theta(a_t \mid \hat{R}_t, s_t, \hat{R}_{t-1}, \ldots, s_1)\right],
\]

where \(\hat{R}_t = \sum_{t' \ge t} r_{t'}\) is the return-to-go of the logged trajectory. At evaluation, \(\hat{R}_1\) is set to the desired return, and the return-to-go is updated by subtracting each observed reward.

## Results

The abstract reports that Decision Transformer "matches or exceeds the performance of state-of-the-art model-free offline RL baselines on Atari, OpenAI Gym, and Key-to-Door tasks". The paper evaluates on these benchmarks against conservative and value-based offline methods.

## Limitations

- **Conditioning on returns.** The desired return must be chosen. The paper scales return-to-go by a multiple of the maximum return in the dataset, and it notes that more principled conditioning is possible.
- **Context length.** The Transformer sees a fixed window of past tokens, which limits the history it can use.

## Connections

- Parent topic: [Offline RL](../index.md).
- It is a sequence-model alternative to value-based offline methods such as [CQL](../cql/index.md) and [IQL](../iql/index.md).
- The sequence-model idea links to the Transformer architecture in [the Transformer model family](../../../../models/transformer/index.md), and to [imitation learning](../../../imitation/index.md), since it is trained by supervised prediction on demonstrations.

## Applications

- **Atari games** from logged play, as in the paper's experiments.
- **Control tasks** from logged trajectories, where the paper evaluates on OpenAI Gym.

## Open questions

- How to combine sequence modelling with value learning so that the model can stitch trajectories.
- How to choose the desired return for a new task.

## References

### Seminal papers

- Chen et al. (2021), "Decision Transformer: Reinforcement learning via sequence modeling", [arXiv:2106.01345](https://arxiv.org/abs/2106.01345) — The Decision Transformer paper, with the return-conditioned sequence model and the Atari, Gym and Key-to-Door results.
- Kumar, Zhou, Tucker & Levine (2020), "Conservative Q-learning for offline reinforcement learning", [arXiv:2006.04779](https://arxiv.org/abs/2006.04779) — A value-based offline method, for comparison with sequence modelling.
- Kostrikov, Nair & Levine (2021), "Offline reinforcement learning with implicit Q-learning", [arXiv:2110.06169](https://arxiv.org/abs/2110.06169) — A value-based offline method that avoids querying unseen actions.
- Fu, Kumar, Nachum, Tucker & Levine (2020), "D4RL: Datasets for deep data-driven reinforcement learning", [arXiv:2004.07219](https://arxiv.org/abs/2004.07219) — The offline benchmark suite used to compare offline methods.
- Fujimoto, Meger & Precup (2019), "Off-policy deep reinforcement learning without exploration", [arXiv:1812.02900](https://arxiv.org/abs/1812.02900) — Batch-constrained Q-learning, an offline baseline.
