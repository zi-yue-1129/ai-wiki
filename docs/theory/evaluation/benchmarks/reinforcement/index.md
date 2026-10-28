---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# Reinforcement Learning Benchmarks

Reinforcement learning benchmarks are environments in which an agent acts and is scored by the return it collects. Results depend on the environment version, the step limit, the number of random seeds and how episodes are averaged, so these must be reported with the score.

| Benchmark | Task | Main metric |
|---|---|---|
| [Arcade Learning Environment](ale.md) | Playing Atari 2600 games from pixels with discrete actions | Game score per game, summarised across games |
| [MuJoCo](mujoco.md) | Controlling simulated bodies with continuous actions | Episode return |

## Common issues

- **Environment versions.** A change to a simulator or a wrapper can change the score, so the version must be recorded.
- **Seed variance.** Results vary between random seeds, so the spread across seeds should be reported with the mean.
- **Simulation gap.** Results in simulation do not guarantee performance on physical hardware.

## Related

- [Benchmarks overview](../index.md) lists all families.
- [Reasoning and agents](../reasoning-agents/index.md) covers agents in text and web settings.
- [Protocols](../../protocols/index.md) covers splits and reporting.

## References

### Seminal papers

- Bellemare, M. G. et al. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research 47. https://doi.org/10.1613/jair.3912 — Introduces the Atari platform and the methodology for comparing agents on it.
- Todorov, E., Erez, T. & Tassa, Y. (2012). *MuJoCo: A physics engine for model-based control*. IROS 2012. https://doi.org/10.1109/IROS.2012.6386109 — Describes the physics engine used for simulated control tasks.

### Articles and documentation

- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — Reports deep reinforcement learning agents evaluated on Atari games.
- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — Describes the common interface that many reinforcement learning environments follow.

### Additional sources

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Free draft of the standard textbook on reinforcement learning.
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a fixed task is a weak measure of intelligence.
