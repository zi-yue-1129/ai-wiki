---
status: draft
last_reviewed: 2026-10-28
tags:
  - imitation learning
  - noise injection
  - robustness
aliases:
  - DART
  - Disturbance-based Augmentation for Robust Training
  - 噪聲注入模仿學習
---

# DART (Noise Injection for Robust Imitation Learning)

DART is a method for imitation learning that makes the expert's demonstrations contain recovery behaviour. It injects noise into the expert's actions while recording demonstrations, so the data cover states the learner is likely to drift into. It gives robustness without requiring the expert to label the learner's own rollouts, as [DAgger](dagger.md) does.

## Problem

[Behavioural cloning](../behavioural-cloning/index.md) learns only from states the expert reaches. A small error by the learner moves it into states with no training data, where errors compound. DAgger solves this by querying the expert online, which is often expensive or unsafe. DART asks whether the same coverage can be built into the demonstrations offline.

## Core idea

While collecting demonstrations, add noise to the expert's executed actions, but record the expert's clean actions as the labels. The learner then sees how the expert recovers from perturbed states. The noise level is tuned to the error of the learned policy, so that the perturbed states resemble those the learner will visit.

## Algorithm

1. Start from a policy learned by behavioural cloning on clean demonstrations.
2. Repeat the demonstration process with noise added to the executed actions, with the noise scale set from the current policy's error.
3. Record the perturbed states together with the expert's clean actions.
4. Train the policy on the combined data set.

The procedure needs no online expert queries after the demonstrations are collected.

## Results

Laskey et al. (2017) report that, in simulated MuJoCo tasks, DART cut computation time by as much as threefold compared with DAgger, while the expert's reward dropped by only about 5% on the Humanoid task. On a physical grasping task the paper reports an average gain of 62% over behavioural cloning. These are the authors' reported results and should be checked in the paper before reuse.

## Limitations

- **Noise tuning.** The noise scale has to be chosen carefully. Too little noise gives no recovery data, and too much moves the data far from the states the learner visits.
- **Expert quality.** The expert must be able to recover from the perturbed states, which is not always true for human experts.
- **Coverage.** DART covers states near the expert's trajectories. Recovery from states far from them is not guaranteed.

## Connections

DART is a counterpart to [DAgger](dagger.md): both address covariate shift, DAgger by querying the expert on the learner's states and DART by making the demonstrations cover them. Both are part of [interactive imitation](index.md). The idea of injecting perturbations is also used for robustness in [behavioural cloning](../behavioural-cloning/index.md) more generally.

## Applications

Robot manipulation where demonstrations are collected by teleoperation with controlled noise, and driving or navigation data collected with perturbed controls to show recovery.

## Open questions

How to set the noise schedule automatically, and how far demonstrations with noise can cover states the learner reaches only after many errors.

## References

### Seminal papers

- Laskey, M., Lee, J., Fox, R., Dragan, A. & Goldberg, K. (2017). *DART: Noise Injection for Robust Imitation Learning*. arXiv:1703.09327. https://arxiv.org/abs/1703.09327 — Introduces DART, which injects noise into demonstrations to gather recovery behaviour without online expert queries.
- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — DAgger, the online alternative that DART is compared with.
- Ross, S. & Bagnell, J. A. (2010). *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — Analyses the compounding error that both DART and DAgger address.

### Articles and preprints

- Kelly, M. et al. (2018). *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — Discusses how human experts behave when they take over from a learned policy, relevant to the expert-quality limit of noise-based methods.
- Wen, C. et al. (2020). *Fighting Copycat Agents in Behavioral Cloning from Observation Histories*. arXiv:2010.14876. https://arxiv.org/abs/2010.14876 — Shows that cloned policies can copy the previous action, a failure that demonstration coverage alone does not fix.
