---
status: draft
last_reviewed: 2026-10-28
tags:
  - optimization
  - reinforcement learning
  - attention
aliases:
  - Attention Model
  - 注意力模型
  - 注意力路線規劃
---

# Attention Model for Routing (Kool et al. 2018)

The attention model is a neural policy that builds a route one stop at a time, using attention layers over the set of stops. Kool, van Hoof and Welling trained it with reinforcement learning and applied one model design and one set of hyperparameters to several routing problems. It is one of the methods described on the parent page [Logistics and Supply Chain](../index.md).

## Overview

Routing problems such as the travelling salesman problem (TSP) and the vehicle routing problem (VRP) are usually solved by specialised solvers and hand-designed heuristics, which take costly development. Learned heuristics aim to reduce that cost. Bello et al. (2016) showed that a pointer network trained with reinforcement learning could produce good TSP tours. Kool et al. argue that the model and the training method both need improvement, and they contribute an attention-based model and a simpler baseline for training. Their stated goal is not to beat the best TSP solvers, but to show that one approach works across several routing variants.

## Key concepts

- **Encoder**: [transformer](../../../theory/models/transformer/index.md)-style attention layers that turn each stop and the depot into an embedding, with a graph embedding summarising the whole instance.
- **Decoder context**: a query built from the graph embedding and the most recent stops, which scores every candidate stop for the next step.
- **REINFORCE**: a [policy-gradient](../../../theory/paradigms/reinforcement-learning/policy-gradient-and-actor-critic/index.md) method that raises the probability of tours that cost less than a baseline.
- **Greedy rollout baseline**: the cost of the tour the current best model builds greedily, used as the baseline.

## How it works

The policy $p_\theta(\pi \mid s)$ generates a solution $\pi$ for an instance $s$, and $L(\pi)$ is its cost, such as tour length. Training minimises the expected cost with the REINFORCE gradient

$$
\nabla \mathcal{L}(\theta \mid s) = \mathbb{E}_{p_\theta(\pi \mid s)}\big[(L(\pi) - b(s)) \nabla \log p_\theta(\pi \mid s)\big],
$$

where $b(s)$ is the cost of the greedy solution from the best model so far. If a sampled tour is better than the greedy one, its probability is increased.

1. Encode all stops with multi-head attention layers.
2. At each step, build the decoder context from the graph embedding and the last stop, and compute compatibility scores with every stop. Clip them with a tanh to a fixed range.
3. Mask infeasible stops and take a softmax over the rest. During training, sample the next stop from this distribution.
4. Once a complete solution is built, compute its cost, and compute the baseline cost from a greedy rollout of the best model.
5. Update the parameters with Adam, and replace the baseline model when the current model improves.

## Results

On TSP instances with 20, 50 and 100 stops, the sampled version of the attention model is reported at objective values of 3.84, 5.73 and 7.94, with gaps of 0.08%, 0.52% and 2.26% to the best value in the table, which is held by strong solvers such as Concorde and LKH3 (Kool et al., 2018). The greedy version is faster and less accurate; at 100 stops it takes about 6 seconds with a gap of 4.53%. The baselines include the open-source OR-Tools solver and classical insertion heuristics. The abstract reports that the model significantly improves over earlier learned heuristics for TSP, and that on the VRP variants, the orienteering problem and the prize-collecting TSP it gets results close to specialised algorithms.

## Limitations

- **Not a replacement for solvers.** Gaps to the strongest solvers grow with problem size, from under 1% at 20 stops to above 2% at 100 stops with sampling.
- **Sampling cost.** Better tours need more samples and more time. Greedy decoding is fast but gives up accuracy.
- **Static instances.** The benchmarks are fixed instances. Real constraints such as time windows, changing orders and stochastic demand are only partly covered.
- **One setting is not one model.** A single hyperparameter setting is not a single trained model that handles every problem and size.

## Open questions

- How well do learned policies generalise to instance sizes and distributions they were not trained on?
- Can learned construction be combined with local search or exact refinement to close the remaining gap?
- How should a learned router react to requests that arrive during execution?

## References

### Seminal papers

- Kool, W., van Hoof, H. & Welling, M. (2018). Attention, learn to solve routing problems! arXiv (ICLR 2019). https://arxiv.org/abs/1803.08475 — Attention-based model trained with REINFORCE and a greedy rollout baseline, applied to TSP and several vehicle-routing variants.
- Bello, I. et al. (2016). Neural combinatorial optimization with reinforcement learning. arXiv. https://arxiv.org/abs/1611.09940 — Early demonstration that a pointer network trained with reinforcement learning can produce good tours for the travelling salesman problem.
- Nazari, M. et al. (2018). Reinforcement learning for solving the vehicle routing problem. arXiv. https://arxiv.org/abs/1802.04240 — Trains a policy with policy gradients to build vehicle routes from reward signals and feasibility rules.
- Vaswani, A. et al. (2017). Attention is all you need. arXiv. https://arxiv.org/abs/1706.03762 — Introduces the transformer attention layers from which the encoder and decoder are built.
- Williams, R. J. (1992). Simple statistical gradient-following algorithms for connectionist reinforcement learning. *Machine Learning*. https://doi.org/10.1007/BF00992696 — Derives the REINFORCE estimator used to train the policy.

### Surveys and textbooks

- Psaraftis, H. N. (1995). Dynamic vehicle routing: status and prospects. *Annals of Operations Research*. https://doi.org/10.1007/bf02098286 — Early review of routing problems in which information arrives while vehicles are already moving.
