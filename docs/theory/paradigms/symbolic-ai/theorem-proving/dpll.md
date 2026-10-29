---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/theorem-proving
tags:
  - automated reasoning
  - SAT
  - backtracking
aliases:
  - DPLL
  - DPLL 演算法
  - SAT solving
  - Boolean satisfiability
---

# DPLL

The DPLL procedure decides whether a propositional formula in conjunctive normal form is satisfiable. It searches over truth assignments by backtracking, and it uses unit propagation and pure-literal elimination to prune the search. Part of [Automated theorem proving](index.md).

## Overview

Satisfiability (SAT) is the basic decision problem of propositional logic, and many verification and planning problems reduce to it. A naive search over all assignments takes exponential time in the number of variables. DPLL reduces the search by propagating the consequences of each choice. The procedure is named after Davis, Putnam, Logemann and Loveland, whose papers introduced its ideas in 1960 and 1962.

## Key concepts

- **Conjunctive normal form (CNF)**: a conjunction of clauses, each a disjunction of literals. Each clause is a constraint.
- **Unit clause**: a clause with a single unassigned literal. It forces that literal to be true.
- **Unit propagation**: repeatedly assigning forced literals and simplifying the clauses. A conflict, an empty clause, signals that the current assignment fails.
- **Pure literal**: a literal that appears with only one sign in the remaining clauses. It can be set to true without losing satisfiability.

## How it works

At each node of the search, the procedure does three things.

1. Apply unit propagation until there are no unit clauses left, or a conflict is found.
2. Apply the pure-literal rule, if it is used.
3. If all clauses are satisfied, return satisfiable. If a conflict is found, backtrack. Otherwise pick an unassigned variable, assign it true, and recurse. If that fails, assign it false and recurse.

If no branch leads to a solution, the formula is unsatisfiable. The branching variable choice and the backtracking strategy strongly affect performance. Davis, Logemann and Loveland (1962) proposed the splitting rule, and later work added heuristics for variable choice.

### Animated walkthrough: propagate, conflict, backtrack

![DPLL animation: decide A true, propagate B, detect a conflict, backtrack to A false and satisfy the clauses with C true.](../../../../assets/concept-animations/dpll-backtrack-motion.svg)

[Static backtracking outcome for GitHub](../../../../assets/concept-animations/dpll-backtrack-still.svg)

Consider the illustrative CNF \((\neg A\lor B)\land(\neg A\lor\neg B)\land(A\lor C)\). In this trace the **optional pure-literal rule is not applied**. First decide \(A=\mathrm{true}\). The first clause forces \(B=\mathrm{true}\), while the second requires \(B=\mathrm{false}\), so the branch conflicts. DPLL **backtracks and discards B's branch-local assignment**. With \(A=\mathrm{false}\), the first two clauses are satisfied and the third becomes the unit clause \(C\), forcing \(C=\mathrm{true}\). The result is **SAT**; B can remain unassigned. This is a deliberately small logical example, **not a measured solver trace**, and does not depict CDCL learning or backjumping.

On MkDocs, use **Play/Pause** or keyboard activation; GitHub readers can open the static outcome. This original **CC BY-SA 4.0** illustration follows the DPLL splitting and propagation procedure described by Davis, Logemann and Loveland (1962), cited below.

## Variants

- **Conflict-driven clause learning (CDCL)** analyses each conflict, learns a new clause that prevents the same conflict, and backjumps. Modern SAT solvers are built on it.
- **Restarts** discard the search tree and start again with learned information, which helps against heavy-tailed search times.
- **Watched literals** is a data structure that makes unit propagation fast by inspecting only two literals per clause.

## Results and limits

- The procedure is complete and terminates, since the search tree is finite.
- The worst case is exponential in the number of variables, as expected for an NP-complete problem.
- The gap between worst-case theory and practice is large: modern solvers handle industrial instances with millions of clauses, while random hard instances remain difficult.
- DPLL proves unsatisfiability by exhausting the search, so proofs can be long; proof-producing variants record the resolution steps.

## Applications

- **Hardware and software verification**: checking that circuits and programs satisfy their properties by encoding them in SAT.
- **Planning**: encoding bounded planning problems as SAT instances, so that a solver finds a plan of a given length.
- **Scheduling and configuration**: combinatorial constraints encoded as SAT.

## Open questions

- Why CDCL solvers work so well on structured instances, while failing on random ones, is only partly understood.
- Better variable-selection and learning heuristics can change performance by orders of magnitude, and their design is largely empirical.

## References

### Seminal papers

- Davis, M. & Putnam, H. (1960). A computing procedure for quantification theory. *Journal of the ACM* 7(3), 201–215. https://doi.org/10.1145/321033.321034 — Introduces the resolution-based procedure from which DPLL descends.
- Davis, M., Logemann, G. & Loveland, D. (1962). A machine program for theorem-proving. *Communications of the ACM* 5(7), 394–397. https://doi.org/10.1145/368273.368557 — Gives the backtracking procedure with unit propagation, the DPLL algorithm.
- Robinson, J. A. (1965). A machine-oriented logic based on the resolution principle. *Journal of the ACM* 12(1), 23–41. https://doi.org/10.1145/321250.321253 — Introduces resolution, the rule on which resolution-based proof traces are built.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook account of SAT and the DPLL algorithm.
- de Moura, L. et al. (2015). The Lean theorem prover (system description). In *Automated Deduction — CADE-25*, Lecture Notes in Computer Science, 378–388. https://doi.org/10.1007/978-3-319-21401-6_26 — Describes a prover that combines interactive proof with automation.
- Hales, T. et al. (2017). A formal proof of the Kepler conjecture. *Forum of Mathematics, Pi* 5. https://doi.org/10.1017/fmp.2017.1 — A large formal development that relies on mechanised proof checking.
