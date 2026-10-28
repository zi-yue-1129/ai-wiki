---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/symbolic-ai/theorem-proving
tags:
  - automated reasoning
  - first-order logic
  - refutation
aliases:
  - 歸結原理
  - 歸結
  - Resolution
  - Resolution principle
---

# Resolution

Resolution is an inference rule that derives a new clause from two clauses containing complementary literals. Refutation with resolution proves a statement by showing that its negation, added to the axioms, leads to the empty clause. Part of [Automated theorem proving](index.md).

## Overview

Logic statements can be converted into a normal form, a set of clauses, each a disjunction of literals. Resolution works on this set. Robinson (1965) showed that a single rule, applied together with unification of variables, is complete for first-order logic: if a set of clauses is unsatisfiable, repeated resolution eventually derives the empty clause. This gave automated provers a single, mechanical inference rule.

## Key concepts

- **Literal and clause**: a literal is an atom or its negation, and a clause is a disjunction of literals. A set of clauses is understood as their conjunction.
- **Complementary literals**: two literals, one the negation of the other, such as \(p\) and \(\neg p\).
- **Unification**: finding a substitution of variables that makes two atoms identical. It lets resolution apply to first-order clauses.
- **Empty clause**: a clause with no literals, which is false. Deriving it proves the set of clauses unsatisfiable.

## How it works

From clauses \(C_1 = A\lor L\) and \(C_2 = B\lor\neg L'\), where \(\sigma\) is the most general unifier of \(L\) and \(L'\), the resolvent is

\[
(A\lor B)\sigma.
\]

Starting from the clauses of the axioms and the negated goal, the prover repeatedly adds resolvents. The proof succeeds when the empty clause is derived. A strategy controls which pairs to resolve. Set-of-support restricts resolution to pairs that involve the negated goal, and linear resolution extends the most recent clause. Both keep the search focused while preserving completeness.

## Variants

- **Factoring** merges literals that are identical after unification within a single clause.
- **Ordered resolution** restricts which literals can be resolved, which reduces the search space.
- **Paramodulation and superposition** add rules for equality, which are needed for many mathematical problems.

## Results and limits

- Resolution with unification is refutation-complete for first-order logic, which is the central result of Robinson (1965).
- The search can grow quickly, because many irrelevant clauses are derived. Strategies control this but do not remove it.
- First-order validity is undecidable in general, so provers may run forever on satisfiable inputs without a proof of satisfiability.
- For propositional problems, resolution is one option, and the DPLL search is often more efficient in practice (Davis, Logemann & Loveland, 1962).

## Applications

- **Logic programming**: Prolog's evaluation is based on a restricted form of resolution.
- **Automated proof search**: many first-order provers implement resolution with search strategies.
- **Knowledge base queries**: answering questions over logical facts by refutation.

## Open questions

- Strategies that reliably find short proofs for large problems are still largely heuristic.
- Combining resolution with learned guidance and with equality reasoning is an active area.

## References

### Seminal papers

- Robinson, J. A. (1965). A machine-oriented logic based on the resolution principle. *Journal of the ACM* 12(1), 23–41. https://doi.org/10.1145/321250.321253 — Introduces resolution with unification and proves its refutation completeness.
- Davis, M. & Putnam, H. (1960). A computing procedure for quantification theory. *Journal of the ACM* 7(3), 201–215. https://doi.org/10.1145/321033.321034 — An early procedure for quantified logic whose propositional core is related to resolution.
- Davis, M., Logemann, G. & Loveland, D. (1962). A machine program for theorem-proving. *Communications of the ACM* 5(7), 394–397. https://doi.org/10.1145/368273.368557 — Gives the backtracking alternative to resolution for propositional problems.

### Surveys and textbooks

- de Moura, L. et al. (2015). The Lean theorem prover (system description). In *Automated Deduction — CADE-25*, Lecture Notes in Computer Science, 378–388. https://doi.org/10.1007/978-3-319-21401-6_26 — Describes a modern prover that combines interactive proof with automation.
- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — Textbook account of resolution and first-order inference.
- Hales, T. et al. (2017). A formal proof of the Kepler conjecture. *Forum of Mathematics, Pi* 5. https://doi.org/10.1017/fmp.2017.1 — A large formal proof that relies on mechanised reasoning of this kind.
