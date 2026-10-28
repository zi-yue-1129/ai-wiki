---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/search
tags:
  - search
  - heuristic search
  - optimal search
aliases:
  - A*
  - A-star
  - A 星搜尋
  - A* 搜尋
---

# A\* Search

A\* is a best-first search algorithm that orders nodes by \(f(n)=g(n)+h(n)\), the cost so far plus an estimate of the cost remaining. With an admissible heuristic it returns an optimal path. Part of [Search algorithms](index.md).

## Overview

Uniform-cost search finds optimal paths but ignores the goal, so it expands many unhelpful nodes. Greedy best-first search follows the heuristic toward the goal, which is fast but can return poor paths. A\* combines the two: \(g\) keeps the path cost honest, and \(h\) pulls the search toward the goal.

## Key concepts

- **\(g(n)\)**: the cost of the cheapest path found so far from the start to node \(n\).
- **\(h(n)\)**: a heuristic estimate of the cost from \(n\) to the goal.
- **Admissibility**: \(h(n)\le h^*(n)\) for the true optimal remaining cost \(h^*(n)\). It guarantees that A\* never misses a better path.
- **Consistency**: \(h(n)\le c(n,n')+h(n')\) for every edge. A consistent heuristic is admissible, and it guarantees that each node is expanded at most once.

## How it works

A\* keeps a priority queue of frontier nodes ordered by \(f\). It repeatedly removes the node with the lowest \(f\), expands it, and updates the \(g\) value of each successor if a cheaper path is found. It stops when the goal is removed from the queue. Hart et al. (1968) showed that with an admissible heuristic the first goal found is optimal. When \(h\equiv 0\), A\* reduces to uniform-cost search, and when \(h\) is only a guess, it is no longer guaranteed to be optimal.

## Variants

- **Weighted A\*** uses \(f=g+w\,h\) with \(w>1\). It expands fewer nodes, but the path can be up to \(w\) times the optimal cost.
- **IDA\*** repeats depth-first searches with an increasing \(f\)-bound. It uses memory linear in the depth, which makes it practical when storing the whole frontier is impossible. Korf (1985) introduced it.
- **Anytime variants** find a first solution quickly and then improve it as time allows.

## Results and limits

- With an admissible heuristic, A\* is optimal, and with a consistent one it is also optimally efficient among algorithms that use the same heuristic.
- Its memory use is the main limit. It stores the whole frontier, so the memory grows exponentially with depth in the worst case.
- The quality of \(h\) determines the speed. A weak heuristic makes A\* behave like uniform-cost search.
- Finding a good heuristic for a new problem is usually the hardest part of applying A\*.

## Applications

- **Path planning**: shortest routes on road networks and grid maps, including robot navigation.
- **Puzzles**: sliding-tile puzzles with the Manhattan distance heuristic.
- **Planning**: heuristic state-space search in classical planning. Helmert (2006) contrasts relaxation-based heuristics with the causal-graph heuristic used by Fast Downward.

## Open questions

- Learning admissible heuristics from data is possible, but guaranteeing admissibility for a learned heuristic is hard.
- Memory-bounded variants trade time for memory, and choosing the trade-off for a given problem is still largely empirical.

## References

### Seminal papers

- Hart, P. E., Nilsson, N. J. & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics* 4(2), 100–107. https://doi.org/10.1109/TSSC.1968.300136 — Defines A\* and proves that an admissible heuristic yields optimal paths.
- Korf, R. E. (1985). Depth-first iterative-deepening: an optimal admissible tree search. *Artificial Intelligence* 27(1), 97–109. https://doi.org/10.1016/0004-3702(85)90084-0 — Introduces IDA\*, a memory-efficient optimal search.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook treatment of A\* with admissible and consistent heuristics.
- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — Describes the Fast Downward planner, a best-first search planner whose heuristic is built from a hierarchical decomposition of the planning task (the causal graph heuristic).
- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — Shows how graph-based heuristics speed up heuristic search for planning.
