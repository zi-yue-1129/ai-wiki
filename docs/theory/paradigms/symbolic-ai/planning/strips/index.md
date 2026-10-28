---
status: draft
last_reviewed: 2026-10-28
tags:
  - planning
  - search
aliases:
  - STRIPS
  - Stanford Research Institute Problem Solver
  - 史丹佛研究院問題解決器
  - 經典規劃
  - Classical planning
---

# STRIPS

STRIPS is the representation and planning approach introduced by Richard Fikes and Nils Nilsson in 1971 for the problem solver built at the Stanford Research Institute. It describes each action by its preconditions and by the facts it adds and deletes, and it finds a plan by searching through the states those actions produce. It is the origin of the classical planning formalism and is the first of the landmark methods in the [automated planning overview](../index.md).

## Overview

A planner needs a compact way to say what an action does. Listing the full effect on the whole world for each action would be tedious. STRIPS keeps the description small: an action changes only the facts it mentions, and everything else is assumed to stay the same.

The representation was designed for a mobile robot, and it connects planning to logic.[^1] The later PDDL language, which standardised planning problems, extends this kind of description.[^2]

## Key concepts

- **Operator (action schema)**: a named action with parameters, such as `move(robot, from, to)`.
- **Precondition list**: facts that must be true before the action is applied.
- **Add list**: facts that become true after the action.
- **Delete list**: facts that stop being true after the action.
- **Closed-world assumption**: any fact not in the state is taken to be false. Negative preconditions are therefore written as the absence of a fact.
- **Relaxed problem**: the same operators with their delete lists removed. Its solution cost is a common heuristic estimate for the original problem.[^3]

## How it works

A state is a set of ground facts. An action $a$ is applicable in state $s$ when its preconditions are contained in $s$. Applying it gives the successor state

$$
\mathrm{succ}(s, a) = \bigl(s \setminus \mathrm{del}(a)\bigr) \cup \mathrm{add}(a), \quad \text{if } \mathrm{pre}(a) \subseteq s.
$$

A planner then runs the following procedure.

1. Start from the initial state $s_0$ and set the frontier to contain it.
2. Remove a state $s$ from the frontier. If the goal facts are all in $s$, return the sequence of actions on the path to $s$.
3. For each operator whose preconditions hold in $s$, compute the successor state with the formula above and record the action that produced it.
4. Add the new states to the frontier, ordered by a search strategy such as breadth-first search, or by A\* with a heuristic. Return to step 2.
5. If the frontier empties, no plan exists.

The search is a graph search. What STRIPS contributes is the compact description from which successors are generated. Later heuristic planners keep this representation and change the search order.[^3]

## Results

The 1971 paper is a method description with worked examples rather than a benchmark. Its evidence is the demonstration that action descriptions and theorem proving can produce plans for a robot task. I did not read the full text, so no numbers are given here. Later evaluation of the same representation came from the planning competitions, where heuristic planners built on STRIPS-style operators performed well.[^3][^4]

## Limitations

- **Expressiveness.** The basic form cannot express conditional effects, quantified goals or numeric quantities. Richer languages such as ADL add conditional effects and quantifiers, and PDDL2.1 adds numeric and temporal features.[^2]
- **Frame assumption.** The rule that unmentioned facts stay unchanged must be handled carefully when actions have side effects, which the basic form does not capture.
- **Search cost.** Without a good heuristic, the number of states grows exponentially with plan length, so the representation alone does not make planning fast.

## Open questions

- How should an action model represent uncertainty, indirect effects and continuous quantities while keeping the simplicity that made STRIPS useful?
- Can operator descriptions be learned from observations, so that people do not need to write them by hand?

## Connections

STRIPS is the representation on which [search-based planning](../../search/index.md) is built, and its heuristics are the reason state-space planners became fast. The planning overview compares it with [hierarchical task networks](../shop2/index.md) and with [language-model planning](../saycan/index.md). For the general search methods used to explore its state space, see [A\*](../../search/a-star/index.md).

## Applications

- **Robot task planning**, which is the original application, where a robot must sequence actions such as moving and pushing objects.
- **Logistics and transport**, modelled in PDDL with operators for loading, moving and unloading, as used in the planning competitions.[^2]

[^1]: Fikes and Nilsson (1971), listed above.
[^2]: Fox and Long (2003), listed above.
[^3]: Hoffmann and Nebel (2001), listed above. The relaxation and its use as a heuristic are described in their abstract.
[^4]: Helmert (2006), listed above. The competition result is as reported in the paper's abstract.

## References

### Seminal papers

- Fikes, R. E. & Nilsson, N. J. (1971). Strips: A new approach to the application of theorem proving to problem solving. *Artificial Intelligence*. https://doi.org/10.1016/0004-3702(71)90010-5 — Introduces the STRIPS representation, with preconditions, add and delete lists, and the planner built on it.
- Bonet, B. & Geffner, H. (2001). Planning as heuristic search. *Artificial Intelligence*. https://doi.org/10.1016/S0004-3702(01)00108-4 — Treats STRIPS-style planning as heuristic search, deriving heuristics from relaxed versions of the problem.

### Articles and documentation

- Fox, M. & Long, D. (2003). PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1129 — Defines the PDDL2.1 extension of STRIPS-style operators to temporal and numeric planning, with its semantics.
- Hoffmann, J. & Nebel, B. (2001). The FF Planning System: Fast Plan Generation Through Heuristic Search. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.855 — Shows heuristic forward search whose goal-distance estimate ignores delete lists, a relaxation of STRIPS operators.
- Helmert, M. (2006). The Fast Downward Planning System. *Journal of Artificial Intelligence Research*. https://doi.org/10.1613/jair.1705 — Describes a planner for PDDL tasks that uses a causal-graph heuristic and won the classical track of the 2004 competition.
