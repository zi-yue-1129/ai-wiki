---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - theory/paradigms/symbolic-ai/search
  - theory/paradigms/probabilistic
tags:
  - planning
  - symbolic AI
  - decision making
aliases:
  - 自動規劃
  - Automated planning
  - AI planning
  - PDDL
---

# Automated Planning

Automated planning is the task of finding a sequence of actions that takes an agent from an initial state to a goal state. A planner works from a description of the actions, their preconditions and their effects. Part of [Symbolic AI, search and planning](../index.md).

## Overview

A planning problem specifies an initial state, a goal, and a set of action schemas. Each action can be applied only when its preconditions hold, and it changes the state through its effects. The planner searches the space of states or of partial plans for a path to the goal. Classical planning assumes a fully known, deterministic world, and it has been extended to uncertain and hierarchical settings.

The standard modelling language for classical planning is PDDL, the Planning Domain Definition Language, which grew out of the STRIPS representation. The two methods below each have their own page.

## Key concepts

- **State**: a set of facts that hold at a moment. In classical planning, states are sets of ground atoms.
- **Action schema**: a template with preconditions, add effects and delete effects.
- **Plan**: a sequence of actions that transforms the initial state into one that satisfies the goal.
- **Heuristic**: an estimate of the number of actions still needed. Good heuristics, often from relaxed problems, make search practical (Bonet & Geffner, 2001).

## How it works

Most planners search. A forward planner starts at the initial state and expands actions whose preconditions hold, with a heuristic to guide the search. A backward planner starts from the goal and regresses it through actions. Graph-based planners build a compact layered structure first and then extract a plan from it. The choice of representation and search strategy largely determines the planner's performance.

## Key methods

- [STRIPS](strips.md): the original representation of actions as preconditions, add lists and delete lists, and the basis of PDDL.
- [GraphPlan](graphplan.md): builds a layered planning graph with mutual-exclusion information and then searches it backwards for a plan.

Other approaches named in the literature include planning as heuristic search (Bonet & Geffner, 2001) and hierarchical task-network planning, which decomposes tasks into subtasks. These are summarised here without their own pages.

## Planning under uncertainty

When actions are stochastic or observations are partial, planning becomes a decision problem. Markov decision processes model fully observable stochastic domains, and partially observable MDPs (POMDPs) handle hidden states. Kaelbling et al. (1998) give the standard formulation of POMDPs for planning and acting. The [reinforcement learning](../../reinforcement-learning/index.md) paradigm approaches the same problems through learning rather than a given model.

## Connections

- [Search algorithms](../search/index.md) provide the search methods that most planners use, such as A\* with planning heuristics.
- [Probabilistic methods](../../probabilistic/index.md) cover the uncertainty models that planning under uncertainty needs.
- [Reinforcement learning](../../reinforcement-learning/index.md) solves sequential decision problems with learned values or policies.

## Applications

- **Logistics**: scheduling deliveries and transport within a fixed set of rules.
- **Space missions and robotics**: autonomous spacecraft and robots that choose their own sequence of actions (Kaelbling et al., 1998).
- **Manufacturing and workflow**: generating process plans that satisfy resource and ordering constraints.

## Open questions

- Domain-independent planners still need domain-specific help to scale. Learning useful heuristics or control knowledge from examples is an active area.
- Combining planning models with learned perception and language models, and checking that the resulting plans are correct, is difficult.
- Hierarchical and uncertain planning are harder than classical planning, and general efficient methods remain limited.

## References

### Seminal papers

- Fikes, R. E. & Nilsson, N. J. (1971). STRIPS: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence* 2(3–4), 189–208. https://doi.org/10.1016/0004-3702(71)90010-5 — Introduces the STRIPS representation of actions and the planner built on it.
- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — Introduces GraphPlan, a planning-graph method that is much faster than earlier planners on benchmarks.
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence* 129(1–2), 5–33. https://doi.org/10.1016/S0004-3702(01)00108-4 — Casts classical planning as heuristic search and studies heuristics derived from relaxed problems.
- Kaelbling, L. P., Littman, M. L. & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence* 101(1–2), 99–134. https://doi.org/10.1016/S0004-3702(98)00023-X — Formulates planning and acting under partial observability with POMDPs.

### Surveys and textbooks

- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — Describes a widely used classical planner built on heuristic search.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook treatment of classical planning, planning graphs and planning under uncertainty.
