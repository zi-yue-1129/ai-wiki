---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/search
tags:
  - search
  - game playing
  - adversarial search
aliases:
  - α–β 剪枝
  - Alpha-beta pruning
  - Minimax
  - 極小極大搜尋
---

# Alpha–Beta Pruning

Alpha–beta pruning is a way of computing the minimax value of a two-player game tree while skipping branches that cannot affect the result. It returns exactly the minimax value, with fewer nodes examined. Part of [Search algorithms](index.md).

## Overview

In a two-player zero-sum game, one player maximises the evaluation and the other minimises it. Minimax search evaluates the whole tree up to a fixed depth and backs values up through the max and min levels. Alpha–beta keeps two bounds during the search: \(\alpha\), the best value the maximiser can already guarantee, and \(\beta\), the best value the minimiser can already guarantee. When a branch cannot improve on these bounds, it is cut off.

## Key concepts

- **Minimax value**: the value of a node when both players play optimally to the search depth.
- **Alpha bound**: the lower bound on the maximising player's value at a node.
- **Beta bound**: the upper bound on the minimising player's value at a node.
- **Cutoff**: stopping the expansion of a node once \(\alpha \ge \beta\), because the rest of its children cannot change the result.

## How it works

The search is depth-first. At a maximising node, each child is searched with the current \(\alpha\) and \(\beta\), and \(\alpha\) is raised whenever a child returns a larger value. At a minimising node, \(\beta\) is lowered in the same way. When \(\alpha\ge\beta\), the remaining children are pruned. The returned value is the same as plain minimax, because pruned branches could not have changed it.

The number of leaves examined depends on move ordering. Searching the strongest moves first lets more branches be pruned.

## Variants

- **Iterative deepening with alpha–beta** searches to increasing depths and reuses move-ordering information from shallower searches.
- **Principal variation search** searches the first child with a full window and the others with a null window, which saves work when ordering is good.
- **Quiescence search** extends the search at unstable positions, such as during captures in chess, to reduce the horizon effect.

## Results and limits

- Alpha–beta returns the minimax value. Its pruning does not change the answer.
- Its benefit depends on move ordering. Poor ordering removes little work.
- Plain depth limits cause the horizon effect, so quiescence or extra search is usually added.
- Alpha–beta needs a static evaluation function at the leaves, and designing it well is a large part of the engineering effort. Campbell et al. (2002) describe how Deep Blue combined alpha–beta search, implemented partly in hardware, with an evaluation function that was largely hand-tuned.

## Applications

- **Chess programs**: alpha–beta with a hand-designed evaluation drove the program Deep Blue (Campbell et al., 2002).
- **Board games**: checkers, Othello and similar games where the branching factor is moderate.
- **Teaching and benchmarks**: a standard example of adversarial search in AI courses.

## Open questions

- Learned evaluation functions can improve alpha–beta, but errors in the learned evaluation can compound with search depth.
- For games with very large branching factors, such as Go, alpha–beta is less effective than sampling-based search (Silver et al., 2016).

## References

### Seminal papers

- Shannon, C. E. (1950). XXII. Programming a computer for playing chess. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science* 41(314), 256–275. https://doi.org/10.1080/14786445008521796 — Early proposal of minimax search with a static evaluation function for chess.
- Knuth, D. E. & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence* 6(4), 293–326. https://doi.org/10.1016/0004-3702(75)90019-3 — Analyses the pruning performance of alpha–beta.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook treatment of minimax and alpha–beta.
- Campbell, M., Hoane, A. J. & Hsu, F.-h. (2002). Deep Blue. *Artificial Intelligence* 134(1–2), 57–83. https://doi.org/10.1016/S0004-3702(01)00129-1 — Describes an alpha–beta search system in practice.
- Browne, C. B. et al. (2012). A survey of Monte Carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games* 4(1), 1–43. https://doi.org/10.1109/TCIAIG.2012.2186810 — Compares alpha–beta with sampling-based search for games.
- Silver, D. et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature* 529(7587), 484–489. https://doi.org/10.1038/nature16961 — Compares tree search with learned evaluation in Go.
