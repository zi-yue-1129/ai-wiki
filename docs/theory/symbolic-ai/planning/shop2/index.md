---
status: draft
last_reviewed: 2026-10-28
tags:
  - planning
  - reasoning
aliases:
  - SHOP2
  - SHOP
  - 階層任務網路規劃器
  - HTN planning
  - Hierarchical task network planning
  - 任務分解
---

# SHOP2

SHOP2 is a hierarchical task network (HTN) planner. Instead of searching for a goal state, it decomposes a high-level task into subtasks, using methods that people write for each kind of task, until only primitive actions remain. It was described by Dana Nau and colleagues in 2003 and won an award at the 2002 International Planning Competition. It is one of the landmark methods in the [automated planning overview](../index.md).

## Overview

Many real problems come with a known way of doing things. To deliver a parcel, a robot fetches it, drives to the destination and hands it over. An HTN planner encodes this knowledge as methods. Each method says which task it solves, under what conditions, and which subtasks it creates, so the planner searches over combinations of methods rather than every possible sequence of actions.

Unlike [STRIPS](../strips/index.md), which must discover the structure of a solution, an HTN planner receives part of that structure from its author. This allows longer plans, at the cost of depending on the methods.

## Key concepts

- **Task**: something to be done. A **primitive task** is an action that can be executed directly. A **compound task** must be decomposed.
- **Method**: a rule that applies to a compound task. It has a precondition on the current state and a list of subtasks that replaces the task when the precondition holds.
- **Task network**: an ordered or partially ordered list of tasks still to be performed.
- **Ordered decomposition**: SHOP2 handles subtasks in the order written.

## How it works

A method $m$ is a triple of a compound task, a precondition over the state and a subtask list. The planner works through the task network from left to right, so that the state at each step is known. The procedure is as follows.

1. Given the current state $s$ and the task network $T$, if $T$ is empty, return the plan built so far.
2. Take the first task $t$ in $T$.
3. If $t$ is primitive, check its preconditions in $s$. If they hold, apply the operator to $s$, append it to the plan and continue with the rest of $T$.
4. If $t$ is compound, find the methods for $t$ whose preconditions hold in $s$. For each in turn, replace $t$ by the method's subtasks and repeat from step 1.
5. If no method leads to a complete plan, backtrack to the most recent choice.

Because the state is known at each step, preconditions can test the full current state. The 2003 paper describes the temporal and metric features behind SHOP2's competition performance.[^1]

## Results

The paper reports that SHOP2 received one of the awards for distinguished performance at the 2002 International Planning Competition. It attributes the result to features that handle temporal and metric domains, and it describes those features in detail.[^1] I did not read the full benchmark tables, so no numbers are quoted here.

## Limitations

- **Authoring cost.** The methods are written by hand, so the planner is only as good as the knowledge it is given. A missing method means that a solution is not found, even when one exists.
- **Dependence on decompositions.** The hierarchy can rule out good plans that do not fit the methods, so the planner is not a general search over all plans.
- **Ordering.** Ordered decomposition commits to the sequence of subtasks early, which can be restrictive when tasks overlap.

## Open questions

- Can methods be learned from demonstrations or from language, so that the authoring cost falls without losing the structure?
- How should an HTN planner recover when an action fails and the world no longer matches its plan?

## Connections

SHOP2 is one way to add hierarchy to planning, and it is compared with the flat search of [STRIPS](../strips/index.md) and the language-model approach of [SayCan](../saycan/index.md) in the [planning overview](../index.md). Hierarchical reinforcement learning is a learning counterpart, in which a policy chooses sub-policies rather than hand-written methods.

## Applications

- **Game AI**, where designers encode how characters carry out tasks such as patrolling or taking cover.
- **Logistics and project planning**, where tasks such as transporting a load already have standard procedures.

[^1]: Nau et al. (2003), listed above. The award and the temporal and metric features are as stated in the paper's abstract.

## References

### Seminal papers

- Nau, D. S. et al. (2003). SHOP2: An HTN Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1141 — Describes SHOP2, its ordered hierarchical decomposition and its features for temporal and metric planning, which won an award at the 2002 competition.
- Fikes, R. E. & Nilsson, N. J. (1971). Strips: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(71)90010-5 — The operator representation that HTN planners use for their primitive actions.

### Articles and documentation

- Fox, M. & Long, D. (2003). PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1129 — Defines the temporal and numeric planning features that SHOP2 is designed to handle.
- Helmert, M. (2006). The Fast Downward Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1705 — Describes a non-hierarchical heuristic planner for PDDL tasks, which won the classical track of the 2004 competition.
- Hoffmann, J. & Nebel, B. (2001). The FF Planning System: Fast Plan Generation Through Heuristic Search. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.855 — Shows heuristic forward search, a flat alternative that does not rely on hand-written methods.
- Ahn, M. et al. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv. https://arxiv.org/abs/2204.01691 — Uses primitive robot skills as the actions of a plan that a language model composes.
