---
status: draft
last_reviewed: 2026-10-28
tags:
  - search
  - planning
aliases:
  - A*
  - A-star
  - A* 搜尋
  - A星演算法
  - 啟發式搜尋
  - Heuristic search
---

# A\* Search

A\* is a best-first search that ranks each frontier node by the cost already paid plus an estimate of the cost still to come. When that estimate never overestimates the true remaining cost, A\* returns a cheapest path. It is the landmark informed search method and is described in the parent [search algorithms overview](../index.md).

## Overview

Breadth-first search treats every unexplored node alike, which wastes effort on places far from a road-network destination. A\* uses a heuristic, such as straight-line distance on a map, to decide which node to expand next.

Peter Hart, Nils Nilsson and Bertram Raphael gave the method a formal basis in 1968. They showed when the heuristic can be trusted to lead to an optimal path. The 1968 paper remains the reference point for the method.[^1]

## Key concepts

- **Cost so far $g(n)$**: the total cost of the path from the start to node $n$ found so far.
- **Heuristic $h(n)$**: an estimate of the cost from $n$ to a goal.
- **Evaluation $f(n)$**: the sum $g(n)+h(n)$, which is the priority of $n$ on the frontier.
- **Admissible heuristic**: one with $0 \le h(n) \le h^*(n)$, where $h^*(n)$ is the true minimum remaining cost. It never overestimates.
- **Consistent heuristic**: one that satisfies $h(n) \le c(n,n') + h(n')$ for every edge, a stronger condition that ensures no node needs to be expanded twice.
- **OPEN and CLOSED lists**: the frontier, and the set of nodes already expanded.

## How it works

The evaluation is

$$
f(n) = g(n) + h(n).
$$

The algorithm proceeds as follows.

1. Put the start node $s$ on OPEN, with $g(s)=0$ and $f(s)=h(s)$.
2. Remove from OPEN the node $n$ with the smallest $f(n)$. If $n$ is a goal, return the path to it.
3. Move $n$ to CLOSED. For each successor $n'$ with edge cost $c(n,n')$, compute $g' = g(n)+c(n,n')$.
4. If $n'$ is new, or $g' < g(n')$, record $n$ as its parent, set $g(n')=g'$ and $f(n')=g'+h(n')$, and put $n'$ on OPEN. If $n'$ was on CLOSED, move it back to OPEN.
5. Repeat from step 2. If OPEN is empty, no path exists.

If $h(n)=0$ for every node, the rule reduces to uniform-cost search, which is Dijkstra's shortest-path method.[^2] A heuristic that is larger but still admissible focuses the search more and expands fewer nodes, while preserving optimality. The guarantee requires admissibility; a heuristic that overestimates can make A\* return a costlier path. When memory is tight, iterative-deepening A\* repeats a depth-first search with a growing bound on $f$.[^3]

## Results

The 1968 paper is a formal analysis and contains no benchmark. Its evidence is proofs. A later correction note restated the main result: if the heuristic is consistent, A\* is optimal and expands no more nodes than any other admissible algorithm that is no more informed than it.[^1] Later experiments came in path finding and planning. In the AIPS-2000 planning competition, the FF planner, which uses a heuristic in the same spirit, was reported to be the most successful automatic planner, and the authors gave data on other benchmark domains.[^4]

## Limitations

- **Memory.** A\* keeps every generated node on OPEN or CLOSED. For large branching factors, memory is the binding constraint long before time is.
- **Heuristic quality.** Optimality depends on admissibility, and efficiency depends on how close $h$ is to $h^*$. A poor heuristic makes A\* behave like breadth-first search.
- **Worst-case cost.** The number of expansions can still grow exponentially with solution depth, even with a good heuristic.

## Open questions

- How can heuristics be learned automatically while keeping the admissibility guarantee? Learned estimates often overestimate.
- How can A\* be combined with learned value functions, as in modern planning and reasoning systems, without losing its guarantees?

## Connections

A\* is the informed counterpart of Dijkstra's shortest-path algorithm, of which it is a generalisation. Its heuristic ideas are the basis of heuristic search in planning, where relaxed problems supply the estimate. The method also points to the [symbolic AI overview](../../index.md), where search and logic are presented together. For the human side, heuristic search is a model of problem solving discussed in [Heuristics and biases](../../../../../brain-mind/cognitive-science/heuristics-and-biases/index.md).

## Applications

- **Route planning and navigation** on road, rail and transport networks, where distance or travel time gives a natural heuristic.
- **Robot motion planning** on grid maps, where the grid distance to the goal is a standard estimate.
- **Automated planning** in puzzles and logistics, where relaxed-problem heuristics guide the search.[^4]

[^1]: Hart, Nilsson and Raphael (1968) and the correction note (1972), listed above. The 1972 abstract describes the consistency result.
[^2]: Dijkstra (1959), listed above.
[^3]: Korf (1985), listed above.
[^4]: Hoffmann and Nebel (2001), listed above. The competition claim is as reported in their abstract.

## References

### Seminal papers

- Hart, P. E., Nilsson, N. J. & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths. *IEEE Transactions on Systems Science and Cybernetics*. https://doi.org/10.1109/TSSC.1968.300136 — The original paper introducing A* and proving its conditions for optimal paths.
- Hart, P. E., Nilsson, N. J. & Raphael, B. (1972). Correction to "A Formal Basis for the Heuristic Determination of Minimum Cost Paths". *ACM SIGART Bulletin*. https://doi.org/10.1145/1056777.1056779 — Correction note restating the optimality results and the consistency condition for A*.
- Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*. https://doi.org/10.1007/BF01386390 — Gives the shortest-path algorithm that A* generalises when the heuristic is zero.
- Korf, R. E. (1985). Depth-first iterative-deepening. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(85)90084-0 — Introduces IDA*, which runs a series of depth-first searches bounded by the f-cost to save memory.

### Articles and documentation

- Hoffmann, J. & Nebel, B. (2001). The FF Planning System: Fast Plan Generation Through Heuristic Search. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.855 — Shows heuristic forward search with a relaxed-problem estimate applied to automated planning.
