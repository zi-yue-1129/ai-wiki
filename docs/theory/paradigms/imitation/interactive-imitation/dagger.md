---
status: draft
last_reviewed: 2026-10-28
tags:
  - imitation learning
  - DAgger
  - covariate shift
aliases:
  - DAgger
  - Dataset Aggregation
  - 資料聚合
---

# DAgger (Dataset Aggregation)

DAgger is an interactive imitation learning algorithm. The learner runs its own policy, the expert labels the states the learner actually visits, and those labels are added to the training set. It fixes the covariate-shift problem of [behavioural cloning](../behavioural-cloning/index.md) by training on the states the policy will face.

## Problem

Behavioural cloning trains on states visited by the expert. At test time the learner drifts into states the expert never produced, where its predictions are unsupervised and errors compound. Ross and Bagnell (2010) analyse this compounding and show that naive cloning can accumulate cost that grows quadratically with the horizon.

## Core idea

Learn from the learner's own distribution. Each iteration rolls out the current policy, asks the expert for the correct action at every visited state, aggregates the new labelled data with all earlier data, and retrains. The aggregate data set therefore covers the state distribution of the policies the learner has produced so far.

## Algorithm

1. Train an initial policy $\pi_1$ on expert demonstrations $\mathcal{D}$.
2. For $i = 1, \dots, N$:
    1. Roll out $\pi_i$ and record the states $s$ it visits.
    2. Query the expert for the action $\pi^*(s)$ at each visited state.
    3. Aggregate: $\mathcal{D} \leftarrow \mathcal{D} \cup \{(s, \pi^*(s))\}$.
    4. Train $\pi_{i+1}$ on $\mathcal{D}$.
3. Return the best policy found on validation rollouts.

In practice the expert sometimes takes over the rollout during early iterations, with a mixing probability that decays over time. This makes the first aggregated states closer to expert behaviour.

## Results and guarantees

Ross, Gordon and Bagnell (2011) show that, for a no-regret online learner, the expected cost of the resulting policy grows linearly with the horizon, compared with the quadratic bound for behavioural cloning. The paper also reports empirical gains over earlier reductions on imitation and structured-prediction tasks. The guarantee assumes the expert can label any state the learner reaches.

## Limitations

- **Expert availability.** The method needs an expert who can label arbitrary states on demand. Human labellers may find this costly or unsafe.
- **Label quality.** Human corrections are noisy, and a human who must take over may label poorly when the policy has already started drifting (Kelly et al., 2018).
- **Data growth.** The aggregate data set grows with every iteration, so retraining cost rises over time unless the data is pruned.

## Connections

DAgger sits between supervised learning and [reinforcement learning](../../reinforcement-learning/index.md). Its rollouts supply the data, as in RL, while the expert supplies the labels, as in behavioural cloning. [DART](dart.md) gives a related route to recovery data without an online expert. The causal failure that can appear when extra observations are added is covered in [causal confusion](../behavioural-cloning/causal-confusion.md).

## Applications

Robot manipulation with teleoperators who label or correct the learner's rollouts, and autonomous driving with safety drivers who take over during learner rollouts.

## Open questions

How to bound the expert's labelling effort when the learner's state distribution moves quickly. How to label states that a human expert cannot judge, and how to combine DAgger with the offline data that already exists.

## References

### Seminal papers

- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — Introduces DAgger and proves its bound on the expected cost of the learned policy. The arXiv version is arXiv:1011.0686.
- Ross, S. & Bagnell, J. A. (2010). *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — Analyses how the errors of a cloned policy compound over the horizon, the problem DAgger addresses.

### Articles and preprints

- Laskey, M. et al. (2017). *DART: Noise Injection for Robust Imitation Learning*. arXiv:1703.09327. https://arxiv.org/abs/1703.09327 — An alternative that gathers recovery data by perturbing the expert instead of querying it online.
- Kelly, M. et al. (2018). *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — A human-gated DAgger variant, and a discussion of the label-quality problem for human experts.
- de Haan, P., Jayaraman, D. & Levine, S. (2019). *Causal Confusion in Imitation Learning*. arXiv:1905.11979. https://arxiv.org/abs/1905.11979 — Shows that extra observations can hurt cloned policies, and proposes targeted expert queries to resolve it.
