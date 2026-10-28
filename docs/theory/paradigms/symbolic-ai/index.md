---
related:
- brain-mind/cognitive-architectures
- brain-mind/psychology
- theory/models/agents
- applications/science
---

# Symbolic AI, Search & Planning

## What is symbolic AI?

"Good old-fashioned AI" (GOFAI): represent knowledge as explicit **symbols** (concepts, rules, logical formulas) and manipulate them by **inference**. Newell and Simon's **physical symbol system hypothesis** (1976) held that a symbol system is necessary and sufficient for general intelligent action.

## Knowledge representation

| Method | Description | Example |
|---|---|---|
| Propositional and first-order logic | Facts and rules as logical formulas | ∀x Human(x) → Mortal(x) |
| Production rules | IF–THEN rules | MYCIN expert system |
| Semantic networks and frames | Concept nodes and relations | Minsky's frames |
| Description logics and ontologies | Rigorous concept hierarchies | OWL, SNOMED CT, Gene Ontology |
| Knowledge graphs | (entity, relation, entity) triples | Wikidata, Google Knowledge Graph |
| Commonsense knowledge bases | Everyday knowledge | Cyc, ConceptNet, ATOMIC |

Detailed pages: [Knowledge graphs and knowledge representation](knowledge-graphs/index.md), with [TransE](knowledge-graphs/transe.md).

## Search

| Kind | Algorithms | Use |
|---|---|---|
| Uninformed | BFS, DFS, iterative deepening, uniform cost | Basics |
| Heuristic | Greedy best-first, A*, IDA* | Path planning, navigation |
| Adversarial | Minimax, α–β pruning | Chess (Deep Blue) |
| Monte Carlo tree search | Random rollouts + UCT | Go (AlphaGo) |
| Local search | Hill climbing, simulated annealing, tabu search | Scheduling, combinatorial optimisation |
| Constraint satisfaction | Backtracking, arc consistency | Sudoku, timetabling |

A* uses \( f(n) = g(n) + h(n) \); with an admissible heuristic \(h\) (never overestimates), A* is optimal.

Detailed pages: [Search algorithms](search/index.md), with [A\* search](search/a-star.md), [alpha–beta pruning](search/alpha-beta-pruning.md) and [Monte Carlo tree search](search/monte-carlo-tree-search.md).

## Automated planning

- **STRIPS / PDDL**: actions with preconditions and effects; planners find action sequences
- **Hierarchical task networks (HTN)**: decompose high-level tasks
- **Planning under uncertainty**: MDPs, POMDPs
- **Applications**: logistics, space missions (NASA's Remote Agent), game AI, robot task planning

Detailed pages: [Automated planning](planning/index.md), with [STRIPS](planning/strips.md) and [GraphPlan](planning/graphplan.md).

## Automated reasoning and theorem proving

- SAT/SMT solvers (Z3): chip and software verification, scheduling
- Interactive theorem provers: Lean, Coq (Rocq), Isabelle
- **AI for mathematics**: LLMs combined with Lean (AlphaProof reached silver-medal level at IMO 2024; several systems later reached gold-medal level on IMO problems); the Mathlib community formalising mathematics

Detailed pages: [Automated theorem proving and formal mathematics](theorem-proving/index.md), with [resolution](theorem-proving/resolution.md) and [DPLL](theorem-proving/dpll.md).

## Strengths and weaknesses

| Strengths | Weaknesses |
|---|---|
| Interpretable, verifiable | Knowledge-acquisition bottleneck |
| Precise multi-step reasoning | Struggles with uncertainty and vagueness |
| Works with little data | Perception (vision, speech) is hard |
| Hard constraints are easy to add | Brittle outside its rules |

## Neuro-symbolic AI

Combine neural networks' perception and learning with symbolic reasoning and interpretability:

- **Neural networks + search**: AlphaGo, AlphaZero
- **LLMs + tools**: LLMs write code or call solvers, calculators, databases (see [AI Agents](../../models/agents/index.md))
- **LLMs + formal verification**: generating Lean proofs; program synthesis checked by tests
- **Differentiable logic**: logic tensor networks, ∂ILP
- **Program induction**: DreamCoder learns reusable program libraries from examples
- **Knowledge graphs + LLMs**: GraphRAG

The cognitive-science counterpart is **dual-process theory**: fast, intuitive "System 1" resembles neural networks; slow, deliberate "System 2" resembles symbolic reasoning (see [Psychology & AI](../../../brain-mind/psychology/index.md)). Some theorists argue human thought relies on a symbolic "language of thought" (Fodor).

Detailed pages: [Neuro-symbolic AI](neuro-symbolic/index.md), with [Markov logic networks](neuro-symbolic/markov-logic-networks.md).

## Resources

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*, chapters 3–11
- [aima-python](https://github.com/aimacode/aima-python) (MIT)
- Microsoft AI-For-Beginners, lesson 2 (symbolic AI)
- Marcus & Davis, *Rebooting AI* (neuro-symbolic perspective)

## References

### Seminal papers

- Garcez, A. d'Avila, & Lamb, L. C. (2020). *Neurosymbolic AI: The 3rd Wave*. arXiv. https://arxiv.org/abs/2012.05876 — An overview arguing that combining learned representations with symbolic reasoning is the next major phase of AI.
- Lake, B. M., et al. (2016). *Building Machines That Learn and Think Like People*. arXiv. https://arxiv.org/abs/1604.00289 — Argues that human-like learning needs intuitive theories, compositionality and causal models, and shows where pattern-matching systems fall short.

### Surveys and textbooks

- Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*, 4th ed. Pearson. http://aima.cs.berkeley.edu/ — The standard AI textbook, covering search, logic, planning and learning; the companion site offers free slides and code.

### Lectures and videos

- Winston, P. H. *6.034 Artificial Intelligence*. MIT OpenCourseWare, Fall 2010. https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/ — Recorded MIT lectures on knowledge representation, search and rule-based systems, the core of classical symbolic AI.

### Articles and documentation

- Marcus, G. (2020). *The Next Decade in AI: Four Steps Towards Robust Artificial Intelligence*. arXiv. https://arxiv.org/abs/2002.06177 — A critique of purely statistical AI and a proposal for hybrid systems that include structured knowledge.
