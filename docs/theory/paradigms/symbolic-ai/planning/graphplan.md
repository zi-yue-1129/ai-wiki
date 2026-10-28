---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/planning
  - theory/paradigms/symbolic-ai/search
tags:
  - planning
  - planning graph
  - classical planning
aliases:
  - GraphPlan
  - 規劃圖
  - Planning graph
---

# GraphPlan

GraphPlan is a classical planner that builds a layered planning graph of possible facts and actions, with mutual-exclusion information, and then searches that graph backwards for a valid plan. Part of [Automated planning](index.md).

## Overview

Forward search in STRIPS-style planning can be slow, because the number of states grows quickly. GraphPlan avoids enumerating states. It builds a compact graph that over-approximates what could be true at each step, and it uses that graph to prune the search for a plan. Blum and Furst (1997) showed that this approach solved benchmark problems much faster than the planners of the time.

## Key concepts

- **Fact layer**: the set of facts that could be true after \(i\) steps.
- **Action layer**: the set of actions whose preconditions could all hold at step \(i\).
- **Mutual exclusion (mutex)**: a pair of facts or actions that cannot both hold, or both be executed, at the same step. Mutexes are propagated through the graph and make the backward search more efficient.
- **Leveling off**: the point at which the graph no longer changes between layers. After that, adding layers does not add new facts, so the search for a plan can be checked for failure.

## How it works

The algorithm alternates two steps.

1. **Expansion**: starting from the initial facts, add an action layer containing every action whose preconditions are in the current fact layer and not mutually exclusive, and then add the next fact layer from their effects. Mutexes are updated at each layer.
2. **Extraction**: when the goal facts appear in a layer without mutual exclusion, search backwards for a set of actions that achieves them, recursively achieving the preconditions at earlier layers. If this fails and the graph has leveled off, the goal is unreachable.

The expansion stops at a layer where all goal facts appear, so the search is over the smallest number of parallel steps the graph shows. Because each layer may contain several actions executed in parallel, the plan length counts layers and is not the same as the number of actions.

## Variants

- **Parallel plans**: the standard GraphPlan finds a plan with the fewest parallel steps, not the fewest actions.
- **Graph-based heuristics**: the same planning graph can give estimates of the distance to the goal for heuristic search, a link to methods such as those in Bonet and Geffner (2001).
- **Later planning-graph planners** reuse the same idea with improved mutex reasoning and extraction.

## Results and limits

- The planning graph is polynomial in size for a fixed number of layers, which avoids enumerating the full state space.
- Blum and Furst (1997) report large speed-ups on benchmark domains compared with contemporary planners.
- The planning graph can still grow large in domains with many objects, and mutex computation is costly.
- Plan optimality in terms of total actions is not guaranteed, because extraction minimises parallel steps.

## Applications

- **Benchmark planning**: GraphPlan was among the first planners to solve many standard benchmark problems quickly, and it set the agenda for later planners.
- **Heuristics for search**: the planning graph supplies distance estimates to search-based planners (Blum & Furst, 1997).
- **Education**: a clear example of how a relaxed view of a problem can drive a practical algorithm.

## Open questions

- The mutex information is only approximate, and better mutex reasoning can improve performance but adds cost.
- Finding good plans in terms of total action cost, not parallel steps, requires different extraction methods.

## References

### Seminal papers

- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — Introduces GraphPlan and reports its performance on benchmarks.
- Fikes, R. E. & Nilsson, N. J. (1971). STRIPS: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence* 2(3–4), 189–208. https://doi.org/10.1016/0004-3702(71)90010-5 — The STRIPS problems that GraphPlan solves.
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence* 129(1–2), 5–33. https://doi.org/10.1016/S0004-3702(01)00108-4 — Relates graph-based relaxations to heuristics for planning.

### Surveys and textbooks

- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — Describes heuristics from relaxed problems, which are closely related to the relaxation a planning graph encodes.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook introduction to planning graphs and GraphPlan.
