---
status: draft
last_reviewed: 2026-10-28
tags:
  - search
  - reasoning
aliases:
  - 邏輯理論家
  - Logic Theorist
  - 通用問題求解器
  - General Problem Solver
  - GPS
  - 手段－目的分析
  - Means–ends analysis
---

# Logic Theorist and General Problem Solver

The Logic Theorist, written by Allen Newell, J. C. Shaw and Herbert Simon in 1956, proves theorems of symbolic logic by heuristic search. Its successor, the General Problem Solver, applied a similar idea of goal-directed search to problems in general. Both are landmark methods of the [symbolic era](../index.md) and of the wider [symbolic AI](../../../../theory/symbolic-ai/index.md) tradition.

## Overview

By the mid-1950s the idea that a computer could manipulate symbols was not new, but few programs did anything resembling reasoning. Newell and Simon wanted a program whose steps could be read as a problem-solving process, and they chose logic because a proof is an unambiguous target. The Logic Theorist took a set of axioms and previously established theorems and tried to derive a new expression.

Its central move was to avoid trying every possible combination. It ranked the expressions it could generate by heuristics and extended only the most promising ones. The approach was presented around the time of the 1956 Dartmouth workshop. The General Problem Solver generalised the idea to any problem that can be described by a goal, a set of operators and a current state.

## Key concepts

- **Heuristic**: a rule of thumb that estimates how promising a candidate is. Heuristics guide search without guaranteeing success.
- **State space**: the set of states a problem can reach, with operators that move between them. A proof is a path from the axioms to the target expression.
- **Difference**: a feature in which the current state differs from the goal.
- **Means–ends analysis**: the rule that, given a difference, the solver picks an operator known to reduce that kind of difference, and then works on any preconditions the operator needs.
- **Subgoal**: a goal set in order to make an operator applicable. Subgoals can produce further subgoals.

## How it works

The Logic Theorist operates on expressions of propositional logic. It begins with the axioms and the theorems already established, and applies operators such as substitution and detachment to produce new expressions. Candidates are ranked by heuristics that look at how close they are to the target. The chain of operations that reaches the target is the proof.

The general method behind the General Problem Solver is a loop:

1. If the current state matches the goal, stop.
2. Find a difference $D$ between the current state and the goal.
3. Select an operator $O$ known to reduce differences of the kind $D$.
4. If $O$ cannot be applied, set its preconditions as subgoals and solve them first.
5. Apply $O$ and return to step 1.

Each application shrinks the remaining difference. The procedure does not guarantee a shortest path, but it makes progress whenever a suitable operator exists.

## Results

The 1956 paper reports runs of the Logic Theorist on theorems of symbolic logic, and the 1957 paper reports further experiments with the same program and its heuristics. The main claim is that heuristic selection let the program find proofs for many of the theorems it was given without an exhaustive search. Exact counts are not restated here; readers should take them from the papers.

For the General Problem Solver, the 1958 paper argues for the theory mainly through its fit with how people solve problems, rather than through a benchmark score.

## Limitations

- **Combinatorial growth.** Heuristics prune the search, but the number of candidate states still grows rapidly with proof length. These programs worked on small domains and struggled beyond them.
- **Hand-written knowledge.** The operators and heuristics are supplied by the programmer and are not learned, so each new domain needs new engineering.
- **Generality.** Means–ends analysis is domain-independent in form, but real problems need domain knowledge to choose good operators, so the General Problem Solver was narrower in practice than its name suggests.
- **Psychological fidelity.** Claims that the program models human thought are contested, and the fit depends on the task.

## Open questions

- Can the heuristics that guided these programs be learned from data while keeping the properties that made search reliable? The [A\* search](../../../../theory/symbolic-ai/search/a-star/index.md) page discusses that tension for admissible heuristics.
- How much of human problem solving is means–ends search, and how much relies on recognition or stored experience? The [cognitive architectures](../../../../brain-mind/cognitive-architectures/index.md) pages discuss this.
- Systems that search over language-model outputs, such as [Tree of Thoughts](../../../../theory/symbolic-ai/search/tree-of-thoughts/index.md), revive the question of how a generator and a search procedure should be combined.

## References

### Seminal papers

- Newell, A. & Simon, H. A. (1956). The logic theory machine: A complex information processing system. *IEEE Transactions on Information Theory*. https://doi.org/10.1109/TIT.1956.1056797 — The original description of the Logic Theorist, which proves theorems by heuristic search over symbolic expressions.
- Newell, A., Shaw, J. C. & Simon, H. A. (1957). Empirical explorations of the logic theory machine. *Papers presented at the Western Joint Computer Conference*. https://doi.org/10.1145/1455567.1455605 — Follow-up experiments on running the Logic Theorist and on the effect of its heuristics.
- Newell, A., Shaw, J. C. & Simon, H. A. (1958). Elements of a theory of human problem solving. *Psychological Review*. https://doi.org/10.1037/h0048495 — Proposes problem solving as heuristic search in general terms, the theory behind the General Problem Solver.
- Simon, H. A. & Newell, A. (1958). Heuristic problem solving: The next advance in operations research. *Operations Research*. https://doi.org/10.1287/opre.6.1.1 — A position paper arguing that heuristic problem-solving programs should extend the methods of operations research.
- Newell, A. & Simon, H. A. (1976). Computer science as empirical inquiry: Symbols and search. *Communications of the ACM*. https://doi.org/10.1145/360018.360022 — The physical symbol system hypothesis, which frames the Logic Theorist as a symbol-processing system.

### Surveys and textbooks

- Nilsson, N. J. (2009). *The Quest for Artificial Intelligence*. Cambridge University Press. https://doi.org/10.1017/CBO9780511819346 — A history of AI covering the early symbolic programs and the search methods they introduced.
