---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/games
  - theory/models/reasoning
  - brain-mind/decision-reward
tags:
  - reinforcement learning
  - planning
  - self-play
aliases:
  - MCTS
  - Monte Carlo tree search
  - 蒙地卡羅樹搜尋
  - 自我對弈
  - Self-play
---

# Monte Carlo Tree Search and Self-Play

Monte Carlo tree search (MCTS) is a planning method that grows a search tree by simulating possible futures and spends most of its effort on the moves that look most promising. Self-play trains an agent by having it play against itself, so that its opponents improve as it does and the training data never runs out. Combined in systems such as AlphaZero, the two produced some of the strongest game-playing programs and are now being tried on the reasoning of language models.

## Overview

Two ideas meet on this page. The first is **search**: when the rules of a problem are known, an agent can look ahead by imagining moves before it commits to one. A full look-ahead is impossible in games such as Go, where a position has far more continuations than any computer can enumerate, so MCTS samples the tree instead, concentrating simulations where they matter. The second is **learning from self-generated experience**. A program that plays itself produces its own training games, so the quality of its data rises with its strength and no human examples are needed.

Earlier game programs used one of these ideas. Search alone, with hand-written evaluation, powered the chess engines of the 1990s. Learning alone, as in TD-Gammon's self-play for backgammon, reached strong play without deep look-ahead. The step that defined this area was to close the loop: search uses a learned network to decide where to look, and the results of that search become the targets that train the network. Each part makes the other better. The games page in [Applications](../../../../applications/games/index.md) traces the history of these programs; this page explains the method.

## Key concepts

- **Game tree**: positions are nodes and moves are edges. The search tries to find the best move from the current position, the root.
- **Simulation (rollout)**: a game played from a position to its end, originally with a fast random or simple heuristic policy.
- **Value**: an estimate of the expected outcome from a position. A learned value function can replace a rollout, or sit alongside one.
- **Prior policy**: a learned distribution over moves that says which moves are worth examining first.
- **Exploration bonus**: a term that favours moves tried only a few times. In UCT it comes from the UCB1 rule for bandit problems, described on the [MCTS method page](monte-carlo-tree-search/index.md).
- **Self-play**: the agent plays against copies or past versions of itself, and each game becomes training data.
- **Curriculum**: an ordering of training tasks from easy to hard. Self-play produces one automatically, because each side's opponent gets stronger as training goes on.
- **Search as policy improvement**: the move counts after a search are a sharper training target than the raw output of the network, because the search has already checked the consequences of each option.

## How it works

Each MCTS simulation repeats four steps:

1. **Selection.** Starting at the root, pick a child move that balances its average outcome so far against how rarely it has been tried.
2. **Expansion.** When the walk reaches a position not yet in the tree, add it.
3. **Evaluation.** Estimate the outcome of the new position, either by a rollout to the end of the game or with a learned value function.
4. **Backup.** Pass the result back up the path, updating each move's average.

After many simulations, the move with the most visits at the root is played. In UCT, the selection rule is

$$
a^\ast = \arg\max_a \left( \bar{Q}(s,a) + c \sqrt{\frac{\ln N(s)}{N(s,a)}} \right),
$$

where $\bar{Q}$ is the average outcome of move $a$, $N(s)$ and $N(s,a)$ are visit counts, and $c$ sets how strongly the search explores.

Self-play then runs as a loop:

```mermaid
flowchart LR
  N[Network: prior and value] --> S[MCTS from the current position]
  S --> M[Play the move with most visits]
  M --> G[Finished game]
  G --> D[Training data: visit counts and outcome]
  D --> T[Update the network]
  T --> N
```

The network proposes moves and values, the search checks them, and the training step makes the next round of proposals more accurate.

## Key methods

Four landmark methods are covered on their own pages. They differ mainly in what is learned and what the search is allowed to know about the game rules.

| Method | Year | Search | What is learned | Needs the rules |
|---|---|---|---|---|
| [MCTS with UCT](monte-carlo-tree-search/index.md) | 2006 | Random rollouts | Nothing; the search alone | Yes, as a simulator |
| [AlphaGo](alphago/index.md) | 2016 | MCTS guided by networks | Policy and value networks, from human games and then self-play | Yes |
| [AlphaZero](alphazero/index.md) | 2017 | MCTS guided by one network | Policy and value, from self-play only | Yes |
| [MuZero](muzero/index.md) | 2019 | MCTS in a learned model | Representation, dynamics, policy and value | No |

## Connections

The method sits inside the wider family of [model-based reinforcement learning](../model-based-rl/index.md): MuZero is the clearest case of planning with a learned model. The learned values that guide the search are the same quantities studied in [value-based methods](../value-based-methods/index.md), and the policy network that proposes moves is an actor in the sense of [policy gradient and actor-critic](../policy-gradient-and-actor-critic/index.md).

The brain angle is suggestive rather than proven. Dopamine signals the reward prediction error that a value function learns, as described in [Decision Making, Dopamine and Reward](../../../../brain-mind/decision-reward/index.md). Human choice studies distinguish habits, which resemble cached values, from goal-directed choice, which resembles planning with a model; see [model-based and model-free control](../../../../brain-mind/decision-reward/model-based-vs-model-free/index.md). In rodents, Pfeiffer and Foster (2013) recorded hippocampal place-cell sequences that run ahead along future paths to goals. This resembles simulation-based look-ahead, but it does not show that the brain runs UCT or any specific tree search.

## Applications

- **Board games.** AlphaZero learned chess, shogi and Go from the rules alone. Later programs in the same family became the reference players for these games.
- **Single-agent planning.** MuZero applied the same search to Atari games, where no rules are given to the search.
- **Reasoning in language models.** Hao et al. (2023) treat a language model both as the reasoning agent and as a world model, and plan over candidate reasoning steps with MCTS. Feng et al. (2023) use an AlphaZero-like search with a learned value function to guide decoding and to improve the model during training. Zhang et al. (2024) use tree search to collect higher-quality reasoning traces and per-step value labels for self-training.
- **Test-time compute.** Snell et al. (2024) study how spending more computation at inference, including searching against process-based verifiers, changes performance compared with simply using a larger model. The [test-time scaling](../../../models/reasoning/test-time-scaling.md) page covers this in more detail.

## Open questions

- **Domains without a simulator.** MCTS needs a way to simulate outcomes. MuZero shows that a learned model can serve, but model errors accumulate over a long search, and it is not clear how far the approach extends to messy real-world tasks.
- **Self-play curricula.** Self-play can produce a useful curriculum, but it may also converge on narrow strategies or cycle among them. Sukhbaatar et al. (2017) show that asymmetric self-play can drive exploration without external rewards, yet when self-play gives the right curriculum for general tasks remains an open question.
- **Language reasoning.** A chess game has a clear winner, while a reasoning chain has no equally clear reward. Tree search with language models depends on the quality of the verifier or value estimate, and the cost of each search step is high.
- **Compute trade-offs.** Whether search with a fixed compute budget beats a larger single pass depends on the problem and the model, and the answer is not settled.

## References

### Seminal papers

- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — Applies the UCB1 bandit rule to choose moves in a tree during Monte Carlo planning, the UCT algorithm.
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — Studies how a Monte Carlo tree chooses which moves to expand and how results are propagated back, with Go as the test domain.
- Tesauro, G. (1995). *Temporal difference learning and TD-Gammon*. Communications of the ACM. https://doi.org/10.1145/203330.203343 — Describes TD-Gammon, a backgammon program that learned a neural evaluation function by playing against itself.
- Silver, D. et al. (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo, which combines policy and value networks with Monte Carlo tree search.
- Silver, D. et al. (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero, which learns Go by self-play from random play, without human game records.
- Silver, D. et al. (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero, one self-play algorithm that learns three different board games from the rules alone.
- Schrittwieser, J. et al. (2020). *Mastering Atari, Go, chess and shogi by planning with a learned model*. Nature. https://doi.org/10.1038/s41586-020-03051-4 — MuZero, which plans with MCTS in a model it learns, without being given the rules.
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — Expert iteration: tree search improves a neural policy, and the improved policy then guides the search.
- Sukhbaatar, S. et al. (2017). *Intrinsic Motivation and Automatic Curricula via Asymmetric Self-Play*. arXiv:1703.05407. https://arxiv.org/abs/1703.05407 — Two agents that propose and solve tasks for one another, generating an automatic curriculum without external rewards.
- Pfeiffer, B. E. & Foster, D. J. (2013). *Hippocampal place-cell sequences depict future paths to remembered goals*. Nature. https://doi.org/10.1038/nature12112 — Recordings in rats showing place-cell sequences that run ahead along paths to goals, a neural parallel to look-ahead.

### Surveys and textbooks

- Browne, C. B. et al. (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — Broad survey of MCTS variants, enhancements and applications beyond games.

### Articles and documentation

- Hao, S. et al. (2023). *Reasoning with Language Model is Planning with World Model*. arXiv:2305.14992. https://arxiv.org/abs/2305.14992 — Uses a language model as a world model and plans reasoning steps with Monte Carlo tree search.
- Feng, X. et al. (2023). *Alphazero-like Tree-Search can Guide Large Language Model Decoding and Training*. arXiv:2309.17179. https://arxiv.org/abs/2309.17179 — Applies an AlphaZero-style tree search with a learned value function to guide language model decoding and training.
- Snell, C. et al. (2024). *Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters*. arXiv:2408.03314. https://arxiv.org/abs/2408.03314 — Studies how spending more inference compute, including search against verifiers, changes performance.
- Zhang, D. et al. (2024). *ReST-MCTS\*: LLM Self-Training via Process Reward Guided Tree Search*. arXiv:2406.03816. https://arxiv.org/abs/2406.03816 — Uses tree search to collect reasoning traces and per-step values for language model self-training.
