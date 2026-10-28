---
status: draft
last_reviewed: 2026-10-28
tags:
  - search
  - reasoning
aliases:
  - CDCL
  - Conflict-driven clause learning
  - 衝突驅動子句學習
  - SAT solver
  - SAT 求解器
  - DPLL
  - DPLL(T)
  - SMT
---

# Conflict-Driven Clause Learning (GRASP 1999)

Conflict-driven clause learning (CDCL) is the search method at the heart of modern SAT solvers. It extends the older DPLL procedure by turning each dead end into a new clause, so the same mistake is not repeated. Extended with theory solvers, the same architecture (DPLL(T)) powers SMT solvers. It is one of the three landmark methods on the parent page [Automated Theorem Proving and Formal Mathematics](../index.md).

## Overview

A SAT problem asks whether a propositional formula in conjunctive normal form is satisfiable. The problem is NP-complete, yet practical solvers handle many structured instances from hardware verification and planning.

DPLL, from 1962, searches over partial assignments and backtracks when a clause is violated. Its weakness is that it can rediscover the same conflict in many branches. Marques-Silva and Sakallah's GRASP added two ideas: analyse each conflict to find the decisions responsible, and store the reason as a new clause, then return to the level where that clause becomes useful.[^1]

## Key concepts

- **Decision and propagation**: the solver assigns a value to a variable, called a decision, then uses unit propagation to set every literal forced by a clause whose other literals are false.
- **Decision level**: the number of decisions made so far. Propagated assignments belong to the level of the decision that caused them.
- **Conflict**: a clause whose literals are all false under the current assignment.
- **First unique implication point (1UIP)**: a point in the implication graph at which the conflict's reason can be captured by a single literal on the current decision level. Solvers commonly learn the clause at this point.
- **Non-chronological backjump**: after learning, the solver returns to the second-highest decision level in the learned clause.
- **Restart**: discarding the assignment and searching again, keeping learned clauses.

## How it works

The core loop of a CDCL solver is:

1. Run unit propagation. If a conflict arises, go to step 3.
2. If every variable is assigned, report the formula satisfiable. Otherwise choose an unassigned variable with a heuristic, make a decision on it, and return to step 1.
3. If the decision level is zero, the formula is unsatisfiable. Otherwise analyse the conflict by walking back through the implication graph to the first unique implication point, and derive the learned clause.
4. Add the learned clause to the formula, backjump to the level the clause specifies, and assign its single literal there. Return to step 1.
5. Occasionally restart and delete learned clauses that have proved unhelpful.

The learned clause is itself a consequence of the formula, and it can be derived by a sequence of resolution steps along the implication graph.[^2] CDCL can therefore be read as resolution steered by the search. The [resolution page](../resolution/index.md) gives the rule.

**SMT.** An SMT solver abstracts each atom of a formula to a propositional variable. A theory solver, for example for linear arithmetic, checks whether the chosen literals are consistent and returns a conflict clause when they are not. Nieuwenhuis, Oliveras and Tinelli give an abstract DPLL framework for this lazy approach.[^3] Z3 is a widely used SMT solver.[^4]

## Results

The strongest recent evidence is from Heule, Kullmann and Marek, who settled the Boolean Pythagorean triples problem by cube-and-conquer, a hybrid of look-ahead and CDCL solvers. The run used a cluster of 800 cores for about two days and produced a verified proof.[^5] GRASP's own experiments are in its paper; the figures are not reproduced here.

## Limitations

- **Worst case.** Unless P equals NP, every solver needs exponential time on some families of instances. Learned clauses also accumulate and must be managed.
- **Heuristic dependence.** Performance depends on decision heuristics, restarts and clause deletion, and good settings vary between instance classes.
- **Certificates.** Unsatisfiability proofs can be enormous, as the Pythagorean triples result shows.
- **Theory limits.** SMT solving is only as strong as its theory solvers, and quantified formulas need different machinery.

## Open questions

- **Learned heuristics.** Whether learned models can beat tuned branching heuristics on industrial instances is an open question.
- **Scaling cube-and-conquer.** Splitting a hard problem into many subproblems works on some instances. How to choose the split well in general is open.
- **Trusting solvers.** Certified proofs, such as DRAT proofs, shift trust to a small checker.

## References

### Seminal papers

- Marques-Silva, J. P. & Sakallah, K. A. (1999). *GRASP: a search algorithm for propositional satisfiability*. IEEE Transactions on Computers. https://doi.org/10.1109/12.769433 — Introduces clause learning and non-chronological backtracking, the core of CDCL.
- Davis, M., Logemann, G. & Loveland, D. (1962). *A machine program for theorem-proving*. Communications of the ACM. https://doi.org/10.1145/368273.368557 — Describes the splitting procedure that CDCL extends.
- Nieuwenhuis, R., Oliveras, A. & Tinelli, C. (2006). *Solving SAT and SAT Modulo Theories*. Journal of the ACM. https://doi.org/10.1145/1217856.1217859 — Gives an abstract DPLL framework extended to SMT.
- de Moura, L. & Bjørner, N. (2008). *Z3: An Efficient SMT Solver*. TACAS 2008. https://doi.org/10.1007/978-3-540-78800-3_24 — Presents Z3, an SMT solver designed for efficiency and widely used in verification.

### Surveys and textbooks

- Marques-Silva, J., Lynce, I. & Malik, S. (2021). *Conflict-Driven Clause Learning SAT Solvers*, chapter 4 of the *Handbook of Satisfiability*. IOS Press. https://doi.org/10.3233/FAIA200987 — A handbook chapter on how CDCL solvers learn clauses and manage their search.

### Articles and documentation

- Heule, M. J. H., Kullmann, O. & Marek, V. W. (2016). *Solving and Verifying the boolean Pythagorean Triples problem via Cube-and-Conquer*. arXiv. https://arxiv.org/abs/1605.00723 — Describes a hybrid SAT method, run on a large cluster, that solved an open Ramsey-theory problem with a verified proof.

[^1]: Marques-Silva and Sakallah (1999), listed above.
[^2]: Marques-Silva, Lynce and Malik (2021), listed above.
[^3]: Nieuwenhuis, Oliveras and Tinelli (2006), listed above.
[^4]: de Moura and Bjørner (2008), listed above.
[^5]: Heule, Kullmann and Marek (2016), listed above. The cluster size and running time are as reported in the abstract.
