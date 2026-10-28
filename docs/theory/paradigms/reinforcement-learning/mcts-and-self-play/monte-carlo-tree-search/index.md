---
status: draft
last_reviewed: 2026-10-28
aliases:
  - UCT
  - Upper Confidence bounds applied to Trees
  - 蒙地卡羅樹搜尋
---

# Monte Carlo Tree Search (UCT, 2006)

Monte Carlo tree search is a planning method that builds a search tree from repeated simulations, using a bandit rule to decide which branch to explore next. Its best-known form, UCT, made it the default search for the game of Go before deep learning arrived. It is the search core of the [parent topic](../index.md).

## Overview

A planner that must choose among moves in a large game tree faces the same trade-off as a gambler choosing between slot machines: each option might be good, and trying it reveals information, but trying a poor option wastes effort. Kocsis and Szepesvári (2006) treated each node of the tree as a multi-armed bandit problem and applied the UCB1 rule to choose which child to visit. Their algorithm, called UCT, grows the tree one simulation at a time and concentrates later simulations on the most promising moves, while still sampling the others occasionally.

The method needs no evaluation function written by hand. Random playouts supply the outcome estimates, which is why it succeeded in games where good static evaluation was hard to write.

## Key concepts

- **Bandit rule (UCB1)**: choose the option whose average reward plus an uncertainty bonus is highest. The bonus shrinks as an option is tried more.
- **Simulation**: one pass down the tree, followed by a rollout and an update.
- **Rollout**: a playout from a new position to a terminal state, often with a random or lightly guided policy.
- **Backup**: updating the average outcome and visit count of every node on the path.

## How it works

The algorithm runs the four steps described on the [parent topic](../index.md): selection, expansion, rollout and backup. Selection picks the child $a$ of node $s$ that maximises

$$
\bar{Q}(s,a) + c\sqrt{\frac{\ln N(s)}{N(s,a)}},
$$

where $N(s)$ counts visits to the parent, $N(s,a)$ counts visits to the child, $\bar{Q}(s,a)$ is the child's average outcome from the current player's view, and $c$ controls exploration.

1. Start at the root. While the current node is fully expanded, move to the child with the highest UCB score.
2. At the first node with an unexplored move, add a new child for that move.
3. Play out the game from the new node with a fast policy, and record the outcome $z \in \{-1, 0, 1\}$ for the player who moved into it.
4. Walk back up the path. At each node, increase the visit count and move the average outcome toward $z$, from the perspective of the player to move at that node.
5. After the time budget ends, play the move with the most visits at the root.

## Results

Kocsis and Szepesvári (2006) showed that the UCT approach performs well on the test problems they used, which include planning tasks where the search must balance breadth and depth. The strongest evidence for the method came from Go programs of the mid-2000s, which used it to reach a level that earlier search methods had not. Browne et al. (2012) survey the many variants and applications that followed. The results are qualitative here; the paper gives the exact figures.

## Limitations

- **Cost.** Good play needs many simulations, so the method is expensive for games with long rollouts.
- **Weak rollouts.** A random playout can be a poor estimate of the outcome in games where the position matters more than chance, which is why later systems replaced rollouts with learned values.
- **Narrow search.** The tree is grown only where the bandit rule directs it, so a rare but important line may stay unexplored.
- **Needs a simulator.** The planner must be able to simulate the next state.

## Open questions

How should rollouts be replaced or combined with learned evaluations without losing the ability to stop the search at any time? Can the bandit rule be improved for trees whose values are correlated across branches? And how well does UCT scale to language or other domains where a simulator exists only through a model that may be wrong?

## Connections

The method is the search step inside [AlphaGo](../alphago/index.md), [AlphaZero](../alphazero/index.md) and [MuZero](../muzero/index.md), where learned networks replace random rollouts and steer the tree. Bandit-style exploration is discussed on the [exploration](../../exploration/index.md) page. The search also appears in language models; see [Hao et al. (2023)](https://arxiv.org/abs/2305.14992) on reasoning with a world model.

## References

### Seminal papers

- Kocsis, L. & Szepesvári, C. (2006). *Bandit Based Monte-Carlo Planning*. Lecture Notes in Computer Science. https://doi.org/10.1007/11871842_29 — Applies the UCB1 bandit rule to choose moves in a tree during Monte Carlo planning, the UCT algorithm.
- Coulom, R. (2007). *Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search*. Lecture Notes in Computer Science. https://doi.org/10.1007/978-3-540-75538-8_7 — Studies how a Monte Carlo tree chooses which moves to expand and how results are propagated back, with Go as the test domain.
- Silver, D. et al. (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature. https://doi.org/10.1038/nature16961 — AlphaGo, which uses Monte Carlo tree search guided by policy and value networks.
- Anthony, T., Tian, Z. & Barber, D. (2017). *Thinking Fast and Slow with Deep Learning and Tree Search*. arXiv:1705.08439. https://arxiv.org/abs/1705.08439 — Expert iteration: tree search improves a neural policy, and the improved policy guides later search.

### Surveys and textbooks

- Browne, C. B. et al. (2012). *A Survey of Monte Carlo Tree Search Methods*. IEEE Transactions on Computational Intelligence and AI in Games. https://doi.org/10.1109/TCIAIG.2012.2186810 — Broad survey of MCTS variants, enhancements and applications beyond games.

### Articles and documentation

- Hao, S. et al. (2023). *Reasoning with Language Model is Planning with World Model*. arXiv:2305.14992. https://arxiv.org/abs/2305.14992 — Uses a language model as a world model and plans reasoning steps with Monte Carlo tree search.
