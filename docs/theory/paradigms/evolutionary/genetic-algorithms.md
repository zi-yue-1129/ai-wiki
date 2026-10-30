---
status: draft
last_reviewed: 2026-10-30
related:
  - theory/paradigms/evolutionary
  - theory/optimization/zeroth-order-and-evolutionary.md
tags:
  - evolutionary
  - population-based
aliases:
  - Genetic algorithm
  - GA
  - 遺傳演算法
---

# Genetic Algorithms

A genetic algorithm searches a space of candidate solutions by keeping a population, scoring each member, and producing the next generation by selection, crossover and mutation. Holland (1975) developed the approach and its theory of schemata. Goldberg (1989) made it widely known as a practical method for engineering search. Part of [Evolutionary & Swarm Intelligence](index.md).

## Overview

A genetic algorithm does not need gradients or a smooth objective. It needs a way to encode a candidate, a score for each candidate, and operators that recombine and perturb encodings. The classic form uses fixed-length bit strings, but the same loop works on vectors, permutations and trees.

## Problem

Many design, scheduling and combinatorial problems have objectives that are discrete, noisy or only available by simulation. Local search from one point gets stuck in local optima, and random sampling wastes evaluations. The genetic algorithm asks whether recombining good partial solutions from a population can find better ones faster than either method alone.

## Core idea

Good solutions tend to share useful building blocks. Crossover combines parts of two parents, so a block that works in both can appear in one child. Selection favours fitter candidates, so blocks that improve fitness become more common. Mutation adds new variation so the population does not collapse onto a single pattern.

## Algorithm

1. Initialise a population of random encodings.
2. Evaluate the fitness of each member.
3. Select parents, for example by tournament selection, where fitter candidates win more often.
4. Apply crossover to pairs of parents with probability \(p_c\). For bit strings, this is one-point or uniform crossover.
5. Apply mutation to each child, flipping each bit with probability \(p_m\).
6. Replace the population with the children, keeping the best member if elitism is used, and repeat.

In Holland's schema analysis, a schema \(H\) is a template over bit strings, with some positions fixed and the rest wildcards. Its expected number of copies in the next generation is bounded below by

\[
\mathbb{E}[m(H,t+1)] \ge m(H,t)\,\frac{f(H)}{\bar f}\left[1 - p_c\frac{\delta(H)}{l-1} - p_m\, o(H)\right],
\]

where \(m(H,t)\) is the number of members that match \(H\) at generation \(t\), \(f(H)\) is their mean fitness, \(\bar f\) is the population mean fitness, \(\delta(H)\) is the distance between the outermost fixed positions, \(o(H)\) is the number of fixed positions, and \(l\) is the string length. Short, low-order, above-average schemata grow in the population. This is the schema theorem, and it is the standard explanation of why the method works.

## Key methods

Two landmark variants keep the selection and variation loop but change what the population contains:

- [Genetic programming](genetic-programming.md) (Koza, 1992) evolves program trees instead of fixed-length strings.
- [NEAT](neat.md) (Stanley and Miikkulainen, 2002) evolves network weights and topology together, protecting new structures with speciation.

## Key results

Holland (1975) gives the schema theorem and the analysis of how selection, crossover and mutation affect schemata. Goldberg (1989) presents the operators and applies them to engineering problems. This page does not quote numerical benchmark results, because the claims depend on the problem and encoding. In the architecture-search setting, Real et al. (2019) report that AmoebaNet-A, found by regularised (aging) evolution, reaches a CIFAR-10 test error of 3.34 ± 0.06% with 3.2 M parameters (F = 36), against 3.41% for the NASNet-A baseline. The paper says evolution reached higher accuracy earlier in the search than reinforcement learning did, and that comparison appears only in a figure.

## Limitations

- The schema theorem explains expected behaviour, but it does not guarantee convergence to the global optimum.
- Performance depends heavily on the encoding. A poor representation makes useful building blocks hard to form.
- Premature convergence is common. The population loses diversity and stops exploring unless mutation or niching keeps it varied.
- Each candidate must be evaluated, so the method is expensive when evaluation is costly.

## Connections

- [Evolutionary & Swarm Intelligence](index.md) is the overview where genetic algorithms sit beside the other population methods.
- [Genetic programming](genetic-programming.md) applies the same loop to program trees instead of fixed-length strings.
- [NEAT](neat.md) applies crossover and speciation to neural network topologies.
- [Zeroth-order and evolutionary optimisation](../../optimization/zeroth-order-and-evolutionary.md) covers continuous-parameter methods such as evolution strategies, which use similar selection ideas.

## Applications

- Scheduling and routing, where the candidates are permutations and the cost is computed by a simulator.
- Architecture search, where recent work uses a tournament-based evolutionary loop to choose network designs, as in Real et al. (2019).

## Open questions

- Which building blocks matter for a given problem, and can an encoding be learned rather than designed by hand?
- How much of the schema theory carries over to real problems with noisy, high-dimensional fitness?

## References

### Seminal papers

- Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems*. University of Michigan Press. https://openlibrary.org/isbn/9780262581110 — Introduces schemata and the schema theorem. The linked record is the MIT Press edition of 1992.
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley. https://openlibrary.org/isbn/0201157675 — The standard textbook treatment of the operators, schema analysis and engineering uses.
- Koza, J. R. (1992). *Genetic Programming: On the Programming of Computers by Means of Natural Selection*. MIT Press. https://openlibrary.org/isbn/0262111705 — Introduces genetic programming, which evolves program trees to solve a stated task.
- Stanley, K. O. & Miikkulainen, R. (2002). Evolving Neural Networks through Augmenting Topologies. *Evolutionary Computation*, 10(2), 99–127. https://doi.org/10.1162/106365602320169811 — Introduces NEAT, which evolves weights and topology together, with speciation.
- Real, E., Aggarwal, A., Huang, Y. & Le, Q. V. (2019). Regularized Evolution for Image Classifier Architecture Search. In *Proceedings of the AAAI Conference on Artificial Intelligence*. arXiv:1802.01548. https://arxiv.org/abs/1802.01548 — A modern example of a genetic-style loop, using tournament selection, to search network architectures.

### Surveys and textbooks

- Eiben, A. E. & Smith, J. E. (2015). *Introduction to Evolutionary Computing*. Springer. https://doi.org/10.1007/978-3-662-44874-8 — Textbook covering representations, operators and the convergence behaviour of genetic algorithms.
- Bäck, T. (1996). *Evolutionary Algorithms in Theory and Practice*. Oxford University Press. https://doi.org/10.1093/oso/9780195099713.001.0001 — Textbook analysis of selection pressure and the other design choices in population search.

## Further learning

Optional pointers for readers who want to go further. These are not references.

- [DEAP](https://github.com/DEAP/deap) is an open-source Python framework for building genetic algorithms and related methods.
