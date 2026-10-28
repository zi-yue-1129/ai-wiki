---
status: draft
last_reviewed: 2026-10-28
tags:
  - reasoning
  - search
aliases:
  - Resolution
  - Resolution principle
  - 歸結
  - 歸結原理
  - Robinson resolution
---

# Resolution (Robinson 1965)

Resolution is an inference rule on clauses, introduced by John Alan Robinson in 1965. A prover adds the negation of a conjecture to a set of clauses and repeatedly combines clauses until it derives a contradiction. It is the classic method of automated first-order theorem proving. It is one of the three landmark methods described on the parent page [Automated Theorem Proving and Formal Mathematics](../index.md).

## Overview

Statements can be written in many logical forms. Resolution works on one standard form, the clause, and uses a single inference rule, so a program can apply it without grasping the meaning of the statement. Robinson's contribution was to combine the rule with unification, so that general patterns match particular terms during the search.

Davis and Putnam had earlier built a procedure for testing validity by computer that used resolution on instances of the formula. Later work replaced much of that with splitting, which led to the modern SAT solver.[^1]

## Key concepts

- **Literal**: an atomic formula or its negation, such as $P(x)$ or $\neg P(f(y))$.
- **Clause**: a disjunction of literals. A set of clauses represents a conjunction, and the set is contradictory if no assignment satisfies all of them.
- **Unifier**: a substitution $\sigma$ that makes two terms identical. The most general unifier, written mgu, is the one that imposes the fewest constraints.
- **Resolvent**: the clause produced from two clauses that contain complementary literals, after applying the unifier.
- **Empty clause**: the clause with no literals, which is always false. Deriving it shows that the clause set is unsatisfiable.

## How it works

The resolution rule takes two clauses that contain literals $L$ and $\neg M$ whose atoms unify, and produces their resolvent:

$$
\frac{C \lor L \qquad D \lor \neg M}{(C \lor D)\sigma}, \qquad \sigma = \mathrm{mgu}(L, M).
$$

To prove a conjecture $\varphi$, the prover checks that the set of clauses for $\neg\varphi$ together with the background axioms is unsatisfiable. The standard procedure is a saturation loop:

1. Convert the axioms and the negated conjecture to clause normal form, removing quantifiers by Skolemisation.
2. Select a pair of clauses that contains complementary literals with a unifier.
3. Add their resolvent to the set, unless it is trivially redundant.
4. If the empty clause appears, stop: the conjecture is proved.
5. If no new clauses can be generated, the set is satisfiable and the conjecture is not valid. Otherwise repeat from step 2, subject to a resource bound.

Refinements limit the blow-up. Set-of-support strategies require one parent of every step to descend from the negated conjecture, and ordering restrictions limit which literals may be resolved. Refutation completeness, the guarantee that an unsatisfiable set always yields the empty clause, is retained in standard forms of the rule.

## Results

Robinson's 1965 paper establishes the rule and its completeness by proof rather than by benchmark. Its significance is therefore theoretical: it gave automated first-order proof search a sound and complete basis. Davis, Logemann and Loveland's 1962 paper discusses the programming of their procedure, its trial runs and possible improvements. Their procedure replaced resolution with splitting and became the ancestor of the solvers discussed on the [CDCL page](../cdcl-sat/index.md). The exact figures on how each program performed are in those papers and are not repeated here.

## Limitations

- **Combinatorial growth.** Unrestricted resolution generates many redundant clauses. Each step can make the set larger, so memory and time grow quickly.
- **Non-termination.** For first-order logic, the saturation loop may run forever on a satisfiable set. The problem is only semi-decidable, so a prover can give no answer.
- **No built-in arithmetic.** Numbers and other theories must be encoded as clauses, which is inefficient.

## Open questions

- **Which clauses to keep?** Modern first-order provers still depend on heuristics for clause selection. Learned selection has been studied: Kaliszyk and colleagues used reinforcement learning to guide proof search in a connection-style prover.[^2]
- **Combining with SAT and SMT.** Ground parts of a problem are often better handled by a SAT or SMT solver. How to split work between the two is an engineering question with no fixed answer.
- **Human proof style.** Resolution proofs are rarely readable as mathematics. Whether machine proofs can be translated into human-style arguments remains open.

## References

### Seminal papers

- Robinson, J. A. (1965). *A Machine-Oriented Logic Based on the Resolution Principle*. Journal of the ACM. https://doi.org/10.1145/321250.321253 — Introduces the resolution principle with unification and proves its refutation completeness.
- Davis, M. & Putnam, H. (1960). *A Computing Procedure for Quantification Theory*. Journal of the ACM. https://doi.org/10.1145/321033.321034 — Proposes an early computer procedure for testing validity in logic.
- Davis, M., Logemann, G. & Loveland, D. (1962). *A machine program for theorem-proving*. Communications of the ACM. https://doi.org/10.1145/368273.368557 — Describes the splitting procedure that replaced much of resolution in later provers.

### Surveys and textbooks

- Marques-Silva, J., Lynce, I. & Malik, S. (2021). *Conflict-Driven Clause Learning SAT Solvers*, chapter 4 of the *Handbook of Satisfiability*. IOS Press. https://doi.org/10.3233/FAIA200987 — Traces the line of solvers that descend from the DPLL procedure.
- Yang, K. et al. (2024). *Formal Mathematical Reasoning: A New Frontier in AI*. arXiv. https://arxiv.org/abs/2412.16075 — A survey placing resolution-based and later proof methods in the context of formal reasoning.

### Articles and documentation

- Kaliszyk, C., Urban, J., Michalewski, H. & Olšák, M. (2018). *Reinforcement Learning of Theorem Proving*. arXiv. https://arxiv.org/abs/1805.07563 — Guides proof search in a connection-style prover with reinforcement learning.
- Fikes, R. E. & Nilsson, N. J. (1971). *STRIPS: A new approach to the application of theorem proving to problem solving*. Artificial Intelligence. https://doi.org/10.1016/0004-3702(71)90010-5 — Shows how theorem proving was applied to planning, the origin of the STRIPS formalism.

[^1]: Davis and Putnam (1960), and Davis, Logemann and Loveland (1962), listed above.
[^2]: Kaliszyk et al. (2018), listed above.
