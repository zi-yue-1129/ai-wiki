---
last_reviewed: 2026-11-04
related:
  - theory/paradigms/symbolic-ai/search
tags:
  - search
  - heuristic search
  - memory-bounded search
aliases:
  - IDA*
  - Iterative-deepening A*
  - 迭代加深 A*
  - 迭代深化 A*
---

# IDA\* Search

IDA\* is an optimal heuristic search algorithm that runs repeated depth-first searches with a growing bound on the cost f(n) = g(n) + h(n). Its memory use is linear in the depth of the search, unlike [A\* search](a-star.md), which keeps the whole frontier. Part of [Search algorithms](index.md).

## Overview

A\* is optimal with an admissible heuristic, but it stores every frontier node, and that is often the limit on large problems. IDA\* keeps only the current path. Korf (1985) showed how to keep A\*'s optimality while using depth-first memory. The price is that the search repeats work in each iteration.

## Key concepts

- **f-bound**: a threshold on f(n) = g(n) + h(n). Nodes whose f exceeds the bound are cut off.
- **Iteration**: a depth-first search that explores all nodes with f below the current bound, and records the smallest f value that was cut off.
- **Admissible heuristic**: as in A\*, a heuristic that never overestimates the remaining cost, needed for optimality.
- **Re-expansion**: nodes are visited again in each iteration. This is the time cost of the small memory footprint.

## How it works

1. Set the bound to h(start), the heuristic value of the start state.
2. Run a depth-first search from the start. Stop expanding any node whose f exceeds the bound, and record the smallest such f value.
3. If a goal is reached within the bound, return the path. With an admissible heuristic it is optimal.
4. Otherwise set the new bound to the smallest f value recorded in step 2, and repeat.

The bound always increases, and each new value is the f-value of some node the previous iteration reached. So the process reaches the optimal cost after a finite number of iterations, when the search has a finite number of distinct f-values to pass through.

## Key methods

- [A\* search](a-star.md): best-first search that keeps the whole frontier. It is optimal and memory-hungry, which motivates IDA\*.
- Related memory-bounded methods are discussed in the references below.

## Results and limits

- With an admissible heuristic, IDA\* is optimal, and its memory grows only linearly with the depth of the search (Korf, 1985).
- Each iteration re-expands the nodes of the previous iterations. When many distinct f-values exist, each iteration adds little new work, and the overhead becomes large.
- Repeated states, such as transpositions in a search graph, are revisited in every branch. Reinefeld and Marsland (1994) add a transposition table to reduce this.
- Solution quality and speed depend on the heuristic, as for A\*.

## Applications

- **Puzzles**: sliding-tile puzzles, where a good heuristic is available and the frontier of A\* would be large.
- **Route finding under memory limits**: navigation on large maps or graphs when storing the frontier is not possible.
- **Planning**: optimal search with admissible heuristics where memory, not time, is the binding limit.

## Open questions

- Choosing between IDA\* and other memory-bounded methods depends on the problem's structure, especially how many states repeat.
- Handling transpositions efficiently without the memory cost that IDA\* was designed to avoid remains a design trade-off.

## References

### Seminal papers

- Korf, R. E. (1985). Depth-first iterative-deepening: an optimal admissible tree search. *Artificial Intelligence* 27(1), 97–109. https://doi.org/10.1016/0004-3702(85)90084-0 — Introduces IDA\*, an optimal search with linear memory.
- Hart, P. E., Nilsson, N. J. & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136 — Defines A\* and its optimality, the baseline that IDA\* preserves.
- Dechter, R. & Pearl, J. (1985). Generalized best-first search strategies and the optimality of A\*. *Journal of the ACM* 32(3), 505–536. https://doi.org/10.1145/3828.3830 — Analyses best-first strategies and the optimality of A\*.
- Korf, R. E. (1993). Linear-space best-first search. *Artificial Intelligence* 62, 41–78. https://doi.org/10.1016/0004-3702(93)90045-d — A linear-space best-first method that addresses the same memory limit of A\*.
- Reinefeld, A. & Marsland, T. A. (1994). Enhanced iterative-deepening search. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 16, 701–710. https://doi.org/10.1109/34.297950 — Improves iterative deepening with a transposition table for repeated states.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook treatment of iterative deepening and memory-bounded search.
