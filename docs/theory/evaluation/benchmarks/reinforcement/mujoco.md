---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# MuJoCo

MuJoCo is a physics engine for simulating articulated bodies and contact, built for model-based control (Todorov et al., 2012). As a benchmark, it is used through continuous-control tasks, such as simulated walkers and arms, that are shipped with common reinforcement learning toolkits (Brockman et al., 2016).

## Task and data

An agent applies continuous torques or forces to a simulated body and is rewarded for progress or for reaching a goal. The simulator supplies the dynamics. The task defines the reward and the rule that ends an episode.

## Protocol and metric

The usual metric is episode return, the sum of rewards over an episode with a fixed step limit, averaged over random seeds. The simulator version, the time step and the reward definition all change the results, so they must be stated.

## What it shows

Continuous-control tasks show how well a method learns smooth, high-dimensional action control. They also allow methods to be compared on the same dynamics.

## Limitations

- **Simulation gap.** Policies that work in simulation may not transfer to physical robots without further work.
- **Reward design.** The task reward is written by hand, so scores reflect the reward as much as the method (Raji et al., 2021).
- **Version drift.** Simulator updates can change the dynamics and make earlier scores hard to reproduce.

## Related

- [Reinforcement overview](index.md) compares the reinforcement benchmarks.
- [Arcade Learning Environment](ale.md) covers discrete-action games.

## References

### Seminal papers

- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — Describes the physics engine and its use for control.

### Articles and documentation

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — Describes the common interface that the continuous-control tasks follow.
- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Free draft explaining reward, return and episodes.

### Additional sources

- Raji, I. D. & Bender, E. M. et al. (2021). *AI and the Everything in the Whole Wide World Benchmark*. arXiv. https://arxiv.org/abs/2111.15366 — Examines construct validity and the limits of broad claims from benchmarks.
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a fixed task is a weak measure of intelligence.
