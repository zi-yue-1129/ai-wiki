---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/planning
  - theory/paradigms/symbolic-ai/search
tags:
  - planning
  - representation
  - classical planning
aliases:
  - STRIPS
  - Stanford Research Institute Problem Solver
  - 史丹福研究院問題求解器
---

# STRIPS

STRIPS is a representation for classical planning in which each action has a precondition list, an add list and a delete list. A state is a set of facts, and an action applies when its preconditions are in the state. Part of [Automated planning](index.md).

## Overview

Before STRIPS, planning systems often depended on theorem proving in logic, which was slow and hard to control. Fikes and Nilsson (1971) represented actions in a restricted form so that planning became a search over sets of facts. The representation was small enough to be efficient and clear enough to be reused, and it became the basis of later modelling languages, including PDDL.

## Key concepts

- **Precondition**: facts that must hold before the action can be applied.
- **Add list**: facts that become true after the action.
- **Delete list**: facts that become false after the action. Facts not mentioned are assumed unchanged, which is the closed-world and frame assumption.
- **Action schema**: an action with variables, instantiated by objects in the problem.

## How it works

Let \(s\) be a state, a set of facts, and let an action \(a\) have precondition \(\mathrm{pre}(a)\), add list \(\mathrm{add}(a)\) and delete list \(\mathrm{del}(a)\). The action is applicable in \(s\) when \(\mathrm{pre}(a)\subseteq s\). Its successor state is

\[
\gamma(s,a) = \left(s\setminus \mathrm{del}(a)\right)\cup \mathrm{add}(a).
\]

A plan is a sequence of applicable actions that leads from the initial state to a state containing the goal facts. A forward planner applies this rule from the initial state, and a backward planner regresses the goal through the actions. Both are usually guided by a heuristic.

## Variants

- **Propositional STRIPS** uses ground facts only. It is the simplest form.
- **ADL** (Action Description Language) allows conditional effects and quantified preconditions, and it is more expressive than STRIPS.
- **PDDL** extends the STRIPS idea with typed objects, numeric fluents and durative actions, and it is used in planning competitions.

## Results and limits

- The representation is simple to read and to implement, and it supports general-purpose heuristics derived from relaxed versions of the problem (Bonet & Geffner, 2001).
- The closed-world assumption means that every fact not in the state is false, which fits some domains but not those with incomplete knowledge.
- Negative preconditions and conditional effects are not part of basic STRIPS, so some domains need extensions.
- Plan existence in general is hard, and the search cost depends on the heuristic used.

## Applications

- **Robot task planning**: Shakey, the robot for which STRIPS was developed, planned sequences of movements and pushes between rooms.
- **Planning benchmarks**: most planning competitions use PDDL, which descends from STRIPS, and planners such as Fast Downward solve these benchmarks with heuristic search (Helmert, 2006).
- **Teaching**: a standard first representation for planning in AI courses.

## Open questions

- Extending STRIPS to uncertainty, numbers and time keeps the representation tractable only in some cases.
- Automatically learning action models from observations, so that the representation does not have to be written by hand, is still hard to do reliably.

## References

### Seminal papers

- Fikes, R. E. & Nilsson, N. J. (1971). STRIPS: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence* 2(3–4), 189–208. https://doi.org/10.1016/0004-3702(71)90010-5 — Introduces the STRIPS representation and its planner.
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence* 129(1–2), 5–33. https://doi.org/10.1016/S0004-3702(01)00108-4 — Shows how heuristics for STRIPS-style problems can be computed from relaxed problems.
- Blum, A. L. & Furst, M. L. (1997). Fast planning through planning graph analysis. *Artificial Intelligence* 90(1–2), 281–300. https://doi.org/10.1016/S0004-3702(96)00047-1 — Plans for STRIPS-style problems with a planning graph, as an alternative to forward search.

### Surveys and textbooks

- Helmert, M. (2006). The Fast Downward planning system. *Journal of Artificial Intelligence Research* 26, 191–246. https://doi.org/10.1613/jair.1705 — Planner for STRIPS-style and PDDL problems, built on heuristic search.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook account of STRIPS actions and the planning problem.
- Kaelbling, L. P., Littman, M. L. & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *Artificial Intelligence* 101(1–2), 99–134. https://doi.org/10.1016/S0004-3702(98)00023-X — Shows what changes when STRIPS-style actions must be planned under partial observability.
