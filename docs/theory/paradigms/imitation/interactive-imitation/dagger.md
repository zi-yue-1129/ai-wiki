---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dart.md
  - theory/paradigms/imitation/interactive-imitation
  - theory/paradigms/reinforcement-learning
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

DAgger is an interactive imitation learning algorithm. The learner runs its own policy, the expert labels the states the learner actually visits, and those labels are added to the training set. It fixes the covariate-shift problem of [behavioural cloning](../behavioural-cloning/index.md) by training on the states the policy will face. The method is from Ross, Gordon and Bagnell (2011), published at AISTATS 2011.

## Overview

Behavioural cloning fits a policy to expert demonstrations, but the learned policy is then evaluated on the states it reaches itself, which the demonstrations may never have covered. DAgger closes that gap by iterating: it rolls out the current policy, collects expert labels for the visited states, and retrains on everything collected so far. The paper gives a performance bound for this procedure that grows linearly with the horizon, where cloning's bound grows quadratically.

## Key concepts

- **Covariate shift**: the learner's inputs at test time come from a different distribution than the expert's inputs in training, because the learner's own actions change which states it sees.
- **Mixed rollout**: during the early iterations the executed policy can be a mixture of the expert and the learner, controlled by a probability \(\beta_i\) that decays over iterations.
- **Aggregated dataset**: the union of labelled states from all iterations, not only the latest one. Keeping all earlier data is what lets the policy learn from the distribution of every earlier policy.
- **Expert labels**: the expert's action \(\pi^*(s)\) at each state the learner visits. The method assumes the expert can give this label for any state.

## How it works

With \(\pi^*\) the expert, the algorithm is:

1. Initialise \(\hat\pi_1\) and set \(\mathcal D\) to empty.
2. For \(i = 1, \dots, N\):
    1. Form the executed policy \(\pi_i = \beta_i\,\pi^* + (1-\beta_i)\,\hat\pi_i\). The paper's simple schedule \(\beta_i = \mathbb 1(i=1)\) makes the first rollout pure expert, and the paper notes this often works best in practice.
    2. Roll out \(\pi_i\) for \(T\) steps and record the visited states.
    3. Label each visited state with the expert, giving \(\mathcal D_i = \{(s, \pi^*(s))\}\).
    4. Aggregate \(\mathcal D \leftarrow \mathcal D \cup \mathcal D_i\), then train \(\hat\pi_{i+1}\) on \(\mathcal D\).
3. Return the policy among \(\hat\pi_1,\dots,\hat\pi_N\) that performs best on validation rollouts.

The mixing schedule only needs the average \(\beta\) to go to zero. If \(\beta_i = 1\) for every iteration, the learner never runs its own policy and the procedure reduces to behavioural cloning on expert states.

## Key methods

### A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (Ross, Gordon & Bagnell, 2011)

- **Problem:** in sequential prediction, the next input depends on earlier predictions, so the usual i.i.d. assumption fails. Behavioural cloning trains on expert-visited states, and a learned policy's errors shift it to states that are not in the training data.
- **Core idea:** treat the policy's own state distribution as the training distribution by iterating rollouts, expert labelling and retraining. Viewed as online learning, the sequence of retrained policies is a no-regret learner, and the paper uses this to bound the cost.
- **Equation or algorithm:** Algorithm 3.1 above. Let \(J(\pi)\) be the total cost over \(T\) steps and \(\ell\) the surrogate loss. The paper gives two bounds. For behavioural cloning, \(J(\hat\pi) \le J(\pi^*) + T^2\varepsilon\), where \(\varepsilon\) is the expert-state error, which is quadratic in \(T\). For DAgger, \(J(\hat\pi) \le J(\pi^*) + uT\,\varepsilon_N + O(1)\), where \(u\) bounds the expert's one-step Q-value gap and \(\varepsilon_N\) is the best per-iteration error, measured on the learner's own states. The DAgger bound is linear in \(T\). A finite-sample version of the bound holds with probability \(1-\delta\) when \(N\) grows with \(T^2\log(1/\delta)\).
- **Results:** the paper reports three experiments. In the Super Tux Kart racing task, the DAgger policy "never falls off the track after 15 iterations of training". In Super Mario Bros., DAgger clearly outperforms the supervised baseline, which stagnates at a much lower score. In handwriting recognition (structured prediction), DAgger reaches 85.5% character accuracy, above the supervised baseline.
- **Limitations:** the bound assumes a strongly convex, bounded surrogate loss and a no-regret learner (Follow-The-Leader analysis). It also assumes the expert can label every state the learner reaches, which is the assumption that makes the method expensive in practice.

## Connections

DAgger sits between supervised learning and [reinforcement learning](../../reinforcement-learning/index.md). Its rollouts supply the data, as in RL, while the expert supplies the labels, as in behavioural cloning. [DART](dart.md) gives a related route to recovery data without an online expert. The causal failure that can appear when extra observations are added, and which DAgger's coverage does not address, is covered in [causal confusion](../behavioural-cloning/causal-confusion.md).

## Applications

Robot manipulation with teleoperators who label or correct the learner's rollouts, and autonomous driving with safety drivers who take over during learner rollouts.

## Open questions

- How to bound the expert's labelling effort when the learner's state distribution moves quickly.
- How to label states that a human expert cannot judge reliably.
- How to combine DAgger with the offline demonstrations that already exist, without letting the old data dominate the aggregate dataset.

## References

### Seminal papers

- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — Introduces DAgger and proves the linear-in-horizon bound compared with the quadratic bound for behavioural cloning.
- Ross, S. & Bagnell, J. A. (2010). Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — Earlier work by the same authors on the same reduction setting, in which compounding errors of cloned policies are analysed.
- Laskey, M., Lee, J., Fox, R., Dragan, A. & Goldberg, K. (2017). DART: Noise Injection for Robust Imitation Learning. CoRL 2017. [arXiv:1703.09327](https://arxiv.org/abs/1703.09327) — An alternative that gathers recovery data by perturbing the expert, without online queries. The paper compares it with DAgger in simulation.

### Surveys and textbooks

- Osa, T. et al. (2018). An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey placing DAgger among other imitation learning methods.

### Articles and preprints

- Kelly, M., Sidrane, C., Driggs-Campbell, K. & Kochenderfer, M. J. (2019). HG-DAgger: Interactive Imitation Learning with Human Experts. ICRA 2019. [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — A human-gated variant of DAgger for interactive learning with human experts.
- de Haan, P., Jayaraman, D. & Levine, S. (2019). Causal Confusion in Imitation Learning. NeurIPS 2019. [arXiv:1905.11979](https://arxiv.org/abs/1905.11979) — Shows that extra observations can hurt cloned policies, a failure that DAgger's data coverage does not fix.
