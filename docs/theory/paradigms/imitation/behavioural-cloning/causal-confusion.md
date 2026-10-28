---
status: draft
last_reviewed: 2026-10-28
tags:
  - imitation learning
  - causal inference
  - behavioural cloning
aliases:
  - causal confusion
  - 因果混淆
---

# Causal Confusion in Imitation Learning

Causal confusion is a failure of behavioural cloning in which the learned policy relies on features that correlate with the expert's actions in the demonstrations but do not cause them. Adding observations can make the policy worse, because the new features give it more ways to pick up the spurious correlation.

## Problem

A cloned policy minimises prediction error on expert data. If some observation, such as the previous action or a dashboard indicator, predicts the expert's next action well, the policy can use it instead of the state that actually drives the expert's decision. The policy then looks accurate on the demonstrations and fails when the correlation breaks at test time.

## Core idea

de Haan, Jayaraman and Levine (2019) argue that behavioural cloning ignores the causal structure that links the expert, the environment and the observations. Without a causal model, the learner cannot tell which observations are causes of the expert's actions and which are only correlated with them. The paper proposes resolving this with targeted probes, such as expert queries or interaction with the environment, that reveal the correct causal model.

## How it works

1. Train a policy by behavioural cloning on observations that include a correlated but non-causal feature.
2. Observe that the policy's test-time performance drops when the feature's relation to the expert action changes.
3. Use targeted interventions, such as querying the expert in chosen states or varying the feature, to identify which observations the expert actually responds to.
4. Select the causal subset and train on it.

## Related failure: copying the previous action

Wen et al. (2020) describe a closely related case called copycat. When expert actions are strongly correlated over time, a cloned policy can predict the previous expert action instead of the next one, because that is the easiest way to lower the training loss. Their remedy is an adversarial feature-learning method that removes the previous-action information from the policy's features.

## Connections

Causal confusion is a form of distribution shift. It is also the reason [DAgger](../interactive-imitation/dagger.md) and [DART](../interactive-imitation/dart.md) address coverage without solving which features matter. The general mechanism appears in other fields that study spurious correlation, see [cognitive science](../../../../brain-mind/cognitive-science/index.md) for the human-side analogue of inferring causes from actions.

## Applications

Driving and robot policies that receive several sensor streams, where a single spurious signal can dominate the learned policy.

## Open questions

How to find causal structure when interventions are expensive, and whether causal discovery methods can scale to high-dimensional sensor inputs.

## References

### Seminal papers

- de Haan, P., Jayaraman, D. & Levine, S. (2019). *Causal Confusion in Imitation Learning*. arXiv:1905.11979. https://arxiv.org/abs/1905.11979 — Shows that behavioural cloning can latch onto non-causal features, and proposes causal identification with targeted interventions.
- Wen, C., Lin, J., Darrell, T., Jayaraman, D. & Gao, Y. (2020). *Fighting Copycat Agents in Behavioral Cloning from Observation Histories*. arXiv:2010.14876. https://arxiv.org/abs/2010.14876 — Identifies the copycat failure, where the policy predicts the previous expert action, and proposes an adversarial remedy.

### Articles and preprints

- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS 2011, PMLR 15:627–635. https://proceedings.mlr.press/v15/ross11a.html — Describes the covariate-shift failure that causal confusion is distinct from but often confused with.
- Ross, S. & Bagnell, J. A. (2010). *Efficient Reductions for Imitation Learning*. AISTATS 2010, PMLR 9:661–668. https://proceedings.mlr.press/v9/ross10a.html — Analyses how errors compound when a cloned policy is deployed.
- Kelly, M. et al. (2018). *HG-DAgger: Interactive Imitation Learning with Human Experts*. arXiv:1810.02890. https://arxiv.org/abs/1810.02890 — An interactive route that gathers expert labels in states the learner reaches, one way to detect spurious features.
