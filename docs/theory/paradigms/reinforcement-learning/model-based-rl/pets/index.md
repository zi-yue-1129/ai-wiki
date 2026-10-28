---
status: complete
last_reviewed: 2026-10-28
aliases:
  - PETS
  - Probabilistic ensembles with trajectory sampling
---

# Probabilistic ensembles with trajectory sampling (Chua et al., 2018)

A model-based method that learns an ensemble of probabilistic neural-network dynamics models, and plans with them by sampling trajectories. The ensemble represents uncertainty about the model, and the sampling propagates that uncertainty through planning.

## Problem

Model-based reinforcement learning is sample efficient, but with high-capacity neural networks it often reaches lower asymptotic performance than the best model-free methods. Chua et al. ask how to close this gap. They study models that report their own uncertainty, so that planning does not trust a model where the data are sparse.

## Core idea

PETS has two components:

- **Probabilistic ensemble.** Each model in the ensemble predicts a distribution over the next state rather than a single point. The ensemble captures two kinds of uncertainty: the aleatoric noise in each prediction, and the epistemic uncertainty from limited data.
- **Trajectory sampling.** To choose actions, the method samples several particles from the ensemble, propagates each particle forward through the model for the planning horizon, and selects the action sequence that scores best on average. The sampling keeps the uncertainty of the models in the plan, instead of collapsing it to the mean prediction.

The agent re-plans at every step (model-predictive control), and it uses only the first action of the chosen sequence.

## Equation or algorithm

For each planning step, the agent:

1. Fits the probabilistic ensemble to the data collected so far.
2. Optimises a sequence of actions over the horizon \(H\) with the cross-entropy method. For each candidate sequence, particles are propagated through the ensemble over the horizon, with each particle using a randomly chosen ensemble member.
3. Scores each candidate by the predicted sum of rewards, averaged over particles, and keeps the best sequence.
4. Executes the first action, observes the next state, adds the data, and repeats.

The method does not learn a policy from imagined data. It plans directly with the model at each step.

## Results

The abstract reports that PETS "matches the asymptotic performance of model-free algorithms on several challenging benchmark tasks, while requiring significantly fewer samples". On the half-cheetah task, the authors report that PETS needs 8 times fewer samples than soft actor-critic and 125 times fewer samples than proximal policy optimisation.

## Limitations

- **Planning cost.** Sampling trajectories at every step is more expensive in computation than running a learned policy.
- **Model class.** The results depend on the ensemble's architecture and on how the uncertainty is represented.
- **Benchmarks.** The experiments are on continuous-control tasks, so their transfer to other settings is not shown.

## Connections

- Parent topic: [Model-based RL](../index.md).
- The planning idea relates to model-predictive control, which the parent page lists as a main approach.
- [MBPO](../mbpo/index.md) uses a similar ensemble but trains a policy with a model-free learner, instead of planning at each step.
- The baselines in the paper are [soft actor-critic](../../policy-gradient-and-actor-critic/sac/index.md) and [PPO](../../proximal-policy-optimisation/index.md).

## Applications

- **Robot control** where few real trials are possible.
- **Continuous-control benchmarks**, such as half-cheetah, where sample efficiency is the main comparison.

## Open questions

- How to make planning cheap enough for large observation spaces.
- How to combine planning with learned policies, so that compute can be traded off at run time.

## References

### Seminal papers

- Chua, Calandra, McAllister & Levine (2018), "Deep reinforcement learning in a handful of trials using probabilistic dynamics models", [arXiv:1805.12114](https://arxiv.org/abs/1805.12114) — The PETS paper, with the probabilistic ensemble, the trajectory sampling and the sample-efficiency comparisons.
- Janner et al. (2019), "When to trust your model: Model-based policy optimization", [arXiv:1906.08253](https://arxiv.org/abs/1906.08253) — MBPO, a model-based method that trains a policy on short model rollouts.
- Kurutach et al. (2018), "Model-ensemble trust-region policy optimization", [arXiv:1802.10592](https://arxiv.org/abs/1802.10592) — An early use of model ensembles to reduce model error in policy optimisation.
- Haarnoja et al. (2018), "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor", [arXiv:1801.01290](https://arxiv.org/abs/1801.01290) — A model-free baseline that PETS compares its sample efficiency against.
- Schulman et al. (2017), "Proximal policy optimization algorithms", [arXiv:1707.06347](https://arxiv.org/abs/1707.06347) — A model-free baseline that PETS compares its sample efficiency against.
