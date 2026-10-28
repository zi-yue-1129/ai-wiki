---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai
  - theory/paradigms/symbolic-ai/neuro-symbolic
tags:
  - automated reasoning
  - theorem proving
  - formal mathematics
aliases:
  - 自動定理證明
  - 形式數學
  - Automated theorem proving
  - Formal mathematics
  - Interactive theorem proving
---

# Automated Theorem Proving and Formal Mathematics

Automated theorem proving builds programs that establish whether a logical statement follows from a set of axioms, and it can produce a checkable proof. Formal mathematics extends this by writing mathematics in a precise language that a computer can verify step by step. Part of [Symbolic AI, search and planning](../index.md).

## Overview

A theorem prover decides or searches for a proof in a formal system. Automated provers run without human guidance on a fixed problem, while interactive provers let a person guide the proof and let the computer check each step. Both kinds are used in mathematics, software and hardware verification, and as a source of verified reasoning for AI systems.

## Key concepts

- **Proof**: a finite sequence of steps, each justified by an axiom or an inference rule, that leads to the statement.
- **Refutation**: proving a statement by showing that its negation together with the axioms is unsatisfiable. Most automated provers work this way.
- **Satisfiability (SAT)**: deciding whether a propositional formula has a satisfying assignment. Many proof problems reduce to it.
- **Proof assistant**: an interactive system that checks a formal proof written by a person or a program, and that keeps a library of verified results.

## How it works

Two families are most widely used. Resolution-based provers refute a set of clauses by repeatedly combining clauses to derive new ones, until the empty clause appears. [Resolution](resolution.md) is the basic inference rule of this family (Robinson, 1965). For propositional problems, the [DPLL](dpll.md) procedure decides satisfiability by search with unit propagation and backtracking (Davis, Logemann & Loveland, 1962). Proof assistants such as Lean and Coq express statements in dependent type theory or related logics, and check proofs with a small trusted kernel (de Moura et al., 2015).

## Key methods

- [Resolution](resolution.md): the inference rule behind many first-order provers.
- [DPLL](dpll.md): the backtracking search for SAT, which is the core of modern SAT solvers.

Proof assistants such as Lean are mentioned as systems and are not covered here as methods.

## Connections

- [Search algorithms](../search/index.md) explain the search over proof states that provers use.
- [Neuro-symbolic AI](../neuro-symbolic/index.md) combines logical reasoning with learned models, including attempts to guide proof search with learned components.
- [Knowledge graphs and knowledge representation](../knowledge-graphs/index.md) share the logical formalisms used to state facts.

## Applications

- **Verification of software and hardware**: proving that programs or circuits meet their specifications.
- **Formal mathematics**: verifying major theorems in a proof assistant. Hales et al. (2017) report a complete formal proof of the Kepler conjecture.
- **AI reasoning**: providing a checkable record for logical inference, and testing learned systems on verified tasks.

## Open questions

- Automated provers struggle with problems that need long chains of reasoning or large libraries of lemmas.
- Using learned models to guide proof search is promising, but the learned guidance has to be checked by the prover, which limits what can be gained.
- Formalising large areas of mathematics takes sustained effort, and the cost of translation from informal to formal text remains high.

## References

### Seminal papers

- Robinson, J. A. (1965). A machine-oriented logic based on the resolution principle. *Journal of the ACM* 12(1), 23–41. https://doi.org/10.1145/321250.321253 — Introduces the resolution inference rule for first-order logic.
- Davis, M., Logemann, G. & Loveland, D. (1962). A machine program for theorem-proving. *Communications of the ACM* 5(7), 394–397. https://doi.org/10.1145/368273.368557 — Gives the backtracking procedure that became DPLL.
- Davis, M. & Putnam, H. (1960). A computing procedure for quantification theory. *Journal of the ACM* 7(3), 201–215. https://doi.org/10.1145/321033.321034 — Introduces the procedure that the later DPLL method refines.
- de Moura, L. et al. (2015). The Lean theorem prover (system description). In *Automated Deduction — CADE-25*, Lecture Notes in Computer Science, 378–388. https://doi.org/10.1007/978-3-319-21401-6_26 — Describes the Lean proof assistant.

### Surveys and textbooks

- Hales, T. et al. (2017). A formal proof of the Kepler conjecture. *Forum of Mathematics, Pi* 5. https://doi.org/10.1017/fmp.2017.1 — Reports a complete formal proof of a major theorem in a proof assistant.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook background on logical inference and resolution.
