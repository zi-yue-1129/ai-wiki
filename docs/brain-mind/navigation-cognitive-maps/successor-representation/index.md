---
status: complete
last_reviewed: 2026-10-28
tags:
- reinforcement learning
- neuroscience
- representation learning
- navigation
aliases:
  - 後繼表徵
  - Successor representation
  - SR
---

# Successor representation (Dayan, 1993)

The successor representation (SR) describes each state by the future states an agent expects to visit from it. Values are then computed by combining this predictive map with the reward at each state. Because the map does not depend on reward, the same map can serve when rewards change. Gershman (2018) reviews the computational logic and the neural evidence.

This page is part of [Spatial Navigation and Cognitive Maps](../index.md). It covers one method in detail. The hippocampal side of the idea is on the [place-cells page](../place-cells/index.md).

## Overview

Consider an agent that walks through a maze to reach food. Its value estimate for each location depends on two things: how often the agent tends to reach the food from there, and how much food is there. The SR keeps the first part as a stored prediction. When the amount of food changes, only the second part needs to be updated.

## Key concepts

- **Occupancy**: how often a future state is visited, weighted by how soon it is visited. Future visits count less than near ones, through a discount factor.
- **Successor representation**: for each state, the vector of expected discounted occupancies of every state from that starting point.
- **Reward vector**: the reward attached to each state. Changing it does not change the SR.
- **Temporal-difference (TD) learning**: the method used to learn the SR from experience, one step at a time.

## Problem

Temporal-difference learning estimates values from experience. Dayan (1993) argued that the representation used to make such estimates matters. The abstract states that appropriate generalisation between states depends on how similar their successors are, so representations should follow that similarity. A plain state-value estimate does not record this structure, and it has to be rebuilt when the reward changes.

## Core idea

Dayan (1993) shows how TD machinery can learn representations in which each state is described by the states that follow it. The SR is learned in the same way as a value estimate. Once learned, the value of a state is the sum of its SR weighted by the rewards. The SR thus separates two parts of the task: the temporal structure of which states lead to which, and the reward attached to each state.

## Equation or algorithm

Let \(M(s, s')\) be the expected discounted number of visits to state \(s'\) starting from state \(s\), and let \(R(s')\) be the reward at \(s'\). Then

\(M(s, s') = \mathbb{E}\left[\sum_{t \ge 0} \gamma^{t}\, \mathbf{1}[s_t = s'] \,\middle|\, s_0 = s\right]\), and \(V(s) = \sum_{s'} M(s, s')\, R(s')\)

where \(\gamma\) is the discount factor. After an observed transition from \(s\) to \(s'\), the row \(M(s, \cdot)\) is updated with a TD step:

\(M(s,\cdot) \leftarrow M(s,\cdot) + \alpha\,[\mathbf{1}_{s} + \gamma\, M(s',\cdot) - M(s,\cdot)]\)

with learning rate \(\alpha\). The reward weights \(R\) are estimated separately, from the rewards observed in each state. Because \(M\) is defined by the agent's policy, a change of policy changes \(M\).

## Results

Dayan (1993) illustrates the approach with a navigation task, and the abstract describes the result as appropriately distributed across states. The abstract presents this as an illustration of the method, not as evidence about brains.

Later work applied the idea to human choice (Momennejad et al., 2017) and related it to hippocampal place cells (Stachenfeld et al., 2017). These are discussed on the relevant pages.

## Limitations

- **Transitions must be relearned when they change.** The SR summarises the transitions between states, so when the paths between states change, the affected predictions have to be updated. The SR removes the need to relearn when only rewards change.
- **Storage.** The SR is a matrix over states. For large state spaces, storing and learning it is costly.
- **Policy dependence.** The SR is defined under a particular policy, so a different way of acting produces a different SR.
- **Representation dependence.** Its usefulness depends on how states are defined, which the method does not solve.

## Connections

- **Dopamine and TD learning**: the SR is learned with the same kind of temporal-difference update that dopamine is thought to signal. See [Dopamine Reward Prediction Error](../../neuroscience/dopamine-reward-prediction-error/index.md).
- **Model-based and model-free control**: the SR stores predictions about the future without a full model of rewards, so it is often discussed as a middle ground (Momennejad et al., 2017; Russek et al., 2017). See [Model-Based vs Model-Free Control](../../decision-reward/model-based-vs-model-free/index.md).
- **Place cells**: a predictive map in the hippocampus can be read as an SR over space. See [Place cells and the cognitive-map hypothesis](../place-cells/index.md).
- **Reinforcement learning in AI**: the SR is one of the representations studied in [Reinforcement Learning](../../../theory/paradigms/reinforcement-learning/index.md), and it is closely tied to [Model-Based RL](../../../theory/paradigms/reinforcement-learning/model-based-rl/index.md).

## Applications

- **Modelling human learning**: Momennejad et al. (2017) apply the SR to human reinforcement learning, asking whether human learning fits this predictive account.
- **Interpreting the hippocampus**: Stachenfeld et al. (2017) propose the hippocampus as a predictive map, built on reinforcement-learning ideas, which links the method to spatial memory.
- **Transfer between tasks**: because the SR does not depend on reward, it can be reused when rewards change, which is the point the SR's definition makes.

## Open questions

- **Where is the SR computed?** Whether the brain computes the SR in the hippocampus, cortex or elsewhere is still under study.
- **How is the SR learned with rich state spaces?** The tabular case in the original paper does not transfer directly to learned or high-dimensional representations.
- **How much of behaviour does it explain?** The SR may account for some choices but not others, and how it interacts with model-based control is still debated.

## References

### Seminal papers

- Dayan, P. (1993). Improving generalization for temporal difference learning: the successor representation. *Neural Computation*. https://doi.org/10.1162/neco.1993.5.4.613 — Shows how temporal-difference learning can learn representations in which each state is described by its successors, illustrated with a navigation task.
- Stachenfeld, K. L., Botvinick, M. M. & Gershman, S. J. (2017). The hippocampus as a predictive map. *Nature Neuroscience*. https://doi.org/10.1038/nn.4650 — Proposes, drawing on reinforcement learning, that hippocampal place cells carry a predictive map rather than a purely spatial one.

### Surveys and textbooks

- Gershman, S. J. (2018). The Successor Representation: Its Computational Logic and Neural Substrates. *Journal of Neuroscience*. https://doi.org/10.1523/JNEUROSCI.0151-18.2018 — Reviews the computational logic of the successor representation and the evidence for it in the brain.

### Articles and documentation

- Momennejad, I. et al. (2017). The successor representation in human reinforcement learning. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-017-0180-8 — Applies the successor representation to human reinforcement learning, testing it in two behavioural studies with humans.
- Russek, E. M. et al. (2017). Predictive representations can link model-based reinforcement learning to model-free mechanisms. *PLoS Computational Biology*. https://doi.org/10.1371/journal.pcbi.1005768 — Argues that predictive representations can link model-based reinforcement learning to model-free mechanisms.
