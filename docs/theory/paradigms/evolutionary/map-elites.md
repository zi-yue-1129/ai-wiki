---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/evolutionary
  - theory/paradigms/reinforcement-learning
tags:
  - evolutionary
  - quality-diversity
aliases:
  - MAP-Elites
  - Multi-dimensional archive of phenotypic elites
  - 品質多樣性
---

# MAP-Elites

Most evolutionary searches keep one best solution, or a population that converges on one. MAP-Elites instead keeps the best solution found in each cell of a grid. The cells are defined by behavioural descriptors, so the archive holds a repertoire of solutions that differ in how they behave.

## Overview

Part of [Evolutionary & Swarm Intelligence](index.md). The parent page compares it with the other population methods. Its aim is different from optimisation: it fills the archive with many good and different solutions.

## Problem

A single optimum can hide useful alternatives. A robot that has one fast gait may fail when a leg is damaged. A design task may need several solutions that trade off different features. Standard evolution discards any solution that is not the single best, so these alternatives are lost.

## Core idea

Mouret and Clune define a grid over a space of behavioural descriptors. Each candidate is evaluated for both its performance and its descriptor. The candidate goes into the cell that its descriptor selects, and it replaces the cell's occupant only if it performs better. Parents for the next generation are drawn at random from the archive, so every filled cell can produce offspring.

## Algorithm

1. Start with a set of random candidates. Evaluate each for fitness \(f\) and descriptor \(b\).
2. Place each candidate in the cell \(c(b)\). Keep it if the cell is empty or if \(f\) beats the cell's current fitness.
3. Repeat: pick an elite uniformly at random from the archive, mutate it (and optionally recombine it with another elite), evaluate the offspring, and insert it as in step 2.

The archive, not a population, is the output. Its coverage (how many cells are filled) and its best-per-cell values are both reported.

## Key results

Mouret and Clune (2015) apply the method to a simulated hexapod robot. It learns a repertoire of gaits, and when a leg is disabled it finds a working gait from the archive instead of searching from scratch. The paper reports that the approach finds high-performing solutions across the grid and that the archive is useful for recovering from damage. The abstract describes these results in general terms, so the page quotes no numbers from it.

## Limitations

- The grid grows exponentially with the number of descriptor dimensions, so the method is practical only for a small number of descriptors. Vassiliades et al. (2018) use centroidal Voronoi tessellations to scale the archive to larger descriptor spaces.
- Choosing the descriptors is a design decision that shapes the result. Poor descriptors give an archive that covers the grid without covering the useful behaviours.
- Insertion is greedy within each cell, so a cell can keep a locally good solution that is far from the best achievable in that behaviour.

## Connections

- [Evolutionary & Swarm Intelligence](index.md) is the overview that places MAP-Elites next to genetic algorithms and evolution strategies.
- Evolution strategies and CMA-ES ([zeroth-order and evolutionary](../../optimization/zeroth-order-and-evolutionary.md)) optimise a single search distribution, whereas MAP-Elites keeps a diverse archive.
- Quality-diversity methods are surveyed in Pugh et al. (2016). Novelty search (Lehman & Stanley, 2011) is an earlier route to diversity that drops the objective altogether.

## Applications

- Robot control with repertoires that can recover from damage.
- Creative and procedural generation, where many distinct outputs are valued.

## Open questions

- How should the descriptor space be chosen automatically, so the grid covers useful behaviours without manual design?
- How can the archive be used efficiently in high-dimensional descriptor spaces?

## References

### Seminal papers

- Mouret, J.-B. & Clune, J. (2015). *Illuminating search spaces by mapping elites*. arXiv:1504.04909. https://arxiv.org/abs/1504.04909 — Introduces MAP-Elites, which keeps the best solution in each cell of a behaviour grid, and applies it to a damage-recovering hexapod robot.
- Cully, A., Clune, J., Tarapore, D. & Mouret, J.-B. (2015). *Robots that can adapt like animals*. arXiv:1407.3501. https://arxiv.org/abs/1407.3501 — Uses a repertoire of behaviours of the kind MAP-Elites builds, so a damaged hexapod can recover by trying alternatives from the archive.
- Vassiliades, V., Chatzilygeroudis, K. & Mouret, J.-B. (2018). *Using centroidal Voronoi tessellations to scale up the multi-dimensional archive of phenotypic elites algorithm*. arXiv:1610.05729. https://arxiv.org/abs/1610.05729 — Uses centroidal Voronoi tessellations to scale the archive to larger descriptor spaces.
- Pugh, J. K., Soros, L. B. & Stanley, K. O. (2016). *Quality diversity: a new frontier for evolutionary computation*. Frontiers in Robotics and AI. https://doi.org/10.3389/frobt.2016.00040 — Surveys quality-diversity methods, the family that includes MAP-Elites.
- Lehman, J. & Stanley, K. O. (2011). *Abandoning objectives: evolution through the search for novelty alone*. Evolutionary Computation. https://www.cs.swarthmore.edu/~meeden/cs81/f17/papers/lehman_ecj11.pdf — Argues for searching for novelty in place of an objective, an early route to diversity.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

(none checked for this page)

## Further learning

- [pyribs](https://pyribs.org/) is an open-source library implementing MAP-Elites and related quality-diversity algorithms.
