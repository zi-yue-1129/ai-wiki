---
related:
  - engineering/evaluation
  - reference/datasets
tags:
  - evaluation
  - benchmarks
  - reinforcement-learning
---

# Arcade Learning Environment

The Arcade Learning Environment (ALE) is a platform that runs Atari 2600 games as reinforcement learning tasks, and the benchmark built on it. It was introduced to evaluate general agents across many games through one interface (Bellemare et al., 2013). Deep reinforcement learning results on Atari games were later reported on this benchmark (Mnih et al., 2015).

## Task and data

An agent receives game frames and chooses from a discrete set of joystick actions, aiming to maximise the game score. The original paper reports results on over 55 games (Bellemare et al., 2013). Each game has its own rules and reward structure, so a method must learn each one from its own experience.

## Protocol and metric

The score is the game's own score at the end of an episode, reported per game. Papers normally average over several seeds and summarise across the suite. Details such as frame skip, action set and episode length change the result, so they must be stated.

## What it shows

It shows how one general method performs across many different games with the same input format. Its results describe game play, not general intelligence.

## Limitations

- **Deterministic setup.** The original setup was deterministic, which allows an agent to exploit a fixed sequence of actions.
- **Scale differences.** Raw scores differ in scale between games, so summaries across games need normalisation, and papers treat this differently.
- **Narrow domain.** Atari games are discrete and visual, so they do not represent robotics or language tasks.

## Related

- [Reinforcement overview](index.md) compares the reinforcement benchmarks.
- [MuJoCo](mujoco.md) covers continuous control.

## References

### Seminal papers

- Bellemare, M. G. et al. (2013). *The Arcade Learning Environment: An Evaluation Platform for General Agents*. Journal of Artificial Intelligence Research 47. https://doi.org/10.1613/jair.3912 — Introduces the platform, the games and the evaluation method.
- Mnih, V. et al. (2015). *Human-level control through deep reinforcement learning*. Nature. https://doi.org/10.1038/nature14236 — Reports deep reinforcement learning agents evaluated on Atari games.

### Articles and documentation

- Brockman, G. et al. (2016). *OpenAI Gym*. arXiv. https://arxiv.org/abs/1606.01540 — Describes the common interface that many reinforcement learning environments follow.

### Additional sources

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Free draft of the standard textbook on reinforcement learning.
- Chollet, F. (2019). *On the Measure of Intelligence*. arXiv. https://arxiv.org/abs/1911.01547 — Argues that skill on a fixed task is a weak measure of intelligence.
