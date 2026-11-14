---
last_reviewed: 2026-11-04
related:
  - theory/paradigms/symbolic-ai/planning
tags:
  - planning
  - hierarchical planning
  - task decomposition
aliases:
  - HTN
  - Hierarchical task network
  - Hierarchical task network planning
  - 階層任務網路
  - 分層任務網路
---

# Hierarchical Task Network Planning

Hierarchical task network (HTN) planning finds a plan by repeatedly decomposing high-level tasks into subtasks, using domain-specific methods, until only primitive actions remain. Part of [Automated planning](index.md).

## Overview

Classical planners such as those in [STRIPS](strips.md) search over states using only primitive actions. HTN planners add knowledge about how a task is usually done. A domain expert writes methods, which are recipes for achieving a task, and the planner expands them. The approach is common in practical systems because the recipes make the search much smaller. Georgievski and Aiello (2015) compare HTN formalisms and planners. Ghallab et al. (2004) give a standard formulation.

## Key concepts

- **Primitive task**: an action that can be executed directly, with preconditions and effects as in STRIPS.
- **Compound task**: a task that is not executable directly and must be decomposed by a method.
- **Method**: a rule that replaces a compound task with subtasks, under stated conditions.
- **Task network**: a set of tasks with ordering constraints that every plan must respect.

## How it works

The planner keeps a list of pending tasks. It takes the first compound task and chooses a method whose conditions hold in the current state. It replaces the task with the method's subtasks and continues. When only primitive tasks remain, the planner checks their preconditions along the sequence. If a check fails, it backtracks and tries another method.

As a schematic example, a task "transport a package from A to C" could have one method that drives directly, with subtasks load, drive from A to C and unload. A second method, used when the direct route is closed, could split the task into a transport from A to B and a transport from B to C. The planner picks whichever method applies.

Some HTN planners decompose tasks in a fixed order, which makes it easy to check the state during decomposition. SHOP2 is one such ordered planner (Nau et al., 2003). Others allow partially ordered task networks, which is more flexible but harder to search.

## Key methods

- [STRIPS](strips.md): the primitive action model that HTN planners build on. HTN planning does not replace it.
- [GraphPlan](graphplan.md): classical planning without decomposition, a useful contrast for how much knowledge the methods supply.

## Results and limits

- Methods encode domain knowledge, so planning can be fast on problems that match the decomposition. The cost is that the knowledge must be written and maintained (Nau et al., 2003).
- A method that is incomplete or wrong can make the planner miss solutions. Completeness depends on the method library.
- HTN formalisms differ in expressivity and computational complexity. Georgievski and Aiello (2015) compare these trade-offs, which depend on the formalism chosen.

## Applications

- **Logistics and transport**, where standard procedures for moving goods can be written as methods.
- **Game AI and robotics**, where task recipes such as "clear the room" are natural.
- **Business and industrial workflows**, where planning follows documented procedures.

## Connections

- [Automated planning](index.md) gives the wider context, including classical and uncertain planning.
- [Search algorithms](../search/index.md): HTN planners search over ways to decompose tasks.
- [Reinforcement learning](../../reinforcement-learning/index.md) shares the idea of decomposing a long task into sub-tasks, through hierarchical methods.

## Open questions

- Writing good methods is labour-intensive. Learning methods from plan traces is an active but difficult problem.
- Combining HTN decomposition with learned models and with acting in real environments remains a research question (Ghallab et al., 2016).

## References

### Seminal papers

- Nau, D. S., Au, T.-C., Ilghami, O., Kuter, U., Murdock, J. W., Wu, D. & Yaman, F. (2003). SHOP2: an HTN planning system. *Journal of Artificial Intelligence Research* 20, 379–404. https://doi.org/10.1613/jair.1141 — Describes SHOP2, an ordered HTN planner that decomposes tasks in plan order.
- Ghallab, M., Nau, D. & Traverso, P. (2004). Hierarchical task network planning. In *Automated Planning: Theory and Practice*, 229–261. https://doi.org/10.1016/b978-155860856-6/50017-x — Standard chapter on the formal definition of HTN planning.

### Surveys and textbooks

- Georgievski, I. & Aiello, M. (2015). HTN planning: overview, comparison, and beyond. *Artificial Intelligence* 222, 124–156. https://doi.org/10.1016/j.artint.2015.02.002 — Overview and comparison of HTN formalisms and planners.
- Ghallab, M., Nau, D. & Traverso, P. (2016). *Automated Planning and Acting*. Cambridge University Press. https://doi.org/10.1017/CBO9781139583923 — Textbook covering HTN planning together with acting and execution.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook background on planning and task decomposition.
