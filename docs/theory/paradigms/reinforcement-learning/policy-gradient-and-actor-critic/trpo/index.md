---
status: complete
last_reviewed: 2026-10-28
aliases:
  - TRPO
  - 信賴區域策略最佳化
---

# Trust region policy optimisation (Schulman et al., 2015)

A policy-gradient method that maximises a surrogate objective subject to a limit on the average KL divergence between the old and new policies.

## Problem

A large policy-gradient step can cause the policy to collapse, and the surrogate used to estimate the gain holds only near the current policy. Schulman et al. ask how to choose an update that is guaranteed to improve the policy as far as the surrogate says, and that keeps the new policy close to the old one.

## Core idea

TRPO optimises a local surrogate of the expected return, which uses the old state visitation frequencies and the probability ratio between the new and old policies. The surrogate is a good estimate only while the policies are close, so the update is restricted to a trust region. The restriction is an average KL divergence constraint, rather than a stricter maximum-KL constraint, which the paper calls impractical because it imposes too many constraints.

## Equation or algorithm

The practical problem is

\[
\max_\theta\ L_{\theta_{\text{old}}}(\theta) \quad \text{subject to} \quad \bar{D}_{\text{KL}}(\theta_{\text{old}}, \theta) \le \delta
\]

where \(L\) is the surrogate and \(\bar{D}_{\text{KL}}\) is the average KL divergence over visited states. The paper estimates both quantities from samples with importance sampling. Two sampling schemes are given, a single-path method and a vine method. The procedure:

1. Collect trajectories with the current policy \(\pi_{\theta_{\text{old}}}\).
2. Estimate the advantage or action-value terms from those samples.
3. Solve the constrained problem for an update that stays within the KL bound \(\delta\).
4. Set \(\theta_{\text{old}} \leftarrow \theta\) and repeat.

The paper uses \(\delta = 0.01\) in all of its experiments.

## Results

- **Simulated locomotion.** Single-path and vine TRPO are trained on the three MuJoCo tasks, Swimmer, Hopper and Walker. The learning curves are averaged over five runs per algorithm, with random initialisations.
- **Atari.** On seven games (Beam Rider, Breakout, Enduro, Pong, Q\*bert, Seaquest and Space Invaders), the paper states: "While our method only outperformed the prior methods on some of the games, it consistently achieved reasonable scores." On Q\*bert, TRPO-vine scored 7732.5, against 1952 for deep Q-learning and 20025 for UCC-I, which shows the method did not win every game. Each run was done once, so the Atari results carry no error statistics.

## Limitations

- **Complex to implement.** The constrained optimisation and the sampled KL estimate make the method harder to implement and tune than a clipped objective.
- **Not every Atari game.** The paper's own results show that the method was not best on every game.
- **Replaced in practice.** [Proximal Policy Optimisation](../../proximal-policy-optimisation/index.md) keeps the goal of a limited step but replaces the hard constraint with a clipped objective, which is simpler to implement. The PPO paper compares against TRPO in its experiments.

## Connections

- Parent topic: [Policy gradient and actor-critic](../index.md), and the wider [Reinforcement Learning](../../index.md) overview.
- The advantage estimates it uses are the same kind as those in [A3C](../a3c/index.md).
- Its successor is [PPO](../../proximal-policy-optimisation/index.md), and [Deep Q-networks](../../deep-q-networks/index.md) is the value-based comparison for Atari.

## Applications

- **Simulated robot locomotion.** The MuJoCo experiments are the paper's main continuous-control evidence.
- **Atari control from pixels.** The seven-game Atari study shows the method on raw screen input.

## Open questions

- Whether a hard trust region is needed, or a softer penalty suffices, once implementation details are controlled.
- How the KL bound \(\delta\) should be set for tasks other than those in the paper.

## References

### Seminal papers

- Schulman, Levine, Moritz, Jordan & Abbeel (2015), "Trust region policy optimization", *Proceedings of the 31st International Conference on Machine Learning (ICML)*, [arXiv:1502.05477](https://arxiv.org/abs/1502.05477) — The TRPO paper, with the surrogate, the KL constraint and the MuJoCo and Atari results above.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — The simpler clipped method that replaces the constraint.
- Schulman et al. (2016), "High-dimensional continuous control using generalized advantage estimation", [arXiv:1506.02438](https://arxiv.org/abs/1506.02438) — Advantage estimation for the policy-gradient updates that trust-region methods rely on.
- Engstrom et al. (2020), "Implementation matters in deep policy gradients: a case study on PPO and TRPO", [arXiv:2005.12729](https://arxiv.org/abs/2005.12729) — Shows that code-level implementation details strongly affect how PPO and TRPO compare.
- Mnih et al. (2015), "Human-level control through deep reinforcement learning", *Nature* 518, 529–533. https://doi.org/10.1038/nature14236 — The deep value-based baseline on the Atari suite.

### Surveys and textbooks

- Sutton, R. S. & Barto, A. G. *Reinforcement Learning: An Introduction*, 2nd ed. MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html — Background on policy-gradient methods and trust-region ideas in the standard textbook.
