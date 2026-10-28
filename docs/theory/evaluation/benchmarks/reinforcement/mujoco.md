---
status: complete
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
  - MuJoCo
  - MuJoCo 物理引擎
---

# MuJoCo

MuJoCo is a physics engine for simulating articulated bodies and contact, built for model-based control (Todorov et al., 2012). As a benchmark, it is used through continuous-control tasks, such as simulated walkers and arms. Gym's 2D and 3D robot tasks run on MuJoCo (Brockman et al., 2016).

## Overview

MuJoCo was built as a physics engine for model-based control, so that control methods for robots and other articulated bodies could be developed and tested in simulation. Model-based control means the controller can use a model of the body's dynamics (Todorov et al., 2012). When it is used as a benchmark, the body and its task are fixed, and the learning algorithm must find a controller from interaction alone.

## Task and data

An agent applies continuous torques or forces to a simulated body at each step and receives an observation of its joint positions and velocities. The reward is designed for the task, typically a combination of progress toward a goal and a penalty for effort. The simulator supplies the dynamics. The task defines the reward and the rule that ends an episode.

## Protocol and metric

The usual metric is episode return, the sum of rewards over an episode with a fixed step limit, averaged over random seeds. Reporting the mean alone hides the spread between seeds, so the spread should be reported too. The simulator version, the time step and the reward definition all change the results, so they must be stated.

## Key concepts

- **Articulated body**: a set of rigid links joined by joints, such as a walker or a robot arm.
- **Continuous control**: actions are real-valued torques or forces, not a choice among discrete moves.
- **Model-based control**: a controller that uses a model of the body's dynamics, the purpose for which MuJoCo was designed.

## What it shows

Continuous-control tasks show how well a method learns smooth, high-dimensional action control. They also allow methods to be compared on the same dynamics, which is harder with physical robots, where each trial takes real time and wears hardware. A score on one fixed simulated task, however, says little beyond that task (Raji et al., 2021).

## Limitations

- **Simulation gap.** Policies that work in simulation may not transfer to physical robots without further work.
- **Reward design.** The task reward is written by hand, so a score reflects the reward as much as the learning method.
- **Version drift.** Simulator updates can change the dynamics and make earlier scores hard to reproduce.
- **Seed variance.** Results can differ widely between seeds, so single-run comparisons are weak evidence (Henderson et al., 2017).

## Connections

- [Robotics](../../../../applications/robotics/index.md) describes the physical robots that simulated control results must eventually be tested on.
- [Reinforcement learning](../../../paradigms/reinforcement-learning/index.md) describes the methods that learn these controllers.

## Related

- [Reinforcement overview](index.md) compares the reinforcement benchmarks.
- [Arcade Learning Environment](ale.md) covers discrete-action games.

## References

### Seminal papers

- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — Describes the physics engine and its use for control.

### Articles and documentation

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — Describes the common interface and shared benchmark collection that many continuous-control suites follow.
- Henderson, P. et al. (2017). *Deep Reinforcement Learning that Matters*. arXiv. https://arxiv.org/abs/1709.06560 — Shows how seed variance and non-determinism make single-run comparisons hard to interpret.
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press. http://incompleteideas.net/book/the-book-2nd.html — Free online textbook explaining reward, return and episodes.
- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
