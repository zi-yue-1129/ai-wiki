---
related:
- theory/paradigms/meta-learning
- applications/science
---

# Evolutionary & Swarm Intelligence

## Evolutionary computation

Borrow Darwinian evolution: a **population** of candidate solutions undergoes **selection, recombination (crossover) and mutation**, improving **fitness** over generations. No gradients needed — suited to non-differentiable, discrete, multi-modal problems.

| Method | Character | Uses |
|---|---|---|
| Genetic algorithms | Bit-string encoding, crossover + mutation | Scheduling, design optimisation |
| Genetic programming | Evolve tree-shaped programs | Symbolic regression, program synthesis |
| Evolution strategies / CMA-ES | Continuous parameters, adaptive covariance | Continuous optimisation, RL policy search |
| Neuroevolution (NEAT etc.) | Evolve weights and network topology | Game control, early NAS |
| Quality-diversity (MAP-Elites) | Find many diverse good solutions, not just one | Robot gaits, creative generation |
| Open-endedness | Keep producing novel, increasingly complex solutions | POET, artificial life |

### Combining with deep learning

- **Neural architecture search**: evolve or RL-search network designs
- **Evolution strategies as an RL alternative** (Salimans et al., 2017): massively parallel
- **LLM-driven evolution**: an LLM acts as the mutation operator, proposing program variants that automated evaluators filter — FunSearch (2023) found new constructions in combinatorics; AlphaEvolve (2025) improved algorithms and data-centre scheduling
- **Evolutionary model merging**: search over combinations of model weights

## Swarm intelligence

Simple agents interacting locally produce collective intelligence.

| Algorithm | Inspiration | Use |
|---|---|---|
| Ant colony optimisation | Pheromone trails | Routing, travelling salesman |
| Particle swarm optimisation | Bird flocks, fish schools | Continuous optimisation |
| Artificial bee colony | Bee foraging | Optimisation |
| Boids | Three flocking rules (separation, alignment, cohesion) | Animation, drone formations |

## Artificial life and complex systems

- Cellular automata (Conway's Game of Life), Lenia, neural cellular automata
- Self-organisation, emergence, self-replication
- Links to biology: morphogenesis and developmental bioelectricity (Michael Levin's work on "basal cognition")

## Relation to the brain

- Brains are products of evolution: evolution supplies innate structure (inductive bias) and learning fine-tunes it. Zador (2019), "A critique of pure learning", argues much animal behaviour comes from genetically encoded wiring rather than learning from scratch — inspiring "genomic bottleneck" and meta-learning research.
- **Neural Darwinism** (Edelman): selection among neuronal groups.
- **Baldwin effect**: how the capacity to learn can steer evolution.

## Resources

- Eiben & Smith, *Introduction to Evolutionary Computing*
- Stanley & Lehman, *Why Greatness Cannot Be Planned* (open-endedness)
- [DEAP](https://github.com/DEAP/deap), [EvoTorch](https://github.com/nnaisense/evotorch), [pyribs](https://pyribs.org/) (quality-diversity)
