---
status: draft
last_reviewed: 2026-10-28
aliases:
  - AlphaGo
  - AlphaGo Zero
  - 阿爾法狗
---

# AlphaGo (Silver et al., 2016)

AlphaGo combined deep policy and value networks with Monte Carlo tree search to play the game of Go at professional level. It is the first of the search-and-self-play systems described in the [parent topic](../index.md), and the one that made the combination famous.

## Overview

Go was a long-standing challenge for AI because its branching factor is far larger than that of chess, which makes both exhaustive search and hand-written evaluation impractical. Before AlphaGo, the best Go programs used [MCTS with UCT](../monte-carlo-tree-search/index.md) and hand-designed features, and reached strong amateur level. AlphaGo added two learned networks. A policy network suggests which moves deserve a look, and a value network estimates who is winning from a position. The search then uses these two networks to focus its simulations.

The original paper trained the policy network first on human expert games, then improved it by reinforcement learning from games against earlier versions of itself. The paper reports that the combined system beat a European Go champion. A later version, AlphaGo Zero (Silver et al., 2017), removed the human games entirely and is covered on the [AlphaZero](../alphazero/index.md) page.

## Key concepts

- **Policy network**: outputs a probability for each legal move, used to bias which branches the search expands.
- **Value network**: outputs an estimate of the winning probability from a position, replacing much of the rollout work.
- **Supervised pretraining**: the policy is first trained to predict the moves of human experts.
- **Self-play refinement**: the policy is then improved by playing against past versions of itself.

## How it works

AlphaGo runs MCTS from the current position. At each simulation it selects moves using the search statistics together with a prior from the policy network, and evaluates the leaf position in two ways: with the value network and with a fast rollout policy. The two estimates are mixed into one leaf value, which is then backed up the tree.

Schematically, the training pipeline is:

1. Train the policy network $p_\sigma$ to predict expert moves from human games.
2. Train a fast rollout policy and the value network $v_\theta$ on positions and outcomes from self-play games.
3. Improve the policy network by reinforcement learning against earlier versions of itself, giving $p_\rho$.
4. At play time, run MCTS, using the policy prior to choose which children to expand and the mixed leaf value to decide which move wins.

The leaf evaluation mixes the value network with the outcome of a rollout, with a mixing weight that the paper tunes.

## Results

The Nature paper reports that AlphaGo won a match against a human European Go champion. The result was a milestone because many researchers had expected Go to remain out of reach for years longer. The exact match scores and the other comparisons are in the paper and should be checked there before they are quoted.

## Limitations

- **Human data.** The first policy relied on a large database of expert games, which limits the approach to domains where such records exist.
- **Heavy search.** Each move needed many network evaluations, so strong play required substantial hardware.
- **Two networks and a rollout.** The design is complex, with separately trained components that must be tuned together.
- **Narrow domain.** The system was built for Go, and its design used Go-specific features as input.

## Open questions

Could a system learn as well without human games from the start? AlphaGo Zero answered yes for Go, and the next question is which parts of the design generalise to other domains. A second question is how much of the strength came from search and how much from the networks, which the later systems were designed to test.

## Connections

AlphaGo is the link between the value-based work on [deep Q-networks](../../deep-q-networks/index.md) and the search work on [MCTS](../monte-carlo-tree-search/index.md). Its self-play refinement is the same idea as the self-play used in [AlphaZero](../alphazero/index.md) and [MuZero](../muzero/index.md), and the history of its matches is covered on the [games](../../../../../applications/games/index.md) page.

## References

### Seminal papers

- Silver, D. et al. (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — The original AlphaGo paper, combining policy and value networks with Monte Carlo tree search.
- Silver, D. et al. (2017). *Mastering the game of Go without human knowledge*. Nature. https://doi.org/10.1038/nature24270 — AlphaGo Zero, which learns Go by self-play from random play, without human game records.
- Silver, D. et al. (2018). *A general reinforcement learning algorithm that masters chess, shogi, and Go through self-play*. Science. https://doi.org/10.1126/science.aar6404 — AlphaZero, the generalisation of AlphaGo Zero to chess and shogi.
- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — The UCT algorithm that AlphaGo's search extends.
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — Selection and backup rules for Monte Carlo tree search in Go programs, the tradition AlphaGo built on.

### Surveys and textbooks

- Browne, C. B. et al. (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — Survey of the MCTS methods that preceded and surrounded AlphaGo.
