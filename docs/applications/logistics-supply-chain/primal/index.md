---
status: draft
last_reviewed: 2026-10-28
tags:
  - reinforcement learning
  - planning
  - imitation learning
aliases:
  - PRIMAL
  - 多智能體強化與模仿路徑規劃
  - 倉庫機器人路徑規劃
---

# PRIMAL (Sartoretti et al. 2019)

PRIMAL is a decentralised policy for multi-agent path finding, in which each robot sees only its local surroundings and plans its next move online. Sartoretti and colleagues trained the policy by combining reinforcement learning with imitation of a central expert planner. The resulting policy can be copied onto any number of robots. It is one of the methods described on the parent page [Logistics and Supply Chain](../index.md), where warehouse robotics is the main application.

## Overview

Multi-agent path finding (MAPF) asks for collision-free paths for many robots that share one map. Centralised planners, such as conflict-based search (Sharon et al., 2015), a search method related to [A* search](../../../theory/paradigms/symbolic-ai/search/a-star/index.md), find high-quality plans but must reason jointly over all robots, so their cost rises quickly with team size. Fully reactive methods, such as the velocity-based ORCA model (van den Berg et al., 2011), avoid collisions online but can deadlock. The paper notes that most state-of-the-art planners scale poorly past a few hundred agents, and aims at a planner that runs online and implicitly coordinates its agents. PRIMAL is a [multi-agent reinforcement learning](../../../theory/paradigms/reinforcement-learning/multi-agent-rl/index.md) method, and its expert demonstrations make it a case of [imitation learning](../../../theory/paradigms/imitation/index.md).

## Key concepts

- **Partial observability**: each agent sees only a limited field of view, here a 10 by 10 window around itself.
- **Observation channels**: the input is split into channels for obstacles, positions of nearby agents, their goals, and the agent's own goal direction and distance.
- **Actor-critic network**: convolutional layers followed by an LSTM, with an extra output that predicts whether the agent is blocking others.
- **Expert demonstrations**: trajectories from the centralised planner ODrM*, used in some training episodes.
- **Reward shaping**: a sharp penalty for collisions, and smaller penalties for standing still away from one's goal.

## How it works

The paper trains a single policy shared by all agents, so that the experience of every robot updates the same parameters.

1. **Sample a world.** Draw a map with a random size and obstacle density, and a team of agents with random start and goal positions. Team size is held fixed during training.
2. **Choose the source of actions.** In some episodes agents follow expert trajectories from ODrM*, and the policy learns to imitate them. In other episodes the learning is reinforcement only.
3. **Act locally.** At each step every agent observes its field of view, and the policy outputs a move. Agents act in a random order, and moves into occupied cells are filtered out.
4. **Update.** The shared network is updated with a policy-gradient loss from the rewards and an imitation loss on the expert actions.
5. **Deploy.** Copy the trained policy to every robot. Each runs it on its own observations, and planning takes less than 0.1 seconds per agent per step on a GPU, according to the paper.

## Results

The paper evaluates success rates in three kinds of randomised world and compares against centralised and decoupled planners (Sartoretti et al., 2019).

- **Large open world (160 by 160, no obstacles).** Centralised planners struggle beyond about 100 agents. PRIMAL handles teams of up to 1024 agents with near-perfect success.
- **Medium world with low obstacle density.** PRIMAL's success rate falls earlier than the other planners' rates, but it remains above 60% with 512 agents, where the other planners perform poorly.
- **Small, densely obstructed world.** All planners handle at most 64 agents. PRIMAL begins to struggle past 8 agents, while ODrM* handles 64.

The paper also reports a small hybrid test in a factory mockup, in which two physical ground robots and simulated robots plan online together.

## Limitations

- **Dense clutter.** In crowded layouts, where agents must move in coordinated ways that a small field of view cannot reveal, PRIMAL is outperformed by the centralised planner.
- **Crowding.** Performance drops as more agents are nearby in a small world. The paper attributes this partly to training with a constant team size, and proposes varying team sizes as future work.
- **Evidence.** Most results come from grid simulations, and the physical test is small.

## Open questions

- Can the crowding weakness be fixed by training over a range of team sizes and densities?
- Warehouses often run continuously, with new tasks arriving. The follow-up PRIMAL2 (Damani et al., 2021) addresses this lifelong setting, and its results should be read alongside the original.

## References

### Seminal papers

- Sartoretti, G. et al. (2019). PRIMAL: Pathfinding via reinforcement and imitation multi-agent learning. *IEEE Robotics and Automation Letters*. https://doi.org/10.1109/lra.2019.2903261 — Decentralised path-finding policies trained by combining reinforcement learning with demonstrations from an expert planner, tested on large randomised worlds and a factory mockup.
- Sharon, G. et al. (2015). Conflict-based search for optimal multi-agent pathfinding. *Artificial Intelligence*. https://doi.org/10.1016/j.artint.2014.11.006 — Centralised search that finds optimal paths for many agents by resolving conflicts between their plans.
- van den Berg, J. et al. (2011). Reciprocal n-body collision avoidance. *Springer Tracts in Advanced Robotics*. https://doi.org/10.1007/978-3-642-19457-3_1 — Velocity-based method for online collision avoidance among many agents, the reactive baseline in PRIMAL's comparison.
- Damani, M. et al. (2021). PRIMAL2: Pathfinding via reinforcement and imitation multi-agent learning - lifelong. *IEEE Robotics and Automation Letters*. https://doi.org/10.1109/lra.2021.3062803 — Extends the approach to lifelong path finding, where new goals keep arriving.

### Surveys and textbooks

- Stern, R. et al. (2019). Multi-agent pathfinding: definitions, variants, and benchmarks. arXiv. https://arxiv.org/abs/1906.08291 — Survey of MAPF problem definitions, variants and benchmarks, useful for placing PRIMAL among other formulations.
