---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - theory/paradigms/reinforcement-learning
tags:
  - search
  - symbolic AI
  - game playing
aliases:
  - 搜尋演算法
  - 搜尋
  - Search algorithms
  - Heuristic search
  - Game-tree search
---

# Search Algorithms

Search algorithms find a sequence of actions or states that reaches a goal, or the best move in a game. The agent explores a space of states, guided by a cost function and sometimes by a heuristic estimate. Part of [Symbolic AI, search and planning](../index.md).

## Overview

Many AI problems can be framed as search. A route-finding problem is a graph search. A chess position is a node in a game tree whose branches are legal moves. The main difficulty is combinatorial: the number of states grows exponentially with depth, so an algorithm must either prune the space or use knowledge to direct the search.

Search methods fall into three groups, shown below. Each has its own detailed page where it is named as a method.

| Family | Idea | Examples |
|---|---|---|
| Uninformed | Expand states without extra knowledge | Breadth-first, depth-first, iterative deepening |
| Heuristic | Use an estimate of the remaining cost | Greedy best-first, [A\*](a-star.md), IDA\* |
| Adversarial | Search a two-player game tree | Minimax with [alpha–beta pruning](alpha-beta-pruning.md) |
| Sampling-based | Estimate values from random rollouts | [Monte Carlo tree search](monte-carlo-tree-search.md) |

## Key concepts

- **State space and successor function**: states, and the actions that move from one state to another.
- **Admissible heuristic**: an estimate \(h(n)\) that never overestimates the true remaining cost. With an admissible heuristic, A\* returns an optimal path.
- **Branching factor and depth**: the number of successors per node, and the depth of the goal. Together they determine the size of the search tree.
- **Pruning**: discarding parts of the tree that cannot change the answer, as alpha–beta does for games.

## How it works

For a heuristic search, nodes are kept in a frontier and expanded in order of an evaluation function. Greedy best-first uses \(f(n)=h(n)\) and is fast but not optimal. A\* uses \(f(n)=g(n)+h(n)\), where \(g(n)\) is the cost so far. Adversarial search alternates between maximising and minimising players, with leaf values coming from a static evaluation function. Monte Carlo methods replace the static evaluation with the average outcome of random playouts.

## Key methods

- [A\* search](a-star.md): best-first search with \(f=g+h\). It is optimal with an admissible heuristic.
- [Alpha–beta pruning](alpha-beta-pruning.md): minimax with pruning. It returns the same value as minimax while examining fewer nodes.
- [Monte Carlo tree search](monte-carlo-tree-search.md): builds a tree from random rollouts with a bandit rule for selection. It is the core of game programs such as AlphaGo.

## Connections

- [Symbolic AI, search and planning](../index.md) places search in the wider classical AI toolkit.
- [Automated planning](../planning/index.md) uses heuristic search over states of a planning problem.
- [Reinforcement learning](../../reinforcement-learning/index.md) shares the idea of trading exploration against exploitation, and learned value functions can replace hand-written evaluation functions in search.

## Applications

- **Route planning and navigation**: A\* and its variants on road and grid graphs.
- **Two-player games**: alpha–beta search with a hand-tuned evaluation drove the chess program Deep Blue (Campbell et al., 2002).
- **Go and other large games**: MCTS combined with neural networks reached expert level in Go (Silver et al., 2016).

## Open questions

- Heuristic search needs good heuristics. Learning admissible or near-admissible heuristics from data is still hard to guarantee.
- Search cost grows exponentially with depth, and no general method removes this dependence.
- Combining search with learned models, so that search uses a learned evaluation or policy, raises questions of accuracy and of how errors compound with depth.

## References

### Seminal papers

- Hart, P. E., Nilsson, N. J. & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136 — Defines A\* and proves its optimality under an admissible heuristic.
- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence* 6(4), 293–326. https://doi.org/10.1016/0004-3702(75)90019-3 — Analyses the cost of alpha–beta pruning on game trees.
- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science* 41(314), 256–275. https://doi.org/10.1080/14786445008521796 — Early proposal of minimax-style search with an evaluation function for chess.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Standard textbook covering uninformed, heuristic and adversarial search.
- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — Survey of MCTS variants and their applications.
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence* 134(1–2), 57–83. https://doi.org/10.1016/S0004-3702(01)00129-1 — Describes the search and evaluation design of the chess system Deep Blue.
