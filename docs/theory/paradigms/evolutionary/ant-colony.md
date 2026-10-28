---
status: complete
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

Dorigo et al. (1996) introduce the Ant System, applied to the travelling salesman problem. This page does not quote numerical results from the paper.

## Limitations

- The method is designed for discrete problems. Continuous variables need a discretisation or a different method.
- Pheromone can converge too quickly on a single route, so variants add limits on pheromone or extra exploration, as in MAX–MIN Ant System (Stützle & Hoos, 2000).
- Performance depends on the choice of heuristic and of the parameters \(\alpha\), \(\beta\) and \(\rho\).

## Connections

- [Evolutionary & Swarm Intelligence](index.md) places ACO among the population methods.
- [Particle swarm optimisation](particle-swarm.md) is the continuous-space swarm method.
- Ant Colony System (Dorigo & Gambardella, 1997) is an early variant that strengthens the preference for the best tour.

## Applications

- Vehicle routing, scheduling and network routing, where good solutions come from a sequence of local choices.

## Open questions

- How should pheromone limits and exploration be set so the colony keeps finding better routes without locking in early?
- How does ACO compare with learned combinatorial solvers on large instances?

## References

### Seminal papers

- Dorigo, M., Maniezzo, V. & Colorni, A. (1996). *Ant system: optimization by a colony of cooperating agents*. IEEE Transactions on Systems, Man, and Cybernetics, Part B, 26, 29–41. https://doi.org/10.1109/3477.484436 — Introduces the Ant System, in which artificial ants build tours guided by pheromone and heuristic values.
- Dorigo, M. & Gambardella, L. M. (1997). *Ant colony system: a cooperative learning approach to the traveling salesman problem*. IEEE Transactions on Evolutionary Computation, 1, 53–66. https://doi.org/10.1109/4235.585892 — Introduces Ant Colony System, a variant with local pheromone updates and a stronger preference for the best tour.
- Stützle, T. & Hoos, H. H. (2000). *MAX–MIN Ant System*. Future Generation Computer Systems, 16, 889–914. https://doi.org/10.1016/S0167-739X(00)00043-1 — Introduces MAX–MIN Ant System, which bounds pheromone levels to limit premature convergence.
- Dorigo, M. & Blum, C. (2005). *Ant colony optimization theory: a survey*. Theoretical Computer Science, 344, 243–278. https://doi.org/10.1016/j.tcs.2005.05.020 — Surveys the theoretical results for ACO.
- Dorigo, M., Birattari, M. & Stützle, T. (2006). *Ant colony optimization: artificial ants as a computational intelligence technique*. IEEE Computational Intelligence Magazine, 1, 28–39. https://doi.org/10.1109/MCI.2006.329691 — Overviews ACO as a computational intelligence technique.

## Further learning

- [Ant colony optimisation on Wikipedia](https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms) gives an overview of the main variants.
