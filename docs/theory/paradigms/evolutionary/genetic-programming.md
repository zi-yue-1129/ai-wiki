---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/symbolic-ai
tags:
  - evolutionary
  - program-synthesis
aliases:
  - Genetic programming
  - GP
  - 遺傳規劃
---

# Genetic Programming

Genetic programming evolves computer programs, usually represented as trees, by applying genetic-algorithm operators to them. Koza (1992) introduced the method for automatically generating programs that solve a stated task. The candidates are expressions rather than fixed-length strings, so the search can find both the structure and the constants of a solution. Part of [Evolutionary & Swarm Intelligence](index.md).

## Overview

A genetic algorithm searches over a fixed encoding. Genetic programming lets the encoding grow: each candidate is a tree of functions and terminals, and its size and shape can change during the search. This makes it suited to symbolic regression, where the goal is an expression that fits data.

## Problem

Writing a program that solves a task usually requires a person to choose its structure in advance. Genetic programming asks whether the structure can be found by search, using test cases to score candidate programs.

## Core idea

A program is a tree. Internal nodes are functions, such as addition or conditionals, and leaves are terminals, such as input variables or constants. Crossover swaps randomly chosen subtrees between two parents, and mutation replaces a subtree with a newly generated one. Fitness is measured by running each program on the test cases.

## Algorithm

1. Build a population of random trees from the function set and the terminal set.
2. Run each tree on the test cases and compute its fitness, such as the error on the data.
3. Select parents by fitness, using tournament or fitness-proportionate selection.
4. Create children by subtree crossover and subtree mutation.
5. Replace the population and repeat until a program meets the success criterion or the budget runs out.

Two conditions on the sets keep the search well-defined. Closure requires every function to accept any value that a terminal or another function can produce. Sufficiency requires the terminal and function sets together to be able to express a solution. Koza (1992) discusses both at length, with examples such as symbolic regression and Boolean function learning.

## Key results

Koza (1992) and the follow-up paper (Koza, 1994) demonstrate that the method can evolve programs for a range of problems defined by test cases. This page does not quote numerical results. Check the papers for the specific problems and figures before citing a performance claim.

## Limitations

- Trees tend to grow without a matching gain in fitness. This phenomenon, called bloat, wastes evaluations and makes the programs hard to read.
- Crossover can break useful subtrees, so the search may need many generations.
- Fitness based on a finite set of test cases can reward programs that fit the cases but do not generalise.
- Evolved programs are difficult to verify, so their correctness on unseen inputs needs separate testing.

## Connections

- [Evolutionary & Swarm Intelligence](index.md) is the overview where genetic programming sits beside the other population methods.
- [Genetic algorithms](genetic-algorithms.md) are the fixed-encoding methods whose operators genetic programming extends to trees.
- [Symbolic AI](../symbolic-ai/index.md) represents knowledge and programs explicitly, which is the representation that genetic programming searches over.
- [NEAT](neat.md) evolves network structure instead of expression trees, using the same population framework.

## Applications

- Symbolic regression, where the output is an interpretable formula fitted to data.
- Automatic design of controllers, filters and circuits, where the task is specified by test cases.

## Open questions

- How can bloat be controlled without limiting the programs that can be found?
- Can genetic programming be combined with learned models so that the search generates programs that generalise beyond their test cases?

## References

### Seminal papers

- Koza, J. R. (1992). *Genetic Programming: On the Programming of Computers by Means of Natural Selection*. MIT Press. https://openlibrary.org/isbn/0262111705 — Introduces tree-based genetic programming, with the closure and sufficiency conditions and the subtree operators.
- Koza, J. R. (1994). Genetic programming as a means for programming computers by natural selection. *Statistics and Computing*, 4(2). https://doi.org/10.1007/bf00175355 — A companion paper that sets out the method and its use for automatic programming.
- Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press. https://doi.org/10.1145/1216504.1216510 — The genetic-algorithm framework that genetic programming extends. The DOI links to a 1975 review of the book.

### Surveys and textbooks

- Eiben, A. E. & Smith, J. E. (2015). *Introduction to Evolutionary Computing*. Springer. https://doi.org/10.1007/978-3-662-44874-8 — Textbook covering the representations and operators that genetic programming uses.
- Bäck, T. (1996). *Evolutionary Algorithms in Theory and Practice*. Oxford University Press. https://doi.org/10.1093/oso/9780195099713.001.0001 — Textbook analysis of population search, including the selection pressure that drives bloat.

## Further learning

Optional pointers for readers who want to go further. These are not references.

- [DEAP](https://github.com/DEAP/deap) includes a genetic programming module with tree-based examples.
