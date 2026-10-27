---
related:
- brain-mind/cognitive-architectures
- brain-mind/psychology
- models/agents
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

## Automated planning

- **STRIPS / PDDL**: actions with preconditions and effects; planners find action sequences
- **Hierarchical task networks (HTN)**: decompose high-level tasks
- **Planning under uncertainty**: MDPs, POMDPs
- **Applications**: logistics, space missions (NASA's Remote Agent), game AI, robot task planning

## Automated reasoning and theorem proving

- SAT/SMT solvers (Z3): chip and software verification, scheduling
- Interactive theorem provers: Lean, Coq (Rocq), Isabelle
- **AI for mathematics**: LLMs combined with Lean (AlphaProof reached silver-medal level at IMO 2024; several systems later reached gold-medal level on IMO problems); the Mathlib community formalising mathematics

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

The cognitive-science counterpart is **dual-process theory**: fast, intuitive "System 1" resembles neural networks; slow, deliberate "System 2" resembles symbolic reasoning (see [Psychology & AI](../../brain-mind/psychology/index.md)). Some theorists argue human thought relies on a symbolic "language of thought" (Fodor).

## Resources

- Russell & Norvig, *Artificial Intelligence: A Modern Approach*, chapters 3–11
- [aima-python](https://github.com/aimacode/aima-python) (MIT)
- Microsoft AI-For-Beginners, lesson 2 (symbolic AI)
- Marcus & Davis, *Rebooting AI* (neuro-symbolic perspective)
