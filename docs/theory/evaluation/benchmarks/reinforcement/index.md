---
status: draft
last_reviewed: 2026-10-28
related:
  - engineering/evaluation
  - reference/datasets
  - theory/paradigms/reinforcement-learning
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
aliases:
  - Reinforcement learning benchmarks
  - 強化學習基準
---

# Reinforcement Learning Benchmarks

Reinforcement learning benchmarks are environments in which an agent acts and is scored by the return it collects. Results depend on the environment version, the step limit, the number of random seeds and how episodes are averaged, so these must be reported with the score.

## Overview

A reinforcement learning benchmark is a simulator or game with a fixed reward, an observation format and an action space, plus a protocol for running agents on it. The Arcade Learning Environment (ALE) made Atari 2600 games into such a testbed. Its authors described it as a platform and a methodology for evaluating general agents, with interfaces to hundreds of games, and they reported results on more than 55 of them (Bellemare et al., 2013). Deep Q-Networks were later evaluated on these games, which made ALE a reference point for value-based deep reinforcement learning (Mnih et al., 2015).

Continuous-control benchmarks use physics simulators instead. MuJoCo is a physics engine built for model-based control (Todorov et al., 2012). OpenAI Gym gave many such environments a common interface and a shared place to report results, so that methods could be compared across suites (Brockman et al., 2016).

## Benchmarks compared

| Benchmark | Task | Main metric |
|---|---|---|
| [Arcade Learning Environment](ale.md) | Playing Atari 2600 games from pixels with discrete actions | Game score per game, summarised across games |
| [MuJoCo](mujoco.md) | Controlling simulated bodies with continuous actions | Episode return |

The two differ in what they stress. ALE tests a single agent across many games with discrete choices and sparse rewards. MuJoCo tests smooth, high-dimensional control on a physical model, where the reward is usually written by hand.

## Key concepts

- **Return**: the sum of rewards an agent collects in one episode, often discounted.
- **Environment version**: a specific release of a simulator or game, with its dynamics, wrappers and settings.
- **Seed**: the random number generator setting for one run. Scores over several seeds show the spread that a single run hides.

## How it works

An agent interacts with the environment for a fixed number of steps or until an episode ends. The return of each episode is recorded, averaged over episodes and over seeds, and reported with the environment version and step limit. Later work on ALE gathered methodological best practices for these choices, and reported new benchmark results under them (Machado et al., 2018).

## Common issues

- **Environment versions.** A change to a simulator or a wrapper can change the score, so the version must be recorded. ALE's authors revisited its protocols and introduced sticky actions to add stochasticity to the environment (Machado et al., 2018).
- **Seed variance.** Results vary between random seeds, and non-determinism in standard environments can make reported gains hard to interpret. The spread across seeds should be reported with the mean (Henderson et al., 2017).
- **Simulation gap.** Results in simulation do not guarantee performance on physical hardware.

## Connections

- [Reinforcement learning](../../../paradigms/reinforcement-learning/index.md) is the learning paradigm whose methods these benchmarks compare.
- [Reasoning and agents](../reasoning-agents/index.md) covers agents in text and web settings.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## Open questions

- Whether a suite of games or simulated bodies can rank methods in a way that predicts performance in new tasks.
- How to make seed counts and evaluation budgets standard enough that published gains can be compared directly.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Robotics](../../../../applications/robotics/index.md) describes the physical setting in which simulated control results must eventually be tested.

## References

### Seminal papers

- Bellemare, M. G., Naddaf, Y., Veness, J. & Bowling, M. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research, 47, 253–279. https://doi.org/10.1613/jair.3912 — Introduces the Atari platform and the methodology for comparing agents on it, with results on more than 55 games.
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature, 529–533. https://doi.org/10.1038/nature14236 — Evaluates deep Q-networks across Atari games with the same input and settings.
- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — Describes the physics engine used for simulated control tasks.

### Articles and documentation

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — Describes the common interface and shared benchmark collection that many environments follow.
- Machado, M. C. et al. (2017). *Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents*. arXiv. https://arxiv.org/abs/1709.06009 — Surveys how ALE is evaluated, sets out best practices, and introduces sticky actions.
- Henderson, P. et al. (2017). *Deep Reinforcement Learning that Matters*. arXiv. https://arxiv.org/abs/1709.06560 — Shows how non-determinism and seed variance make reported deep RL results hard to interpret.
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — Free online textbook on reward, return and episodes.
