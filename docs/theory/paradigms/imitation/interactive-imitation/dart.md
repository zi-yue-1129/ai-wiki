---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dagger.md
  - theory/paradigms/imitation/interactive-imitation
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

DART is a method for imitation learning that makes the expert's demonstrations contain recovery behaviour. While the demonstrations are collected, it adds noise to the controls that are executed, but records the expert's clean actions as the labels. The data then cover states the learner is likely to drift into, and no online expert is needed to label the learner's own rollouts, unlike [DAgger](dagger.md). The method is from Laskey, Lee, Fox, Dragan and Goldberg (2017), published at the 1st Conference on Robot Learning (CoRL 2017).

## Overview

[Behavioural cloning](../behavioural-cloning/index.md) learns only from states the expert reaches. A small error by the learner moves it into states with no training data, where errors compound. DAgger addresses this by querying the expert on the learner's own states, which is often expensive or unsafe for a human. DART asks whether the same coverage can be built into the demonstrations, so that the expert is only needed up front.

## Key concepts

- **Executed versus recorded action**: the action the robot executes is the expert's action plus noise, while the training label is the expert's clean action. The learner then sees how the expert responds from a state the expert did not reach on its own.
- **Recovery data**: the perturbed states and their clean labels, which show how to return to the expert's path after an error.
- **Noise level**: the amount of noise is set from the error of the current learned policy, so the perturbed states resemble those the learner will visit. The paper's noise is Gaussian, with a covariance that is scaled to an anticipated error level \(\alpha\).

## How it works

Let \(\pi^*\) be the expert and \(x_t\) the state at step \(t\). During demonstration, the executed control is drawn as

\[
u_t \sim \mathcal N\big(\pi^*(x_t), \Sigma\big),
\]

while the recorded training pair is \((x_t, \pi^*(x_t))\), with the clean expert action as the label. The covariance \(\Sigma\) is estimated from how far the current learned policy deviates from the expert on the states it reaches, and is then rescaled so that its size matches the anticipated error \(\alpha\) of the final policy. The procedure is:

1. Start from a policy learned on clean demonstrations.
2. Collect demonstrations with the noisy executed controls above, with \(\Sigma\) set from the current policy's deviation.
3. Record the perturbed states with the expert's clean actions.
4. Train the policy on the combined data, and update the noise level as the policy improves.

After the demonstrations are collected, no further expert queries are needed.

## Key methods

### DART: Noise Injection for Robust Imitation Learning (Laskey et al., 2017)

- **Problem:** behavioural cloning fails when the learner drifts from the demonstrations, and DAgger's online expert queries are costly. The paper asks whether recovery behaviour can be collected offline.
- **Core idea:** perturb the expert during demonstration, label the perturbed states with the clean expert action, and tune the perturbation to the learned policy's error.
- **Equation or algorithm:** executed controls \(u_t\sim\mathcal N(\pi^*(x_t),\Sigma)\), labelled with \(\pi^*(x_t)\), with \(\Sigma\) estimated from the current policy's deviation and rescaled to the anticipated error \(\alpha\). The procedure is repeated, with the noise updated across iterations.
- **Results:** in simulated MuJoCo tasks, on the high-dimensional Humanoid task, DART is about 3 times faster in computation time than DAgger (the abstract says "up to 3x"). It reduces the supervisor's cumulative reward by only 5% during training, while DAgger's policies get about 80% less cumulative reward than the supervisor's. The paper says DART reaches parity with DAgger across the domains. In a physical experiment, a Toyota HSR robot grasped objects in clutter after human supervisors demonstrated. DART reached a 79% success rate against 49% for behavioural cloning, with a 62% average performance increase over behavioural cloning reported in the abstract.
- **Limitations:** the noise level must be tuned. The experiments are a small set of MuJoCo tasks and one physical task. The expert must be able to recover from perturbed states, which a human expert may not do well. The noise-based coverage is concentrated near the expert's trajectories, so recovery from far-off states is not guaranteed.

## Connections

DART is a counterpart to [DAgger](dagger.md): both address covariate shift, DAgger by querying the expert on the learner's states and DART by making the demonstrations cover them. Both are part of [interactive imitation](index.md). The noise idea is one way to build robustness into [behavioural cloning](../behavioural-cloning/index.md) more generally. DART does not address causal confusion, where the learner relies on a feature that is not a cause of the expert's action, see [causal confusion](../behavioural-cloning/causal-confusion.md).

## Applications

Robot manipulation where demonstrations are collected by teleoperation with controlled noise, and driving or navigation data collected with perturbed controls to show recovery.

## Open questions

- How to set the noise schedule automatically, rather than from a hand-chosen error level \(\alpha\).
- How far noisy demonstrations can cover states that the learner reaches only after many errors.
- How well the method works with human experts whose recovery actions are imperfect.

## References

### Seminal papers

- Laskey, M., Lee, J., Fox, R., Dragan, A. & Goldberg, K. (2017). DART: Noise Injection for Robust Imitation Learning. CoRL 2017 (1st Conference on Robot Learning). [arXiv:1703.09327](https://arxiv.org/abs/1703.09327) — Introduces DART, which injects noise into demonstrations to gather recovery behaviour without online expert queries.
- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — DAgger, the online alternative that DART is compared with.
- Ross, S. & Bagnell, J. A. (2010). Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — Analyses the compounding error that both DART and DAgger address.

### Surveys and textbooks

- Osa, T. et al. (2018). An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey placing noise-based and online interactive methods within imitation learning.

### Articles and preprints

- Kelly, M., Sidrane, C., Driggs-Campbell, K. & Kochenderfer, M. J. (2019). HG-DAgger: Interactive Imitation Learning with Human Experts. ICRA 2019. [arXiv:1810.02890](https://arxiv.org/abs/1810.02890) — A human-gated variant of DAgger, relevant to the question of how much an interactive human expert can provide compared with offline noise-based collection.
