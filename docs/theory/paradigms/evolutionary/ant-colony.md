---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/symbolic-ai
tags:
  - swarm
  - combinatorial
  - optimisation
aliases:
  - Ant colony optimisation
  - ACO
  - 螞蟻演算法
---

# Ant Colony Optimisation

Ant colony optimisation (ACO) solves discrete problems, such as finding short routes, with a colony of artificial ants. Ants build solutions step by step, and the paths that lead to good solutions receive more pheromone, which makes later ants more likely to follow them.

## Overview

Part of [Evolutionary & Swarm Intelligence](index.md). The parent page compares ACO with the continuous swarm method [particle swarm optimisation](particle-swarm.md) and with the genetic methods.

## Problem

Combinatorial problems such as the travelling salesman problem have too many candidate routes to enumerate. A method is needed that builds good solutions from simple local decisions and shares information between attempts without a central planner.

## Core idea

Dorigo, Maniezzo and Colorni (1996) take the stigmergy of real ants: they lay pheromone on the paths they use, and other ants prefer paths with more pheromone. In the artificial version, each ant builds a tour by choosing the next city with probability that depends on the pheromone on the edge and a heuristic value (for the travelling salesman problem, the inverse distance). After all ants have built tours, pheromone evaporates everywhere and is reinforced on the edges of the shorter tours.

## Algorithm

For an ant at city \(i\) choosing among unvisited cities \(j\), the probability is

\[
p_{ij} = \frac{\tau_{ij}^{\alpha}\, \eta_{ij}^{\beta}}{\sum_{k \in \mathcal{N}_i} \tau_{ik}^{\alpha}\, \eta_{ik}^{\beta}},
\]

where \(\tau_{ij}\) is the pheromone on the edge, \(\eta_{ij}\) is the heuristic value, \(\alpha\) and \(\beta\) weight them, and \(\mathcal{N}_i\) is the set of unvisited neighbours. After each iteration, pheromone is updated as \(\tau_{ij} \leftarrow (1-\rho)\,\tau_{ij} + \Delta\tau_{ij}\), where \(\rho\) is the evaporation rate and \(\Delta\tau_{ij}\) is the amount deposited by ants whose tours use edge \((i,j)\).

## Key results

Dorigo et al. (1996) introduce the Ant System for the travelling salesman problem. This page does not quote any results from the paper, since the abstract was not checked against the full text.

## Limitations

- The method is designed for discrete problems. Continuous variables need a discretisation or a different method.
- Pheromone can converge too quickly on a single route, so variants add limits on pheromone or extra exploration.
- Performance depends on the choice of heuristic and of the parameters \(\alpha\), \(\beta\) and \(\rho\).

## Connections

- [Evolutionary & Swarm Intelligence](index.md) places ACO among the population methods.
- [Particle swarm optimisation](particle-swarm.md) is the continuous-space swarm method.

## Applications

- Vehicle routing, scheduling and network routing, where good solutions come from a sequence of local choices.

## Open questions

- How should pheromone limits and exploration be set so the colony keeps finding better routes without locking in early?
- How does ACO compare with learned combinatorial solvers on large instances?

## References

### Seminal papers

- Dorigo, M., Maniezzo, V. & Colorni, A. (1996). *Ant system: optimization by a colony of cooperating agents*. IEEE Transactions on Systems, Man, and Cybernetics, Part B. https://doi.org/10.1109/3477.484436 — Introduces the Ant System, in which artificial ants build tours guided by pheromone and heuristic values.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)

## Further learning

- [Ant colony optimisation on Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) gives an overview of the main variants.
