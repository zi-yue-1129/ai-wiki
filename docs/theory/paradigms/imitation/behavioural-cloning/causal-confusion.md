---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/imitation/behavioural-cloning
  - theory/paradigms/imitation/interactive-imitation/dagger.md
  - theory/paradigms/imitation/interactive-imitation/dart.md
  - theory/paradigms/supervised
tags:
  - imitation learning
  - causal inference
  - behavioural cloning
aliases:
  - causal confusion
  - causal misidentification
  - 因果混淆
---

# Causal Confusion in Imitation Learning

Causal confusion is a failure of [behavioural cloning](index.md) in which the learned policy relies on observations that correlate with the expert's actions in the demonstrations but do not cause them. Adding observations can make the policy worse, because each new feature gives it another way to pick up the spurious correlation. The term and the analysis come from de Haan, Jayaraman and Levine (2019), who call the failure *causal misidentification* in the paper body.

## Overview

A cloned policy is trained to predict expert actions from observations. Predictive accuracy on the demonstrations does not tell the learner which observations the expert actually responds to. When the relation between a spurious observation and the expert's action changes at test time, the policy fails even though its training loss was low. The paper argues that the root cause is that behavioural cloning ignores the causal structure linking the expert, the environment and the observations.

## Key concepts

- **Causal versus spurious feature**: a feature is causal if the expert's decision depends on it, and spurious if it is only correlated with the decision through some other variable, such as the consequence of the action.
- **Causal misidentification**: the paper's name for a policy that treats a spurious feature as a cause.
- **Targeted intervention**: a query that changes what the learner sees or does, such as asking the expert about a chosen state, or running a candidate policy in the environment, so that the response reveals which inputs matter.
- **Covariate shift versus causal confusion**: covariate shift is a change in the state distribution caused by the learner's own errors, which [DAgger](../interactive-imitation/dagger.md) addresses. Causal confusion is a wrong choice of inputs, which more data from the learner's distribution does not necessarily fix.

## How it works

The paper's method treats the choice of inputs as a causal model and selects it using interventions:

1. Train one policy across several candidate causal graphs. Each graph \(G\) selects a subset \(S_G\) of observation variables, and the policy is conditioned only on \(o_{S_G}\), so it can be evaluated under many input sets.
2. Run targeted interventions to estimate how well each graph explains the expert. The paper uses two modes:
    - **Expert queries**: the expert labels states chosen where the candidate policies disagree.
    - **Policy execution**: each candidate policy is run in the environment and its episode return is the evidence.
3. Select the most likely graph, and use the inputs it names as the causal model.

Written as a standard cloning objective, the baseline minimises \(\sum_{(o,a)\in\mathcal D}\ell(\pi_\theta(o), a)\) over all observations \(o\). The fix is to restrict \(o\) to the causal subset \(S_{G^\star}\) for the selected graph \(G^\star\).

## Key methods

### Causal Confusion in Imitation Learning (de Haan, Jayaraman & Levine, 2019)

- **Problem:** behavioural cloning on rich observations can fail under distribution shift. A policy that sees a feature which correlates with the expert's action can rely on it, even though the feature is an effect of the action rather than its cause. The introduction's example is a car whose dashboard light comes on when the brake is applied. A policy that learns braking from the light is confused about the cause.
- **Core idea:** use the policy as a probe of causal structure. Train over candidate sets of inputs, then use targeted interventions to find which set the expert's behaviour is actually explained by, and keep that set.
- **Equation or algorithm:** the baseline is the cloning objective \(\sum\ell(\pi_\theta(o),a)\) over full observations. The method trains a graph-conditioned policy \(\pi_G(a\mid o_{S_G})\) across sampled graphs, scores each graph with expert-query or policy-execution interventions, and picks the most likely graph \(G^\star\).
- **Results:** on MountainCar, the paper's Table 2 reports rewards of \(-137\) for policy execution and \(-140\) for expert queries with the disentangled state, against \(-145\) and \(-165\) with the entangled state. The Table 1 driving comparison (GTA-V setup, from Wang et al.) shows that the HISTORY model has lower validation perplexity (0.834 against 0.989), but more interventions (2.94 against 1.30) and more collisions (6.49 against 3.38) than NO-HISTORY. The appendix text says DAgger needs hundreds of queries on MountainCar, and tens of thousands on Hopper, to reach similar reward. Atari results are reported qualitatively.
- **Limitations:** the experiments are small (MountainCar, Hopper, three Atari games and a driving setup). As described, the candidate graphs are built over a predefined set of observation variables, so the method only chooses among the inputs it is given. The intervention step depends on expert queries or environment rollouts, which can be expensive. The paper does not report how often causal confusion occurs in the wild.

## Related failure: copycat policies

Wen et al. (2020) study *copycat agents*, cloned policies trained from observation histories that predict the previous expert action rather than the next one. Because expert actions are often strongly correlated over time, copying the last action is an easy way to reduce the training loss. It is a concrete case of the same mechanism: a shortcut feature that predicts the target well on the demonstrations but does not reflect the intended behaviour.

## Connections

Causal confusion is a form of distribution shift, and it is distinct from the covariate shift that [DAgger](../interactive-imitation/dagger.md) corrects. Collecting more data on the learner's own states does not by itself tell the policy which inputs matter. [DART](../interactive-imitation/dart.md) improves coverage offline and has the same blind spot. The general problem of learning spurious correlations appears in other areas, and the human side of inferring causes from others' actions is discussed in [cognitive science](../../../../brain-mind/cognitive-science/index.md).

## Applications

Driving and robot policies that receive several sensor streams, where a single spurious signal, such as an indicator light, a previous command, or a past-state feature, can dominate the learned policy and break when the sensor or the operator's habits change.

## Open questions

- How to find causal structure when interventions are expensive, for example when each query needs a human expert.
- Whether causal discovery methods can scale to high-dimensional sensor inputs without a hand-written list of candidate variables.
- How to separate causal confusion from ordinary covariate shift in a real dataset, where both produce similar errors.

## References

### Seminal papers

- de Haan, P., Jayaraman, D. & Levine, S. (2019). Causal Confusion in Imitation Learning. NeurIPS 2019 (33rd Conference on Neural Information Processing Systems). [arXiv:1905.11979](https://arxiv.org/abs/1905.11979) — Shows that cloned policies can rely on non-causal features and proposes selecting the causal inputs with targeted interventions.
- Wen, C., Lin, J., Darrell, T., Jayaraman, D. & Gao, Y. (2020). Fighting Copycat Agents in Behavioral Cloning from Observation Histories. NeurIPS 2020. https://proceedings.neurips.cc/paper/2020/hash/1b113258af3968aaf3969ca67e744ff8-Abstract.html — Studies the copycat failure, where the policy predicts the previous expert action.
- Ross, S., Gordon, G. J. & Bagnell, J. A. (2011). A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning. AISTATS 2011, PMLR 15. [arXiv:1011.0686](https://arxiv.org/abs/1011.0686) — Gives the covariate-shift analysis of cloning, which causal confusion is distinct from but is often confused with.
- Ross, S. & Bagnell, J. A. (2010). Efficient Reductions for Imitation Learning. AISTATS 2010, PMLR 9. https://proceedings.mlr.press/v9/ross10a.html — Earlier work by the same authors on the reduction view of imitation learning.

### Surveys and textbooks

- Osa, T. et al. (2018). An Algorithmic Perspective on Imitation Learning. Foundations and Trends in Robotics. [arXiv:1811.06711](https://arxiv.org/abs/1811.06711) — Survey of imitation learning methods, with background on behavioural cloning and its failure modes.

### Articles and preprints

- Geirhos, R. et al. (2020). Shortcut Learning in Deep Neural Networks. [arXiv:2004.07780](https://arxiv.org/abs/2004.07780) — Describes shortcut learning, where models rely on features that correlate with the target but do not reflect the intended task. This is the general pattern behind causal confusion.
