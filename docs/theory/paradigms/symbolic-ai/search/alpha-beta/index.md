---
status: draft
last_reviewed: 2026-10-28
related:
  - applications/games
tags:
  - search
  - games
aliases:
  - Alpha-beta pruning
  - α-β 剪枝
  - Alpha-beta
  - Minimax
  - 極小化極大
  - 對抗搜尋
  - Adversarial search
---

# Minimax with Alpha-Beta Pruning

Minimax is the basic rule for choosing a move in a two-player zero-sum game: each player is assumed to pick the option that is best for itself. Alpha-beta pruning computes exactly the same answer while skipping parts of the game tree that cannot affect it. Together they are the classical method of adversarial search, described in the parent [search algorithms overview](../index.md).

## Overview

In a game such as chess, the searcher looks ahead a few moves and must assume the opponent replies with the strongest counter-move. The value of a position alternates between the searcher's maximum over its own moves and the opponent's minimum over the replies. The search is usually limited to a fixed depth, after which a heuristic evaluation scores the position.

Claude Shannon proposed this approach for computer chess in 1950. Knuth and Moore later analysed how much alpha-beta pruning saves.[^1]

## Key concepts

- **Game tree**: positions as nodes and legal moves as edges. MAX and MIN nodes are positions where the searcher or the opponent is to move.
- **Evaluation function**: a heuristic that scores a position at the depth limit.
- **Alpha**: the best value the searcher can already guarantee along the current path.
- **Beta**: the best value the opponent can already guarantee along the current path.
- **Move ordering**: the order in which moves are examined. It decides how many branches pruning can remove.

## How it works

Plain minimax evaluates a node by recursion:

$$
V(n) =
\begin{cases}
\text{eval}(n) & \text{if } n \text{ is a leaf or at the depth limit}\\
\max_{c \in \text{children}(n)} V(c) & \text{if } n \text{ is a MAX node}\\
\min_{c \in \text{children}(n)} V(c) & \text{if } n \text{ is a MIN node.}
\end{cases}
$$

Alpha-beta carries two bounds down the tree and stops early when they cross.

1. Call the procedure on the root with $\alpha=-\infty$ and $\beta=+\infty$.
2. At a leaf or depth limit, return the evaluation.
3. At a MAX node, set $v=-\infty$. For each child, set $v=\max(v, \text{result of child})$ and $\alpha=\max(\alpha, v)$. If $\alpha \ge \beta$, stop examining children. This is a beta cutoff.
4. At a MIN node, set $v=+\infty$. For each child, set $v=\min(v, \text{result of child})$ and $\beta=\min(\beta, v)$. If $\alpha \ge \beta$, stop. This is an alpha cutoff.
5. Return $v$.

The cutoff is safe: once $\alpha \ge \beta$, the player to move at the parent already has an option at least as good elsewhere, so the remaining children cannot change the root value.

The saving depends heavily on move ordering. Knuth and Moore showed that when the best move is always examined first, a uniform tree with branching factor $b$ and depth $d$ needs to examine only about $b^{\lceil d/2\rceil}+b^{\lfloor d/2\rfloor}-1$ leaves, roughly the square root of the number that plain minimax examines.[^2] Real programs cannot order moves perfectly, but simple ordering heuristics recover much of the gain.

## Results

Shannon's 1950 paper is a proposal and a design analysis, not an experiment. Knuth and Moore's 1975 result is analytic: it bounds the number of leaves examined under ideal ordering. As is standard, pruning does not change the value found. The main empirical evidence comes from chess programs. Deep Blue combined alpha-beta search with custom hardware and a large set of handcrafted evaluation features, and it defeated the reigning world champion in a 1997 match.[^3]

The later AlphaZero work takes a different route, replacing handcrafted evaluation with learned networks and using Monte Carlo tree search instead of alpha-beta. Its abstract reports that, starting from random play, it reached superhuman play in chess, shogi and Go within 24 hours.[^4]

## Limitations

- **Depth limit.** A fixed-depth search can miss a threat just beyond its horizon. This is the horizon effect, and it can make a program play badly even with a strong evaluation.
- **Evaluation quality.** The result is only as good as the evaluation at the depth limit. Writing good evaluation functions by hand is labour-intensive.
- **Scope.** The method assumes perfect information, two players and a zero-sum outcome. Games with chance, such as backgammon, or hidden information, such as poker, need extensions such as expectiminimax or different methods.

## Open questions

- How can learned evaluations and search be combined most efficiently? AlphaZero suggests that learned search can outperform handcrafted alpha-beta in some games, but the trade-offs in cost and generality are still debated.
- Can move ordering be learned well enough to approach the ideal case?

## Connections

Alpha-beta is the search half of the classic game-playing systems on the [Games](../../../../../applications/games/index.md) page. Its learned counterpart, Monte Carlo tree search, is covered in [reinforcement learning](../../../reinforcement-learning/index.md), and the general family is in the [parent overview](../index.md). For the brain side of planning over possible futures, see [Decision-making and reward](../../../../../brain-mind/decision-reward/index.md).

## Applications

- **Chess.** Deep Blue, and the engines that followed it, used alpha-beta search with a handcrafted evaluation.[^3]
- **Baseline for learned methods.** Alpha-beta-style search of deterministic two-player games is the reference against which learned search, such as the AlphaZero work above, is measured.

[^1]: Knuth and Moore (1975), listed above.
[^2]: Knuth and Moore (1975), listed above. The leaf count is their result for a uniform tree under ideal ordering.
[^3]: Campbell, Hoane and Hsu (2002), listed above.
[^4]: Silver et al. (2017), listed above. The 24-hour figure is taken from the abstract.

## References

### Seminal papers

- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(75)90019-3 — Analyses the savings from alpha-beta pruning and the best-case behaviour under perfect move ordering.
- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*. https://doi.org/10.1080/14786445008521796 — Early proposal for computer chess based on depth-limited search with a heuristic evaluation of positions.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*. https://doi.org/10.1038/nature16961 — Combines deep neural networks with Monte Carlo tree search, the system behind AlphaGo.
- Silver, D. et al. (2017). Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm. arXiv. https://arxiv.org/abs/1712.01815 — Replaces handcrafted evaluation with a single learned algorithm that plays chess, shogi and Go by self-play.

### Articles and documentation

- Campbell, M., Hoane, A. J. & Hsu, F. (2002). Deep Blue. *Artificial Intelligence*. https://doi.org/10.1016/S0004-3702(01)00129-1 — Describes the design of the system that defeated the world chess champion, combining alpha-beta search, hardware and evaluation.
