---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/meta-learning
  - theory/optimization/zeroth-order-and-evolutionary
  - applications/science
tags:
  - evolutionary
  - swarm
  - population-based
aliases:
  - Evolutionary computation
  - Swarm intelligence
  - Population-based search
  - 演化計算
  - 群體智慧
---

# Evolutionary & Swarm Intelligence

Some search problems have no gradient to follow: the objective is discrete, multi-modal, or only available by running a simulator. Evolutionary and swarm methods handle these by keeping a **population** of candidate solutions, scoring each one, and building the next population from the best. The population, not a single point, carries the search.

## Overview

Part of the [Paradigms](../index.md) folder. Each method has its own page, and this one compares them. The zeroth-order methods that estimate gradients from function values (evolution strategies and CMA-ES) are treated in [Zeroth-Order and Evolutionary Optimisation](../../optimization/zeroth-order-and-evolutionary.md), and are only summarised here.

## Key methods

| Method | Population update | Typical use | Page |
|---|---|---|---|
| Genetic algorithms | Selection, crossover and mutation on bit strings or vectors | Scheduling, design | Planned |
| Genetic programming | Crossover and mutation on program trees | Symbolic regression | Planned |
| Evolution strategies and CMA-ES | Sample a Gaussian, move its mean and covariance toward good samples | Continuous black-box optimisation | [Zeroth-order and evolutionary](../../optimization/zeroth-order-and-evolutionary.md) |
| NEAT | Evolve weights and topology together, with innovation numbers | Neuroevolution, control | [NEAT](neat.md) |
| MAP-Elites | Keep the best solution in each cell of a behaviour grid | Diverse solutions, robot repertoires | [MAP-Elites](map-elites.md) |
| Particle swarm optimisation | Each particle moves by its own and its neighbours' best positions | Continuous optimisation | [Particle swarm](particle-swarm.md) |
| Ant colony optimisation | Ants deposit pheromone on good paths; paths are sampled in proportion | Combinatorial routing | [Ant colony](ant-colony.md) |

## Key concepts

- **Fitness:** a score for each candidate, computed by running the objective. Nothing is differentiated.
- **Variation:** new candidates come from recombining and perturbing existing ones. Crossover mixes parents; mutation adds noise.
- **Selection pressure:** how strongly the best candidates are favoured. Too much pressure loses diversity; too little makes the search drift.
- **Diversity:** a population that has converged to one point can no longer explore. Niching, speciation and quality-diversity methods keep several solutions alive at once.

## Combining with deep learning

- **Neural architecture search:** a population of network designs is evolved, and each is scored by training it. This is expensive, so later work shares weights between candidates.
- **Evolution strategies as a reinforcement-learning alternative:** Salimans et al. (2017) show that a simple evolution-strategy estimator can train policies at scale across many parallel workers, without backpropagating through the environment.
- **LLM-driven search:** a language model proposes new candidates and an automatic evaluator scores them. FunSearch (Romera-Paredes et al., 2023) uses this to search for programs that construct new mathematical objects. AlphaEvolve (Novikov et al., 2025) applies the same pattern to algorithm discovery.

## Swarm intelligence

Swarm methods use simple agents that interact locally and produce a useful collective result. Particle swarm optimisation and ant colony optimisation are the two methods here with their own pages. Boids, a flocking model from computer graphics, is an early example of the same principle and is not treated further.

## Relation to the brain

Evolution shapes innate structure, and learning tunes it. Zador (2019) argues that much of animal behaviour comes from wiring specified by the genome rather than from learning from scratch. This view motivates work on meta-learning and on the inductive biases that a learner starts with. See [Meta-learning](../meta-learning/index.md).

## Limitations

- Evaluations are expensive. Each candidate usually needs a full run of the objective, so population methods need many more evaluations than gradient methods on smooth problems.
- Results depend on encodings and operators. The same problem can be easy or hard depending on how candidates are represented.
- Convergence guarantees are weak for most of these methods. Their success is usually shown empirically.

## Open issues

- **Scaling with learned variation.** LLM-driven operators make the mutation step much richer, but the evaluators need to be cheap and reliable.
- **Open-endedness.** Whether a search can keep producing novel, increasingly complex solutions without a fixed objective remains unresolved.

## References

### Seminal papers

- Salimans, T., Ho, J., Chen, X., Sidor, S. & Sutskever, I. (2017). *Evolution Strategies as a Scalable Alternative to Reinforcement Learning*. arXiv:1703.03864. https://arxiv.org/abs/1703.03864 — Shows that an evolution-strategy estimator can train policies at scale across many parallel workers.
- Romera-Paredes, B., et al. (2023). *Mathematical discoveries from program search with large language models*. Nature. https://doi.org/10.1038/s41586-023-06924-6 — Pairs a language model with an automatic evaluator to search for programs that construct new mathematical objects.
- Mouret, J.-B. & Clune, J. (2015). *Illuminating search spaces by mapping elites*. arXiv:1504.04909. https://arxiv.org/abs/1504.04909 — Introduces MAP-Elites, which keeps the best solution in each cell of a behaviour grid.

### Surveys and textbooks

(none checked for this page)

### Lectures and videos

(none checked for this page)

### Articles and documentation

- Novikov, A., et al. (2025). *AlphaEvolve: A coding agent for scientific and algorithmic discovery*. arXiv:2506.13131. https://arxiv.org/abs/2506.13131 — A language-model coding agent that evolves programs against automatic evaluators for scientific and algorithmic problems.
- Zador, A. M. (2019). *A critique of pure learning and what artificial neural networks can learn from animal brains*. Nature Communications. https://pmc.ncbi.nlm.nih.gov/articles/PMC6704116 — Argues that much animal behaviour comes from genetically encoded structure rather than learning from scratch.

## Further learning

- [DEAP](https://github.com/DEAP/deap), [EvoTorch](https://github.com/nnaisense/evotorch) and [pyribs](https://pyribs.org/) are open-source libraries for evolutionary and quality-diversity search.
