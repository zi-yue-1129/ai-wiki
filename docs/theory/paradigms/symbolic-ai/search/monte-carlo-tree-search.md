---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/search
  - theory/paradigms/reinforcement-learning
tags:
  - search
  - game playing
  - sampling
aliases:
  - 蒙地卡羅樹搜尋
  - MCTS
  - UCT
  - Monte Carlo tree search
---

# Monte Carlo Tree Search

Monte Carlo tree search (MCTS) builds a search tree by repeating four steps: selection, expansion, simulation and backpropagation. It estimates the value of moves from random playouts, and a bandit rule decides where to search next. Part of [Search algorithms](index.md).

## Overview

Alpha–beta needs a good static evaluation, which is hard to write for games such as Go. MCTS avoids this by estimating values from the outcomes of random games. It grows the tree where the estimates are promising and uncertain, so the search concentrates on useful lines without a full-width expansion.

## Key concepts

- **Playout (rollout)**: a fast, usually random, simulation from a position to the end of the game.
- **Exploration–exploitation**: choosing between moves with high estimated value and moves with few visits.
- **UCB1 rule**: a child is chosen to maximise \(\bar{x}_j+c\sqrt{\ln N/n_j}\), where \(\bar{x}_j\) is the mean outcome, \(n_j\) the child's visit count and \(N\) the parent's count. Auer et al. (2002) analyse this bound for the bandit problem.
- **UCT**: the tree policy that applies UCB1 at every node visited during selection. Kocsis and Szepesvári (2006) introduced it for MCTS.

## How it works

Each iteration starts at the root and does four things:

1. **Selection**: descend the tree by choosing children with the UCB1 rule until a node with unexplored moves is reached.
2. **Expansion**: add one child for an unexplored move.
3. **Simulation**: play out the game from the new node, usually with random moves, to a terminal result.
4. **Backpropagation**: update the visit count and mean outcome of every node on the path.

After the budget of iterations, the move with the most visits, or the highest mean, is chosen. Coulom (2007) coined the name and studied backup operators for Go.

## Variants

- **UCT** is the standard selection rule, and most MCTS implementations use it.
- **RAVE** shares statistics between moves that appear at different points in the tree. It speeds up learning in Go.
- **Learned policies and values**: AlphaGo used neural networks to guide selection and to replace random playouts with value estimates (Silver et al., 2016).

## Results and limits

- MCTS works without a hand-written evaluation function, and it improves steadily with more iterations.
- Random playouts can be misleading in games where a single move decides the outcome, so the simulation policy matters.
- The method needs many iterations for accurate estimates, which makes it expensive in time-limited settings.
- Browne et al. (2012) survey the variants and their behaviour across games.

## Applications

- **Go**: MCTS with neural networks reached strong play in Go (Silver et al., 2016).
- **General game playing**: MCTS handles many games with little game-specific knowledge.
- **Planning**: sampling-based search for decision problems with large branching factors.

## Open questions

- Choosing the exploration constant and the simulation policy for a new game still relies on tuning.
- Combining MCTS with learned models, and understanding when learned values help or hurt, is an active area.
- Extending MCTS to imperfect information and to continuous action spaces is harder than the perfect-information case.

## References

### Seminal papers

- Kocsis, L. & Szepesvári, C. (2006). Bandit based Monte-Carlo planning. In *Machine Learning: ECML 2006*, Lecture Notes in Computer Science, 282–293. https://doi.org/10.1007/11871842_29 — Introduces UCT (UCB applied to trees). The paper proves consistency and finite-sample bounds for finite-horizon MDPs, and reports on P-game trees that UCT's failure rate goes to zero. It does not prove convergence to the minimax value.
- Coulom, R. (2007). Efficient selectivity and backup operators in Monte-Carlo tree search. In *Computers and Games*, Lecture Notes in Computer Science, 72–83. https://doi.org/10.1007/978-3-540-75538-8_7 — Names the method and studies its backup operators for Go.
- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). Finite-time analysis of the multiarmed bandit problem. *Machine Learning* 47(2–3), 235–256. https://doi.org/10.1023/A:1013689704352 — Gives the UCB1 bound that the selection rule depends on.

### Surveys and textbooks

- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — Survey of MCTS variants and applications.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529(7587), 484–489. https://doi.org/10.1038/nature16961 — Combines MCTS with deep networks to reach expert-level Go.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook background on adversarial and sampling-based search.
